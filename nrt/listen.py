# -*- coding: utf-8 -*-

"""
This module defines a Listen object of an Nginx Resolution Tree. A Listen object is uniquely
identified by the pair IP:PORT. This pair is usually referred to as the address. Neither the IP
address nor the port are mandatory parameters: the first defaults to 0.0.0.0, while the latter to
80.  Each Listen object is also associated with a list of unique ServerName objects.
"""

from re import compile, match
from socket import AF_INET, error, inet_aton, inet_pton

from nrt.servername import ServerName

class Listen(object):
    """
    This class represents a Listen object.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes a Listen instance.
        """
        self._directives = []
        self.ip = kwargs.get("ip", "0.0.0.0")
        self.port = kwargs.get("port", 80)
        self._server_names = {}

        if not isinstance(self.port, str) and not isinstance(self.port, int):
            raise TypeError("The port is expected either as a string or an integer, not %s." % (type(self.port)))
        if not self.__is_valid_ipv4_address(**{"ip" : self.ip}):
            raise ValueError("%s is not a valid IPv4 address." % (self.ip))
        if int(self.port) < 1 or int(self.port) > 65535:
            raise ValueError("%s is not a valid port." % (self.port))
        if not isinstance(self.ip, str):
            raise TypeError("The IP address is expected as a string, not %s." % (type(self.ip)))


    def __is_valid_ipv4_address(self, *args, **kwargs):
        """
        Validates an IPv4 address.
        """
        ip = kwargs.get("ip", None)

        if ip is None:
            raise ValueError("An IP must be provided.")
        if not isinstance(ip, str):
            raise TypeError("The IP address is expected as a string, not %s." % (type(ip)))

        try:
            inet_pton(AF_INET, ip)
        except AttributeError:
            try:
                inet_aton(ip)
            except error:
                return False
            return ip.count('.') == 3
        except error:
            return False
        return True


    def _build(self):
        """
        Turns the input directives into a unique list of ServerName objects.
        """
        for directive in self.directives:
            alias, ip, port, server_name, location = directive["signature"].split(":")

            if server_name not in self.server_names.keys():
                handle_server_name = ServerName(**{
                                                    "domain" : server_name,
                                                    }
                                                )
                self.server_names = handle_server_name

            self.server_names[server_name].directives = directive
            self.server_names[server_name]._build()


    @property
    def directives(self):
        """
        Returns the directives associated to this Listen object.
        """
        return self._directives


    @directives.setter
    def directives(self, directive):
        """
        Adds a directive to the directives of the Listen object.
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


    @property
    def address(self):
        """
        Returns the address associated to the Listen object.
        """
        return "%s:%s" % (self.ip, self.port)


    @property
    def is_valid(self):
        """
        Returns whether the Listen is valid or not. The Listen is not valid if any of its server
        names is not.
        """
        for server_name in self.server_names.values():
            if not server_name.is_valid:
                return False
        return True


    @property
    def server_names(self):
        """
        Returns the ServerName instances associated to the Listen object.
        """
        return self._server_names


    @server_names.setter
    def server_names(self, server_name):
        """
        Adds an ServerName instance to those associated to the ServerName.
        """
        if server_name is None:
            raise ValueError("A server name must be given.")
        if not isinstance(server_name, ServerName):
            raise TypeError("The server name must be a ServerName instance, not %s." % (type(server_name)))

        if server_name.domain not in self.server_names.keys():
            self._server_names[server_name.domain] = server_name
