# Django Rest Framework Complex Filter

[![codecov](https://codecov.io/gh/kit-oz/drf-complex-filter/branch/main/graph/badge.svg?token=B6Z1LWBXOP)](https://codecov.io/gh/kit-oz/drf-complex-filter)

DRF filter for complex queries

## Installing

For installing use ``pip``

```bash
    pip install drf-complex-filter
```

## Usage

Add ``ComplexQueryFilter`` to ``filter_backends``:

```python

  from drf_complex_filter.filters import ComplexQueryFilter

  class UserViewSet(ModelViewSet):
      queryset = User.objects.all()
      serializer_class = UserSerializer
      filter_backends = [ComplexQueryFilter]

```

And get some records

```

  GET /users?filters={"type":"operator","data":{"attribute":"first_name","operator":"=","value":"John"}}
```

## Filter operator

Operator may be one of three types

```python

  # Will return Q(field_name=value_for_compare)
  operator_filter = {
    "type": "operator",
    "data": {
      "attribute": "field_name",
      "operator": "=",
      "value": "value_for_compare",
    }
  }

  # Will combine through AND all operators passed in "data"
  and_filter = {
    "type": "and",
    "data": []
  }

  # Will combine through OR all operators passed in "data"
  or_filter = {
    "type": "or",
    "data": []
  }

```

## Lookup operators

There are several basic operators in the package, but you are free to replace or expand this list.

### Existing operators

Operator label | Query operator
-------------- | --------------
Is | =
Is not | !=
Case-insensitive contains | *
Case-insensitive not contains | !
Greater | >
Greater than or is | >=
Less | <
Less than or is | <=
Value in list | in
Value not in list | not_in
Current user | me
Not current user | not_me

### Adding operators

First, create a class containing your operators. It should contain at least a "get_operators" method that returns a dictionary with your operators.

```python
class YourClassWithOperators:
    def get_operators(self):
        return {
            "simple_operator": lambda f, v, r, m: Q(**{f"{f}": v}),
            "complex_operator": self.complex_operator,
        }

    @staticmethod
    def complex_operator(field: str, value=None, request=None, model: Model = None)
        return Q(**{f"{field}": value})
```

Next, specify this class in the configuration.

```python
COMPLEX_FILTER_SETTINGS = {
    "COMPARISON_CLASSES": [
        "drf_complex_filter.comparisons.CommonComparison",
        "drf_complex_filter.comparisons.DynamicComparison",
        "path.to.your.module.YourClassWithOperators",
    ],
}
```

You can now use these operators to filter models.

## Computed value

Sometimes you need to get the value dynamically on the server side instead of writing it directly to the filter.
To do this, you can create a class containing the "get_functions" method.

```python
class YourClassWithFunctions:
    def get_functions(self):
        return {
            "calculate_value": self.calculate_value,
        }

    @staticmethod
    def calculate_value(request, model, my_arg):
        return str(my_arg)
```

Then register this class in settings.

```python
COMPLEX_FILTER_SETTINGS = {
    "VALUE_FUNCTIONS": [
        "drf_complex_filter.functions.DateFunctions",
        "path.to.your.module.YourClassWithFunctions",
    ],
}
```

And create an operator with a value like this:

```python

  value = {
    "func": "name_of_func",
    "kwargs": { "my_arg": "value_of_my_arg" },
  }

  operator_filter = {
    "type": "operator",
    "data": {
      "attribute": "field_name",
      "operator": "=",
      "value": value,
    }
  }
```

Where:

* __func__ - the name of the method to call
* __kwargs__ - a dictionary with arguments to pass to the method

The value will be calculated before being passed to the operator. That allows you to use the value obtained in this way with any operator that can correctly process it

## Subquery calculation

If you have one big query that needs to be done in chunks (not one big execution, just few small execution in related models),
You can add construction `RelatedModelName___` to your attribute name in operator,
After that, this construction is executed in a separate request. 

```python

  operator_filter = {
    "type": "operator",
    "data": {
      "attribute": "RelatedModelName___field_name",
      "operator": "=",
      "value": "value_for_compare",
    }
  }
  
  # if this RelatedModelName.objects.filter(field_name="value_for_compare") return objects with ids `2, 5, 9`,
  # so this `operator_filter` is equivalent to
  
  new_filter = {
    "type": "operator",
    "data": {
      "attribute": "RelatedModelName_id",
      "operator": "in",
      "value": [2, 5, 9],
    }
  }
  
  # and have two selects in DB:
  # `select id from RelatedModelName where field_name = 'value_for_compare'`
  # and `select * from MainTable where RelatedModelName_id in (2, 5, 9)`

```
