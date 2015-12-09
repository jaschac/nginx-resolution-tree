# -*- coding: utf-8 -*-

"""
This module tests the Location module.
"""

from nrt.location import Location
from nrt.tests.test_base import TestBase


class TestLocation(TestBase):
    """
    A class containing unit tests for the Location module.
    """
    def setUp(self, *args, **kwargs):
        '''
        Initializes whatever is needed during the tests.
        '''
        super(TestLocation, self).setUp(*args, **{
                                                    "test_module_filename" : __file__
                                                    }
                                        )
        self.valid_alias = "foo"
        self.valid_location_root = "/"
        self.valid_location = "/var/www/foo/"


    def test_init_correct(self):
        """
        Tests that an Location object is properly instantiated if a proper location is passed in
        during initialization. 
        """
        handle_location = Location(**{
                                        "location" : self.valid_location
                                        }
                                    )
        self.assertEqual(handle_location.location, self.valid_location)
        self.assertEqual(handle_location.alias, [])
        self.assertFalse(handle_location.is_valid)
        del handle_location


    def test_init_correct_root(self):
        """
        Tests that an Location object is properly instantiated if a root location, that is a simple
        forward slash, is passed in during initialization.
        """
        handle_location = Location(**{
                                        "location" : self.valid_location_root
                                        }
                                    )
        self.assertEqual(handle_location.location, self.valid_location_root)
        self.assertEqual(handle_location.alias, [])
        self.assertFalse(handle_location.is_valid)
        del handle_location


    def test_init_wrong_missing_location(self):
        """
        Tests that an Location object cannot be instantiated and a ValueError exception is raised
        if the location is not passed.
        """
        self.assertRaises(
                            ValueError,
                            Location,
                            **{}
                            )


    def test_init_wrong_mistyped_location(self):
        """
        Tests that an Location object cannot be instantiated and a TypeError exception is raised
        if a location is passed in, but it's not a string.
        """
        self.assertRaises(
                            TypeError,
                            Location,
                            **{
                                "location" : 1234,
                                }
                            )


    def test_init_wrong_misfromatted_location(self):
        """
        Tests that an Location object cannot be instantiated and a TypeError exception is raised
        if a location is passed in as a string, but it does not have the required format.
        """
        for wrong_location in "/wrong", "wrong/", "", "wrong":
            self.assertRaises(
                                ValueError,
                                Location,
                                **{
                                    "location" : wrong_location,
                                    }
                                )


    def test_alias_correct_multiple_times_the_same_alias(self):
        """
        Tests that if a Location object is passed multiple times the same alias, only one is
        stored.
        """
        handle_location = Location(**{
                                        "location" : self.valid_location
                                        }
                                    )
        for i in range(10):
            handle_location.alias = self.valid_alias
        self.assertEqual(handle_location.alias.count(self.valid_alias), 1)
        del handle_location


    def test_alias_wrong_missing(self):
        """
        Tests that a ValueError exception is raised if a Location is assigned an alias, but no
        alias is passed in.
        """
        handle_location = Location(**{
                                        "location" : self.valid_location
                                        }
                                    )
        self.assertRaises(
                            ValueError,
                            setattr,
                            handle_location,
                            "alias",
                            None,
                            )
        del handle_location


    def test_alias_wrong_mistyped(self):
        """
        Tests that a TypeError exception is raised if a Location is assigned an alias that is not
        a string.
        """
        handle_location = Location(**{
                                        "location" : self.valid_location
                                        }
                                    )
        self.assertRaises(
                            TypeError,
                            setattr,
                            handle_location,
                            "alias",
                            123,
                            )
        del handle_location


    def test_alias_wrong_misformatted(self):
        """
        Tests that a TypeError exception is raised if a Location is assigned an empty string as an
        alias.
        """
        handle_location = Location(**{
                                        "location" : self.valid_location
                                        }
                                    )
        self.assertRaises(
                            ValueError,
                            setattr,
                            handle_location,
                            "alias",
                            "",
                            )
        del handle_location


    def test_is_valid_correct_one_alias(self):
        """
        Tests that the is_valid property correctly returns True if the Location is assigned a
        unique alias.
        """
        handle_location = Location(**{
                                        "location" : self.valid_location
                                        }
                                    )
        handle_location.alias = self.valid_alias
        self.assertTrue(handle_location.is_valid)
        del handle_location


    def test_is_valid_correct_no_alias(self):
        """
        Tests that the is_valid property correctly returns False if the Location is not assigned
        an alais at all.
        """
        handle_location = Location(**{
                                        "location" : self.valid_location
                                        }
                                    )
        self.assertFalse(handle_location.is_valid)
        del handle_location


    def test_is_valid_correct_multiple_aliases(self):
        """
        Tests that the is_valid property correctly returns False if the Location is assigned two or
        more aliases.
        """
        handle_location = Location(**{
                                        "location" : self.valid_location
                                        }
                                    )
        handle_location.alias = "foo1"
        handle_location.alias = "foo2"
        self.assertFalse(handle_location.is_valid)
        del handle_location
