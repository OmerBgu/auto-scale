import time
import random
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.model_selection import KFold, cross_val_score
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from urllib.request import urlopen

plt.style.use('ggplot')
pd.set_option('display.max_columns', 500)


def cross_val_metrics(fit, training_set, class_set, estimator, print_results = True):
    """
    Purpose
    ----------
    Function helps automate cross validation processes while including
    option to print metrics or store in variable

    Parameters
    ----------
    fit: Fitted model
    training_set:  Data_frame containing 80% of original dataframe
    class_set:     data_frame containing the respective target vaues
                      for the training_set
    print_results: Boolean, if true prints the metrics, else saves metrics as
                      variables

    Returns
    ----------
    scores.mean(): Float representing cross validation score
    scores.std() / 2: Float representing the standard error (derived
                from cross validation score's standard deviation)
    """
    my_estimators = {
    'rf': 'estimators_',
    'nn': 'out_activation_',
    'knn': '_fit_method'
    }
    try:
        # Captures whether first parameter is a model
        if not hasattr(fit, 'fit'):
            return print("'{0}' is not an instantiated model from scikit-learn".format(fit))

        # Captures whether the model has been trained
        if not vars(fit)[my_estimators[estimator]]:
            return print("Model does not appear to be trained.")

    except KeyError as e:
        print("'{0}' does not correspond with the appropriate key inside the estimators dictionary. \
\nPlease refer to function to check `my_estimators` dictionary.".format(estimator))
        raise

    n = KFold(n_splits=10)
    scores = cross_val_score(fit,
                         training_set,
                         class_set,
                         cv = n)
    if print_results:
        for i in range(0, len(scores)):
            print("Cross validation run {0}: {1: 0.3f}".format(i, scores[i]))
        print("Accuracy: {0: 0.3f} (+/- {1: 0.3f})"\
              .format(scores.mean(), scores.std() / 2))
    else:
        return scores.mean(), scores.std() / 2


def create_conf_mat(test_class_set, predictions):
    """Function returns confusion matrix comparing two arrays"""
    if (len(test_class_set.shape) != len(predictions.shape) == 1):
        return print('Arrays entered are not 1-D.\nPlease enter the correctly sized sets.')
    elif (test_class_set.shape != predictions.shape):
        return print('Number of values inside the Arrays are not equal to each other.\nPlease make sure the array has the same number of instances.')
    else:
        # Set Metrics
        test_crosstb_comp = pd.crosstab(index = test_class_set,columns = predictions)
        # Changed for Future deprecation of as_matrix
        test_crosstb = test_crosstb_comp.values
        return test_crosstb


def plot_roc_curve(fpr, tpr, auc, estimator, xlim=None, ylim=None):
    """
    Purpose
    ----------
    Function creates ROC Curve for respective model given selected parameters.
    Optional x and y limits to zoom into graph

    Parameters
    ----------
    * fpr: Array returned from sklearn.metrics.roc_curve for increasing
            false positive rates
    * tpr: Array returned from sklearn.metrics.roc_curve for increasing
            true positive rates
    * auc: Float returned from sklearn.metrics.auc (Area under Curve)
    * estimator: String represenation of appropriate model, can only contain the
    following: ['knn', 'rf', 'nn']
    * xlim: Set upper and lower x-limits
    * ylim: Set upper and lower y-limits
    """
    my_estimators = {'knn': ['Kth Nearest Neighbor', 'deeppink'],
              'rf': ['Random Forest', 'red'],
              'nn': ['Neural Network', 'purple']}

    try:
        plot_title = my_estimators[estimator][0]
        color_value = my_estimators[estimator][1]
    except KeyError as e:
        print("'{0}' does not correspond with the appropriate key inside the estimators dictionary. \
\nPlease refer to function to check `my_estimators` dictionary.".format(estimator))
        raise

    fig, ax = plt.subplots(figsize=(10, 10))

    plt.plot(fpr, tpr,
             color=color_value,
             linewidth=1)
    plt.title('ROC Curve For {0} (AUC = {1: 0.3f})'\
              .format(plot_title, auc))

    plt.plot([0, 1], [0, 1], 'k--', lw=2) # Add Diagonal line
    plt.plot([0, 0], [1, 0], 'k--', lw=2, color = 'black')
    plt.plot([1, 0], [1, 1], 'k--', lw=2, color = 'black')
    if xlim is not None:
        plt.xlim(*xlim)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.show()
    plt.close()


