import csv
import typing as t

from mario import plug


registry = plug.make_plugin_commands_registry("mario_addons.plugins")


def read_csv(
    file, header: bool, **kwargs
) -> t.Iterable[t.Dict[t.Union[str, int], str]]:
    "Read csv rows into an iterable of dicts."

    rows = list(file)

    first_row = next(csv.reader(rows))
    if header:
        fieldnames = first_row
        reader = csv.DictReader(rows, fieldnames=fieldnames, **kwargs)
        return list(reader)[1:]

    fieldnames = range(len(first_row))
    return csv.DictReader(rows, fieldnames=fieldnames, **kwargs)
