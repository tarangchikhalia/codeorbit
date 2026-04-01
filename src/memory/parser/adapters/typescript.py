import tree_sitter_typescript as tst
from tree_sitter import Language

from src.memory.parser.models import LanguageSpec

COMMON_NODE_TYPES = (
    "class_declaration",
    "function_declaration",
    "lexical_declaration"
)


TYPESCRIPT_SPEC = LanguageSpec(
    language_id="typescript",
    extensions=(".ts",),
    node_types=COMMON_NODE_TYPES,
    language=Language(tst.language_typescript()),
)


TSX_SPEC = LanguageSpec(
    language_id="tsx",
    extensions=(".tsx",),
    node_types=COMMON_NODE_TYPES,
    language=Language(tst.language_tsx()),
)
