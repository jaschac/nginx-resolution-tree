# -*- coding: utf-8 -*-

"""
This module defines a ServerName of an Nginx Resolution Tree. The server name represents the
pattern describing the domain(s) served. According to the Nginx documentation, first the address is
matched then, the server name of those Listen entries that were positive. A ServerName is
associated to Listen objects. Two ServerName instances can have the same value but be associated
to different Listen instances: despite having the same value, they are different instances.

Each ServerName has one to N unique Location objects associated to it.
"""

from re import compile, match

from nrt.location import Location


class ServerName(object):
    """
    This class represents a ServerName object.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes a ServerName instance. 
        """
        self._directives = []
        self.domain = kwargs.get("domain", None)
        self._locations = {}


    def _build(self, *args, **kwargs):
        """
        Turns the input directives into a unique list of Location objects.
        """
        for directive in self.directives:
            alias, ip, port, server_name, location = directive["signature"].split(":")
            parameters = directive.get("parameters", {})

            if location not in self.locations.keys():
                handle_location = Location(**{
                                                "language" : parameters.get("language", None),
                                                "location" : location,
                                                }
                                            )
                self.locations = handle_location

            self.locations[location].directives = directive


    @property
    def directives(self):
        """
        Returns the directives associated to this ServerName object.
        """
        return self._directives


    @directives.setter
    def directives(self, directive):
        """
        Adds a directive to the directives of the ServerName object.
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
    def domain(self):
        """
        Returns the domain associated to the ServerName.
        """
        return self._domain


    @domain.setter
    def domain(self, value):
        """
        Associates a domain to a ServerName.
        """
        if hasattr(self, "_domain"):
            raise ValueError("A ServerName's domain cannot be changed.")
        if value is None:
            raise ValueError("A ServerName must be given a domain.")
        if not isinstance(value, str):
            raise TypeError("The domain must be a string, not %s." % (type(value)))
        if value is "":
            raise ValueError("A empty string is not a valid domain.")
        self._domain = value


    @property
    def is_valid(self):
        """
        Returns whether the ServerName is valid or not. The ServerName is not valid if any of its
        locations is not.
        """
        for location in self.locations.values():
            if not location.is_valid:
                return False
        return True


    @property
    def locations(self):
        """
        Returns the locations associated to the ServerName.
        """
        return self._locations


    @locations.setter
    def locations(self, location):
        """
        Adds an Location instance to those associated to the ServerName.
        """
        if location is None:
            raise ValueError("A location must be given.")
        if not isinstance(location, Location):
            raise TypeError("The location must be a Location instance, not %s." % (type(location)))

        if location.location not in self._locations.keys():
            self._locations[location.location] = location
