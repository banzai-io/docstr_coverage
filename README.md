Docstr-Coverage
===============

If the health of your documentation is in dire straits, `docstr-coverage` will see you now.

`docstr-coverage` is a simple tool that lets you measure your Python source code's
[docstring](http://www.python.org/dev/peps/pep-0257/#what-is-a-docstring) coverage. It can show you which of your functions,
classes, methods, and modules don't have docstrings. It also provide statistics about overall docstring coverage for individual
files, and for your entire project.
It's based on docstr-coverage:

* **Source:** https://github.com/HunterMcGushion/docstr_coverage
* **Documentation:** [https://docstr-coverage.readthedocs.io](https://docstr-coverage.readthedocs.io/en/latest/api_essentials.html)


Current version applies support for Django project (requires Django >= 1.11):

##### Django manage command to measure the coverage against full project:

Example:
-------

```
>>> banzai-platform-django$ python manage.py docstr_coverage

Included common
Included accounts
---------------------------------------------------------------------------------

 DOCSTR-COVERAGE:


File: "common/diff_tracker.py"
 - No module docstring
 Needed: 40; Found: 39; Missing: 1; Coverage: 97.5%

File: "accounts/factories.py"
 - No module docstring
 Needed: 9; Found: 8; Missing: 1; Coverage: 88.9%

...
Overall statistics for 122 files (10 files are empty):
Docstrings needed: 1518; Docstrings found: 603; Docstrings missing: 915
Total docstring coverage: 39.7%;  Grade: Not good
---------------------------------------------------------------------------------
```

How Do I Use It?
----------------

#### The command takes all options supported by base version, but <path to dir or module> is not required,
the command will collect all registered django apps (according to `settings.INSTALLED_APPS`). Extra settings could be applied using:
* settings.DOCSTR_EXTRA_DIRS (list): list of extra dirs (not included to `settings.INSTALLED_APPS`)
                                     to include them to the docstr-coverage measure;
* settings.DOCSTR_EXCLUDE (str): regex identifying filepaths to exclude used as default `exclude` parameter;
* settings.DOCSTR_CODE_EXCLUDES (dic): dict with extra excludes directly for code, examples:

```python
DOCSTR_CODE_EXCLUDES = {
    'MODULES': ("views.py", "forms.py", "factories.py", "models.py", "admin.py"),  # list of modules to skip module-level docstring
    'NAMES': (  # tuple with name regex to skip docstrings
        '[A-Z].*(Form|Admin|TestCase|Model)$',  # skip all class names that end on Form/Admin/TestCase/Model
        '[A-Z].*View[.]get_success_url',  # skip <get_success_url> for all Views
        '[A-Z].*Manager[.]get_queryset',  # skip <get_queryset> for all Managers
        'Meta',  # skip all <class Meta> definitions
    ),
}
```
By default the command Ignore all magic methods (skipmagic=True).
The command supports all options from docstr-coverage package v1.0.3 and could be used agains any directry/file.

##### Options:
* *--skipmagic, -m* - Ignore all magic methods (like `__init__`, and `__str__`)
* *--skipfiledoc, -f* - Ignore module docstrings (at the top of files)
* *--exclude=\<regex\>, -e \<regex\>* - Filepath pattern to exclude from analysis
    * To exclude the contents of a virtual environment `env` and your `tests` directory, run:
    <br>```$ docstr-coverage some_project/ -e "env/*|tests/*"```
* *--verbose=\<level\>, -v \<level\>* - Set verbosity level (0-3)
    * 0 - Silence
    * 1 - Print overall statistics
    * 2 - Also print individual statistics for each file
    * 3 - Also print missing docstrings (function names, class names, etc.)

Usage:
-------

Measure docstr coverage for all apps:
```
>>> banzai-platform-djangeo$ python manage.py docstr_coverage
```

Measure docstr coverage for `accounts` module:
```
>>> banzai-platform-djangeo$ python manage.py docstr_coverage accounts
```

Measure docstr coverage for all apps with verbosity lvl 1:
```
>>> banzai-platform-djangeo$ python manage.py docstr_coverage --verbose=1
```

Measure docstr coverage for `accounts` module, skip skipfiledoc with verbosity lvl 1:
```
>>> banzai-platform-djangeo$ python manage.py docstr_coverage -f --verbose=1
```

#### Package in Your Project

As for base version. you can also use `docstr-coverage` as a part of your project by importing it thusly, it also takes optional code_excludes arg, with structure as settings.DOCSTR_CODE_EXCLUDES:

```python
from django.conf import settings
from docstr_coverage import get_docstring_coverage

my_coverage = get_docstring_coverage(
    ['some_dir/file_0.py', 'some_dir/file_1.py'],
    code_excludes=settings.DOCSTR_CODE_EXCLUDES)


code_excludes = {
    'MODULES': ("views.py", "forms.py", "factories.py", "models.py", "admin.py")
}
my_coverage = get_docstring_coverage(
    ['some_dir/file_0.py', 'some_dir/file_1.py'],
    code_excludes=code_excludes)

```

##### Arguments:
* Required arg: `filenames` \<list of string filenames\>
* Optional kwargs: `skip_magic` \<bool\>, `skip_file_docstring` \<bool\>, `verbose` \<int (0-3)\>
	* For more info on `get_docstring_coverage` and its parameters, please see its [documentation](https://docstr-coverage.readthedocs.io/en/latest/api_essentials.html#get-docstring-coverage)

##### Results:
```get_docstring_coverage``` returns two dicts: 1) stats for each file, and 2) total stats.
For more info, please see the `get_docstring_coverage` [documentation](https://docstr-coverage.readthedocs.io/en/latest/api_essentials.html#get-docstring-coverage)


Installation
------------

```
pip install git+https://github.com/banzai-io/docstr_coverage.git
```
