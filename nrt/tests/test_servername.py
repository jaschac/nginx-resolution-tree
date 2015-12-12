# -*- coding: utf-8 -*-

"""
This module tests the ServerName module.
"""

from nrt.location import Location
from nrt.servername import ServerName
from nrt.tests.test_base import TestBase


class TestServerName(TestBase):
    """
    A class containing unit tests for the ServerName module.
    """
    def setUp(self, *args, **kwargs):
        '''
        Initializes whatever is needed during the tests.
        '''
        super(TestServerName, self).setUp(*args, **{
                                                        "test_module_filename" : __file__
                                                    }
                                        )
        self.valid_domain = "www.foo.boo"


    def test_init_correct(self):
        """
        Tests that an ServerName object is properly instantiated if a proper location is passed in
        during initialization. 
        """
        handle_servername = ServerName(**{
                                            "domain" : self.valid_domain,
                                        }
                                    )
        self.assertEqual(handle_servername.domain, self.valid_domain)
        self.assertEqual(handle_servername.locations, [])
        del handle_servername


    def test_init_wrong_missing_domain(self):
        """
        Tests that a ServerName object cannot be instantiated and a ValueError exception is raised
        if the location is not passed.
        """
        self.assertRaises(
                            ValueError,
                            ServerName,
                            **{}
                            )


    def test_init_wrong_mistyped_domain(self):
        """
        Tests that an ServerName object cannot be instantiated and a TypeError exception is raised
        if a domain is passed in, but it's not a string.
        """
        self.assertRaises(
                            TypeError,
                            ServerName,
                            **{
                                "domain" : 1234,
                                }
                            )


    def test_init_wrong_empty_domain(self):
        """
        Tests that an ServerName object cannot be instantiated and a TypeError exception is raised
        if a domain is passed in as an empty string.
        """
        self.assertRaises(
                            ValueError,
                            ServerName,
                            **{
                                "domain" : "",
                                }
                            )


    def test_init_wrong_reassign_domain(self):
        """
        Tests that once instantiated, a ValueError exception is raised if the ServerName object is
        assigned a domain again.
        """
        handle_servername = ServerName(**{
                                            "domain" : self.valid_domain,
                                        }
                                    )
        self.assertRaises(
                            ValueError,
                            setattr,
                            handle_servername,
                            "domain",
                            "a_new_domain",
                            )
        del handle_servername


    def test_domain_correct(self):
        """
        Tests that the domain can be properly retrieved once a ServerName object has been correctly
        instantiated.
        """
        handle_servername = ServerName(**{
                                            "domain" : self.valid_domain,
                                        }
                                    )
        self.assertEqual(handle_servername.domain, self.valid_domain)
        del handle_servername


    def test_locations_wrong_missing_location(self):
        """
        Tests that a ValueError exception is raised if a location is added but no value is given.
        """
        handle_servername = ServerName(**{
                                            "domain" : self.valid_domain,
                                        }
                                    )
        self.assertRaises(
                            ValueError,
                            setattr,
                            handle_servername,
                            "locations",
                            None,
                            )
        del handle_servername


    def test_locations_wrong_mistyped_location(self):
        """
        Tests that a TypeError exception is raised if a location is added but it is not a Location
        instance.
        """
        handle_servername = ServerName(**{
                                            "domain" : self.valid_domain,
                                        }
                                    )
        self.assertRaises(
                            TypeError,
                            setattr,
                            handle_servername,
                            "locations",
                            "not_a_Location_instance",
                            )
        del handle_servername


    def test_locations_correct_multiple_times_the_same_location(self):
        """
        Tests that if a ServerName object is passed multiple times the same Location, only one is
        added.
        """
        location = "/var/www/foo/"
        handle_servername = ServerName(**{
                                            "domain" : self.valid_domain,
                                        }
                                    )
        for i in range(10):
            handle_location = Location(**{
                                            "location" : location
                                            }
                                        )
            handle_servername.locations = handle_location
        self.assertEqual(len(handle_servername.locations), 1)
        self.assertEqual(handle_servername.locations[0].location, location)
        del handle_servername


    def test_locations_correct(self):
        """
        Tests that if a ServerName object properly returns the stored location(s).
        """
        location = "/var/www/foo/"
        handle_servername = ServerName(**{
                                            "domain" : self.valid_domain,
                                        }
                                    )
        handle_location = Location(**{
                                        "location" : location
                                        }
                                    )
        handle_servername.locations = handle_location
        self.assertEqual(handle_servername.locations[0].location, location)
        del handle_location
        del handle_servername