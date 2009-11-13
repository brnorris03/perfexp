
class AbstractMetric:

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
    
    def runAnalysis(self):
        '''Perform the analysis.'''
        raise NotImplementedError
    
    def getScalingFactor(self):
        '''Metric scaling factor when using this tool (w.r.t. standard units)'''
        # TODO: define standard units somewhere
        return 1  # default

    # --- end of class AbstractAnalyzer
    
