"""
Ploomber spec API provides a quick and simple way to use Ploomber using YAML,
it is not indented to replace the Python API which offers more flexibility and
advanced features.

`Click here for a live demo. <https://mybinder.org/v2/gh/ploomber/projects/master?filepath=spec%2FREADME.md>`_

To create a new project with basic structure:

.. code-block:: bash

    ploomber new


Build pipeline:

.. code-block:: bash

    python entry pipeline.yaml

To start an interactive session:

.. code-block:: bash

    ipython -i -m ploomber.entry pipeline.yaml -- --action status

Once the interactive session opens, use the ``dag`` object.


Visualize dependencies:

.. code-block:: python

    dag.plot()

Develop scripts interactively:

.. code-block:: python

    dag['some_task'].develop()


Line by line debugging:

.. code-block:: python

    dag['some_task'].debug()


Print the rendered source code from SQL scripts:


.. code-block:: python

    print(dag['some_sql_task'].source)


``pipeline.yaml`` schema
------------------------

Values within {curly brackets} contain explanations, otherwise, they represent
default values.

.. code-block:: yaml

    # pipeline.yaml
    meta:
        extract_product: False

        # inspect source code to extract upstream dependencies
        extract_upstream: True

        # if any task does not have a "product_class" key, it will look up this
        # dictionary using the task class
        product_default_class:
            SQLDump: File
            NotebookRunner: File
            SQLScript: SQLRelation

    # For allowed keys and values see ploomber.DAGConfigurator
    config:
        {config-key}: {config-value}

    # clients are objects that connect to databases
    clients:
        {task or product class name}: {dotted.path.to.function}

    tasks:
        - {task dictionary, see below}


Notes
-----
* The meta section and clients is optional.
* The spec can also just be a list of tasks for DAGs that don't use clients and do not need to modify meta default values.
* If using a factory, the spec can just be

.. code-block:: yaml

    # pipeline.yaml
    location: {dotted.path.to.factory}

``task`` schema
---------------

.. code-block:: yaml

    # Any of the classes available in the tasks module
    # If missing, it will be inferred from "source".
    # NotebookRunner for .py and .ipynb files, SQLScript for .sql
    # and ShellScript for .sh
    class: {task class, optional}

    source: {path to source file}

    # Products that will be generated upon task execution. Should not exist
    # if meta.extract_product is set to True. This can be a dictionary if
    # the task generates more than one product. Required if extract_product
    # is False
    product: {str or dict}

    # Any of the classes available in the products module, if missing, the
    # class is looked up in meta.product_default_class using the task class
    product_class: {str, optional}

    # Optional task name, if missing, the value passed in "source" is used
    # as name
    name: {task name, optional}

    # Dotted path to a function that has no parameters and returns the
    # client to use. By default the class-level client at config.clients is
    # used, this value overrides it. Only required for tasks that require
    # clients
    client: {dotted.path.to.function, optional}

    # Same as "client" but applies to the product, most of the time, this will
    # be the same as "client". See the FAQ for more information (link at the
    # bottom)
    product_client: {dotted.path.to.function, optional}

    # Dependencies for this task. Only required if meta.extract_upstream is
    # set to True
    upstream: {str or list, optional}

    # NOTE: All remaining values are passed to the task constructor as keyword
    arguments


Click here to go to :doc:`faq_index/`.


Python script example
---------------------

.. code-block:: python

    # annotated python file (it will be converted to a notebook during execution)
    import pandas as pd

    # + tags=["parameters"]
    # this script depends on the output generated by a task named "clean"
    upstream = {'clean': None}
    product = None

    # during execution, a new cell is added here

    # +
    df = pd.read_csv(upstream['some_task'])
    # do data processing...
    df.to_csv(product['data'])


SQL script example
------------------

.. code-block:: sql

    DROP TABLE IF EXISTS {{product}};

    CREATE TABLE {{product}} AS
    -- this task depends on the output generated by a task named "clean"
    SELECT * FROM {{upstream['clean']}}
    WHERE x > 10

"""
