from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.utils import timezone
from .models import DataPoint, Setting
from .graphing import html_graph
import datetime

def index(request):
    latest_data_point = DataPoint.objects.latest('time')
    return render(request,
                  'greenhouse/overview.html',
                  {'latest_data_point':latest_data_point})

def detailed(request, detailed_url):
    settings = Setting.objects.get()
    if detailed_url in DataPoint.url_to_variables:
        delta = datetime.timedelta(hours=settings.graph_range_detailed)
        end = timezone.now()
        start = end - delta
        graph_html = html_graph(detailed_url, start, end)
        context = {
            'graph_html':graph_html,
            'detailed_url':detailed_url.title()
        }
        return render(request, 'greenhouse/detailed.html', context)
    else:
        raise Http404('\"{}\" is not defined as a data point variable'
                      .format(detailed_url))

def redirect(request):
    return HttpResponseRedirect("/")

def video(request):
    latest_data_point = DataPoint.objects.latest('time')
    return render(request,
                  'greenhouse/video.html',
                  {'latest_data_point':latest_data_point})

def contact(request):
    return render(request,
                  'greenhouse/contact.html')

def about(request):
    return render(request,
                  'greenhouse/about.html')