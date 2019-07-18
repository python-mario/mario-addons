=====
Usage
=====

``jsonl``
=========

.. code-block:: toml

   [[alias]]

   name = "jsonl"
   help = "Load jsonlines into python objects."

   [[alias.stage]]

   command = "map"
   options = {code="json.loads"}


Now we can use it like a regular command:

.. code-block:: bash

    $ mario jsonl  <<< $'{"a":1, "b":2}\n{"a": 5, "b":9}'
    {'a': 1, 'b': 2}
    {'a': 5, 'b': 9}


The new command ``jsonl`` can be used in pipelines as well. To get the maximum value in a sequence of jsonlines objects:

.. code-block:: bash

   $ mario jsonl map 'x["a"]' apply max <<< $'{"a":1, "b":2}\n{"a": 5, "b":9}'
   5


``yml2json``
============

Convenient for removing trailing commas.

.. code-block:: bash

    $ mario yml2json <<<'{"x": 1,}'
    {"x": 1}

.. code-block:: toml

    [[alias]]

        name = "yml2json"
        help = "Convert yaml to json"

        [[alias.stage]]

        command = "stack"
        options = {code="yaml.safe_load ! json.dumps"}



``xpath``
=========

Pull text out of xml documents.

.. code-block:: bash


    $ mario xpath '//'  map 'x.text' <<EOF
          <slide type="all">
            <title>Overview</title>
              <item>Anything in here</item>
          </slide>
    EOF
    Overview
    Anything in here


.. code-block:: toml

    [[alias]]
        name="xpath"
        help = "Find xml elements matching xpath query."
        arguments = [{name="query", type="str"}]
        inject_values=["query"]

        [[alias.stage]]
        command = "stack"
        options= {code="x.encode() ! io.BytesIO ! lxml.etree.parse ! x.findall(query) ! list" }

        [[alias.stage]]
        command="chain"


``jo``
======

.. code-block:: bash

    $ mario jo 'name=Alice age=21 hobbies=["running"]'
    {"name": "Alice", "age": 21, "hobbies": ["running"]}


.. code-block:: toml

    [[alias]]


        name="jo"
        help="Make json objects"
        arguments=[{name="pairs", type="str"}]
        inject_values=["pairs"]

        [[alias.stage]]
        command = "eval"
        options = {code="pairs"}

        [[alias.stage]]
        command = "map"
        options = {code="shlex.split(x, posix=False)"}

        [[alias.stage]]
        command = "chain"

        [[alias.stage]]
        command = "map"
        options = {code="x.partition('=') ! [x[0], ast.literal_eval(re.sub(r'^(?P<value>[A-Za-z]+)$', r'\"\\g<value>\"', x[2]))]"}

        [[alias.stage]]
        command = "apply"
        options = {"code"="dict"}

        [[alias.stage]]
        command = "map"
        options = {code="json.dumps"}


``csv``
=======

Read a csv file into Python dicts. Given a csv like this:


.. code-block::

    name,age
    Alice,21
    Bob,25

try:

.. code-block:: bash

    $ mario csv <<EOF
    name,age
    Alice,21
    Bob,25
    EOF
    {'name': 'Alice', 'age': '21'}
    {'name': 'Bob', 'age': '25'}


.. code-block:: toml

    base_exec_before = '''
    import csv
    import typing as t


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

    '''




    [[alias]]
        name = "csv"
        help = "Load csv rows into python dicts. With --no-header, keys will be numbered from 0."
        inject_values=["delimiter", "header"]

        [[alias.options]]
        name = "--delimiter"
        default = ","
        help = "field delimiter character"

        [[alias.options]]
        name = "--header/--no-header"
        default=true
        help = "Treat the first row as a header?"

        [[alias.stage]]
        command = "apply"
        options = {code="read_csv(x, header=header, delimiter=delimiter)"}

        [[alias.stage]]
        command = "chain"

        [[alias.stage]]
        command = "map"
        options = {code="dict(x)"}
