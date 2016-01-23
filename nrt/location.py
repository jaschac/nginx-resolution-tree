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
        self._allow = ["all"]
        self._alias = []
        self._deny = []
        self._directives = []
        self._language = "html"
        self._language_configuration = {}
        self.location = kwargs.get("location", None)


    def _build(self, *args, **kwargs):
        """
        Turns the input directives into a unique list of alias entries.
        """
        language_configuration_map = {
                                        "php" : "phpfmp",
                                        "python" : "gunicorn",
                                        }

        for directive in self.directives:
            alias, ip, port, server_name, location = directive["signature"].split(":")
            parameters = directive.get("parameters", {})

            if alias not in self.alias:
                self.alias = alias

            self.allow = parameters.get("allow", None)
            self.deny = parameters.get("deny", None)
            self.language = parameters.get("language", None)
            self.language_configuration = parameters.get(language_configuration_map.get(self.language, None), {})


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
            directives = ["all"]
        if not isinstance(directives, list):
            raise TypeError("The allow directives must be a list, not %s." % (type(directives).__name__))
        
        if "all" in directives:
            self._allow = ["all"]
            return

        if directives == []:
            self._allow = []
            return

        self._allow = [directive for directive in set(directives) if directive not in self.allow]


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
        
        if "all" in directives:
            self._deny = ["all"]
            return

        self._deny = [directive for directive in set(directives) if directive not in self.deny]


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
        return len(self._alias) == 1 and not ("all" in self.allow and "all" in self.deny) and not (self.allow == [] and self.deny == [])


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
    def language_configuration(self):
        """
        Returns the configuration specific to the language served at this location.
        """
        return self._language_configuration


    @language_configuration.setter
    def language_configuration(self, configuration):
        """
        Sets the configuration specific to the language of the object.
        """
        if not isinstance(configuration, dict):
            raise TypeError("The language configuration must be a dictionary, not %s." % (type(configuration).__name__))
        
        if self.language == "python":
            if "ip" not in configuration.keys():
                configuration["ip"] = "127.0.0.1"
            if "port" not in configuration.keys():
                configuration["port"] = "8000"
            if not isinstance(configuration["ip"], str):
                raise TypeError("GUnicorn's IP must be a string, not %s." % (type(configuration["ip"]).__name__))
            if not isinstance(configuration["port"], str):
                raise TypeError("GUnicorn's port must be a string, not %s." % (type(configuration["port"]).__name__))

        self._language_configuration = configuration


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
