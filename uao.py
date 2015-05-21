'''
Created on May 21, 2015

@author: pnikiel
'''



class Session(object):
    def __init__(self, client):
        self.client = client
        



class Node(object):
    """Represents node in UA address space."""
    def __init__(self, session, address):
        self.session = session
        self.is_bound = True
        self.address = address

class Variable(Node):
    """ Represents a variable in UA address space. Can read/write/subscribe to the address space. """
    def __init__(self, node):
        self.__dict__ = node.__dict__
        self.offline_data = None
        
    def __getattr__(self, name):
        if name=='value' and self.is_bound:
            self.read()
        if name in ['value', 'status', 'source_t']:
            return self.offline_data[name]
        else:
            return self.__dict__[name]
    def read(self):
        self.offline_data = {'value':3, 'status':True}

class Object(Node):
    """Represents node whose type is Object and which may contain variables, methods and other objects"""
    def __init__(self, node):
        self.__dict__ = node.__dict__
        self.variables = {}
    def __getattr__(self, name):
        if name in self.variables.keys():
            return self.variables[name]
        else:
            return self.__dict__[name]
