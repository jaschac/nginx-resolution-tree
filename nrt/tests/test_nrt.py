# -*- coding: utf-8 -*-

"""
This module tests the Nrt module.
"""
from collections import defaultdict

from nrt.nrt import Nrt
from nrt.tests.test_base import TestBase


class TestNrt(TestBase):
    """
    A class containing unit tests for the Nrt module.
    """
    def setUp(self, *args, **kwargs):
        '''
        Initializes whatever is needed during the tests.
        '''
        super(TestNrt, self).setUp(*args, **{
                                                "test_module_filename" : __file__
                                                }
                                    )


    def test_init_correct(self):
        """
        Tests that an Nrt object is properly instantiated if its mandatory parameters are properly
        passed in.
        """
        directives = [
                        { "signature" : "a:0.0.0.0:80:a.b.c:/"},
                        ]
        handle_nrt = Nrt(**{
                                "directives" : directives
                                }
                            )
        self.assertEqual(directives, handle_nrt.directives)


    def test_init_correct_no_directives(self):
        """
        Tests that an Nrt object is properly instantiated if its mandatory parameters are properly
        passed in but they are empty.
        """
        directives = []
        handle_nrt = Nrt(**{
                                "directives" : directives
                                }
                            )
        self.assertEqual(directives, handle_nrt.directives)


    def test_init_wrong_mistyped_directives(self):
        """
        Tests that a TypeError exception is raised if an Nrt is initialized with the directives
        parameter not being a list.
        """
        self.assertRaises(
                            TypeError,
                            Nrt,
                            **{
                                "directives" : "not_a_list",
                                }
                            )


    def test_init_wrong_mistyped_directive(self):
        """
        Tests that a TypeError exception is raised if any of the directives passed in to Nrt is not
        a dictionary.
        """
        self.assertRaises(
                            TypeError,
                            Nrt,
                            **{
                                "directives" : [
                                                "not_a_dictionary_1",
                                                "not_a_dictionary_2",
                                                ],
                                }
                            )


    def test_init_wrong_directive_missing_signature(self):
        """
        Tests that a ValueError exception is raised if any of the directives passed in to Nrt does
        not have the mandatory signature key.
        """
        self.assertRaises(
                            ValueError,
                            Nrt,
                            **{
                                "directives" : [
                                                {"not_signature" : 124,},
                                                ],
                                }
                            )


    def test_init_wrong_directive_mistyped_signature(self):
        """
        Tests that a TypeError exception is raised if any of the directives passed in to Nrt has
        a signature that is not a string.
        """
        self.assertRaises(
                            TypeError,
                            Nrt,
                            **{
                                "directives" : [
                                                {"signature" : ["not_a_string"],},
                                                ],
                                }
                            )


    def test_init_wrong_directive_misformatted_signature(self):
        """
        Tests that a TypeError exception is raised if any of the directives passed in to Nrt has
        a signature with the wrong format.
        """
        self.assertRaises(
                            ValueError,
                            Nrt,
                            **{
                                "directives" : [
                                                {"signature" : "wrong_format",},
                                                ],
                                }
                            )


    def test_listens_correct(self):
        """
        Tests that the listen method turns the input directives into proper Listen objects.
        """
        handle_nrt = Nrt(**{
                                "directives" : [
                                                    { "signature" : "a:0.0.0.0:80:a.b.c:/"},
                                                ]
                                }
                            )
        handle_nrt.listens()
        expected_response = defaultdict(list)
        expected_response["0.0.0.0:80"].append("a:a.b.c:/")
        self.assertEqual(handle_nrt.listen, expected_response)


    def test_listens_correct_no_directives(self):
        """
        Tests that the listen method generated an tempy list of directives into an empty list of
        Listen objects.
        """
        handle_nrt = Nrt(**{
                                "directives" : []
                                }
                            )
        handle_nrt.listens()
        expected_response = defaultdict(list)
        self.assertEqual(handle_nrt.listen, expected_response)
