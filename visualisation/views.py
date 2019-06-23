from django.http import HttpResponse
from .dash_apps import fileUpload,columnStats,lineplot,scatterPlot,barPlot
import pandas as pd
from django.shortcuts import render,render_to_response


fileUpload()
#comment out the following line
lineplot()
scatterPlot()
barPlot()
def statistics(request):
    stats=columnStats()   
    context={
        'stats':stats
    }     
    return render(request, 'statistics.html',context)
