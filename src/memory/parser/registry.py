from pathlib import Path

from src.memory.parser.adapters import LANGUAGE_SPECS
from src.memory.parser.models import LanguageSpec


class LanguageRegistry:
    """
    Description="Resolves file extensions to registered language specifications."
    Arguments=[]
    Returns=""
    """

    def __init__(self, specs: tuple[LanguageSpec, ...]) -> None:
        """
        Description="Builds an in-memory lookup table for language specifications keyed by file extension."
        Arguments=["specs: Registered language specifications to index."]
        Returns=""
        """

        self._by_extension: dict[str, LanguageSpec] = {}
        for spec in specs:
            for extension in spec.extensions:
                self._by_extension[extension] = spec

    def get_by_extension(self, extension: str) -> LanguageSpec:
        """
        Description="Returns the language specification registered for a given file extension."
        Arguments=["extension: File extension including the leading dot."]
        Returns="LanguageSpec mapped to the provided extension."
        """

        try:
            return self._by_extension[extension]
        except KeyError as exc:
            supported = ", ".join(sorted(self._by_extension))
            raise ValueError(
                f"Unsupported file type: {extension}. Supported extensions: {supported}"
            ) from exc

    def get_for_path(self, path: str | Path) -> LanguageSpec:
        """
        Description="Returns the language specification associated with a file path."
        Arguments=["path: File system path whose suffix should be resolved."]
        Returns="LanguageSpec mapped to the path suffix."
        """

        return self.get_by_extension(Path(path).suffix.lower())

    @property
    def supported_extensions(self) -> tuple[str, ...]:
        """
        Description="Lists the extensions currently registered in the language registry."
        Arguments=[]
        Returns="Tuple of supported file extensions sorted alphabetically."
        """

        return tuple(sorted(self._by_extension))


REGISTRY = LanguageRegistry(LANGUAGE_SPECS)
