'''
Created on May 21, 2015

@author: pnikiel
'''

from pyuaf.util             import Address, NodeId, ExpandedNodeId, opcuaidentifiers
from  pyuaf.util import nodeclasses

class Session(object):
    def __init__(self, client, server_uri):
        self.client = client
        self.server_uri = server_uri
        
    def build_objects(self, address):
        o = Object(Node(self, address))
        browse_result = self.client.browse([address])
        for ri in xrange(len(browse_result.targets[0].references)):
            ref = browse_result.targets[0].references[ri]
            print ref.displayName
            # now we have information - node class
            if ref.nodeClass == nodeclasses.Variable:
                o.variables[str(ref.displayName.text())] = Variable( Node( self, Address(ExpandedNodeId(ref.nodeId)) ))
            elif ref.nodeClass == nodeclasses.Method:
                o.methods[str(ref.displayName.text())] = Method( Node( self, Address(ExpandedNodeId(ref.nodeId)) ), o )
            elif ref.nodeClass == nodeclasses.Object:
                o.children_objects [str(ref.displayName.text())] = self.build_objects( Address(ExpandedNodeId(ref.nodeId)) )
        return o
    
        
    def get_object(self, string_a, ns):
        n = NodeId( string_a, ns )
        a = Address( n, self.server_uri )
        return self.build_objects(a)

class Node(object):
    """Represents node in UA address space.
    TODO: i think it should have a list of all things it links to
    """
    def __init__(self, session, address):
        self.session = session
        self.is_bound = True
        self.address = address

class Variable(Node):
    """ Represents a variable in UA address space. Can read/write/subscribe to the address space. """
    def __init__(self, node):
        super(Variable,self).__init__(node.session, node.address)
        self.offline_data = None   
    def __getattr__(self, name):
        if name=='value' and self.is_bound:
            self.read()
        if name in ['value', 'status', 'source_t']:
            return self.offline_data[name]
        else:
            return self.__dict__[name]
    def __setattr__(self, name, value):
        if name == 'value':
            raise Exception ("Not implemented")
        else:
            self.__dict__[name] = value
    def read(self):
        self.offline_data = {'value':3, 'status':True}

class Method(Node):
    def __init__(self, node, parentObject):
        super(Method,self).__init__(node.session, node.address)
        self.parentObject = parentObject

    def __call__(self,*args):
        self.session.client.call( self.parentObject.address, self.address )
        print 'method was called on '+str(self.address)
        

class Object(Node):
    """Represents node whose type is Object and which may contain variables, methods and other objects
    TODO: merge variables,objects,methods into one __ua_mapping__
    """
    def __init__(self, node):
        super(Object,self).__init__(node.session, node.address)
        self.variables = {}
        self.children_objects = {}
        self.methods = {}
    def __getattr__(self, name):
        if name in ['variables','children_objects','methods']:
            return self.__dict__[name]
        if name in self.variables.keys():
            return self.variables[name]
        elif name in self.children_objects.keys():
            return self.children_objects[name]
        elif name in self.methods.keys():
            return self.methods[name]
        else:
            return self.__dict__[name]
    def __setattr__(self, name, value):
        print '__setattr_ name='+str(name)+" value="+str(value)
        if name in ['variables','children_objects','methods','session','address','is_bound']:
            super(Node,self).__setattr__(name,value)
        elif name in self.variables.keys():
            self.variables[name].value = value
        elif name in self.children_objects.keys():
            raise Exception ('?')
        elif name in self.methods.keys():
            raise Exception
        else:
            self.__dict__[name] = value

