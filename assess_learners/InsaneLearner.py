import numpy as np
import BagLearner as bl
import LinRegLearner as lr

class InsaneLearner(object):
    def __init__(self, verbose):
        pass
    def author(self):
        return 'sbaek47'
    def addEvidence(self,dataX,dataY):
        self.learner=bl.BagLearner(learner = bl.BagLearner, kwargs = {"learner": lr.LinRegLearner, "bags":20, "kwargs": {}, "boost": False, "verbose": False}, bags=20, boost=False, verbose=False)
        self.learner.addEvidence(dataX, dataY)
    def query(self,points):
        return self.learner.query(points)

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
