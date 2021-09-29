from django.shortcuts import render
from django.http import HttpResponse
from . import neural

def home(request):
    return HttpResponse('<h1>DOE home</h1>')

def graph(request):

    a = neural.test()
    print(a)

    # irrelevant test data
    data = [
        ("01-01-2021", 1597),
        ("02-01-2021", 1456),
        ("03-01-2021", 1908),
        ("04-01-2021", 896),
        ("05-01-2021", 755),
        ("06-01-2021", 453),
        ("07-01-2021", 1100),
        ("08-01-2021", 1234),
        ("09-01-2021", 1478),
    ]

    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    context = {
        'labels': labels,
        'values': values
    }

    return render(request, "graph.html", context)

