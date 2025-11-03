from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from scripts.converters import convert_pdf_to_md_advanced as module


class DummyDoc:
    def __init__(self, content: str) -> None:
        self._content = content

    def export_to_markdown(self) -> str:
        return self._content


class DummyResult:
    def __init__(self, content: str) -> None:
        self.document = DummyDoc(content)


class DummyConverter:
    def __init__(self, storage: list[str]) -> None:
        self.storage = storage

    def convert(self, pdf_path: str) -> DummyResult:
        self.storage.append(pdf_path)
        return DummyResult("Converted body")


@pytest.fixture
def fixed_datetime(monkeypatch: pytest.MonkeyPatch) -> str:
    class DummyDateTime:
        @staticmethod
        def now() -> Any:
            class DummyNow:
                @staticmethod
                def isoformat() -> str:
                    return "2025-01-02T03:04:05"

            return DummyNow()

    monkeypatch.setattr(module, "datetime", DummyDateTime)
    return "2025-01-02T03:04:05"


def test_convert_pdf_to_markdown_writes_metadata_header(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, fixed_datetime: str
) -> None:
    pdf_file = tmp_path / "sample.pdf"
    pdf_file.write_bytes(b"pdf")

    call_log: list[str] = []

    def fake_converter_factory(*_: Any, **__: Any) -> DummyConverter:
        return DummyConverter(call_log)

    monkeypatch.setattr(module, "DocumentConverter", fake_converter_factory)

    output_path = module.convert_pdf_to_markdown(pdf_file)

    assert call_log == [str(pdf_file)]
    content = output_path.read_text(encoding="utf-8")
    assert content.startswith("---\n")
    assert f"source: {pdf_file.name}" in content
    assert f"conversion_date: {fixed_datetime}" in content
    assert "Converted body" in content


def test_convert_pdf_to_markdown_requires_overwrite(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, fixed_datetime: str
) -> None:
    pdf_file = tmp_path / "exists.pdf"
    pdf_file.write_bytes(b"pdf")

    markdown_file = tmp_path / "exists.md"
    markdown_file.write_text("existing", encoding="utf-8")

    monkeypatch.setattr(module, "DocumentConverter", lambda: DummyConverter([]))

    with pytest.raises(FileExistsError):
        module.convert_pdf_to_markdown(pdf_file, output_path=markdown_file, overwrite=False)


def test_cli_directory_conversion_preserves_structure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source_dir = tmp_path / "pdfs"
    nested = source_dir / "nested"
    nested.mkdir(parents=True)

    root_pdf = source_dir / "root.pdf"
    nested_pdf = nested / "child.pdf"
    root_pdf.write_bytes(b"root")
    nested_pdf.write_bytes(b"child")

    outputs: list[Path] = []

    def fake_convert(pdf_path: Path, output_path: Path | None, overwrite: bool) -> Path:
        target = output_path or pdf_path.with_suffix(".md")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f"converted {pdf_path.name}", encoding="utf-8")
        outputs.append(target)
        return target

    monkeypatch.setattr(module, "convert_pdf_to_markdown", fake_convert)

    module.convert(
        pdf_file=source_dir,
        output=tmp_path / "out",
        overwrite=True,
        recursive=True,
    )

    expected_paths = {
        tmp_path / "out" / "root.md",
        tmp_path / "out" / "nested" / "child.md",
    }

    assert set(outputs) == expected_paths
    for path in expected_paths:
        assert path.read_text(encoding="utf-8").startswith("converted")
