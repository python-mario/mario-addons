"""Functions for walking a tree."""

import builtins
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


def prefixes(multi_attribute_access: str) -> t.List[str]:
    """Get prefixes of a namepsaced name.

    >>> prefixes('a.b.c')
    ['a.b.c', 'a.b', 'a']
    """
    split = multi_attribute_access.split(".")
    out = []
    while split:
        out.append(".".join(split))
        split.pop(-1)
    return out


def get_type_object(namespaced_type_name: str) -> t.Type:
    """Turns a qualname into the corresponding object."""

    if "." not in namespaced_type_name:
        return getattr(builtins, namespaced_type_name)

    name_to_module = mario.interpret.build_name_to_module(namespaced_type_name)
    for module_name in prefixes(namespaced_type_name):
        module = name_to_module.get(module_name)
        if module is not None:
            break
    else:
        raise ImportError(module_name)

    obj = module
    # pylint: disable=undefined-loop-variable
    remainder = namespaced_type_name[len(module_name) :]
    names = [name for name in remainder.split(".") if name]

    while names:
        obj = getattr(obj, names[0])
        names.pop()

    return obj


def build_mapping(pairs: t.Iterable[t.Tuple[str, str]]):
    """Build a type-to-transformer mapping."""
    mapping = {}

    for input_type, converter in pairs:
        converter_namespace = mario.interpret.build_name_to_module(converter)
        mapping[get_type_object(input_type)] = make_func(converter, converter_namespace)
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
