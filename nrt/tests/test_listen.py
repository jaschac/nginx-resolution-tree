# -*- coding: utf-8 -*-

"""
This module tests the Listen module.
"""

from nrt.listen import Listen
from nrt.location import Location
from nrt.servername import ServerName
from nrt.tests.test_base import TestBase


class TestListen(TestBase):
    """
    A class containing unit tests for the Listen module.
    """
    def setUp(self, *args, **kwargs):
        '''
        Initializes whatever is needed during the tests.
        '''
        super(TestListen, self).setUp(*args, **{
                                                    "test_module_filename" : __file__
                                                }
                                        )
        self.valid_domain = "www.foo.boo"
        self.valid_ip = "1.2.3.4"
        self.valid_port = 1234


    def aux_generate_handle_servername(self, *args, **kwargs):
        """
        Auxiliary method that creates a ServerName object and returns it.
        """
        domain = kwargs.get("domain", self.valid_domain)
        handle_servername = ServerName(**{
                                            "domain" : domain,
                                        }
                                    )
        return handle_servername


    def test_address_correct(self):
        """
        Tests that the address property properly returns the address associated to a Listen object.
        """
        handle_listen = Listen(**{
                                    "ip" : self.valid_ip,
                                    "port" : self.valid_port,
                                    }
                                )
        response = handle_listen.address
        expected_response = "%s:%s" % (self.valid_ip, self.valid_port)
        self.assertEqual(response, expected_response)
        del handle_listen


    def test_directives_correct(self):
        """
        Tests that a Listen object properly returns the directives that were assigned to it.
        """
        directives = [
                        { "signature" : "a:0.0.0.0:80:a.b.c:/"},
                        { "signature" : "a:0.0.0.0:8080:a.b.c:/"}
                        ]
        handle_listen = Listen(**{})
        for directive in directives:
            handle_listen.directives = directive
        self.assertEqual(len(handle_listen.directives), 2)
        for directive, expected_directive in zip(handle_listen.directives, directives):
            self.assertEqual(directive, expected_directive)
        del handle_listen


    def test_directives_correct_empty(self):
        """
        Tests that a Listen object properly returns an empty list, if no directive was assigned to
        it.
        """
        handle_listen = Listen(**{})
        self.assertEqual(handle_listen.directives, [])
        del handle_listen


    def test_directives_correct_no_dupes(self):
        """
        Tests that a Listen object properly returns a unique directive if the same directive is
        added multiple times.
        """
        directive = { "signature" : "a:0.0.0.0:80:a.b.c:/"}
        handle_listen = Listen(**{})
        for i in range(10):
            handle_listen.directives = directive
        self.assertEqual(len(handle_listen.directives), 1)
        self.assertEqual(directive, handle_listen.directives[0])
        del handle_listen
        

    def test_directives_wrong_missing_directive(self):
        """
        Tests that a ValueError exception is raised if we try to add a directive to a Listen
        object but we don't pass any.
        """
        handle_listen = Listen(**{})
        self.assertRaises(
                            ValueError,
                            setattr,
                            handle_listen,
                            "directives",
                            None,
                            )
        del handle_listen


    def test_directives_wrong_mistyped_directive(self):
        """
        Tests that a TypeError exception is raised if we try to add a directive to a Listen
        object but the directive passed in is not a dictionary.
        """
        handle_listen = Listen(**{})
        self.assertRaises(
                            TypeError,
                            setattr,
                            handle_listen,
                            "directives",
                            "not_a_dictionary",
                            )
        del handle_listen


    def test_directives_wrong_missing_signature(self):
        """
        Tests that a ValueError exception is raised if we try to add a directive to a Listen
        object but the directive passed in, despite being a dictionary, lacks the 'signature'
        key.
        """
        handle_listen = Listen(**{})
        self.assertRaises(
                            ValueError,
                            setattr,
                            handle_listen,
                            "directives",
                            {"not_signature" : 124}
                            )
        del handle_listen


    def test_directives_wrong_mistyped_signature(self):
        """
        Tests that a TypeError exception is raised if we try to add a directive to a Listen
        object but the directive passed in has a signature that is not a string.
        """
        handle_listen = Listen(**{})
        self.assertRaises(
                            TypeError,
                            setattr,
                            handle_listen,
                            "directives",
                            {"signature" : 124}
                            )
        del handle_listen


    def test_directives_wrong_misformatted_signature(self):
        """
        Tests that a ValueError exception is raised if we try to add a directive to a Listen
        object but the directive passed in has a signature that has a wrong format.
        """
        handle_listen = Listen(**{})
        self.assertRaises(
                            ValueError,
                            setattr,
                            handle_listen,
                            "directives",
                            {"signature" : "wrong_format"}
                            )
        del handle_listen


    def test_init_correct(self):
        """
        Tests that an Listen object is properly instantiated if proper parameters are passed in
        during initialization. 
        """
        handle_listen = Listen(**{
                                    "ip" : self.valid_ip,
                                    "port" : self.valid_port,
                                    }
                                )
        self.assertEqual(handle_listen.address, "%s:%s" % (self.valid_ip, self.valid_port))
        self.assertEqual(handle_listen.directives, [])
        self.assertEqual(handle_listen.ip, self.valid_ip)
        self.assertEqual(handle_listen.port, self.valid_port)
        self.assertEqual(handle_listen.server_names, {})
        del handle_listen


    def test_init_correct_default_args(self):
        """
        Tests that an Listen object is properly instantiated with the default parameters if nothing
        is passed in during initialization.
        """
        handle_listen = Listen(**{})
        self.assertEqual(handle_listen.address, "0.0.0.0:80")
        self.assertEqual(handle_listen.directives, [])
        self.assertEqual(handle_listen.ip, "0.0.0.0")
        self.assertEqual(handle_listen.port, 80)
        self.assertEqual(handle_listen.server_names, {})
        del handle_listen


    def test_init_wrong_mistyped_ip(self):
        """
        Tests that an Listen object cannot be instantiated and a TypeError exception is raised
        if an IP is passed in, but not as a string.
        """
        self.assertRaises(
                            TypeError,
                            Listen,
                            **{
                                "ip" : 12345,
                                }
                            )


    def test_init_wrong_misformatted_ip(self):
        """
        Tests that an Listen object cannot be instantiated and a TypeError exception is raised
        if an IP is passed in as a string, but it's not a valid IPv4.
        """
        self.assertRaises(
                            ValueError,
                            Listen,
                            **{
                                "ip" : "999.999.999.999",
                                }
                            )


    def test_init_wrong_mistyped_port(self):
        """
        Tests that an Listen object cannot be instantiated and a TypeError exception is raised
        if the port is passed in, but neither as a string nor as an integer.
        """
        self.assertRaises(
                            TypeError,
                            Listen,
                            **{
                                "port" : ["something_wrong"],
                                }
                            )


    def test_init_wrong_invalid_port(self):
        """
        Tests that an Listen object cannot be instantiated and a TypeError exception is raised
        if the port is passed in, but neither as a string nor as an integer.
        """
        for invalid_port in (-1, 0, 77777):
            self.assertRaises(
                                ValueError,
                                Listen,
                                **{
                                    "port" : invalid_port,
                                    }
                                )


    def test_is_valid_correct(self):
        """
        Tests that the is_valid property correctly returns True if all the ServerName objects
        associated to a Listen instance are valid.
        """
        directives = [
                        { "signature" : "container1:0.0.0.0:80:a.b.c:/location1/"},
                        { "signature" : "container1:0.0.0.0:80:a.b.c:/location2/"}
                        ]
        handle_listen = Listen(**{})
        for directive in directives:
            handle_listen.directives = directive
        handle_listen.resolve()    
        self.assertTrue(handle_listen.is_valid)
        del handle_listen


    def test_is_valid_correct_invalid_location(self):
        """
        Tests that the is_valid property correctly returns False if any of its ServerNames is
        invalid.
        """
        directives = [
                        { "signature" : "container1:0.0.0.0:80:a.b.c:/location1/"},
                        { "signature" : "container2:0.0.0.0:80:a.b.c:/location1/"}
                        ]
        handle_listen = Listen(**{})
        for directive in directives:
            handle_listen.directives = directive
        handle_listen.resolve()    
        self.assertFalse(handle_listen.is_valid)
        del handle_listen


    def test_is_valid_ipv4_address_correct_valid_ip(self):
        """
        Tests that __is_valid_ipv4_address properly returns True if it is passed a valid IPv4.
        """
        handle_listen = Listen(**{})
        response = handle_listen._Listen__is_valid_ipv4_address(**{"ip" : self.valid_ip})
        self.assertTrue(response)
        del handle_listen


    def test_is_valid_ipv4_address_correct_invalid_ip(self):
        """
        Tests that __is_valid_ipv4_address properly returns False if it is passed an IP whose
        format is valid, but is not a valid IPv4.
        """
        handle_listen = Listen(**{})
        response = handle_listen._Listen__is_valid_ipv4_address(**{"ip" : "10.11.12.256"})
        self.assertFalse(response)
        del handle_listen


    def test_is_valid_ipv4_address_wrong_missing_ip(self):
        """
        Tests that a ValueError exception is raised if __is_valid_ipv4_address is called but the
        mandatory parameter ip is not given.
        """
        handle_listen = Listen(**{})
        self.assertRaises(
                            ValueError,
                            handle_listen._Listen__is_valid_ipv4_address,
                            **{}
                            )
        del handle_listen


    def test_is_valid_ipv4_address_wrong_mistyped_ip(self):
        """
        Tests that a TypeError exception is raised if __is_valid_ipv4_address is given the
        mandatory parameter ip, but not as a string.
        """
        handle_listen = Listen(**{})
        self.assertRaises(
                            TypeError,
                            handle_listen._Listen__is_valid_ipv4_address,
                            **{
                                "ip" : 12345,
                                }
                            )
        del handle_listen


    def test_resolve_correct(self):
        """
        Tests that the resolve method properly turns the directives into unique ServerName objects.
        """
        handle_listen = Listen(**{})
        directives = [
                        { "signature" : "a:0.0.0.0:80:a.b.c.d:/"},
                        { "signature" : "a:0.0.0.0:8080:aa.bb.cc.dd:/"},
                        ]
        for directive in directives:
            handle_listen.directives = directive
        self.assertEqual(handle_listen.server_names, {})
        handle_listen.resolve()
        self.assertEqual(len(handle_listen.server_names.keys()), 2)
        del handle_listen


    def test_resolve_correct_no_dupes(self):
        """
        Tests that the resolve method properly generate a unique ServerName object if we try to
        resolve the same server name twice.
        """
        handle_listen = Listen(**{})
        server_name = "a.b.c.d"
        directive = {"signature" : "a:0.0.0.0:80:%s:/" % (server_name)}
        for _ in range(10):
            handle_listen.directives = directive
        handle_listen.resolve()
        self.assertEqual(len(handle_listen.server_names.keys()), 1)
        self.assertEqual(list(handle_listen.server_names.keys())[0], server_name)
        del handle_listen


    def test_server_names_correct_empty(self):
        """
        Tests that the server_names property properly returns a map of ServerName instances
        associated to a Listen object.
        """
        handle_listen = Listen(**{
                                    "ip" : self.valid_ip,
                                    "port" : self.valid_port,
                                    }
                                )
        response = handle_listen.server_names
        expected_response = {}
        self.assertEqual(response, expected_response)
        del handle_listen


    def test_server_names_correct(self):
        """
        Tests that the server_names property properly returns a map of ServerName instances
        associated to a Listen object.
        """
        handle_servername1 = self.aux_generate_handle_servername(**{"domain" : "www.servername1.com"})
        handle_servername2 = self.aux_generate_handle_servername(**{"domain" : "www.servername2.com"})
        handle_listen = Listen(**{
                                    "ip" : self.valid_ip,
                                    "port" : self.valid_port,
                                    }
                                )
        for handle_servername in [handle_servername1, handle_servername2]:
            handle_listen.server_names = handle_servername

        self.assertEqual(len(handle_listen.server_names), 2)

        for server_name, expected_server_name in zip(sorted(handle_listen.server_names.values(), key = lambda x: x.domain), [handle_servername1, handle_servername2]):
            self.assertIsInstance(server_name, ServerName)
            self.assertEqual(server_name.domain, expected_server_name.domain)

        del handle_servername1
        del handle_servername2
        del handle_listen


    def test_server_names_correct_no_dupes(self):
        """
        Tests that the server_names property properly returns a map of unique ServerName instances
        associated to a Listen object.
        """
        domain = "www.servername1.com"
        handle_servername = self.aux_generate_handle_servername(**{"domain" : domain})
        handle_listen = Listen(**{
                                    "ip" : self.valid_ip,
                                    "port" : self.valid_port,
                                    }
                                )
        handle_listen.server_names = handle_servername
        handle_listen.server_names = handle_servername
        handle_listen.server_names = handle_servername
        self.assertEqual(len(handle_listen.server_names), 1)
        self.assertEqual(list(handle_listen.server_names.keys())[0], domain)
        del handle_servername
        del handle_listen


    def test_server_names_wrong_missing_server_name(self):
        """
        Tests that a ValueError exception is raised if we try to assign a ServerName to a Listen
        object without passing in the mandatory server_name parameter.
        """
        handle_listen = Listen(**{
                                    "ip" : self.valid_ip,
                                    "port" : self.valid_port,
                                    }
                                )
        self.assertRaises(
                            ValueError,
                            setattr,
                            handle_listen,
                            "server_names",
                            None,
                            )
        del handle_listen


    def test_server_names_wrong_mistyped_server_name(self):
        """
        Tests that a ValueError exception is raised if we try to assign a ServerName to a Listen
        object passing in a server_name that is not an instance of ServerName.
        """
        handle_listen = Listen(**{
                                    "ip" : self.valid_ip,
                                    "port" : self.valid_port,
                                    }
                                )
        self.assertRaises(
                            TypeError,
                            setattr,
                            handle_listen,
                            "server_names",
                            "not_a_ServerName_instance",
                            )
        del handle_listen
