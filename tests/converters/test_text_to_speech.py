"""Tests for text_to_speech converter."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from scripts.converters import text_to_speech as module


class TestStripMarkdown:
    """Tests for strip_markdown function."""

    def test_removes_headers(self) -> None:
        text = "# Header 1\n## Header 2\n### Header 3"
        result = module.strip_markdown(text)
        assert "Header 1" in result
        assert "#" not in result

    def test_removes_bold_and_italic(self) -> None:
        text = "This is **bold** and *italic* and __also bold__ and _also italic_."
        result = module.strip_markdown(text)
        assert result == "This is bold and italic and also bold and also italic."

    def test_removes_inline_code(self) -> None:
        text = "Use `print()` to output."
        result = module.strip_markdown(text)
        assert result == "Use print() to output."

    def test_removes_links_keeps_text(self) -> None:
        text = "Click [here](https://example.com) to continue."
        result = module.strip_markdown(text)
        assert result == "Click here to continue."

    def test_removes_images(self) -> None:
        text = "See image: ![alt text](image.png) below."
        result = module.strip_markdown(text)
        assert "alt text" not in result
        assert "image.png" not in result

    def test_removes_code_blocks(self) -> None:
        text = "Code:\n```python\nprint('hello')\n```\nEnd."
        result = module.strip_markdown(text)
        assert "print" not in result
        assert "End." in result

    def test_removes_bullet_points(self) -> None:
        text = "List:\n- item 1\n* item 2\n+ item 3"
        result = module.strip_markdown(text)
        assert "item 1" in result
        assert "- " not in result
        assert "* " not in result


class TestSplitIntoSentences:
    """Tests for split_into_sentences function."""

    def test_splits_on_period(self) -> None:
        text = "First sentence. Second sentence. Third sentence."
        result = module.split_into_sentences(text)
        assert result == ["First sentence.", "Second sentence.", "Third sentence."]

    def test_splits_on_question_mark(self) -> None:
        text = "Is this a question? Yes it is."
        result = module.split_into_sentences(text)
        assert result == ["Is this a question?", "Yes it is."]

    def test_splits_on_exclamation(self) -> None:
        text = "Wow! That is amazing."
        result = module.split_into_sentences(text)
        assert result == ["Wow!", "That is amazing."]

    def test_handles_empty_text(self) -> None:
        result = module.split_into_sentences("")
        assert result == []

    def test_handles_single_sentence(self) -> None:
        text = "Just one sentence here."
        result = module.split_into_sentences(text)
        assert result == ["Just one sentence here."]


class TestChunkSentences:
    """Tests for chunk_sentences function."""

    def test_single_chunk_when_small(self) -> None:
        sentences = ["Short.", "Also short."]
        result = module.chunk_sentences(sentences, max_size=100)
        assert result == ["Short. Also short."]

    def test_splits_into_multiple_chunks(self) -> None:
        sentences = ["First sentence.", "Second sentence.", "Third sentence."]
        result = module.chunk_sentences(sentences, max_size=30)
        assert len(result) >= 2

    def test_handles_oversized_sentence(self) -> None:
        sentences = ["A" * 100]
        result = module.chunk_sentences(sentences, max_size=50)
        assert len(result) >= 1
        for chunk in result:
            assert len(chunk) <= 100  # May be split or truncated

    def test_empty_input(self) -> None:
        result = module.chunk_sentences([], max_size=100)
        assert result == []


class TestTextToSpeech:
    """Integration tests for text_to_speech function."""

    @pytest.fixture
    def mock_openai_client(self) -> MagicMock:
        """Create a mock OpenAI client."""
        client = MagicMock()
        response_mock = MagicMock()
        response_mock.__enter__ = MagicMock(return_value=response_mock)
        response_mock.__exit__ = MagicMock(return_value=False)
        response_mock.stream_to_file = MagicMock()
        client.audio.speech.with_streaming_response.create.return_value = response_mock
        return client

    def test_generates_audio_for_short_text(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, mock_openai_client: MagicMock
    ) -> None:
        input_file = tmp_path / "test.txt"
        input_file.write_text("Hello world.", encoding="utf-8")
        output_file = tmp_path / "output.mp3"

        monkeypatch.setenv("OPENAI_API_KEY", "test-key")

        with patch("openai.OpenAI", return_value=mock_openai_client):
            module.text_to_speech(input_file, output_file)

        mock_openai_client.audio.speech.with_streaming_response.create.assert_called_once()
        call_kwargs = mock_openai_client.audio.speech.with_streaming_response.create.call_args[1]
        assert call_kwargs["input"] == "Hello world."
        assert call_kwargs["model"] == "tts-1"
        assert call_kwargs["voice"] == "alloy"

    def test_strips_markdown_for_md_files(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, mock_openai_client: MagicMock
    ) -> None:
        input_file = tmp_path / "test.md"
        input_file.write_text("# Header\n**Bold text** here.", encoding="utf-8")
        output_file = tmp_path / "output.mp3"

        monkeypatch.setenv("OPENAI_API_KEY", "test-key")

        with patch("openai.OpenAI", return_value=mock_openai_client):
            module.text_to_speech(input_file, output_file)

        call_kwargs = mock_openai_client.audio.speech.with_streaming_response.create.call_args[1]
        assert "#" not in call_kwargs["input"]
        assert "**" not in call_kwargs["input"]
        assert "Bold text" in call_kwargs["input"]

    def test_raises_error_without_api_key(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        input_file = tmp_path / "test.txt"
        input_file.write_text("Hello.", encoding="utf-8")
        output_file = tmp_path / "output.mp3"

        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        with pytest.raises(module.TTSError, match="OPENAI_API_KEY not found"):
            module.text_to_speech(input_file, output_file)

    def test_raises_error_for_empty_file(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, mock_openai_client: MagicMock
    ) -> None:
        input_file = tmp_path / "empty.txt"
        input_file.write_text("", encoding="utf-8")
        output_file = tmp_path / "output.mp3"

        monkeypatch.setenv("OPENAI_API_KEY", "test-key")

        with patch("openai.OpenAI", return_value=mock_openai_client):
            with pytest.raises(module.TTSError, match="No text content"):
                module.text_to_speech(input_file, output_file)

    def test_uses_custom_voice_and_model(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, mock_openai_client: MagicMock
    ) -> None:
        input_file = tmp_path / "test.txt"
        input_file.write_text("Hello.", encoding="utf-8")
        output_file = tmp_path / "output.mp3"

        monkeypatch.setenv("OPENAI_API_KEY", "test-key")

        with patch("openai.OpenAI", return_value=mock_openai_client):
            module.text_to_speech(input_file, output_file, voice="nova", model="tts-1-hd")

        call_kwargs = mock_openai_client.audio.speech.with_streaming_response.create.call_args[1]
        assert call_kwargs["voice"] == "nova"
        assert call_kwargs["model"] == "tts-1-hd"
