# -*- coding: utf-8 -*-

"""
This module defines the an Nginx Resolution Tree. It is responsible of turning the input into
proper objects and build relationships between them, so that the initial directives can be properly
split into valid vhost configuration files.

An NRT object represents the root of the tree. Its leafs are unique listen directives. A directive
is a dictionary with two elements: a signature, which is a colon separated mandatory parameter; and
optional, which is a dictionary containing extra information such as default servers and
redirections.

A signature has the following format:
alias:ip:port:server_name:location
"""

from collections import defaultdict
from re import compile, match


class Nrt(object):
    """
    Represent an Nginx Resolution Tree object.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes an Nrt instance. Requires the client to provide the Nginx directives passed in
        by the linked containers. 
        """
        directives = kwargs.get("directives", [])
        signature_regex =  compile("^\w+:[\w\.]+:\d+:[\w\.]+:[\w/]+$")

        if not isinstance(directives, list):
            raise TypeError("The directives are expected as a list, not %s." % (type(directives)))
        for directive in directives:
            if not isinstance(directive, dict):
                raise TypeError("A directive is expected as a dictionary, not %s." % (type(directive)))
            if 'signature' not in directive.keys():
                raise ValueError("A directive is expected to have a signature.")
            if not isinstance(directive['signature'], str):
                raise TypeError("The signature of a directive is expected as a string, not %s." % (type(directive)))
            if not signature_regex.match(directive['signature']):
                raise ValueError("A signature must have the following format: 'alias:ip:port:server_name:location'")

        self.directives = directives
        self.listen = defaultdict(list)

    def listens(self):
        """
        Turns signatures into Listen objects. Listen objects are uniquely identified by the tuple
        ip:port.
        """
        for directive in self.directives:
            alias, ip, port, server_name, location = directive['signature'].split(":")
            listen = "%s:%s" % (ip, port)
            listen_directive = "%s:%s:%s" % (alias, server_name, location)
            self.listen[listen].append(listen_directive)                    # pass it to Listen


    def resolve(self):
        """
        Resolve the current NRT into vhost configuration files.
        """
        raise NotImplementedError
