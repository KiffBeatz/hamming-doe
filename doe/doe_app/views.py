from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.shortcuts import render
from . import neural
from .models import Dataset
import numpy as np

def home(request):
    return render(request, "home.html")

def graph(request):
    # Default dataset
    graph_title = 'FRACTIONAL_FACTORIAL_RUNS'
    if request.method == "POST":
        chosen_name = request.POST['dataset_choice']
        dataset_object = Dataset.objects.filter(name=chosen_name)
        graph_title = dataset_object[0].name

    ## TODO: ## TODO: dynamic input loading
    ## TODO: ## TODO: loads neural data file from db
    ## TODO: ## TODO: must take input: num_output, num_feature
    num_feature, num_output = 1, 0
    # test = neural.NN('doe_app/neural_data/{file_name}.csv'.format(file_name = graph_title))
    # test.fit()
    dataset_list = getDatasetList(graph_title)
    test = neural.NN(dataset_list)
    test.fit()

    # Use Score data to build context for html
    data = test.score(num_feature, num_output)
    ylabel = test.y_labels[num_output].split(":")[1]

    # Discrete
    labels = []
    values = []
    for i in range(len(data)):
        if (i % 2 == 0):
            labels.append(data[i].split(":")[1])
        else:
            values.append(data[i][0].astype(np.float64))

    context = {
        'labels': labels,
        'values': values,
        'ylabel': ylabel,
        'xlabels': test.x_labels,
        'ylabels': test.y_labels,
        'graph_title': graph_title
    }

    return render(request, "graph.html", context)

def datasets(request):
    return render(request, "datasets.html")

def csv_view(request):
    return render(request, "csv_view.html")

def upload(request):
    if request.method == "POST":
        uploaded_file = request.FILES['file']
        dataset_name = uploaded_file.name.split(".")[0]
        # Check if it is a csv file
        if not uploaded_file.name.split(".")[1] == 'csv':
            print("Please only upload .csv files")
            return render(request, "upload.html")
        # Read file and get strings
        read_file = uploaded_file.read()
        decoded = read_file.decode('utf-8')
        split = decoded.splitlines()
        # Check if table exists in database
        check = Dataset.objects.filter(pk=dataset_name).exists()
        if not check:
            dataset_headers = split[0]
            dataset_types = split[1]
            dataset_data = decoded.split('\n', 2)[2]
            Dataset.objects.create(name=dataset_name, headers=dataset_headers, types=dataset_types, data=dataset_data)

    return render(request, "upload.html")

def view(request):
    dataset_names = []
    all_datasets = Dataset.objects.all()
    for set in all_datasets:
        dataset_names.append(set.name)

    context = {
        'names': dataset_names
    }

    return render(request, "view.html", context)

#Reads data from the database and formats it into a list that the neural network accepts
def getDatasetList(dataset_name):
    check = Dataset.objects.filter(pk=dataset_name).exists()
    if check:
        current_dataset = Dataset.objects.filter(pk=dataset_name).values()[0]
        final_list = []

        dataset_headers = current_dataset["headers"].split(",")
        final_list.append(dataset_headers)

        dataset_types = current_dataset["types"].split(",")
        final_list.append(dataset_types)

        dataset_data = current_dataset["data"].split("\r\n")
        for a in dataset_data:
            if(a.split(",") != [""]):
                final_list.append(a.split(","))

        return final_list