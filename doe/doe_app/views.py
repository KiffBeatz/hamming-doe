from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.shortcuts import render
from . import neural
from .models import Dataset
import numpy as np

def home(request):
    return render(request, 'home.html')

def graph(request):
    if request.method != 'POST':
        return view(request)

    if request.method == 'POST':
        chosen_name = request.POST['dataset_choice']
        dataset_object = Dataset.objects.filter(name=chosen_name)
        graph_title = dataset_object[0].name

        # Load data from DB & Train
        dataset_list = getDatasetList(graph_title)
        nn = neural.NN(dataset_list, 'doe_app/neural_data/{file_name}.csv'.format(file_name=graph_title))
        nn.fit()

        # Scores of each feature for NN
        scores = []
        for j in range(len(nn.y_labels)): # outputs
            for i in range(len(nn.x_labels)): # features
                values = []
                labels = []
                score = nn.score(i, j)
                for s in score:
                    if isinstance(s, str):
                        if s[0] == "C":
                            lab = s.split("=")[1][1:]
                            labels.append(round(float(lab), 2))
                        elif s[0] == "D":
                            labels.append(s.split(":")[1])
                    else:
                        values.append(s[0])
                data = [values, labels]
                scores.append({nn.x_labels[i] + "&" + nn.y_labels[j]:data})

        context = {
            'scores' : scores,
            'xlabels': nn.x_labels,
            'ylabels': nn.y_labels,
            'dataset': graph_title,
            'X_labels': nn.X_labels,
            'x_min': nn.min,
            'x_max': nn.max,
        }

        return render(request, "graph.html", context)

def results(request):
    if request.method != 'POST':
        return view(request)

    if request.method == 'POST':
        chosen_name = request.POST['dataset_choice']
        dataset_object = Dataset.objects.filter(name=chosen_name)
        graph_title = dataset_object[0].name

        # Load data from DB & Train
        dataset_list = getDatasetList(graph_title)
        nn = neural.NN(dataset_list, 'doe_app/neural_data/{file_name}.csv'.format(file_name=graph_title))
        nn.fit()

        N = 1
        values = []
        count = 0
        name = "x_" + str(count)
        c_name = "cx_" + str(count)

        while (name in request.POST) or (c_name in request.POST):
            if name not in request.POST:
                values.append([request.POST[c_name], request.POST["cx_"+str(count+1)]])
                count += 2
            else:
                values.append(request.POST[name])
                count += 1
            name = "x_" + str(count)
            c_name = "cx_" + str(count)

        X = []
        for v in values:
            if isinstance(v, list):
                v[0], v[1] = float(v[0]), float(v[1])
                mid = (v[0] + v[1])/2
                X.append("c")
                X.append([v[0], (v[0] + mid)/2, mid, (mid + v[1])/2, v[1]])
            if isinstance(v, str):
                X.append("d")
                if v == "Any":
                    x = []
                    idx = values.index(v)
                    label = nn.x_labels[idx]
                    for l in nn.X_labels:
                        if label in l:
                            x.append(l.split("= ")[1])
                    X.append(x)
                else:
                    X.append([v])
        for x in X:
            N = N * len(x)

        scores = {}
        tests = []
        # for i in range(N):
        #     test = np.zeros(len(nn.X_labels))
        #     for j in range(len(nn.x_labels)):
        #         idx = []
        #         for x in range(len(nn.X_labels)):
        #             if nn.x_labels[j] in nn.X_labels[x]:
        #                 idx.append(x)
        #
        #         type = nn.x_labels[j].split(":")[0]
        #         if type == "D":
        #             if len(X[j]) == 1:
        #                 for x in idx:
        #                     test[x] =
        #             else:
        #
        #         if type == "C":

        dict = {}
        x = [1, 1, 13, 3, ]



        print(X)
        context = {

        }

    return render(request, "results.html", context)


def format(request):
    return render(request, "format.html")

def datasets(request):
    data1 = Dataset.objects.all()
    if data1:
      for info1 in data1:
        info = info1

      data2 = info.name
      data3 = info.headers
      data4 = info.types
      data5 = info.data
      data3 = data3.split(",")
      width = len(data3)
      data4 = data4.split(",")
      subval = width * 10
      data5 = data5.replace("\n",",")
      data5 = data5.split(",")
      data5 = data5[:subval]
      data5 = np.array(data5)
      data6 = np.reshape(data5, (-1, width) )
      data5 = np.arange(10)
      data7 = np.arange(width)


      context1 = {
        'data1': data1,
        'data2': data2,
			  'data3': data3,
			  'data4': data4,
        'data5': data5,
			  'data6': data6,
        'data7': data7,
        'width': width,
				'subval': subval
      }
    if request.method == "POST":
        uploaded_file = request.FILES['file']
        dataset_name = uploaded_file.name.split(".")[0]
        # Check if it is a csv file
        if not uploaded_file.name.split(".")[1] == 'csv':
            raise Exception("Please only upload .csv files.")
        # Read file and get strings
        read_file = uploaded_file.read()
        decoded = read_file.decode('utf-8')
        split = decoded.splitlines()
        # Check if table exists in database
        check = Dataset.objects.filter(pk=dataset_name).exists()
        if not check:
            #Get data
            if len(split) < 3:
                raise Exception("Missing headers/types/data row.")
            dataset_headers = split[0]
            dataset_types = split[1]
            dataset_data = decoded.split('\n', 2)[2]
            #Check data valid before adding to database
            header_count = len(dataset_headers.split(","))
            types = dataset_types.split(",")
            types_count = len(types)

            for entries in types:
                if entries != "D" and entries != "C" and entries != "O":
                    raise Exception("Invalid data type. Expected: 'D/C/O' Got: '" + str(entries) + "'.")

            if (header_count != types_count):
                raise Exception("Inconsistent header/types length. Headers: '" + str(header_count) + "' Types: '" + str(types_count) + "'.")
            else: 
                dataset_count_list = dataset_data.split("\n")
                if dataset_count_list[0] == "":
                    raise Exception("'No data given.'")
                line = 3
                for a in dataset_count_list:
                    if(a.split(",") != [""]):
                        if (len(a.split(",")) != header_count):
                            raise Exception("Inconsistent data length. Expected: '" + str(header_count) + "' Data length: '" + str(len(a.split(","))) + "' on file line: '" + str(line) + "'.")
                    line = line + 1
            Dataset.objects.create(name=dataset_name, headers=dataset_headers, types=dataset_types, data=dataset_data)
        else:
            raise Exception("Already uploaded database.")
    if data1:
      return render(request, "datasets.html", context1)
    else:
      return render(request, "datasets.html", {'data1': data1})

def view(request):
    dataset_names = []
    all_datasets = Dataset.objects.all()
    for set in all_datasets:
        dataset_names.append(set.name)

    context = {
        'names': dataset_names
    }

    return render(request, "view.html", context)


# Reads data from the database and formats it into a list that the neural network accepts
def getDatasetList(dataset_name):
    check = Dataset.objects.filter(pk=dataset_name).exists()
    if check:
        current_dataset = Dataset.objects.filter(pk=dataset_name).values()[0]
        final_list = []

        dataset_headers = current_dataset["headers"].split(",")
        final_list.append(dataset_headers)

        dataset_types = current_dataset["types"].split(",")
        final_list.append(dataset_types)

        dataset_data = current_dataset["data"].split("\n")
        for a in dataset_data:
            if(a.split(",") != [""]):
                final_list.append(a.split(","))

        return final_list
    
    return None

def getIndex(labels, label):
    for i in range(len(labels)):
        if (labels[i] == label):
            return i
    return 0