'''
Created on May 21, 2015

@author: pnikiel
'''

class session(object):
    def __init__(self, client):
        self.client = client



class node(object):
    def __init__(self, session):
        self.session = session

class variable(node):
    pass

class uaobject(node):
    pass
