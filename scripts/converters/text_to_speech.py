#!/usr/bin/env python3
"""Convert text/markdown files to speech audio using OpenAI TTS API."""

import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Literal

import typer
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

BUILD_ROOT = PROJECT_ROOT / "build"
AUDIO_OUTPUT_ROOT = BUILD_ROOT / "audio"

# Load environment variables from .env
load_dotenv(PROJECT_ROOT / ".env")

app = typer.Typer()

VoiceType = Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
ModelType = Literal["tts-1", "tts-1-hd"]
FormatType = Literal["mp3", "opus", "aac", "flac", "wav"]

MAX_CHUNK_SIZE = 4000  # Leave margin below 4096 limit


class TTSError(RuntimeError):
    """Raised when TTS conversion fails."""


def strip_markdown(text: str) -> str:
    """Remove common markdown formatting from text."""
    # Remove code blocks first (before other processing)
    text = re.sub(r"```[^`]*```", "", text, flags=re.DOTALL)
    # Remove images (before links, as images use similar syntax)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    # Remove headers
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    # Remove bold/italic
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"__([^_]+)__", r"\1", text)
    text = re.sub(r"_([^_]+)_", r"\1", text)
    # Remove inline code
    text = re.sub(r"`([^`]+)`", r"\1", text)
    # Remove links, keep text
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    # Remove horizontal rules
    text = re.sub(r"^[-*_]{3,}\s*$", "", text, flags=re.MULTILINE)
    # Remove bullet points
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)
    # Remove numbered lists
    text = re.sub(r"^\s*\d+\.\s+", "", text, flags=re.MULTILINE)
    # Clean up extra whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_into_sentences(text: str) -> list[str]:
    """Split text into sentences."""
    # Split on sentence-ending punctuation followed by whitespace
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if s.strip()]


def chunk_sentences(sentences: list[str], max_size: int = MAX_CHUNK_SIZE) -> list[str]:
    """Group sentences into chunks that fit within max_size."""
    chunks = []
    current_chunk = []
    current_size = 0

    for sentence in sentences:
        sentence_size = len(sentence)

        # If single sentence exceeds max, split it further
        if sentence_size > max_size:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_size = 0
            # Split long sentence by comma or just truncate
            parts = sentence.split(", ")
            for part in parts:
                if len(part) <= max_size:
                    chunks.append(part)
                else:
                    # Truncate if still too long
                    chunks.append(part[:max_size])
            continue

        if current_size + sentence_size + 1 > max_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_size = sentence_size
        else:
            current_chunk.append(sentence)
            current_size += sentence_size + 1  # +1 for space

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def generate_audio_chunk(
    client,
    text: str,
    output_path: Path,
    voice: VoiceType,
    model: ModelType,
    audio_format: FormatType,
) -> None:
    """Generate audio for a single text chunk."""
    with client.audio.speech.with_streaming_response.create(
        model=model,
        voice=voice,
        input=text,
        response_format=audio_format,
    ) as response:
        response.stream_to_file(output_path)


def concatenate_audio_files(chunk_files: list[Path], output_path: Path, audio_format: str) -> None:
    """Concatenate multiple audio files into one."""
    try:
        from pydub import AudioSegment
    except ImportError as exc:
        raise TTSError("pydub is required for audio concatenation. Run: pdm add pydub") from exc

    combined = AudioSegment.empty()
    for chunk_file in chunk_files:
        segment = AudioSegment.from_file(chunk_file, format=audio_format)
        combined += segment

    combined.export(output_path, format=audio_format)


def text_to_speech(
    input_path: Path,
    output_path: Path,
    voice: VoiceType = "alloy",
    model: ModelType = "tts-1",
    audio_format: FormatType = "mp3",
) -> None:
    """Convert text file to speech audio."""
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise TTSError("openai is required for TTS. Run: pdm add openai") from exc

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise TTSError("OPENAI_API_KEY not found. Add it to .env file in project root.")

    client = OpenAI(api_key=api_key)

    # Read and process text
    text = input_path.read_text(encoding="utf-8")

    # Strip markdown if it's a .md file
    if input_path.suffix.lower() == ".md":
        text = strip_markdown(text)

    # Split into chunks
    sentences = split_into_sentences(text)
    chunks = chunk_sentences(sentences)

    if not chunks:
        raise TTSError("No text content found in file.")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Single chunk - direct output
    if len(chunks) == 1:
        typer.secho(f"Generating audio for {input_path.name}...", fg=typer.colors.BLUE)
        generate_audio_chunk(client, chunks[0], output_path, voice, model, audio_format)
        return

    # Multiple chunks - generate and concatenate
    typer.secho(
        f"Processing {len(chunks)} chunks for {input_path.name}...", fg=typer.colors.BLUE
    )

    chunk_files = []
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        for i, chunk in enumerate(chunks):
            chunk_file = temp_path / f"chunk_{i:03d}.{audio_format}"
            typer.secho(f"  Generating chunk {i + 1}/{len(chunks)}...", fg=typer.colors.CYAN)
            generate_audio_chunk(client, chunk, chunk_file, voice, model, audio_format)
            chunk_files.append(chunk_file)

        typer.secho("  Concatenating audio chunks...", fg=typer.colors.CYAN)
        concatenate_audio_files(chunk_files, output_path, audio_format)


@app.command()
def convert(
    input_file: Path = typer.Argument(..., help="Path to the input text/markdown file."),
    output_dir: Path = typer.Option(
        AUDIO_OUTPUT_ROOT,
        "--output-dir",
        "-o",
        help="Output directory for audio files.",
    ),
    voice: VoiceType = typer.Option(
        "alloy",
        "--voice",
        "-v",
        help="Voice to use: alloy, echo, fable, onyx, nova, shimmer.",
    ),
    model: ModelType = typer.Option(
        "tts-1",
        "--model",
        "-m",
        help="TTS model: tts-1 (fast) or tts-1-hd (high quality).",
    ),
    audio_format: FormatType = typer.Option(
        "mp3",
        "--format",
        "-f",
        help="Output format: mp3, opus, aac, flac, wav.",
    ),
) -> None:
    """Convert a text or markdown file to speech audio using OpenAI TTS."""
    if not input_file.exists() or not input_file.is_file():
        typer.secho(f"Error: Input file not found at {input_file}", fg=typer.colors.RED)
        raise typer.Exit(1)

    absolute_input = input_file.resolve()
    output_file = (output_dir / absolute_input.stem).with_suffix(f".{audio_format}")

    try:
        text_to_speech(absolute_input, output_file, voice, model, audio_format)
        typer.secho(
            f"Successfully converted {input_file.name} to {output_file}",
            fg=typer.colors.GREEN,
        )
    except TTSError as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
