import numpy as np

class BagLearner(object):

    def __init__(self, learner, kwargs, bags, boost, verbose):
        self.bags = bags
        self.boost=boost
        self.verbose=verbose

        self.learners = []
        for i in range(0, self.bags):
            self.learners.append(learner(**kwargs))
        pass

    def author(self):
        return 'sbaek47'

    def addEvidence(self,dataX,dataY):

        collection_of_Xbags=[]
        collection_of_Ybags=[]

        for i in range(self.bags):
            random=np.random.choice(dataX.shape[0], dataX.shape[0], replace =True)
            Xbag=dataX[random,:]
            Ybag=dataY[random]
            self.learners[i].addEvidence(Xbag, Ybag)

    def query(self,points):

        y_value=np.empty([self.bags, points.shape[0]])
        for i in range(self.bags):
            y_value[i]=self.learners[i].query(points)
        answer = np.mean(y_value, axis=0)
        return answer

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
