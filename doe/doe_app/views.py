from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.shortcuts import render
from . import neural
from .models import Dataset
from itertools import combinations
import numpy as np

def home(request):
    return render(request, 'home.html')

def graph(request):
    if request.method != 'POST':
        return view(request)

    if request.method == 'POST':
        chosen_name = request.POST['dataset_choice']
        add_data = request.POST.get("add_data", "off")
        final_data = ""
        new_data = ""

        i = 1
        while new_data != "input_end":
            new_data = request.POST.get("input_data_" + str(i), "input_end")
            if new_data != "input_end":
                final_data = final_data + new_data + ","
            i = i + 1

        i = 1
        while new_data != "output_end":
            new_data = request.POST.get("output_data_" + str(i), "output_end")
            if new_data != "output_end":
                final_data = final_data + new_data + ","
            i = i + 1

        print(chosen_name)
        print(request.POST)

        final_data = final_data[:-1]
        dataset_list = getDatasetList(chosen_name, final_data, add_data)

        nn = neural.NN(dataset_list, 'doe_app/neural_data/{file_name}.csv'.format(file_name=chosen_name))
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
            'dataset': chosen_name,
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
        dataset_list = getDatasetList(graph_title, "", "")
        nn = neural.NN(dataset_list, 'doe_app/neural_data/{file_name}.csv'.format(file_name=graph_title))
        nn.fit()


        #
        # Save data from html form
        #

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
                X.append(v)

        #
        # Generate test lists
        #

        a_count = 0
        a = [0,1,2,3,4]
        A = []

        N = 1
        for x in X:
            if isinstance(x, list):
                N = N * len(x)
            if x == "c":
                a_count += 1

        uniqueList = [",".join(map(str, comb)) for comb in combinations(a, a_count)]
        for i in range(len(uniqueList)):
            sublist = uniqueList[i].split(",")
            A.append(sublist)
        a_count = 0

        A = [[0,0], [0,1], [0,2], [0,3], [0,4], [1,0], [1,1], [1,2], [1,3], [1,4],
             [2,0], [2,1], [2,2], [2,3], [2,4], [3,0], [3,1], [3,2], [3,3], [3,4],
             [4,0], [4,1], [4,2], [4,3], [4,4]]

        tests = []
        for i in range(N):
            x = np.zeros(len(nn.X_labels))
            count = 0
            for j in range(len(nn.x_labels)):
                if X[2*j] == "c":
                    if count == 0:
                        x[count] = X[2*j+1][int(A[i][0])]
                    else:
                        x[count] = X[2*j+1][int(A[i][1])]
                    count += 1
                if X[2 * j] == "d":
                    idx = []
                    for k in range(len(nn.X_labels)):
                        if nn.x_labels[j] in nn.X_labels[k]:
                            if X[2*j + 1] == nn.X_labels[k].split("= ")[1]:
                                x[count] = 1
                            else:
                                x[count] = 0
                            count += 1
            tests.append(x)

        y_num = 0
        for y in range(len(nn.y_labels)):
            if request.POST.get('output') == nn.y_labels[y]:
                y_num = y

        scores = []
        for x in tests:
            score = []
            y_score = nn.nn[y_num].predict(x.reshape(1, -1))
            for i in range(len(x)):
                score.append(x[i])
            score.append(y_score[0])
            scores.append(score)

        scores_labels = [nn.X_labels, request.POST.get('output')]
        
        context = {
            'scores' : scores,
            'scores_labels' : scores_labels,
            'xlabels': nn.x_labels,
            'ylabels': nn.y_labels,
            'dataset': chosen_name,
            'X_labels': nn.X_labels,
            'x_min': nn.min,
            'x_max': nn.max,
        }

    return render(request, "results.html", context)

def format(request):
    return render(request, "format.html")

def datasets(request):
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
            
    return render(request, "datasets.html")

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
def getDatasetList(dataset_name, new_data, add_data):
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
            if (a.split(",") != [""]):
                final_list.append(a.split(","))

        if len(new_data.split(",")) == len(dataset_headers):
            if not ("" in new_data.split(",")):
                final_list.append(new_data.split(","))
                if current_dataset["data"][-1] != "\n":
                    current_dataset["data"] = current_dataset["data"] + "\r\n"

                new = current_dataset["data"] + new_data + "\r\n"
                if add_data == 'on':
                    with open('doe_app/neural_data/{file_name}.csv'.format(file_name=dataset_name), 'a') as file:
                        file.write(new_data + '\r\n')
                    Dataset.objects.filter(pk=dataset_name).update(name=dataset_name,
                                                                   headers=current_dataset["headers"],
                                                                   types=current_dataset["types"], data=new)
        return final_list

    return None

def getIndex(labels, label):
    for i in range(len(labels)):
        if (labels[i] == label):
            return i
    return 0