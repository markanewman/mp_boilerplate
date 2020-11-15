# Build the package

In order to rebuild the package, please refer to the full [PyPI](https://packaging.python.org/tutorials/packaging-projects/) instructions.
**Note:** If a step calls for `python3 ...` and it does not work, try `python ...` without the '3'.

## Quick Copy/Paste

As a quick copy paste, open an admin PowerShell window and do the below.
If it works, great.
If not, review the full documentation.

* The username is `__token__`, the password comes from PyPi's [account](https://pypi.org/manage/account/) page.
* Ctrl+v does not work.
  It is a know issue.
  Use the file menu's paste.

```{ps1}
cd "D:\repos\markanewman\mp_boilerplate"
python -m pip install --user --upgrade setuptools wheel
python setup.py sdist bdist_wheel
python -m twine upload --repository pypi dist/*
```
