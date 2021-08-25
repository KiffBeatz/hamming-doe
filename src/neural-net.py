from sklearn.neural_network import MLPRegressor
import numpy as np

# labels of original 7 features and 3 outputs
labels = [["RunOrder"],
        ["Temperature"],
        ["Speed"],
        ["Thickness of Layer"],
        ["Extrusion Width"],
        ["Test Tube Position"],
        ["Internal Fill Angle"],
        ["Young(GPa)"],
        ["Break in Tension(MPa)"],
        ["Breakage Deformation"]]


# read in input file
input_file = open("run_orders.txt", "r")
runs = input_file.read()
run_list = runs.split(" ")
input_file.close()


# vertical/horizontal constants
vert = 1
hor = 0


# fixup input
for i in range(64):
  run_list[10*i]=i+1
  idx = 10*i+5
  if run_list[idx] == "Vertical":
    run_list[idx] = vert
  else:
    run_list[idx] = hor

A = np.array(run_list[0:640])
B = np.reshape(A, (-1, 10))
X = B[:,1:]

x_labels = B[:,:1]
x_train = X[:50,:-3].astype(float)
y_train = X[:50,-1:].reshape(50).astype(float)
x_test = X[50:,:-3].astype(float)
y_test = X[50:,-1:].reshape(14).astype(float)


# Neural Network of 50 samples and 14 tests
NN = MLPRegressor(max_iter=3000).fit(x_train, y_train)
for i in range(14):
  print("Test "+str(i+1))
  print(NN.predict(x_test[i].reshape(1,-1)))
  
  # Haven't figured out why, but the predict is very inconsistent 
  # and not close to the tests
  
  print(y_test[i])
  print("")
