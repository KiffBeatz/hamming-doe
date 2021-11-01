from sklearn.neural_network import MLPRegressor
from collections import Counter
import numpy as np
import csv

class NN:
	""" A class for the neurel network backend of the dynamic DOE """

	""" INIT """
	def __init__(self, data_list, file_name):
		# If statement to take care of default data issue
		if data_list == None:
			self.data = list(csv.reader(open(file_name, 'r')))
		else:
			self.data = data_list
		self.nn = [] # list of neural networks, one for each output
		self.x_labels = [] # list of labels for each feature
		self.X_labels = [] # list of labels for each feature (normalized)
		self.y_labels = [] # list of labels for each output
		self.min = [] # list of min of each feature
		self.max = [] # list of max of each feature

	""" FIT """
	def fit(self):
		# Input data
		labels = self.data[0]
		data_types = self.data[1]
		A = np.vstack(self.data[2:])

		# Num observations, Num features+outputs
		N, k = A.shape

		# Convert input
		# Lists of vectors X=(Dynamic | Continuous) y=Output)
		i_c, i_d, i_o = 0, 0, 0
		x_list, y_list, X_list = [], [], []
		for i in range(k):
			if (data_types[i] == "D"):
				i_d += 1
				x_list.append(A[:,i])
				self.x_labels.append("D:" + labels[i])
			elif (data_types[i] == "C"):
				i_c += 1
				x_list.append(A[:,i])
				self.x_labels.append("C:" + labels[i])
			elif (data_types[i] == "O"):
				i_o += 1
				y_list.append(A[:,i])
				self.y_labels.append("O:" + labels[i])

		#Normalization
		d = i_c + i_d
		for i in range(d):
			if (data_types[i] == "D"): #Discrete Normalization
				disc_vals = np.unique(x_list[i])
				min_val = Counter(x_list[i].tolist()).most_common()[-1][0]
				max_val = Counter(x_list[i].tolist()).most_common(1)[0][0]

				for dis in disc_vals:
					if (dis == max_val):
						self.min.append(0)
						self.max.append(1)
					elif (dis == min_val):
						self.min.append(1)
						self.max.append(0)
					else:
						self.min.append(0)
						self.max.append(0)

					x = np.zeros(N, dtype=int)
					for j in range(N):
						if (x_list[i][j] == dis):
							x[j] = 1

					X_list.append(x)
					self.X_labels.append("D:" + labels[i] + " = " + dis)

			elif (data_types[i] == "C"):
				#Continous Standardization
				x = np.array(x_list[i]).astype(np.float64)
				x = (x - x.mean()) / (x.std())
				X_list.append(x)
				self.min.append(np.min(x))
				self.max.append(np.max(x))
				self.X_labels.append("C:" + labels[i])

		# Convert lists
		d = len(X_list)
		X = np.zeros((N, d))
		for i in range(d):
			x = X_list[i]
			for j in range(N):
				X[j][i] = x[j]

		# Neural Network outputs
		for y in y_list:
			nn_out = MLPRegressor(max_iter = 50000).fit(X, y.astype(np.float64))
			self.nn.append(nn_out)


	""" SCORE """
	def score(self, feature, output):
		if (feature > (len(self.x_labels)-1) or feature < 0):
			print("Please specify an feature index between 0 and " + str(len(self.x_labels)-1))
			print("Usage: NN.score(feature_idx, output_idx)")
			return -1
		if (output > (len(self.y_labels)-1) or output < 0):
			print("Please specify an output index between 0 and " + str(len(self.y_labels)-1))
			print("Usage: NN.score(feature_idx, output_idx)")
			return -1

		if (self.x_labels[feature].split(":")[0] == "D"):
			I = []
			ret = []
			for i in range(len(self.X_labels)):
				if self.x_labels[feature] in self.X_labels[i]:
					I.append(i)
					ret.append("")
					ret.append(0)

			count = 0
			for i in I:
				ret[count*2] = self.X_labels[i]

				a = np.array(self.min)
				for j in I:
					a[j] = 0
				a[i] = 1
				
				for j in range(2):
					ret[count*2+1] += (self.nn[output].predict(a.reshape(1, -1)))/2
				
				a = np.array(self.max)
				for j in I:
					a[j] = 0
				a[i] = 1
				
				for j in range(2):
					ret[count*2+1] += (self.nn[output].predict(a.reshape(1, -1)))/2

				count += 1

			return ret

		elif (self.x_labels[feature].split(":")[0] == "C"):
			ret = ["",0,"",0,"",0,"",0,"",0]
			idx, min_val, max_val = -1,-1,-1

			for i in range(len(self.X_labels)):
				if self.x_labels[feature] in self.X_labels[i]:
					idx = i
					min_val = self.min[idx]
					max_val = self.max[idx]

			mid = (min_val+max_val)/2
			cts_range = [min_val, (min_val+mid)/2, mid, (max_val+mid)/2, max_val]

			count = 0
			for i in cts_range:
				ret[count*2] = self.x_labels[feature] + " = " + str(i)

				a = np.array(self.min)
				a[idx] = i

				for j in range(2):
					ret[count*2+1] += (self.nn[output].predict(a.reshape(1,-1)))/2

				a = np.array(self.max)
				a[idx] = i

				for j in range(2):
					ret[count*2+1] += (self.nn[output].predict(a.reshape(1,-1)))/2

				count += 1

			return ret

# 	""" Helper Function """
# 	# Program to find most frequent element in a list
# 	def most_frequent(List):
# 		return max(set(List), key = List.count)
#
# 	""" Helper Function """
# 	# Program to find most frequent element in a list
# 	def least_frequent(List):
# 		return min(set(List), key = List.count)
#
# test = NN(None, "SURFACE_RESPONSE_RUNS.csv")
# test.fit()
# print(test.min)
# for i in range(len(test.x_labels)):
# 	for j in range(len(test.y_labels)):
# 		print(test.score(i,j))
# 		print("")
