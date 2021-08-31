from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
import numpy as np

# INPUT
my_input = open('printer_runs.txt','r').read().split('\n')
A = [] 

for line in my_input:
  for a in line.split(","):
    A.append(a)

labels = A[0:9]
X = np.array(A[9:585]).reshape(-1, 9).astype(np.float64)



# STANDARDIZING INPUT - must still normalize
x_train = X[:54,:-3]
y_train = X[0:54:,7]
x_test = X[54:,:-3]
y_test = X[54:,7]

scale = StandardScaler(with_mean=0, with_std=1).fit(x_train, y_train)
train_norm = scale.transform(x_train)
test_norm = scale.transform(x_test)



# Neural Network of 54 samples and 10 tests
NN = MLPRegressor(max_iter=10000).fit(train_norm, y_train)
for i in range(10):
  print("Test "+str(i+1))
  print(NN.predict(test_norm[i].reshape(1,-1)))
  print(y_test[i])
  print("")



# testing one of features as example
print("Testing: " + labels[2])
test_a = scale.transform(np.array([180,60,0.1,0.6,0,1]).reshape(1,-1))
test_b = scale.transform(np.array([180,60,0.5,0.6,0,1]).reshape(1,-1))
print("0.1: "+str(NN.predict(test_a)))
print("0.5: "+str(NN.predict(test_b))) #thicc boi gives better score


# TEST COMMENT :D
