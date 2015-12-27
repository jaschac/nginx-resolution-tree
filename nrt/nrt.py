# -*- coding: utf-8 -*-

"""
This module defines an Nginx Resolution Tree class, which represents the resolution problem per se.

An NRT tree takes, as an input, a list of directives. Each synthetises the specific blocks required
to serve content at a specific location. Each directive is represented as a dictionary, whose keys
are a mandatory signature and optional parameters. The former is a colon separated string, while
the latter is, again, a dictionary which contains extra information such as default servers and
redirections.

The Nrt class is responsible of igniting the process of resolution of the input directives into
objects and relationships, and, eventually, into vhost configuration files, if the overall scenario
is Nginx-valid. As such, an Nrt instance occupies the root of the resolution tree. Its children
are, in order, instances of the Listen, ServerName and Location classes. They do occupy the second,
third and fouth levels of the Nrt tree. The leafs of the tree are the aliases of the containers.
They are not represented by a class.

An Nrt instance, per se, does keep track of its unique Listen objects. This is achieved through a
dictionary which maps the unique address to the reference itself. The Nrt class is thus responsible
of instantiating Listen instances. The Nrt class, though, is not responsible of generating any
other component of the tree. Each level of the tree is indeed responsible of generating its lower
level, properly mapping those objects.
"""

from collections import defaultdict
from re import compile, match

from nrt.listen import Listen


class Nrt(object):
    """
    Represent an Nginx Resolution Tree object.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes an Nrt instance. Requires the client to provide the Nginx directives passed in
        by the linked containers. 
        """
        self._directives = []
        self._listen = {}


    @property
    def directives(self, *args, **kwargs):
        """
        Returns the directives that are currently part of the Nrt.
        """
        return self._directives


    @directives.setter
    def directives(self, directive):
        """
        Adds a directive to those currently part of the Nrt.
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
        
        if directive["signature"] not in [directive["signature"] for directive in self._directives]:
            self._directives.append(directive)


    @property
    def export(self, *args, **kwargs):
        """
        Exports the Nrt into virtual host configuration files. Only valid Nrts can be exported to
        file.
        """
        raise NotImplementedError


    @property
    def is_valid(self):
        """
        Returns whether the Nrt's current status is valid or not. Only valid Nrts can be exported
        to virtual host files.
        """
        raise NotImplementedError


    @property
    def listen(self, *args, **kwargs):
        """
        Returns the Listen objects that are currently part of the Nrt.
        """
        return self._listen


    @listen.setter
    def listen(self, listen):
        """
        Adds a Listen instance to those currently part of the Nrt.
        """
        if listen is None:
            raise ValueError("A listen must be given.")
        if not isinstance(listen, Listen):
            raise TypeError("The listen must be a Listen instance, not %s." % (type(listen)))
        
        if listen.address not in self._listen.keys():
            self._listen[listen.address] = listen


    def resolve(self):
        """
        Resolve the input directives into a unique list of Listen objects. They in turn will turn
        the non address part of the directives into objects and relationships.
        """

        # Generate Listen objects
        for directive in self.directives:
            alias, ip, port, server_name, location = directive["signature"].split(":")
            handle_listen = Listen(**{
                                        "directive" : directive,
                                        "ip" : ip,
                                        "port" : port,
                                        }
                                    )
            self.listen = handle_listen

        # Validate the Nrt (check the paper!)