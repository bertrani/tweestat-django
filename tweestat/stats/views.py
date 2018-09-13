from django.http import HttpResponse
import logging

from django.http import HttpResponseRedirect
from django.template import loader

from .forms import StatForm

from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_exempt

from . import graphs

logger = logging.getLogger(__name__)

def stat(request):
    if request.method == "POST":
        # Get the posted form
        field = request.POST["field"]
        start_date = request.POST["start_date"]
        start_time = request.POST["start_time"]
        end_date = request.POST["end_date"]
        end_time = request.POST["end_time"]

        start = "{}T{}".format(start_date, start_time)
        end = "{}T{}".format(end_date, end_time)
        return redirect("/stats/mean/{}/{}/{}/".format(field, start, end))
    else:
        my_form = StatForm

    return render(request, 'stats/form.html', {'form': my_form})


def index(request):
    return render(request, 'stats/form.html')

def mean(request, field, start, end):
    my_graph = graphs.Graph(field, start, end)
    return my_graph.get_graph()


