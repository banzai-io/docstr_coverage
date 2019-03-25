import os
import re
import sys

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand

from docstr_coverage import get_docstring_coverage


class Command(BaseCommand):
    help = 'Deploys the app to the GitHub staging repo'

    def add_arguments(self, parser):
        """ Run docstr-coverage script against all the project or according to given options
        P.S. the options are duplicated from docstr-coverage package v1.0.3, except skipmagic is set as True by default
        """
        parser.add_argument(
            "-e",
            "--exclude",
            dest="exclude",
            type=str,
            help="Regex identifying filepaths to exclude",
        )
        parser.add_argument(
            "--verbose",
            dest="verbose",
            default="3",
            metavar="LEVEL",
            help="Verbosity level <0-3>, default=3",
            type=int,
            choices=[0, 1, 2, 3],
        )
        parser.add_argument(
            "-m",
            "--skipmagic",
            action="store_true",
            dest="skip_magic",
            default=True,
            help='Ignore docstrings of magic methods (except "__init__")',
        )
        parser.add_argument(
            "-f",
            "--skipfiledoc",
            action="store_true",
            dest="skip_file_docstring",
            default=False,
            help="Ignore module docstrings",
        )
        parser.add_argument(
            "-i",
            "--skipinit",
            action="store_true",
            dest="skip_init",
            default=False,
            help='Ignore docstrings of "__init__" methods',
        )
        parser.add_argument(
            "-c",
            "--skipclassdef",
            action="store_true",
            dest="skip_class_def",
            default=False,
            help="Ignore docstrings of class definitions",
        )
        parser.add_argument(
            "-l",
            "--followlinks",
            action="store_true",
            dest="follow_links",
            default=False,
            help="Follow symlinks",
        )

    def handle(self, *args, **options):
        """ If fisrt arg for docstr-coverage (directory or filename to measure docstr coverage) is not set -
        the command will collect all registered django apps (according to `settings.INSTALLED_APPS`)
        placed in `settings.BASE_DIR'.
        Extra settings:
            settings.DOCSTR_EXTRA_DIRS (list): list of extra dirs (not included to `settings.INSTALLED_APPS`)
                to include them to the docstr-coverage measure
            settings.DOCSTR_EXCLUDE (str): regex identifying filepaths to exclude used as default `exclude` parameter
        """
        if len(args) > 1:
            print("Expected a single path argument. Received invalid argument(s): {}".format(args[1:]))
            sys.exit()

        verbose = options.get('verbose')

        if not args:
            base = self.collect_dirs()
            filenames = []
            for directory in base:
                found_files = self.collect_filenames(directory, options)
                if found_files:
                    if verbose > 1:
                        print("Included {}".format(directory))
                    filenames.extend(found_files)
        else:
            base = args[0]
            if base.endswith(".py"):
                filenames = [base]
            else:
                filenames = self.collect_filenames(directory, options)

        if len(filenames) < 1:
            sys.exit("No Python files found")

        if verbose > 0:
            print("-" * 81)
            print("\n DOCSTR-COVERAGE: \n")

        code_excludes = getattr(settings, 'DOCSTR_CODE_EXCLUDES', None)

        get_docstring_coverage(
            filenames,
            skip_magic=options.get('skip_magic'),
            skip_file_docstring=options.get('skip_file_docstring'),
            skip_init=options.get('skip_init'),
            skip_class_def=options.get('skip_class_def'),
            verbose=options.get('verbose'),
            code_excludes=code_excludes,
        )

        if verbose > 0:
            print("-" * 81)
            print("\n")

    def collect_dirs(self):
        """ Collect directories to apply docstr-coverage """
        base_dirs = set(os.listdir(settings.BASE_DIR))
        app_dirs = {app.label for app in apps.get_app_configs()}
        extra_dirs = getattr(settings, 'DOCSTR_EXTRA_DIRS', [])
        app_dirs.union(extra_dirs)
        app_dirs = base_dirs.intersection(app_dirs.union(extra_dirs)) - set(['staticfiles', 'naomi'])
        return list(app_dirs)

    def collect_filenames(self, base, options):
        """ Collect filenames to apply docstr-coverage """
        exclude = options.get('exclude') or getattr(settings, 'DOCSTR_EXCLUDE', None)
        exclude_re = re.compile(r"{}".format(exclude)) if exclude else None
        filenames = []
        for root, dirs, f_names in os.walk(base, followlinks=options.get('follow_links')):
            if exclude_re is not None:
                dirs[:] = [directory for directory in dirs if not exclude_re.match(directory)]

            new_files = [os.path.join(root, directory) for directory in f_names if directory.endswith(".py")]
            if exclude_re is not None:
                filenames.extend([directory for directory in new_files if not exclude_re.match(directory)])
            else:
                filenames.extend(new_files)
        return filenames
