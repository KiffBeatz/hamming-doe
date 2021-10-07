from sklearn.neural_network import MLPRegressor
import numpy as np
import csv

class NN:
	""" A class for the neurel network backend of the dynamic DOE """

	""" INIT """
	def __init__(self, file_name):
		self.data = list(csv.reader(open(file_name, 'r')))
		self.nn = [] # list of neural networks, one for each output
		self.x_labels = [] # list of labels for each feature
		self.X_labels = [] # list of labels for each feature (normalized)
		self.y_labels = [] # list of labels for each output
		self.mean = None # list of mean of each feature

		# Checking validity of input (TODO)


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
		mean_list = []
		for i in range(d):
			if (data_types[i] == "D"):
				#Discrete Normalization
				disc_vals = np.unique(x_list[i])
				mean_list.append(1)
				for dis in disc_vals:
					mean_list.append(0)
					x = np.zeros(N, dtype=int)
					for j in range(N):
						if (x_list[i][j] == dis):
							x[j] = 1
					X_list.append(x)
					self.X_labels.append("D:" + labels[i] + " = " + dis)
				mean_list.pop()
				#labels[i] = str(len(disc_vals)-1) + labels[i]
			elif (data_types[i] == "C"):
				#Continous Standardization
				x = np.array(x_list[i]).astype(np.float64)
				x = (x - x.mean()) / (x.std())
				X_list.append(x)
				mean_list.append(x.mean())
				self.X_labels.append("C:" + labels[i])


		# Convert lists
		self.mean = np.array(mean_list)
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
			i_list = []
			a = self.mean
			ret = []
			for i in range(len(self.X_labels)):
				if self.x_labels[feature] in self.X_labels[i]:
					i_list.append(i)

			for i in i_list:
				a[i] = 0

			for i in i_list:
				a[i] = 1
				ret.append(self.X_labels[i])
				ret.append(self.nn[output].predict(a.reshape(1,-1)))
				a[i] = 0

			return ret

		elif (self.x_labels[feature].split(":")[0] == "C"):
			a = self.mean
			k = 0
			for i in range(len(self.X_labels)):
				if self.x_labels[feature] in self.X_labels[i]:
				    k = i
			ret = []
			cts_range = [-1.6, -0.8, 0, 0.8, 1.6]
			for i in cts_range:
				a[k] = i
				score = 0
				for j in range(2):
					score += (self.nn[output].predict(a.reshape(1,-1)))/2
				ret.append(self.x_labels[feature] + " = " + str(i))
				ret.append(score)
			return ret
