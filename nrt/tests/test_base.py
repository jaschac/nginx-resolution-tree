# -*- coding: utf-8 -*-

"""
This module provides all tests with a common base to build upon.
"""

from pickle import loads
from re import sub
from os.path import basename, dirname, realpath
from unittest import main, TestCase

class TestBase(TestCase):

    def setUp(self, *args, **kwargs):
        """
        Initializes whatever is commonly needed by all test modules.

        self.mocks: this dictionary is dynamically filled in with data coming from the pickle
        containing a module's mock data. When a specific test module is being setup, it does pass
        to the base its (file)name, so that the base can dynamically use it to load its own data.

        For example, the test module test_nrt would find in self.mocks the content of the
        pickle file nrt/tests/files/nrt.p.
        """
        _test_module_filename   =   kwargs.get("test_module_filename", None)
        self.mocks              =   None
        self.verbose_mode       =   kwargs.get("verbose_mode", False)

        # Load the mocks' JSON of a specific test module
        try:
            _test_module_mocks_filename = "%s/files/%s" % (dirname(realpath(__file__)), sub("test_", "", sub("py", "p", basename(_test_module_filename))))
            with open(_test_module_mocks_filename, "rb") as _test_module_mocks_file_handle:
                self.mocks = loads(_test_module_mocks_file_handle.read())
        except (IOError, ValueError) as e:
            if self.verbose_mode:
                print("An error occurred trying to load %s's mocks: %s" % (basename(_test_module_filename), e))
        except AttributeError as e:
            if self.verbose_mode:
                print("The setUp method MUST be provided with the test_module_filename parameter.")
        except Exception as e:
            if self.verbose_mode:
                print("Some unexpected error happened: %s" % (e))

if __name__ == '__main__':
    main()