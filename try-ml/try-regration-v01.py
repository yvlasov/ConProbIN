#!/usr/bin/python
"""
============================
Nearest Neighbors regression
============================

Demonstrate the resolution of a regression problem
using a k-Nearest Neighbor and the interpolation of the
target using both barycenter and constant weights.

"""
###############################################################################
# Generate sample data
import pandas
import numpy as np
import matplotlib.pyplot as plt
from sklearn import neighbors



#url = "MotionSymulationForNNet.csv"
url = "20000-samples.csv"
names = ['ShortCurve', 'ShortCurveDer', 'LongTail', 'NoizeSignal', 'SignalWave']
#names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
dataset = pandas.read_csv(url, names=names)

url = "MotionSymulationForNNet-control.csv"
names = ['ShortCurve', 'ShortCurveDer', 'LongTail', 'NoizeSignal', 'SignalWave']
#names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
dataset_control = pandas.read_csv(url, names=names)

T = np.linspace(0, 1, 1001)[:, np.newaxis]

# Split-out validation dataset
array = dataset.values
#print array
X = array[:,0:4]
y = array[:,4]

array = dataset_control.values
#print array
X_control = array[:,0:4]
y_control = array[:,4]
#print X
#print Y
#validation_size = 0.20
#seed = 7
#X_train, X_validation, Y_train, Y_validation = cross_validation.train_test_split(X, Y, test_size=validation_size, random_state=seed)
###############################################################################
# Fit regression model
n_neighbors = 20000

print(len(T))
print(len(X))
print(len(y))

for i, weights in enumerate(['uniform', 'distance']):
    knn = neighbors.KNeighborsRegressor(n_neighbors, weights=weights)
    y_ = knn.fit(X, y).predict(X_control)
    plt.subplot(2, 1, i + 1)
#    plt.scatter(T, y_control, c='r', label='data')
#'ShortCurveDer', 'LongTail', 'NoizeSignal', 'SignalWave']
#    plt.plot(T, X_control[:,0], c='k', label='ShortCurve')
#    plt.plot(T, X_control[:,1], c='grey', label='ShortCurveDer')
#    plt.plot(T, X_control[:,2], c='b', label='LongTail')
    plt.plot(T, X_control[:,3], c='y', label='NoizeSignal')
    plt.plot(T, y_, c='g', label='prediction')
 
    plt.plot(T, (y_-y_control), c='m', label='Prediction Error')
    plt.plot(T, (y_-X_control[:,0]), c='c', label='Shortcurve Error')


    plt.plot(T, y_control, c='r', label='Control Out')
    plt.axis('tight')
    plt.legend()
    plt.title("KNeighborsRegressor (k = %i, weights = '%s')" % (n_neighbors,
                                                                weights))

plt.show()
