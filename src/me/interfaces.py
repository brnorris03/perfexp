
class AbstractPlatform:
    def runApp(self, cmd):
        raise NotImplementedError
    
    def loadTrials(self, storage):
        '''
        Load the performance data into the specified storage,
        which is an implementation of the storage.interfaces.AbstractStorage 
        interface.
        '''
        raise NotImplementedError

    def validateModel(self, model):
        '''
        Validate the model (the parameter is an instance of an implementation of AbstractModel).
        '''
        raise NotImplementedError

class AbstractCollector:
    def setCounters(self):
        raise NotImplementedError

    def getCommand(self):
        '''returns command string'''
        raise NotImplementedError

    def getDataFormat(self):
        raise NotImplementedError
