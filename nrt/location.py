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
        self.allow = kwargs.get("allow", [])
        self._alias = []
        self.deny = kwargs.get("deny", [])
        self._directives = []
        self.language = kwargs.get("language", "html")
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
    def allow(self):
        """
        Returns the allow directives enforced at this location.
        """
        return self._allow


    @allow.setter
    def allow(self, directives):
        """
        Sets the allow directives enforced at this location.
        """
        if directives is None:
            directives = []
        if not isinstance(directives, list):
            raise TypeError("The allow directives must be a list, not %s." % (type(directives).__name__))
        if not hasattr(self, "_allow"):
            self._allow = []
        if "all" in self.allow:
            return
        for directive in directives:
            if directive == "all":
                self._allow = ["all"]
                break;
            elif directive not in self.allow:
                self._allow.append(directive)


    @property
    def deny(self):
        """
        Returns the deny directives enforced at this location.
        """
        return self._deny


    @deny.setter
    def deny(self, directives):
        """
        Sets the deny directives enforced at this location.
        """
        if directives is None:
            directives = []
        if not isinstance(directives, list):
            raise TypeError("The deny directives must be a list, not %s." % (type(directives).__name__))
        if not hasattr(self, "_deny"):
            self._deny = []
        if "all" in self.deny:
            return
        for directive in directives:
            if directive == "all":
                self._deny = ["all"]
                break;
            elif directive not in self.deny:
                self._deny.append(directive)


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
    def language(self):
        """
        Returns the language served at this location.
        """
        return self._language


    @language.setter
    def language(self, language):
        """
        Sets the language of the object.
        """
        if language is None:
            language = 'html'
        if not isinstance(language, str):
            raise TypeError("The language must be a string, not %s." % (type(language).__name__))
        if language.lower() not in ("html", "php", "python"):
            raise ValueError("%s is not a valid language." % (language))

        self._language = language.lower()


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
