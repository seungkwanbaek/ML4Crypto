from util import entropy, information_gain, partition_classes
import numpy as np

class DecisionTree(object):
    def __init__(self):
        self.tree = []

    def build_tree(self, X, y):
        if np.array([i == y[0] for i in y]).all():
            leaf = np.array([[-999, y[0], np.nan, np.nan]])
            return leaf
        elif np.array([x == X[0] for x in X]).all():
            leaf = np.array([[-999, np.argmax(np.bincount(y)), np.nan, np.nan]])
            return leaf
        else:

            max_IG = None
            index = None
            SplitVal = None

            for j in range(len(X[0])):
                if isinstance(X[0][j], basestring):
                    string_split = max(set([t[j] for t in X]), key=[t[j] for t in X].count)

                    X_left, X_right, y_left, y_right = partition_classes(X, y, j, string_split)
                    Information_Gain = information_gain(y, [y_left, y_right])
                    if Information_Gain > max_IG:
                        index = j
                        SplitVal = string_split
                        max_IG = Information_Gain
                else:
                    num_split = np.mean([t[j] for t in X])
                    X_left, X_right, y_left, y_right = partition_classes(X, y, j, num_split)
                    Information_Gain = information_gain(y, [y_left, y_right])
                    if Information_Gain > max_IG:
                        index = j
                        SplitVal = num_split
                        max_IG = Information_Gain

            X_left, X_right, y_left, y_right = partition_classes(X, y, index, SplitVal)

            lefttree = self.build_tree(X_left, y_left)
            righttree = self.build_tree(X_right, y_right)

            if (righttree.shape[0]==0):
                leaf = np.array([[-999, np.mean(np.bincount(y)), np.nan, np.nan]])
                return leaf

            root = np.array([index, SplitVal, 1, lefttree.shape[0]+1])
            return np.vstack([root,lefttree,righttree])

    def learn(self, X, y):
        self.tree = self.build_tree(X, y)

    def classify(self, record):
        # TODO: classify the record using self.tree and return the predicted label
        y_value = np.ones(len(record))

        index = 0
        while (int(float(self.tree[index][0])) > -950):
            tree_factor = int(float(self.tree[index][0]))
            Splitval = self.tree[index][1]

            if isinstance(Splitval, basestring):
                if record[tree_factor] == Splitval:
                    index = int(index + int(float(self.tree[int(index)][2])))
                else:
                    index = int(index + int(float(self.tree[int(index)][3])))
            else:
                if record[tree_factor] <= Splitval:
                    index = int(index + int(float(self.tree[int(index)][2])))
                else:
                    index = int(index + int(float(self.tree[int(index)][3])))

        y_value = self.tree[int(index)][1]

        return int(float(y_value))

if __name__ == "__main__":
    print "asdf"
