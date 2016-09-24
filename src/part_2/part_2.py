import matplotlib.pyplot as plt  # pyplot is used to plot a chart
from sklearn import datasets  # datasets are used as a sample dataset, contains set that has number recognition data
from sklearn import svm  # for the sklearn Support Vector Machine

digits = datasets.load_digits()  # digits variable loaded with digit dataset

print(digits.data)  # features (actual data)

print(digits.target)  # label assigned to data

clf = svm.SVC()  # specify the classifier using defaults

clf = svm.SVC(gamma=0.001, C=100)  # specify the classifier

# load all but the last 10 data points and use for training
# X contains all of the "coordinates" and y is the "target" or "classification"
# X has pixel data, y is the number that the pixels form
X, y = digits.data[:-10], digits.target[:-10]

clf.fit(X, y)  # train

print("Prediction: ", clf.predict(digits.data[-5]))  # predict what the 5th from last element is

# visualization
plt.imshow(digits.images[-5], cmap=plt.cm.gray_r, interpolation='nearest')
plt.show()

# adjusting gamma
# larger values increase speed, lower accuracy
# speed changes by factors of 10
clf = svm.SVC(gamma=0.01, C=100)
clf.fit(X, y)  # train
print("Prediction: ", clf.predict(digits.data[-5]))  # predict what the 5th from last element is

# less accurate
clf = svm.SVC(gamma=0.0001, C=100)
clf.fit(X, y)  # train
print("Prediction: ", clf.predict(digits.data[-5]))  # predict what the 5th from last element is
