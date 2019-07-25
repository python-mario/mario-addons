"""Functions for walking a tree."""

import collections.abc
import typing as t

import mario.interpret


def build_new(old, new):
    """Build a new instance of the old type, with new data."""
    return type(old)(new)


def traverse_one_level_json(handle_item, tree):
    """Traverse one level of a json-like tree."""

    if isinstance(tree, collections.abc.Sequence) and not isinstance(tree, str):
        return build_new(tree, [handle_item(x) for i, x in enumerate(tree)])
    if isinstance(tree, collections.abc.Mapping):

        return build_new(tree, {k: handle_item(v) for k, v in tree.items()})

    return tree


def build_walker(descend: t.Callable, handle_item: t.Callable) -> t.Callable:
    """Build a walker with specified functions."""

    def walk_tree(data, *args, **kwargs):
        recursed = descend(walk_tree, data, *args, **kwargs)
        return handle_item(recursed, *args, **kwargs)

    return walk_tree


def make_func(code: str, namespace: t.Dict[str, object]) -> t.Callable:
    """Make a transformer function."""
    # pylint: disable=fixme
    # TODO Use the parser from mario core.
    if "x" not in code:
        code += "(x)"

    # pylint: disable=fixme
    # TODO Move this earlier in the process so it only needs to be executed
    # once, maybe with click.ParamType.

    # pylint: disable=eval-used
    return lambda x: eval(code, {**namespace, "x": x})


def build_mapping(pairs: t.Iterable[t.Tuple[str, str]]):
    """Build a type-to-transformer mapping."""
    mapping = {}

    for input_type, converter in pairs:
        input_type_namespace = mario.interpret.build_name_to_module(input_type)
        converter_namespace = mario.interpret.build_name_to_module(converter)
        # pylint: disable=eval-used
        mapping[eval(input_type, input_type_namespace)] = make_func(
            converter, converter_namespace
        )
    return mapping


def build_transforming_json_walker(pairs: t.List[t.Tuple[str, str]]) -> t.Callable:
    """Build a walker for json-like trees."""

    mapping = build_mapping(pairs)

    def transform_type(value):
        func = mapping.get(type(value), lambda y: y)
        return func(value)

    return build_walker(descend=traverse_one_level_json, handle_item=transform_type)


# class PairParam(click.ParamType):
#     def __init__(self, left_type, right_type):
#         self.left_type = left_type
#         self.right_type = right_type

#     def convert(self, value, param, ctx):
#         left, right = value.split("=", maxsplit=1)
#         return self.left_type.convert(left), self.right_type.convert(right)


# class EvalParam(click.ParamType):
#     def convert(self, value, param, ctx):
#         return make_func(value, mario.interpret.build_name_to_module(value))
