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
        chosen_range_min = request.POST.get("chosen_range_min", -1)
        chosen_range_max = request.POST.get("chosen_range_max", -1)
        add_data = request.POST.get("add_data", "off")
        final_data = ""
        new_data = ""
        if chosen_range_max == '' or chosen_range_min == '':
            chosen_range_min = -1
            chosen_range_max = -1
        if int(chosen_range_max) < int(chosen_range_min):
            chosen_range_min = -1
            chosen_range_max = -1

        final_range = [chosen_range_min, chosen_range_max]
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

        final_data = final_data[:-1]
        #TODO Fix glitch where new_data is uploaded again on refresh

        dataset_list = getDatasetList(chosen_name, final_data, add_data, final_range)
        dataset_object = Dataset.objects.filter(name=chosen_name)
        
        graph_title = dataset_object[0].name

        # Load data from DB & Train
        
        nn = neural.NN(dataset_list, 'doe_app/neural_data/{file_name}.csv'.format(file_name=graph_title))
        nn.fit()

        # Scores of each feature for NN
        scores = []
        for j in range(len(nn.y_labels)):
            for i in range(len(nn.x_labels)):
                values = []
                labels = []
                score = nn.score(i, j)
                for s in score:
                    if isinstance(s, str):
                        if s[0] == "C":
                            labels.append(s.split("=")[1][1:])
                        elif s[0] == "D":
                            labels.append(s.split(":")[1])
                    else:
                        values.append(s[0])
                data = [values, labels]
                scores.append({nn.x_labels[i] + "&" + nn.y_labels[j]:data})

        context = {
            'chosen_name' : chosen_name,
            'scores' : scores,
            'xlabels': nn.x_labels,
            'ylabels': nn.y_labels,
        }

        return render(request, "graph.html", context)
#
# def graph(request):
#     # Variables
#     global discrete
#     labels, values = [], []
#
#     # Request Input
#     graph_title = "FRACTIONAL_FACTORIAL_RUNS"   #default get dataset
#     if request.method == 'POST':
#         chosen_name = request.POST['dataset_choice']
#         dataset_object = Dataset.objects.filter(name=chosen_name)
#         graph_title = dataset_object[0].name
#         if 'output' not in request.POST:
#             output_label = ''
#         else:
#             output_label = request.POST['output']
#         if 'feature' not in request.POST:
#             feature_label = ''
#         else:
#             feature_label = request.POST['feature']
#
#     # Load data from DB & Train
#     dataset_list = getDatasetList(graph_title)
#     test = neural.NN(dataset_list, 'doe_app/neural_data/{file_name}.csv'.format(file_name = graph_title))
#     test.fit()
#
#     # Use Score data to build context for html
#     num_feature, num_output = getIndex(test.x_labels, feature_label), getIndex(test.y_labels, output_label)
#     score_data = test.score(num_feature, num_output)
#
#     for i in range(len(score_data)):
#         if (i % 2 == 0):
#             labels.append(score_data[i].split(":")[1])
#         else:
#             values.append(score_data[i][0].astype(np.float64))
#
#     if (test.x_labels[num_feature].split(":")[0] == "C"):
#         discrete = 0
#     if (test.x_labels[num_feature].split(":")[0] == "D"):
#         discrete = 1
#
#     context = {
#         'discrete' : discrete,
#         'labels': labels,
#         'values': values,
#         'ylabel': test.y_labels[num_output].split(":")[1],
#         'xlabels': test.x_labels,
#         'ylabels': test.y_labels,
#         'graph_title': graph_title
#     }
#
#     print(context)
#
#     return render(request, "graph.html", context)

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
def getDatasetList(dataset_name, new_data, add_data, data_range):
    check = Dataset.objects.filter(pk=dataset_name).exists()
    if check:
        current_dataset = Dataset.objects.filter(pk=dataset_name).values()[0]
        final_list = []

        dataset_headers = current_dataset["headers"].split(",")
        final_list.append(dataset_headers)

        dataset_types = current_dataset["types"].split(",")
        final_list.append(dataset_types)

        dataset_data = current_dataset["data"].split("\n")
        range = 1
        for a in dataset_data:
            if(a.split(",") != [""]):
                if int(data_range[0]) != -1:
                    if range >= int(data_range[0]) and range <= int(data_range[1]):
                        final_list.append(a.split(","))
                else:
                    final_list.append(a.split(","))
                range = range + 1

        if len(new_data.split(",")) == len(dataset_headers):
            if not ("" in new_data.split(",")):
                final_list.append(new_data.split(","))
                if current_dataset["data"][-1] != "\n":
                    current_dataset["data"] = current_dataset["data"] + "\r\n"

                new = current_dataset["data"] + new_data + "\r\n"
                if add_data == 'on':
                    with open('doe_app/neural_data/{file_name}.csv'.format(file_name=dataset_name), 'a') as file:
                        file.write(new_data + '\r\n')
                    Dataset.objects.filter(pk=dataset_name).update(name=dataset_name, headers=current_dataset["headers"], types=current_dataset["types"], data = new)            
        return final_list
    
    return None

def getIndex(labels, label):
    for i in range(len(labels)):
        if (labels[i] == label):
            return i
    return 0