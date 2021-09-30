from django.shortcuts import render
from django.http import HttpResponse
from . import neural
import numpy as np

def home(request):
    return render(request, "home.html")

def graph(request):
    test = neural.NN('doe_app/neural_data/FRACTIONAL_FACTORIAL_RUNS.csv')
    test.fit()

    num_feature = 0
    num_output = 0
    data = test.score(num_feature, num_output)

    ylabel = test.y_labels[num_output].split(":")[1]
    print(ylabel)

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
        'ylabel': ylabel
    }

    return render(request, "graph.html", context)
