=====
Usage
=====

``jsonl``
=========

Read line-separated json.

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

Convenient for removing trailing commas or handling single-quoted strings.

.. code-block:: bash

    $ mario yml2json <<<'{"x": 1,}'
    {"x": 1}



``xpath``
=========

Pull data out of xml documents using xpath.

.. code-block:: bash


    $ mario xpath '//'  map 'x.text' <<EOF
          <slide type="all">
            <title>Overview</title>
              <item>Anything in here</item>
          </slide>
    EOF
    Overview
    Anything in here




``jo``
======

Create json objects with a simple syntax.

.. code-block:: bash

    $ mario jo 'name=Alice age=21 hobbies=["running"]'
    {"name": "Alice", "age": 21, "hobbies": ["running"]}



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


Specify the ``--delimiter=`` or ``--no-header`` options as needed.
