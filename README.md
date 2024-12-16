# Django Complex Filter

[![codecov](https://codecov.io/gh/kit-oz/drf-complex-filter/branch/main/graph/badge.svg?token=B6Z1LWBXOP)](https://codecov.io/gh/kit-oz/drf-complex-filter)
[![PyPI version](https://badge.fury.io/py/drf-complex-filter.svg)](https://badge.fury.io/py/drf-complex-filter)
[![Python Versions](https://img.shields.io/pypi/pyversions/drf-complex-filter.svg)](https://pypi.org/project/drf-complex-filter/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful and flexible declarative filter for Django ORM that enables complex query construction through a simple JSON-based API. Perfect for building advanced filtering capabilities in your Django REST Framework applications.

## Features

- **Advanced Filtering**: Complex AND/OR operations with nested conditions
- **Declarative Syntax**: Simple JSON-based query structure
- **Dynamic Values**: Support for computed values and server-side calculations
- **Related Model Queries**: Efficient subquery handling for related models
- **Extensible**: Easy to add custom operators and value functions
- **Type Safe**: Built-in operator validation
- **DRF Integration**: Seamless integration with Django REST Framework

## Installation

```bash
pip install drf-complex-filter
```

## Quick Start

1. Add `ComplexQueryFilter` to your ViewSet:

```python
from drf_complex_filter.filters import ComplexQueryFilter

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [ComplexQueryFilter]
```

2. Make API requests with complex filters:

```bash
# Simple equality filter
GET /users?filters={"type":"operator","data":{"attribute":"first_name","operator":"=","value":"John"}}

# Complex AND condition
GET /users?filters={"type":"and","data":[
    {"type":"operator","data":{"attribute":"age","operator":">","value":18}},
    {"type":"operator","data":{"attribute":"is_active","operator":"=","value":true}}
]}
```

## Filter Types

### 1. Simple Operator
```python
{
    "type": "operator",
    "data": {
        "attribute": "field_name",
        "operator": "=",
        "value": "value_to_compare"
    }
}
```

### 2. AND Operator
```python
{
    "type": "and",
    "data": [
        # List of operators to combine with AND
    ]
}
```

### 3. OR Operator
```python
{
    "type": "or",
    "data": [
        # List of operators to combine with OR
    ]
}
```

## Available Operators

| Operator | Description | Symbol |
|----------|-------------|---------|
| Is | Equality | = |
| Is not | Inequality | != |
| Contains | Case-insensitive contains | * |
| Not contains | Case-insensitive not contains | ! |
| Greater | Greater than | > |
| Greater or equal | Greater than or equal | >= |
| Less | Less than | < |
| Less or equal | Less than or equal | <= |
| In | Value in list | in |
| Not in | Value not in list | not_in |
| Current user | Current authenticated user | me |
| Not current user | Not current authenticated user | not_me |

## Advanced Features

### Custom Operators

1. Create your operator class:
```python
class CustomOperators:
    def get_operators(self):
        return {
            "custom_op": lambda f, v, r, m: Q(**{f"{f}__custom": v}),
        }
```

2. Register in settings:
```python
COMPLEX_FILTER_SETTINGS = {
    "COMPARISON_CLASSES": [
        "drf_complex_filter.comparisons.CommonComparison",
        "path.to.CustomOperators",
    ],
}
```

### Dynamic Values

1. Create value functions:
```python
class CustomFunctions:
    def get_functions(self):
        return {
            "current_time": lambda request, model: timezone.now(),
        }
```

2. Register in settings:
```python
COMPLEX_FILTER_SETTINGS = {
    "VALUE_FUNCTIONS": [
        "drf_complex_filter.functions.DateFunctions",
        "path.to.CustomFunctions",
    ],
}
```

3. Use in filters:
```python
{
    "type": "operator",
    "data": {
        "attribute": "created_at",
        "operator": ">",
        "value": {
            "func": "current_time",
            "kwargs": {}
        }
    }
}
```

### Related Model Queries

Use `ModelName___` prefix for efficient subqueries:
```python
{
    "type": "operator",
    "data": {
        "attribute": "Profile___is_verified",
        "operator": "=",
        "value": true
    }
}
```

## Requirements

- Python >= 3.6
- Django >= 3.0.0
- Django REST Framework

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
