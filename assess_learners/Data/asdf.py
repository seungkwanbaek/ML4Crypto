import numpy as np
import csv
import string

data=np.loadtxt(open("Istanbul.csv", "rb"), delimiter=",", skiprows=1, usecols=(1,2,3,4,5,6,7,8,9))

#################DOOOOOO
#check the 1st param
#is it lendata or just data?
#**kwargs


def build_tree(data):
    leaf_size=1
    dataX_same=np.all(x == data[:,:-1][0] for x in data[:,:-1])
    dataY_same=np.all(y == data[:,-1][0] for y in data[:,-1])

    if (data.shape[0]<=leaf_size) or (dataX_same==True) or (dataY_same==True):
        leaf=np.array([[-999.0, np.mean(data[:,-1]), np.nan, np.nan]])
        return leaf
    else:
        max_value= None
        index=None
        for x in range (0, data.shape[1]-2):
            corr=abs(np.corrcoef(data[:,x], data[:,-1])[1,0])
            if corr > max_value:
                index=x
                max_value = corr
        SplitVal=np.median(data[:,index])

        lefttree_data=data[data[:,index]<=SplitVal]
        righttree_data=data[data[:,index]>SplitVal]

        #median doesn't split evenly; try the mean
        if (righttree_data.shape[0]==0):
            SplitVal_mean=np.mean(data[:,index])
            lefttree_data=data[data[:,index]<=SplitVal_mean]
            righttree_data=data[data[:,index]>SplitVal_mean]

            #mean doesn't work: lump all the nodes together
            if (righttree_data.shape[0]==0):
                leaf=np.array([[-999.0, np.mean(data[:,-1]), np.nan, np.nan]])
                return leaf

        lefttree=build_tree(lefttree_data)
        righttree=build_tree(righttree_data)

        root=np.array([[index, SplitVal, 1, lefttree.shape[0]+1]])
        return np.vstack([root,lefttree,righttree])

# tree=build_tree(Xtrain)

def query(Xtest):
    #create y_value array
    y_value=np.ones(len(Xtest))
    for y in range(len(Xtest)):
        index=0
        #whiel leaf (-999)is not found
        while (tree[index][0] > -998):
            tree_factor = tree[index][0]
            Splitval = tree[index][1]

            if Xtest[y][tree_factor]<=Splitval:
                index=index+tree[index][2]
            else:
                index=index+tree[index][3]

        #return y-value
        y_value[y]=tree[index][1]

    return y_value

# result=query(Xtrain)
# print np.corrcoef(result, Ytrain)[1,0]
