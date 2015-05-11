import pyuaf
from pyuaf.client           import Client
from pyuaf.client.settings  import ClientSettings, SessionSettings
from pyuaf.util             import Address, NodeId, ExpandedNodeId, opcuaidentifiers
from pyuaf.util.errors      import UafError, ConnectionError
import pdb
from  pyuaf.util import nodeclasses

server_uri='urn:AtlasDcs:OpcUaCanOpenServer'
server_address='opc.tcp://pcatldcsp11.cern.ch:4841'
client = None
unfold = False


def connect( ):
    global client
    cs = ClientSettings("myClient", [server_address])
    client = Client(cs)
    rootNode = Address( NodeId(opcuaidentifiers.OpcUaId_RootFolder, 0), server_uri )
    result=client.browse ([ rootNode ])
    




class ObjectifiedNode():
    pass

    def __init__(self,addr):
        self.a = addr
        self.contained = {}
        self.variables = {}
        #  execute browse
        browse_result = client.browse([ self.a ])
        for ri in xrange(len(browse_result.targets[0].references)):
            ref = browse_result.targets[0].references[ri]
            print ref.displayName
            
            # now we have information - node class
            if ref.nodeClass == nodeclasses.Variable:
                self.variables[str(ref.displayName.text())] = Address(ExpandedNodeId(ref.nodeId))
            elif ref.nodeClass == nodeclasses.Object:
                if unfold:
                    self.contained[str(ref.displayName.text())] = ObjectifiedNode( Address(ExpandedNodeId(ref.nodeId)) )
            
        
    
    def __getattr__(self,name):
        if self.variables.has_key(name):
            a = self.variables[name]
            r = client.read([a])
            return r.targets[0].data.value
        elif self.contained.has_key(name):
            return self.contained[name]
        else:
            raise AttributeError
        



def get_object( string_a, ns ):
    n = NodeId( string_a, ns )
    a = Address( n, server_uri )
    return ObjectifiedNode(a)
