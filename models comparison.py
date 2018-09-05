# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 12:42:55 2018

@author: KARIS
"""

import pandas as pd
df = pd.read_csv("main_df_final2.csv")
df.drop(["Unnamed: 0", "user_name","source"], inplace = True ,  axis = 1)

df["lexical_diversity"]=df["lexical_diversity"].fillna(0)
df["account_reputation"]=df["account_reputation"].fillna(0)
df_2 =df.sample(frac = 1)
features = df_2.iloc [: , [0,1,2,3,4,5,6,7] ].values
labels = df_2.iloc[: , -1:].values


from sklearn.model_selection import train_test_split as TTS
features_train , features_test,labels_train , labels_test = TTS(features ,labels , test_size = 0.3 , random_state = 0)




#knn
from sklearn.neighbors import KNeighborsClassifier
clf = KNeighborsClassifier(n_neighbors = 5 , p = 2)
clf.fit(features_train , labels_train)

pred2 = clf.predict(features_test)

Score = clf.score(features_test , labels_test)


#decision tree
from sklearn.tree import DecisionTreeClassifier
clfdt = DecisionTreeClassifier(criterion = 'entropy' , random_state = 0)
clfdt.fit(features_train , labels_train)

preddt = clfdt.predict(features_test)

Scoredt= clfdt.score(features_test , labels_test)

from sklearn.metrics import confusion_matrix
cmdt = confusion_matrix(labels_test, preddt)
#random forest


from sklearn.ensemble import RandomForestClassifier as RFC
clfrfc = RFC(n_estimators = 10 , criterion  = 'entropy', random_state = 0 )
clfrfc.fit(features_train , labels_train)

predrfc = clfrfc.predict(features_test)

Scorerfc= clfrfc.score(features_test , labels_test)
cmrfc = confusion_matrix(labels_test, predrfc)


#logistic regression



# Fitting logistic regression to the Training set
from sklearn.linear_model import LogisticRegression as lg
clflg = lg(random_state = 0)
clflg.fit(features_train , labels_train)

predlg = clflg.predict(features_test)

Scorelg= clflg.score(features_test , labels_test)

cmlg = confusion_matrix(labels_test, predlg)

#svm
from sklearn.svm import SVC
clfsvc = SVC(kernel = 'rbf' , random_state = 0)
clfsvc.fit(features_train , labels_train)

labels_pred = clfsvc.predict(features_test)


cmsvc = confusion_matrix(labels_test, labels_pred)


Scoresvc = clfsvc.score(features_test , labels_test)

# Applying k-Fold Cross Validation
from sklearn.model_selection import cross_val_score
accuraciessvc = cross_val_score(estimator = clfrfc, X = features_train, y = labels_train, cv = 10)

import numpy as np

import statsmodels.formula.api as sm
features = np.append(arr = np.ones((3651,1)).astype(int), values = features , axis =1)
features_opt = features[:,0:9]
regressor_OLS = sm.OLS(endog = labels , exog = features_opt).fit()
regressor_OLS.summary()
