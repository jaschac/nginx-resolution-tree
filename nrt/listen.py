# -*- coding: utf-8 -*-

"""
This module defines a Listen object of an Nginx Resolution Tree. A Listen object is uniquely
identified by the pair IP:PORT. This pair is usually referred to as the address. Neither the IP
address nor the port are mandatory parameters: the first defaults to 0.0.0.0, while the latter to
80.  Each Listen object is also associated with a list of unique ServerName objects.
"""

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
        self.ip = kwargs.get("ip", "0.0.0.0")
        self.port = kwargs.get("port", 80)
        self._server_names = []

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


    @property
    def address(self):
        """
        Returns the address associated to the Listen object.
        """
        return "%s:%s" % (self.ip, self.port)


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
       
        if server_name.domain not in [server_name.domain for server_name in self._server_names]:
            self._server_names.append(server_name)
