from sklearn.ensemble import RandomForestClassifier
import sys
import pandas
from numpy import genfromtxt
from sklearn import model_selection



def predict(qoe,podsnumber):
    #qoe=int(sys.argv[1])
    #podsnumber=int(sys.argv[2])
    #podsnumber=1
#    url = '/home/omer/PycharmProjects/untitled/data/try.csv'

	#load data	
	train='/home/ubuntu/train.csv'
	train='train.csv'
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
	# train_set_as_array=transformed_values
	for i in range(1, len(train_set_as_array) - 1):
   		train_set_as_array[i].astype(float)

	#train_set_as_array = list(map(int, train_set_as_array))

	X = train_set_as_array[:, 0:row - 1]
	Y = train_set_as_array[:, row - 1]
	validation_size = 0.2
	seed = 7
	X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size,
                                                                                random_state=seed)
	# Make predictions on validation train_set
	RandomForestClassifier(bootstrap=True, class_weight=None, criterion='entropy',
        	    min_samples_leaf=1, min_samples_split=2,
        	    min_weight_fraction_leaf=0.0, n_estimators=10, n_jobs=2,
        	    warm_start=False)
	rf = RandomForestClassifier()
	rf.fit(X_train, Y_train)
	predictions = rf.predict(test)
	sampleNumber = 5
	results = list(map(int, predictions))
	avg= reduce(lambda x, y: x + y, results) / len(results)
	delta=avg-qoe
	if(delta>1):
    		return 1 # delta is more than 1 scale up
	if (delta<0):
    		return -1 #qoe is negative scale down
	return 0 # no need to scale

if __name__ == "__main__":
	predict()

