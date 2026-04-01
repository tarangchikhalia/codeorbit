from dataclasses import dataclass
from pathlib import Path

from tree_sitter import Language


@dataclass(frozen=True)
class SyntaxRegion:
    """
    Description="Represents a syntax-aware line range extracted from a parsed source file."
    """

    start_line: int
    end_line: int


@dataclass(frozen=True)
class LanguageSpec:
    """
    Description="Defines the parser configuration and node selection rules for a supported language."
    """

    language_id: str
    extensions: tuple[str, ...]
    node_types: tuple[str, ...]
    language: Language


@dataclass(frozen=True)
class ParsedFile:
    """
    Description="Stores the normalized output produced by the parsing layer for a single source file."
    """

    path: Path
    language_id: str
    source_bytes: bytes
    source_lines: list[bytes]
    regions: list[SyntaxRegion]
