# здесь будет производиться создание классификатора методом ближайшего соседа
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

from createleningdata.vectorworlds import creatingleningvector
dataX,dataY=creatingleningvector()
dataY=dataY
X_train, X_test, Y_train, Y_test = train_test_split(np.array(dataX), np.array(dataY), test_size=0.33, random_state=42)
clf_bnb=KNeighborsClassifier()
clf_bnb.fit(X_train,Y_train)
m=clf_bnb.predict(X_test)
k=0
for i,j in zip(m,Y_test):
    if i!=j:
        k+=1
print(k*100/len(Y_test))