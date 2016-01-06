# -*- coding: utf-8 -*-

"""
This module tests the Nrt module.
"""
from collections import defaultdict

from nrt.listen import Listen
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


    def test_build_correct(self):
        """
        Tests that the _build method properly turns the directives into unique Listen objects.
        """
        handle_nrt = Nrt(**{})
        directives = [
                        { "signature" : "a:0.0.0.0:80:a.b.c:/"},
                        { "signature" : "a:0.0.0.0:8080:a.b.c:/"},
                        { "signature" : "a:0.0.0.0:80:a.b.c:/"},
                        ]
        for directive in directives:
            handle_nrt.directives = directive
        self.assertEqual(handle_nrt.listen, {})
        handle_nrt._build()
        self.assertEqual(len(handle_nrt.listen.keys()), 2)
        del handle_nrt


    def test_build_correct_no_dupes(self):
        """
        Tests that the _build method properly generate a unique Listen object if we try to resolve
        the same address twice but the directives per se are different.
        """
        handle_nrt = Nrt(**{})
        address = "0.0.0.0:80"
        directives = [
                        { "signature" : "a:%s:a.b.c:/" % (address)},
                        { "signature" : "a:%s:aa.bb.cc:/" % (address)},
                        ]
        for directive in directives:
            handle_nrt.directives = directive
        handle_nrt._build()
        self.assertEqual(len(handle_nrt.listen.keys()), 1)
        self.assertEqual(list(handle_nrt.listen.keys())[0], address)
        del handle_nrt


    def test_directives_correct(self):
        """
        Tests that an Nrt object properly returns the directives that were added to it.
        """
        handle_nrt = Nrt(**{})
        directives = [
                        { "signature" : "a:0.0.0.0:80:a.b.c:/"},
                        { "signature" : "a:0.0.0.0:8080:a.b.c:/"}
                        ]
        for directive in directives:
            handle_nrt.directives = directive
        response = handle_nrt.directives
        for directive, expected_directive in zip(response, directives):
            self.assertEqual(directive, expected_directive)
        del handle_nrt


    def test_directives_correct_no_dupes(self):
        """
        Tests that an Nrt object only stores a unique copy of directives having the same signature.
        """
        handle_nrt = Nrt(**{})
        directives = [
                        { "signature" : "a:0.0.0.0:80:a.b.c:/"},
                        { "signature" : "a:0.0.0.0:80:a.b.c:/"},
                        { "signature" : "a:0.0.0.0:80:a.b.c:/"},
                        ]
        for directive in directives:
            handle_nrt.directives = directive
        response = handle_nrt.directives
        self.assertEqual(len(response), 1)
        del handle_nrt


    def test_directives_correct_no_directives(self):
        """
        Tests that an emtpy list is returned if an Nrt object isn't given any directive.
        """
        handle_nrt = Nrt(**{})
        response = handle_nrt.directives
        expected_response = []
        self.assertEqual(response, expected_response)
        del handle_nrt


    def test_directives_wrong_missing_directive(self):
        """
        Tests that a ValueError exception is raised if we try to add a directive without passing
        one in.
        """
        handle_nrt = Nrt(**{})
        self.assertRaises(
                            ValueError,
                            setattr,
                            handle_nrt,
                            "directives",
                            None,
                            )
        del handle_nrt


    def test_directives_wrong_mistyped_directive(self):
        """
        Tests that a TypeError exception is raised if we try to add a directive but the directive
        itself is not a dictionary.
        """
        handle_nrt = Nrt(**{})
        self.assertRaises(
                            TypeError,
                            setattr,
                            handle_nrt,
                            "directives",
                            "not_a_dictionary",
                            )
        del handle_nrt


    def test_directives_wrong_missing_signature(self):
        """
        Tests that a ValueError exception is raised if any of the directives passed in to Nrt does
        not have the mandatory signature key.
        """
        handle_nrt = Nrt(**{})
        self.assertRaises(
                            ValueError,
                            setattr,
                            handle_nrt,
                            "directives",
                            {"not_signature" : 124},
                            )
        del handle_nrt


    def test_directives_wrong_mistyped_signature(self):
        """
        Tests that a TypeError exception is raised if any of the directives passed in to Nrt has
        a signature that is not a string.
        """
        handle_nrt = Nrt(**{})
        self.assertRaises(
                            TypeError,
                            setattr,
                            handle_nrt,
                            "directives",
                            {"signature" : 124},
                            )
        del handle_nrt


    def test_directives_wrong_misformatted_signature(self):
        """
        Tests that a ValueError exception is raised if any of the directives passed in to Nrt has
        a signature with the wrong format.
        """
        handle_nrt = Nrt(**{})
        self.assertRaises(
                            ValueError,
                            setattr,
                            handle_nrt,
                            "directives",
                            {"signature" : "wrong_format",},
                            )
        del handle_nrt


    def test_export(self):
        """
        Tests that the export property hasn't been implemented, yet.
        """
        handle_nrt = Nrt(**{})
        self.assertRaises(
                            NotImplementedError,
                            getattr,
                            handle_nrt,
                            "export",
                            )
        del handle_nrt


    def test_init_correct(self):
        """
        Tests that an Nrt object is properly instantiated if its mandatory parameters are properly
        passed in.
        """
        handle_nrt = Nrt(**{})
        self.assertEqual(handle_nrt.directives, [])
        self.assertEqual(handle_nrt.listen, {})
        del handle_nrt


    def test_is_valid_correct(self):
        """
        Tests that the is_valid property correctly returns True if all the ServerName objects
        associated to a Listen instance are valid.
        """
        directives = [
                        { "signature" : "container1:0.0.0.0:80:a.b.c:/location1/"},
                        { "signature" : "container1:0.0.0.0:80:a.b.c:/location2/"}
                        ]
        handle_nrt = Nrt(**{})
        for directive in directives:
            handle_nrt.directives = directive
        handle_nrt._build()
        self.assertTrue(handle_nrt.is_valid)
        del handle_nrt


    def test_is_valid_correct_invalid_location(self):
        """
        Tests that the is_valid property correctly returns False if any of its Listen is
        invalid.
        """
        directives = [
                        { "signature" : "container1:0.0.0.0:80:a.b.c:/location1/"},
                        { "signature" : "container2:0.0.0.0:80:a.b.c:/location1/"}
                        ]
        handle_nrt = Nrt(**{})
        for directive in directives:
            handle_nrt.directives = directive
        handle_nrt._build()
        self.assertFalse(handle_nrt.is_valid)
        del handle_nrt


    def test_listen_correct(self):
        """
        Tests that the listen property properly returns the listen objects stored into it, by
        mapping them to their address.
        """
        ip = "1.2.3.4"
        port = 1234
        handle_nrt = Nrt(**{})
        handle_listen = Listen(**{
                                    "ip" : ip,
                                    "port" : port,
                                    }
                                )
        handle_nrt.listen = handle_listen
        self.assertTrue(handle_listen.address in handle_nrt.listen.keys())
        del handle_nrt
        del handle_listen


    def test_listen_correct_empty(self):
        """
        Tests that an empty dictionary is properly returned if the Nrt instance has no listen
        object associated to it.
        """
        handle_nrt = Nrt(**{})
        response = handle_nrt.listen
        expected_response = {}
        self.assertEqual(response, expected_response)
        del handle_nrt


    def test_listen_correct_no_dupes(self):
        """
        Tests that an Nrt object properly stores unique Listen addresses.
        """
        ip = "1.2.3.4"
        port = 1234
        handle_nrt = Nrt(**{})
        handle_listen = Listen(**{
                                    "ip" : ip,
                                    "port" : port,
                                    }
                                )
        for i in range(10):
            handle_nrt.listen = handle_listen
        self.assertEqual(len(handle_nrt.listen.keys()), 1)
        del handle_nrt
        del handle_listen


    def test_listen_wrong_missing_listen(self):
        """
        Tests that a ValueError exception is raised if we try to set the listen property of an Nrt
        object without passing in any listen.
        """
        handle_nrt = Nrt(**{})
        self.assertRaises(
                            ValueError,
                            setattr,
                            handle_nrt,
                            "listen",
                            None
                            )
        del handle_nrt


    def test_listen_wrong_mistyped_listen(self):
        """
        Tests that a TypeError exception is raised if we try to set the listen property of an Nrt
        object passing in a listen that is not an instance of the Listen class.
        """
        handle_nrt = Nrt(**{})
        self.assertRaises(
                            TypeError,
                            setattr,
                            handle_nrt,
                            "listen",
                            "not_an_instance_of_Listen"
                            )
        del handle_nrt
