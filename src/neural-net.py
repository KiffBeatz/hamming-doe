from sklearn.neural_network import MLPRegressor
import numpy as np

# ---------------------------------------------------------------
# INPUT
# ---------------------------------------------------------------

my_input = open('printer_runs.txt','r').read().split('\n')
A = [] 

for line in my_input:
  for a in line.split(","):
    A.append(a)

labels = A[0:9]


B = np.array(A[9:585]).reshape(-1, 9)
b = ['180','40','0.1','0.55','V','0']
X = np.zeros((64, 12))
Y = np.zeros((64, 3))

for i in range(len(B)):
  for j in range(6):
    if B[i][j] == b[j]:
      X[i][2*j]=1
      X[i][2*j+1]=0
    else:
      X[i][2*j]=0
      X[i][2*j+1]=1
  for j in range(3):
    Y[i][j] = B[i][j+6]

Y_0 = Y[:,0]
Y_1 = Y[:,1]
Y_2 = Y[:,2]

# ---------------------------------------------------------------
# THREE NEURAL NETWORKS --> 64 Input Observations (samples)
# ---------------------------------------------------------------

NN_Young = MLPRegressor(max_iter=50000).fit(X, Y_0)
NN_Break_In_Tention = MLPRegressor(max_iter=50000).fit(X, Y_1)
NN_Breakage_Deform = MLPRegressor(max_iter=50000).fit(X, Y_2)

print("Young(GPA) with different Test Tube Positions")
print("Horizontal Position: " + str(NN_Young.predict(np.array([0,1,0,1,0,1,0,1,0,1,0,1]).reshape(1,-1))))
print("Vertical Position: " + str(NN_Young.predict(np.array([0,1,0,1,0,1,0,1,1,0,0,1]).reshape(1,-1))))
print("")
print("Young(GPA) with different Extrusion Widths")
print("0.55 Width: " + str(NN_Young.predict(np.array([0,1,0,1,0,1,1,0,0,1,0,1]).reshape(1,-1))))
print("0.75 Width: " + str(NN_Young.predict(np.array([0,1,0,1,0,1,0,1,0,1,0,1]).reshape(1,-1))))
