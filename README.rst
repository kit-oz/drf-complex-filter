====================================
Django Rest Framework Complex Filter
====================================

DRF filter for complex queries

Installing
----------

For installing use ``pip``

::

    $ pip install drf-complex-filter

Usage
-----

Add ``ComplexQueryFilter`` to ``filter_backends``:

::

  from drf_complex_filter.filters import ComplexQueryFilter


  class UserViewSet(ModelViewSet):
      queryset = User.objects.all()
      serializer_class = UserSerializer
      filter_backends = [ComplexQueryFilter]



And get some records

::

  GET /users?filters={"type":"operator","data":{"attribute":"first_name","operator":"=","value":"John"}}

Filter operator
---------------

Operator may be one of three types

::

  {
    "type": "operator",
    "data": {
      "attribute": "field_name",
      "operator": "one_of_lookup_operators",
      "value": "value_for_compare",
    }
  }


::

  {
    "type": "and",
    "data": []
  }


::

  {
    "type": "or",
    "data": []
  }




Lookup operators
----------------

=============================  ==============
Operator label                 Query operator
=============================  ==============
Is                             =
Is not                         !=
Greater                        >
Greater than or is             >=
Less                           <
Less than or is                <=
Case-insensitive contains      \*
Case-insensitive not contains  !
Case-sensitive contains        cnt
Case-sensitive not contains    ncnt
=============================  ==============
