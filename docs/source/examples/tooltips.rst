Tooltips
========

A custom role to create tooltips in your documentation. The tooltip text can be provided inline or loaded from a glossary entry.

.. warning:: Ensure that the included content is appropriate for display as a tooltip, as long text or complex formatting may not render well.

Syntax
------

.. code-block:: rst

   :include_tooltip:`display text <tooltip text or term name>`

Usage
-----

Tooltip with text
.................

Using:

.. code-block:: rst

   Here is a :include_tooltip:`word <This is the tooltip text>`.

Results in:

Here is a :include_tooltip:`word <This is the tooltip text>`.

Tooltip from a glossary entry
.............................

Using:

.. code-block:: rst

   Here is a :include_tooltip:`term <Term 1>`.

This will load the definition of `term-name` from your project's glossary and use it as the tooltip text for "term".


Results in:

Here is a :include_tooltip:`term <Term 1>`.

Tooltip with long description
-----------------------------

Using:

.. glossary::

   Long description
      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec sed lorem quis dui mattis suscipit sit amet id dui. Suspendisse elementum rutrum vulputate. Cras in velit sapien. Etiam egestas turpis eget arcu feugiat semper. Ut blandit sagittis cursus. Maecenas at varius ex, et porttitor mi. Nullam tortor elit, tincidunt et nulla id, porta vestibulum nibh. Quisque tellus elit, maximus at congue quis, molestie eget urna. Donec odio lorem, semper sed pharetra eu, sodales eget velit. Donec dignissim quam mi, nec vehicula magna gravida in. Vestibulum consectetur, sem a tristique porta, risus est laoreet nibh, sed cursus nibh est vel massa. Vestibulum aliquet varius tellus eu pulvinar. Integer a lorem sollicitudin, placerat orci eu, lobortis velit. Pellentesque sit amet magna porta augue iaculis egestas dapibus sed dui.

      Cras rutrum eros felis, ac pulvinar arcu mattis ac. Cras consectetur, risus vel luctus ultrices, risus elit pellentesque turpis, sed posuere tortor neque quis diam. Donec viverra libero ac magna viverra convallis. Morbi ac felis vel ligula maximus venenatis eget a libero. Mauris sagittis, lacus nec posuere venenatis, neque massa fermentum ex, sit amet dictum massa risus sit amet erat. Suspendisse tempus, nisl nec consectetur auctor, eros erat tempus neque, a placerat sapien est vel felis. Nulla a porta mauris. Etiam dignissim finibus lorem sed faucibus. Praesent elementum dolor at faucibus tristique. Morbi quis dui gravida, placerat metus ut, viverra elit. Curabitur vel orci non elit vehicula tempor nec sed turpis. In purus mauris, accumsan quis nulla sit amet, consequat auctor odio. Curabitur a mi id ligula interdum condimentum scelerisque ac libero.



.. code-block:: rst

   Here is a :include_tooltip:`term <Long description>`.

Results in:

Here is a :include_tooltip:`term <Long description>`.
