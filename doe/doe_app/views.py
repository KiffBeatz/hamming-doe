from django.shortcuts import render
from . import neural
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
