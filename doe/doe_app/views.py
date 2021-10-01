from django.shortcuts import render
from . import neural
from .models import Dataset
import numpy as np

def home(request):
    return render(request, "home.html")

def graph(request):
    ## TODO: ## TODO: dynamic input loading
    ## TODO: ## TODO: loads neural data file from db
    ## TODO: ## TODO: must take input: num_output, num_feature
    num_feature, num_output = 0, 0
    test = neural.NN('doe_app/neural_data/FRACTIONAL_FACTORIAL_RUNS.csv')
    test.fit()

    # Use Score data to build context for html
    data = test.score(num_feature, num_output)
    ylabel = test.y_labels[num_output].split(":")[1]
    if (data[0][0] == "D"):
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
        'ylabels': test.y_labels
    }

    return render(request, "graph.html", context)

def datasets(request):
    if request.method == "POST":
        uploaded_file = request.FILES['file']
        dataset_name = uploaded_file.name.split(".")[0]
        # Check if it is a csv file
        if not uploaded_file.name.split(".")[1] == 'csv':
            print("Please only upload .csv files")
            return render(request, "datasets.html")
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

    return render(request, "datasets.html")
