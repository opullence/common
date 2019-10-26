# python-project-template
Python project template used as starting point for other projects.

## Content

Basic python project containing the minimum working elements so as to create a clean python package.

## Explanation
### `docs/`
Sphinx generated documentation of the project. This folder contains:
- `api.rst`: a brief description of the API,
- `conf.py`: configuration file of Sphinx, where you can specify the name of the project, the version and so on,
- `index.rst`: home page of the documentation,
- `installation.rst`: installation procedure of the package,
- `make.bat`: bat script for making the documentation,
- `Makefile`: file used to make the documentation.

### `requirements/`
Contains requirements files for `pip install`:
- `development.txt`: development requirements, consists in production+others packages,
- `production.txt`: minimum requirements, for use in production.

### `tests/`
Unit testing script files. Unit testing is done using `unittest`. This folder should contains an `__init__.py` file. Each unit testing script should be named `test_featurename.py`.

### `opulence/python_template/`
Core of the package. Contains all the source codes. Be careful to add the relevant sub-modules in the `__init__.py` for installation.

### `.gitignore`
Contains the files not concerned by the Git versionning.

### `.pre-commit-config.yaml`
Ensure code quality before a commit. Be sure to have `pre-commit` installed in your environment using:

    pip install pre-commit

Then launch `pre-commit` for your project:

    pre-commit install

Now for every new commit `pre-commit` will check several requirements for a good code quality.

### `LICENSE`
License file.

### `pyproject.toml`
Setup environment basic package requirements to properly install the package.

### `README.md`
The present document. Contains a overall description of the package.

### `requirements.txt`
Requirement file used before to install the package.

### `setup.cfg`
Configuration file for setup. Run several tests for ensure good code quality.

### `setup.py`
Setup file to install the package.

### `tox.ini`
Configuration of `tox`: run tests on several versions of Python to ensure compatibility.
