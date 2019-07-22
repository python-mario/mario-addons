from __future__ import annotations

import csv
import io
import itertools
import typing as t

import yaml


def write_csv_dicts(rows: t.Iterable[t.Dict], header: bool, dialect: str) -> str:
    """Write iterable of dicts to csv."""
    file = io.StringIO()

    it = iter(rows)
    first_row = next(it)
    fieldnames = list(first_row.keys())
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    if header:
        writer.writeheader()
    writer.writerows(itertools.chain([first_row], it))

    return file.getvalue()


def write_csv_tuples(rows: t.Iterable[t.Tuple], dialect: str) -> str:
    """Write iterable of tuples to csv."""
    file = io.StringIO()

    writer = csv.writer(file, dialect)
    writer.writerows(rows)

    return file.getvalue()


def write_yaml(data) -> str:
    file = io.StringIO()
    yaml.dump(data, file)
    return file.getvalue()