def print_class_report(predictions, alg_name):
        """
        Purpose
        ----------
        Function helps automate the report generated by the
        sklearn package. Useful for multiple model comparison

        Parameters:
        ----------
        predictions: The predictions made by the algorithm used
        alg_name: String containing the name of the algorithm used

        Returns:
        ----------
        Returns classification report generated from sklearn.
        """
        print('Classification Report for {0}:'.format(alg_name))
        print(classification_report(predictions,
                                    test_class_set,
                                    target_names=dx))

if __name__ == '__main__':
    train_data = pd.read_csv('trainExample.csv')
    names = ["cpu_requests_milicore", "cpu_requests_precent", "cpu_limit_milicore", "memory_requests_Mi",
                         "memory_requests_precent", "memory_limits_Mi", "memory_limits_percent","QoE"]

    names_index = names[:1]

    dx = ['QoE - 1', 'QoE - 2', 'QoE - 3']

    #print (train_data.head())
    #print (train_data.describe())

    feature_space = train_data.iloc[:, train_data.columns != 'QoE']
    feature_class = train_data.iloc[:, train_data.columns == 'QoE']

    training_set, test_set, class_set, test_class_set = train_test_split(feature_space,feature_class,test_size = 0.20,random_state = 42)

    # Cleaning test sets to avoid future warning messages
    class_set = class_set.values.ravel()
    test_class_set = test_class_set.values.ravel()

    # Set the random state for reproducibility
    fit_rf = RandomForestClassifier(random_state=42)

    np.random.seed(42)
    start = time.time()

    param_dist = {'max_depth': [2, 3, 4,5,6,7],
              'bootstrap': [True, False],
              'max_features': ['auto', 'sqrt', 'log2', None,7]}

    cv_rf = GridSearchCV(fit_rf, cv = 10,
                     param_grid=param_dist,
                     n_jobs = 3)

    # Set best parameters given by grid search
    fit_rf.set_params(criterion='entropy',max_features='auto',max_depth=2)
    cv_rf.fit(training_set, class_set)
    print('Best Parameters using grid search: \n',cv_rf.best_params_)
    end = time.time()
    print('Time taken in grid search: {0: .2f}'.format(end - start))

    fit_rf.set_params(warm_start=True,oob_score=True)

    min_estimators = 30
    max_estimators = 80

    error_rate = {}

    for i in range(min_estimators, max_estimators + 1):
        fit_rf.set_params(n_estimators=i)
        fit_rf.fit(training_set, class_set)

        oob_error = 1 - fit_rf.oob_score_
        error_rate[i] = oob_error

    # Convert dictionary to a pandas series for easy plotting
    oob_series = pd.Series(error_rate)
    print(oob_series)
    fig, ax = plt.subplots(figsize=(10, 10))

    #ax.set_facecolor('lightblue')

    oob_series.plot(kind='line',color='red')
    plt.axhline(0.055,color='#875FDB',linestyle='--')
    plt.axhline(0.05,color='#875FDB',linestyle='--')
    plt.xlabel('n_estimators')
    plt.ylabel('OOB Error Rate')
    plt.title('OOB Error Rate Across various Forest sizes \n(From 15 to 1000 trees)')

    plt.show()
    #TODO : chagne n_estimators to max from last graph
    fit_rf.set_params(n_estimators=400,bootstrap=True,warm_start=False,oob_score=False)

    fit_rf.fit(training_set, class_set)
    cross_val_metrics(fit_rf, training_set, class_set, 'rf',print_results = True)
    predictions_rf = fit_rf.predict(test_set)

    conf_mat = create_conf_mat(test_class_set, predictions_rf)
    sns.heatmap(conf_mat, annot=True, fmt='d', cbar=False)
    plt.xlabel('Predicted Values')
    plt.ylabel('Actual Values')
    plt.title('Actual vs. Predicted Confusion Matrix')
    plt.show()

    accuracy_rf = fit_rf.score(test_set, test_class_set)

    print("Here is our mean accuracy on the test set:\n {0:.3f}" .format(accuracy_rf))

    # Here we calculate the test error rate!
    test_error_rate_rf = 1 - accuracy_rf
    print("The test error rate for our model is:\n {0: .4f}" .format(test_error_rate_rf))

    # We grab the second array from the output which corresponds to
    # to the predicted probabilites of positive classes
    # Ordered wrt fit.classes_ in our case [0, 1] where 1 is our positive class
    predictions_prob = fit_rf.predict_proba(test_set)[:, 1]

    fpr2, tpr2, _ = roc_curve(test_class_set,predictions_prob,pos_label=1)

    auc_rf = auc(fpr2, tpr2)
    plot_roc_curve(fpr2, tpr2, auc_rf, 'rf',xlim=(-0.01, 1.05), ylim=(0.001, 1.05))

    print(classification_report(predictions_rf, test_class_set, target_names=dx))
