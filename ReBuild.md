# Build the package

In order to rebuild the package, refer to the [PyPI](https://packaging.python.org/tutorials/packaging-projects/) instructions.
Note: If a step calls for `python3 ...` and it does not work, try `python ...` without the '3'.

```{ps1}
python setup.py sdist bdist_wheel
python -m twine upload --repository pypi dist/*
```
