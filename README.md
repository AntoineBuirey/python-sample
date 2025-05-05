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
Will automatically reload the file if it detected that the file has changed.

Support logging with [gamuLogger](https://github.com/T0ine34/gamuLogger). if not installed, will print nothing.

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

Support logging with [gamuLogger](https://github.com/T0ine34/gamuLogger). if not installed, will print nothing.

### `version.py`

A class to manage versions.  
Compliant with [semver](https://semver.org/) and support comparison between versions.
```python
from version import Version
v1 = Version(1,0,0)
v2 = Version(1,0,1)
print(v1 < v2) # True
```
Support incrementing and decrementing the version, as well as converting to string.
```python
v1.major_increment() # 2.0.0
v1.patch_increment() # 2.0.1
v1.minor_increment() # 2.1.0 (reset patch to 0)
v1.major_decrement() # 1.0.0 (reset minor and patch to 0)
```

Support converting to string, and parsing from string.
```python
v1 = Version.from_string("1.0.0")
print(str(v1)) # 1.0.0
```

Support pre-release and build metadata.
```python
v1 = Version(1,0,0,"alpha", "build.1")
print(str(v1)) # 1.0.0-alpha+build.1
```



### `http_code.py`

An enum containing the most common HTTP status codes.
```python
from http_code import HttpCode
print(HttpCode.OK) # 200
```

### `colors.py`

A class to manage colors, allowing conversion between different color formats (RGB, RGBA, HEX), and operation like conversion to grayscale, black and white, and opposite color.
