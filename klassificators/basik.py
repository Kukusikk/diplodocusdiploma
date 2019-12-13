# здесь будет производиться создание наивного байсевского классификатора
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB
import numpy as np
from createleningdata.vectorworlds import creatingleningvector
dataX,dataY=creatingleningvector()
dataY=dataY[:7]
X_train, X_test, Y_train, Y_test = train_test_split(np.array(dataX), np.array(dataY), test_size=0.33, random_state=42)
clf_bnb=BernoulliNB()
clf_bnb.fit(X_train,Y_train)
print(clf_bnb.predict(X_test))
print(Y_test)