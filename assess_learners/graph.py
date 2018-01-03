import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import RTLearner as rt
import DTLearner as dt
import BagLearner as bl
import LinRegLearner as lr

data=pd.read_csv('Data/Istanbul.csv')
data=data.drop(data.columns[0], axis=1)
data=np.array(data, dtype=np.float32)

traintestsplit=math.floor(data.shape[0]*0.6)

np.random.shuffle(data)
training, test = data[:traintestsplit,:], data[traintestsplit:,:]

trainX=training[:,:-1]
trainY=training[:,-1]

testX = test[:,:-1]
testY = test[:,-1]

leaves=(range(100))
#leaves=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,30,40,50,70,100]
i=0
in_first_RMSE=np.ones(len(leaves))
out_first_RMSE=np.ones(len(leaves))

for leaf_size in leaves:
    first_learner = dt.DTLearner(leaf_size=leaf_size, verbose = False)
    first_learner.addEvidence(trainX, trainY)
    Y_preds_in = first_learner.query(trainX)
    Y_preds_out = first_learner.query(testX)
    in_first_RMSE[i] = math.sqrt(((trainY - Y_preds_in) ** 2).mean())
    out_first_RMSE[i] = math.sqrt(((testY - Y_preds_out) ** 2).mean())
    i+=1

# df = pd.concat([in_first_RMSE, out_first_RMSE], keys=['In Sample', 'Out of Sample'], axis=1)

# ax = df.plot(title="Assessing Overfitting with DTLearner", fontsize=12)
# ax.set_xlabel('Leaf Size')
# ax.set_ylabel('RMSE')

plt.plot(leaves, in_first_RMSE)
plt.plot(leaves, out_first_RMSE)
plt.title("Assessing Overfitting with DTLearners")
plt.ylabel('RMSE')
plt.xlabel('Leaf Size')
plt.show()

df0=pd.DataFrame(leaves)
df1=pd.DataFrame(in_first_RMSE)
df2=pd.DataFrame(out_first_RMSE)
frames=[df0, df1,df2]
result=pd.concat(frames, axis=1)
print result
# #################################################################
in_second_RMSE=np.ones(len(leaves))
out_second_RMSE=np.ones(len(leaves))

j=0

for leaf_size in leaves:
    second_learner=bl.BagLearner(learner=dt.DTLearner, kwargs={"leaf_size" :leaf_size, "verbose": False}, bags=20, boost=False, verbose=False)
    second_learner.addEvidence(trainX, trainY)

    Y_preds_in = second_learner.query(trainX)
    Y_preds_out = second_learner.query(testX)
    in_second_RMSE[j] = math.sqrt(((trainY - Y_preds_in) ** 2).mean())
    out_second_RMSE[j] = math.sqrt(((testY - Y_preds_out) ** 2).mean())


    j+=1

plt.plot(leaves, in_second_RMSE)
plt.title("Assessing Overfitting with BagLearner of 20 DTLearners")
plt.ylabel('RMSE')
plt.xlabel('Leaf Size')
plt.show()

df3=pd.DataFrame(leaves)
df4=pd.DataFrame(in_second_RMSE)
df5=pd.DataFrame(out_second_RMSE)
frames1=[df3,df4, df5]
result1=pd.concat(frames1, axis=1)
print result1
#################################################################
k=0
in_third_RMSE=np.ones(len(leaves))
out_third_RMSE=np.ones(len(leaves))

for leaf_size in leaves:
    third_learner = rt.RTLearner(leaf_size=leaf_size, verbose = False)
    third_learner.addEvidence(trainX, trainY)

    Y_preds_in = third_learner.query(trainX)
    Y_preds_out = third_learner.query(testX)
    in_third_RMSE[k] = math.sqrt(((trainY - Y_preds_in) ** 2).mean())
    out_third_RMSE[k] = math.sqrt(((testY - Y_preds_out) ** 2).mean())

    k+=1

plt.plot(leaves, out_third_RMSE)
plt.title("Assessing Overfitting with RTLearner")
plt.ylabel('RMSE')
plt.xlabel('Leaf Size')
plt.show()

df6=pd.DataFrame(leaves)
df7=pd.DataFrame(in_third_RMSE)
df8=pd.DataFrame(out_third_RMSE)
frames2=[df6,df7,df8]
result2=pd.concat(frames2, axis=1)

print result2
