# python-sample
a collection of python classes and functions that I use in my projects

## content : 

### `config.py`

A class to read and write configuration files, currently only in json format.  
Support nested dictionaries and lists, as well as combined keys (e.g. `a.b.c`).  
Also support referencing other keys :
```properties
a = "hello"
b = "${a} world"
```

### `cache.py`

A decorator to cache the result of a function.  
It uses a dictionary to store the result, and a list to store the keys.  
It also support expiration time for the cache.
```python
from cache import Cache
from datetime import timedelta

@Cache(expire_in=timedelta(seconds=10))
def my_function(a, b):
    return a + b
```

### `version.py`

A class to manage versions.  
It support versions with undefined number of parts (minimum 1 part), separated by dots (e.g. `1.0`, `1.0.0`, `1.0.0.0`)
Allow comparing versions (even with different number of parts)

### `http_code.py`

An enum containing the most common HTTP status codes.
```python
from http_code import HttpCode
print(HttpCode.OK) # 200
```

### `colors.py`

A class to manage colors, allowing conversion between different color formats (RGB, RGBA, HEX), and operation like conversion to grayscale, black and white, and opposite color.
