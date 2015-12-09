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


class Location(object):
    """
    Represent a unique location within Nginx.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes a Location instance.
        """
        self._alias = []
        self.location = kwargs.get("location", None)


    @property
    def alias(self):
        """
        Returns the alias(es) associated to the Location.
        """
        return self._alias
    

    @alias.setter
    def alias(self, value):
        """
        Adds an alias to the Location.
        """
        if value is None:
            raise ValueError("An alias must be provided.")
        if not isinstance(value, str):
            raise TypeError("The alias must be a string, not %s." % (type(value)))
        if value not in self._alias:
            self._alias.append(value)


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
    def location(self, value=None):
        """
        Sets the location of the object.
        """
        if value is None:
            raise ValueError("A Location must be given a location.")
        if not isinstance(value, str):
            raise TypeError("The location must be a string, not %s." % (type(value)))
        if value is "":
            raise ValueError("A empty string is not a valid location.")
        if not value[0] == value[-1] == "/":
            raise ValueError("The locations must start and end with a forward slash.")
        self._location = value
