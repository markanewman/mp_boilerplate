# mp_boilerplate

A collection of patterns to use over top of the built in multiprocessing package.

# Install

```{shell}
pip install mp_boilerplate
```

# Use Case: (E)xtract (P)arallel (T)ransform (S)ave

The extract parallel transform save (EPTS) use case is as follows:

* A producer(single)/consumer(multiple) that applies a transform
* A producer(multiple)/consumer(single) that saves the transform

This usually means: read a file/folder, do something to each item, save the result.

```{py}
import mp_boilerplate as mpb
import typing as t
from typeguard import typechecked

def extract() -> t.Iterator:
    for i in range(100):
        yield i
def transform(i):
    return i + 1
def save(items: t.Iterator):
    for item in items:
        print(item)

if __name__ == '__main__':
    worker = mpb.EPTS(extract, transform, save)
    worker.start()
    worker.join()
```
