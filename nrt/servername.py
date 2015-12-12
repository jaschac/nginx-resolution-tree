# -*- coding: utf-8 -*-

"""
This module defines a ServerName of an Nginx Resolution Tree. The server name represents the
pattern describing the domain(s) served. According to the Nginx documentation, first the address is
matched then, the server name of those Listen entries that were positive. A ServerName is
associated to Listen objects. Two ServerName instances can have the same value but be associated
to different Listen instances: despite having the same value, they are different instances.

Each ServerName has one to N unique Location objects associated to it.
"""

from nrt.location import Location


class ServerName(object):
    """
    This class represents a ServerName object.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes a ServerName instance. 
        """
        self.domain = kwargs.get("domain", None)
        self.locations = None


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
    def locations(self):
        """
        Returns the locations associated to the ServerName.
        """
        return self._locations
    

    @locations.setter
    def locations(self, value):
        """
        Adds an Location instance to those associated to the ServerName.
        """
        if not hasattr(self, "_locations"):
            self._locations = []
        elif hasattr(self, "_locations"):
            if value is None:
                raise ValueError("A location must be given.")
            if not isinstance(value, Location):
                raise TypeError("The location must be a Location instance, not %s." % (type(value)))
            if value.location not in [location.location for location in self._locations]:
                self._locations.append(value)
        else:
            print("This should never happen")
