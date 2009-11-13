
class AbstractMetric:

    def __init__(self, params={}):
        '''
        Metric constructor with an optional dictionary of name=value parameters.
        '''
        raise NotImplementedError
    
    def generate(self, analyzer=None):
        '''
        Generate the performance metric computation.
        '''
        raise NotImplementedError
    
    # --- end of class AbstractMetric

class AbstractModel:

    def validate(self, params):
        '''
        Validates the model for the given parameters.
        Returns an estimate of the metric being validated, e.g., wall-clock time.
        '''
        raise NotImplementedError
    
    # --- end of class AbstractModel

class AbstractAnalyzer:
    
    def runAnalysis(self, metric):
        '''
        Perform the analysis. The argument metric is an instance of an implementation
        of the analysis.interfaces.AbstractMetric interface.
        '''
        raise NotImplementedError
    
    def getScalingFactor(self):
        '''Metric scaling factor when using this tool (w.r.t. standard units)'''
        # TODO: define standard units somewhere
        return 1  # default

    # --- end of class AbstractAnalyzer
    
