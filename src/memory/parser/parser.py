from pathlib import Path

from tree_sitter import Parser, Node

from src.memory.parser.models import ParsedFile, SyntaxRegion
from src.memory.parser.registry import REGISTRY

def file_parser(path: str | Path) -> ParsedFile:
    """
    Description="Parses a source file, resolves its language, and returns structured parsing data for downstream consumers."
    Arguments=["path: Source file path to parse."]
    Returns="ParsedFile containing the file metadata, split lines, and syntax regions."
    """

    file_path = Path(path)
    source = file_path.read_bytes()
    if not source:
        raise ValueError(f"File {file_path} is empty")

    spec = REGISTRY.get_for_path(file_path)
    parser = Parser()
    parser.language = spec.language
    tree = parser.parse(source)

    source_lines = source.splitlines(keepends=True)
    regions = collect_regions(tree.root_node, spec.node_types)

    return ParsedFile(
        path=file_path,
        language_id=spec.language_id,
        source_bytes=source,
        source_lines=source_lines,
        regions=regions,
    )

def collect_regions(root: Node, node_types: tuple[str, ...]) -> list[SyntaxRegion]:
    """
    Description="Collects and orders syntax regions for nodes matching the provided Tree-sitter node types."
    Arguments=["root: Root node of the parsed syntax tree.", "node_types: Node type names that should become chunk boundaries."]
    Returns="List of ordered SyntaxRegion objects derived from matching nodes."
    """

    target_types = set(node_types)
    nodes = _collect_nodes(root, target_types)
    nodes.sort(key=lambda node: (node.start_point[0], node.end_point[0]))

    return [
        SyntaxRegion(
            start_line=node.start_point[0],
            end_line=_node_end_line(node),
        )
        for node in nodes
    ]


def _collect_nodes(root: Node, node_types: set[str]) -> list[Node]:
    """
    Description="Traverses a syntax tree iteratively and returns nodes whose type matches the requested set."
    Arguments=["root: Root node of the syntax tree to traverse.", "node_types: Node types to match during traversal."]
    Returns="List of Tree-sitter nodes matching the requested types."
    """

    matches: list[Node] = []
    stack = [root]

    while stack:
        node = stack.pop()
        if node.type in node_types:
            matches.append(node)

        stack.extend(reversed(node.children))

    return matches


def _node_end_line(node: Node) -> int:
    """
    Description="Normalizes a Tree-sitter node end position into an exclusive line index."
    Arguments=["node: Syntax node whose end position should be normalized."]
    Returns="Exclusive end line index for the node."
    """

    end_line = node.end_point[0]
    if node.end_point[1] > 0:
        end_line += 1
    return end_line
