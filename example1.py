from pyuaf.client           import Client
from pyuaf.client.settings  import ClientSettings, SessionSettings
from pyuaf.util             import Address, NodeId, opcuaidentifiers
import uao

server_uri = 'urn:CERN:QuasarOpcUaServer'  # needs to match the factual server URI
server_address = 'opc.tcp://127.0.0.1:4841'
cs = ClientSettings("myClient", [server_address])
client = Client(cs)
# next 2 lines are not necessary but help to ensure good state of OPC-UA connectivity
rootNode = Address( NodeId(opcuaidentifiers.OpcUaId_RootFolder, 0), server_uri )
result=client.browse ([ rootNode ])

session = uao.Session(client, server_uri )


obj = session.get_object('anObject', 2)  # needs to match factuall existing object

