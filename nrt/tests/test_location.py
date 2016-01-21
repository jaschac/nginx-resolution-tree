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
        self.valid_languages = ["html", "php", "python"]
        self.valid_location_root = "/"
        self.valid_location = "/var/www/foo/"


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


    def test_build_correct(self):
        """
        Tests that the _build method properly turns the directives into unique alias entries.
        """
        handle_location = Location(**{
                                        "location" : self.valid_location
                                        }
                                    )
        directives = [
                        { "signature" : "a:0.0.0.0:80:a.b.c.d:/"},
                        { "signature" : "b:0.0.0.0:80:a.b.c.d:/"},
                        ]
        for directive in directives:
            handle_location.directives = directive
        self.assertEqual(len(handle_location.alias), 2)
        del handle_location


    def test_build_correct_no_dupes(self):
        """
        Tests that the _build method properly generates a unique alias if provided with the same
        alias twice.
        """
        handle_location = Location(**{
                                        "location" : self.valid_location
                                        }
                                    )
        alias = "this_container"
        directives = [
                        { "signature" : "%s:0.0.0.0:80:a.b.c.d:/" % (alias)},
                        { "signature" : "%s:0.0.0.0:80:a.b.c.d:/" % (alias)},
                        ]
        for directive in directives:
            handle_location.directives = directive
        self.assertEqual(len(handle_location.alias), 1)
        self.assertEqual(list(handle_location.alias)[0], alias)
        del handle_location


    def test_directives_correct(self):
        """
        Tests that a Location object properly returns the directives that were assigned to it.
        """
        directives = [
                        { "signature" : "a:0.0.0.0:80:a.b.c:/"},
                        { "signature" : "a:0.0.0.0:8080:a.b.c:/"}
                        ]
        handle_location = Location(**{
                                        "location" : self.valid_location
                                        }
                                    )
        for directive in directives:
            handle_location.directives = directive
        self.assertEqual(len(handle_location.directives), 2)
        for directive, expected_directive in zip(handle_location.directives, directives):
            self.assertEqual(directive, expected_directive)
        del handle_location


    def test_directives_correct_empty(self):
        """
        Tests that a Location object properly returns an empty list, if no directive was
        assigned to it.
        """
        handle_location = Location(**{
                                        "location" : self.valid_location
                                        }
                                    )
        self.assertEqual(handle_location.directives, [])
        del handle_location


    def test_directives_correct_no_dupes(self):
        """
        Tests that a Location object properly returns a unique directive if the same directive
        is added multiple times.
        """
        directive = { "signature" : "a:0.0.0.0:80:a.b.c:/"}
        handle_location = Location(**{
                                        "location" : self.valid_location
                                        }
                                    )
        for i in range(10):
            handle_location.directives = directive
        self.assertEqual(len(handle_location.directives), 1)
        self.assertEqual(directive, handle_location.directives[0])
        del handle_location
        

    def test_directives_wrong_missing_directive(self):
        """
        Tests that a ValueError exception is raised if we try to add a directive to a ServerName
        object but we don't pass any.
        """
        handle_location = Location(**{
                                        "location" : self.valid_location
                                        }
                                    )
        self.assertRaises(
                            ValueError,
                            setattr,
                            handle_location,
                            "directives",
                            None,
                            )
        del handle_location


    def test_directives_wrong_mistyped_directive(self):
        """
        Tests that a TypeError exception is raised if we try to add a directive to a Listen
        object but the directive passed in is not a dictionary.
        """
        handle_location = Location(**{
                                        "location" : self.valid_location
                                        }
                                    )
        self.assertRaises(
                            TypeError,
                            setattr,
                            handle_location,
                            "directives",
                            "not_a_dictionary",
                            )
        del handle_location


    def test_directives_wrong_missing_signature(self):
        """
        Tests that a ValueError exception is raised if we try to add a directive to a Listen
        object but the directive passed in, despite being a dictionary, lacks the 'signature'
        key.
        """
        handle_location = Location(**{
                                        "location" : self.valid_location
                                        }
                                    )
        self.assertRaises(
                            ValueError,
                            setattr,
                            handle_location,
                            "directives",
                            {"not_signature" : 124}
                            )
        del handle_location


    def test_directives_wrong_mistyped_signature(self):
        """
        Tests that a TypeError exception is raised if we try to add a directive to a Listen
        object but the directive passed in has a signature that is not a string.
        """
        handle_location = Location(**{
                                        "location" : self.valid_location
                                        }
                                    )
        self.assertRaises(
                            TypeError,
                            setattr,
                            handle_location,
                            "directives",
                            {"signature" : 124}
                            )
        del handle_location


    def test_directives_wrong_misformatted_signature(self):
        """
        Tests that a ValueError exception is raised if we try to add a directive to a Listen
        object but the directive passed in has a signature that has a wrong format.
        """
        handle_location = Location(**{
                                        "location" : self.valid_location
                                        }
                                    )
        self.assertRaises(
                            ValueError,
                            setattr,
                            handle_location,
                            "directives",
                            {"signature" : "wrong_format"}
                            )
        del handle_location


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
        self.assertEqual(handle_location.language, 'html')
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
        self.assertEqual(handle_location.language, 'html')
        self.assertEqual(handle_location.alias, [])
        self.assertFalse(handle_location.is_valid)
        del handle_location


    def test_init_correct_language(self):
        """
        Tests that an Location object is properly instantiated if, apart from a proper location, the
        object is passed in a valid language.
        """
        for language in self.valid_languages:
            handle_location = Location(**{
                                            "language" : language,
                                            "location" : self.valid_location
                                            }
                                        )
            self.assertEqual(handle_location.location, self.valid_location)
            self.assertEqual(handle_location.language, language)
            self.assertEqual(handle_location.alias, [])
            self.assertFalse(handle_location.is_valid)
            del handle_location


    def test_init_correct_language_explicitly_set_to_none(self):
        """
        Tests that an Location object is properly instantiated and the language set by default to
        'html' if, apart from a proper location, the language is explicitly set to None.
        """
        handle_location = Location(**{
                                        "language" : None,
                                        "location" : self.valid_location
                                        }
                                    )
        self.assertEqual(handle_location.location, self.valid_location)
        self.assertEqual(handle_location.language, 'html')
        self.assertEqual(handle_location.alias, [])
        self.assertFalse(handle_location.is_valid)
        del handle_location


    def test_init_wrong_invalid_language(self):
        """
        Tests that an Location object cannot be instantiated and a ValueError exception is raised
        if a language is passed in as a string, but its value is not among the valid ones.
        """
        self.assertRaises(
                            ValueError,
                            Location,
                            **{
                                "language" : "ruby",
                                "location" : self.valid_location,
                                }
                            )


    def test_init_wrong_mistyped_language(self):
        """
        Tests that an Location object cannot be instantiated and a TypeError exception is raised
        if a language is passed in, but not as a string.
        """
        self.assertRaises(
                            TypeError,
                            Location,
                            **{
                                "language" : 1234,
                                "location" : self.valid_location,
                                }
                            )


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
