# -*- coding: utf-8 -*-

"""
This module defines a basic Nginx Location block. As such, it will represent one of the many
location entries of a server block. A Location block is defined by a location, which can be either
a literal string or a regular expression.

As per official documentation, Nginx first searched the first literal string that matches the needs
of the request; it then searches any regular expression able to satisfy it. If one is found, it is
used; else the literal string that matched is used.

The LocationBlock class has a mandatory attribute, which represent the aforementioned literal or
regex. It also has several optional attributes: allow is a list of string, each representing an IP
or range that is allowed to access the content. deny is the other way around. By default Nginx 
applies an allow all rule.

It has an export method that returns a properly formatted string representation of the whole object
so that it can be used to create a virtual host file.
"""


class LocationBlock(object):
    """
    Represent a basic Nginx Location block.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes a LocationBlock instance.
        """
        self._allow = []
        self._deny = []
        self._location = None


    @property
    def allow(self):
        """
        Returns the allow directives associated to the Location block.
        """
        return self._allow


    @allow.setter
    def allow(self, directive=None):
        """
        Adds an allow directive to those currently part of the Location block. The content of an
        allow directive is not validated. The client is responsible to provide valid ones.
        """
        if directive is None:
            raise ValueError("A directive name must be given.")
        if not isinstance(directive, str):
            raise TypeError("The directive name must be a string, not %s." % (type(directive).__name__))

        if directive not in self._allow:
            self._allow.append(directive)


    @property
    def deny(self):
        """
        Returns the deny directives associated to the Location block.
        """
        return self._deny


    @allow.setter
    def deny(self, directive=None):
        """
        Adds a deny directive to those currently part of the Location block. The content of a
        deny directive is not validated. The client is responsible to provide valid ones.
        """
        if directive is None:
            raise ValueError("A directive name must be given.")
        if not isinstance(directive, str):
            raise TypeError("The directive name must be a string, not %s." % (type(directive).__name__))

        if directive not in self._deny:
            self._deny.append(directive)


    def export(self):
        """
        Returns the class as a properly formatted string ready to be used to create a virtual host.
        """
        pass


    @property
    def location(self):
        """
        Returns the location literal or regex associated to the Location block.
        """
        return self._location


    @allow.setter
    def location(self, location=None):
        """
        Adds a location literal or regex to those currently part of the Location block. The
        goodness of the location itself is not validated.
        """
        if location is None:
            raise ValueError("A location name must be given.")
        if not isinstance(directive, str):
            raise TypeError("The location name must be a string, not %s." % (type(location).__name__))

        self._location = location
