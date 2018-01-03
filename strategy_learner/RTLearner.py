"""
RTLearner

Seungkwan Bryan Baek
sbaek47
"""

import numpy as np

class RTLearner(object):

    def __init__(self, leaf_size, verbose=False):
        self.leaf_size = leaf_size

    def author(self):
        return 'sbaek47'

    def build_tree(self, data):
        dataX_same=np.all(x == data[:,:-1][0] for x in data[:,:-1])
        dataY_same=np.all(y == data[:,-1][0] for y in data[:,-1])

        if (data.shape[0]<=self.leaf_size) or (dataX_same==True) or (dataY_same==True):
            leaf=np.array([[-999, np.mean(data[:,-1]), np.nan, np.nan]])
            return leaf
        else:
            index = np.random.randint(data.shape[1]-2)

            SplitVal = np.median(data[:,index])

            lefttree_data=data[data[:,index]<=SplitVal]
            righttree_data=data[data[:,index]>SplitVal]

            #median doesn't split evenly; try the mean
            if (righttree_data.shape[0]==0):
                leaf=np.array([[-999, np.mean(data[:,-1]), np.nan, np.nan]])
                return leaf

            lefttree=self.build_tree(lefttree_data)
            righttree=self.build_tree(righttree_data)

            root=np.array([[index, SplitVal, 1, lefttree.shape[0]+1]])
            return np.vstack([root,lefttree,righttree])

    def addEvidence(self,dataX,dataY):

        data=np.column_stack((dataX, dataY))
        self.tree=self.build_tree(data)

    def query(self,points):

        y_value=np.ones(points.shape[0])
        for y in range(len(points)):
            index=0
            #whiel leaf (-999)is not found
            while (int(self.tree[int(index)][0]) > -1):
                tree_factor = int(self.tree[index][0])
                Splitval = self.tree[index][1]
                if points[y][tree_factor]<=Splitval:
                    index=int(index+self.tree[int(index)][2])
                else:
                    index=int(index+self.tree[int(index)][3])
            y_value[y]=self.tree[int(index)][1]

        return y_value

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
