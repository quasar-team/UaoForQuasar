

class ObjectifiedNode():
    pass

    def __init__(self,addr):
        self.a = addr
        self.contained = {}
        self.variables = {}
        # here -- scan it
        
    
    def __getattr__(self,name):
        if self.variables.has_key(name):
            # todo  -- read from the variable
            return 'has this variable'
        elif self.contained.has_key(name):
            # todo -- return the object
            return 'an object'
        else:
            raise AttributeError
        

root = ObjectifiedNode('a')
