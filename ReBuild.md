# Build the package

In order to rebuild the package, refer to the full [PyPI](https://packaging.python.org/tutorials/packaging-projects/) instructions.
**Note:** If a step calls for `python3 ...` and it does not work, try `python ...` without the '3'.

# Quick Copy/Paste

Below is a quick copy paste script.
If it does not work, you will need to follow the full instructions above.
The username is `__token__` and the password is the API token from PyPi's [account](https://pypi.org/manage/account/) page.
**Note:** the user/pass does not work with ctrl+v.
Instead, use the upper left icon to paste.


```{ps1}
cd "D:\repos\markanewman\mp_boilerplate"
remove-item build
remove-item dist
remove-item mp_boilerplate.egg-info
python setup.py sdist bdist_wheel
python -m twine upload --repository pypi dist/*
```
