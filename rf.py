"""
random forest prediction  
===================

what we predict?  
----------
the examined feature are the pod's cpu, memory and the predicted target us the current network delay at the client that
normalized to the formula of TRUNC(IF(H138<1.2,1,IF(H138<1.5,2,3)))
"""

from sklearn.ensemble import RandomForestClassifier
import sys
import pandas
from numpy import genfromtxt
from sklearn import model_selection

#Todo: 
 # change data to delay from wireshark, how? -> IO graph, unit->advance, count frames of field frame.time_delta 
 #and pick view as time of day and then copy to train1(or other number of pods train2,3...).
 # check if it will work like it if the decision of others pod will be correct 
 # again find a new fourmula for train, maybe for each train decide on a threshold formula of qoe per delay 
 # if wont wore so worst case is to parse so that each pod will be examined and if one of them is needed to scale scale all system  
 # maybe all of the split of the data was unnecessary ...
def predict(qoe,podsnumber):
	#url = '/home/omer/PycharmProjects/untitled/data/try.csv'
        #load data  
 	train='/home/ubuntu/train'+str(podsnumber)+".csv" #true path on the vm
 	train='train'+str(podsnumber)+".csv" #just for debug path on my computer
 	#url=url+str(podsnumber)+'.csv'
	# train dat just cpu and memory and pod
 	testpath = '/home/ubuntu/test.csv'
  	testpath='test.csv'
  	train_set = pandas.read_csv(train)  # the data from offline measurments
  	test = pandas.read_csv(testpath)  # , names=namesTrain
  	test_set = genfromtxt('test.csv', delimiter=',')
  	# take average of the samples
  	row = 2 + podsnumber * 2
  	# Split-out validation train_set
  	train_set_as_array = train_set.values
	print len (train_set.values)
  	# train_set_as_array=transformed_values
  	for i in range(1, len(train_set_as_array) - 1):
        	train_set_as_array[i].astype(float)
  	#train_set_as_array = list(map(int, train_set_as_array))
  	X = train_set_as_array[:, 0:row - 1]
  	Y = train_set_as_array[:, row - 1]
  	split=abs(float(float(len(test_set))/float(len(train_set_as_array)))) # for more dynamic sizes
  	split = 0.2 
  	seed = 7
  	X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=split,
                                                                                random_state=seed)
  	# Make predictions on validation train_set
	rf=RandomForestClassifier(bootstrap=True, class_weight=None, criterion='entropy',min_samples_leaf=1, 		min_samples_split=2,min_weight_fraction_leaf=0.0, n_estimators=10, n_jobs=2,warm_start=False)
  	#rf = RandomForestClassifier()
  	#rf.fit(X_train, Y_train)
	rf.fit(X, Y)
  	predictions = rf.predict(test)
  	results = list(map(int, predictions))
  	avg= reduce(lambda x, y: x + y, results) / len(results)
  	delta=avg-qoe
  	if(delta>1):
		print "scale up"
        	return 1 # delta is more than 1 scale up		
  	if (delta<0):
		print  "scale down"
                return -1 #qoe is negative scale down
	return 0 # no need to scale
if __name__ == "__main__":
        predict(1,1) #just for debug values

