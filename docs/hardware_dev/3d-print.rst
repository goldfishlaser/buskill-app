Header 1
========
--------
Subtitle
--------

Example text.

.. contents:: Table of Contents

Header 2
--------

1. Blah blah ``code`` blah

2. More ``code``, hooray

3. Somé UTF-8°

The UTF-8 quote character in this table used to cause python to go boom. Now docutils just silently ignores it.

.. csv-table:: Things that are Awesome (on a scale of 1-11)
	:quote: ”

	Thing,Awesomeness
	Icecream, 7
	Honey Badgers, 10.5
	Nickelback, -2
	Iron Man, 10
	Iron Man 2, 3
	Tabular Data, 5
	Made up ratings, 11

.. code::

	A block of code

.. code:: python

	python.code('hooray')
	
.. code:: javascript

	export function ƒ(ɑ, β) {}

.. doctest:: ignored