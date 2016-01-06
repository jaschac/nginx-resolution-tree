# -*- coding: utf-8 -*-

"""
This module defines the Location class, which represent an Nginx's location block and its
properties. Multiple location blocks can be present within the same server block, but they must be
unique. Each instance of the Location class is identified by its name. The name of a location must
start and end with a forward slash, with the unique exception of the root location, which is
represented by a single forward slash.

A Location is associated to a list of containers, referred to as alias. For an Nginx configuration
file to be valid, multiple containers must not redefine the same location within the same server
block.

A property, is_valid, returns whether the current location is valid or not.
"""

from re import compile, match

class Location(object):
    """
    Represent a unique location within Nginx.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes a Location instance.
        """
        self._alias = []
        self._directives = []
        self.location = kwargs.get("location", None)


    def _build(self, *args, **kwargs):
        """
        Turns the input directives into a unique list of alias entries.
        """
        for directive in self.directives:
            alias, ip, port, server_name, location = directive["signature"].split(":")

            if alias not in self.alias:
                self.alias = alias


    @property
    def alias(self):
        """
        Returns the alias(es) associated to the Location.
        """
        return self._alias
    

    @alias.setter
    def alias(self, alias):
        """
        Adds an alias to the Location.
        """
        if alias is None:
            raise ValueError("An alias must be provided.")
        if not isinstance(alias, str):
            raise TypeError("The alias must be a string, not %s." % (type(alias)))
        if alias is "":
            raise ValueError("A empty string is not a valid alias.")
        
        if alias not in self.alias:
            self._alias.append(alias)


    @property
    def directives(self):
        """
        Returns the directives associated to this Location object.
        """
        return self._directives


    @directives.setter
    def directives(self, directive):
        """
        Adds a directive to the directives of the Location object.
        """
        signature_regex =  compile("^\w+:[\w\.]+:\d+:[\w\.]+:[\w/]+$")

        if directive is None:
            raise ValueError("A directive name must be given.")
        if not isinstance(directive, dict):
            raise TypeError("The directive name must be a dictionary, not %s." % (type(directive)))
        if 'signature' not in directive.keys():
            raise ValueError("A directive is expected to have a 'signature'.")
        if not isinstance(directive['signature'], str):
            raise TypeError("The signature is expected as a string, not %s." % (type(directive['signature'])))
        if not signature_regex.match(directive['signature']):
            raise ValueError("A signature must have the following format: 'alias:ip:port:server_name:location'")

        if directive not in self._directives:
            self._directives.append(directive)

        self._build()


    @property
    def is_valid(self):
        """
        Returns whether the Location is valid or not.
        """
        return len(self._alias) == 1


    @property
    def location(self):
        """
        Returns the location.
        """
        return self._location


    @location.setter
    def location(self, location):
        """
        Sets the location of the object.
        """
        if location is None:
            raise ValueError("A Location must be given a location.")
        if not isinstance(location, str):
            raise TypeError("The location must be a string, not %s." % (type(location)))
        if location is "":
            raise ValueError("A empty string is not a valid location.")
        if not location[0] == location[-1] == "/":
            raise ValueError("The locations must start and end with a forward slash.")

        self._location = location
