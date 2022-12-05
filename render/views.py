# from django.shortcuts import render

# def index(request):
#     return render(request, 'render/index.html', {})

from django.shortcuts import render
from django.http import HttpResponse, FileResponse
import os
from urllib import parse
# from .models import Greeting
import requests
from numpy.random import randint
from numpy import array
from scipy.spatial import Delaunay
from scipy.interpolate import interp2d

from .triangles_minimal import *

# Create your views here.
# def index(request):
#     # return HttpResponse('Hello from Python!')
#     return render(request, "index.html")

# def index(request):
#     r = requests.get('http://httpbin.org/status/418')
#     print(r.text)
#     return HttpResponse('<pre>' + r.text + '</pre>')

def svgResponse(request):
    host = str(os.environ.get('HOST_NAME'))
    url = "/"+ request.path + "?" + str(dict(request.META)["QUERY_STRING"])
    url = parse.urlsplit(url)
    print(dict(parse.parse_qsl(url.query)))
    query = dict(parse.parse_qsl(url.query))

    
    arr = []
    size = [1080, 1920]
    if "xmax" in query:
        if "ymax" in query:
            size = [int(query["ymax"]), int(query["xmax"])]
        else:
            size = [1080, int(query["xmax"])]
    elif "ymax" in query:
        size = [int(query["ymax"]), 1920]

    density = 150 
    if "density" in query:
        density = int(query["density"])
    createRndPoints(density, arr, size[0], size[1])
    createAxisPoints(density, arr, size[0], size[1])
    pointsxy = array(pointsAsxy(arr))
    color1, color2, color3 = createColors()
    colors = [[color1.hex, color2.hex], [color3.hex, color3.hex, color3.hex, color3.hex]]
    colorPoints = []
    createRndClrPoints(colorPoints, size[0], size[1], maincolors=colors[0], bgcolors=colors[1])
    for x in colorPoints:
        x.printPoint()
    tri = Delaunay(pointsxy)
    tri = tri.simplices.copy()
    svg = returnSVGTriangles(tri, arr, size[0], size[1], colorPoints)
    return svg

def favicon(request):
    BASE_DIR = str(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print(BASE_DIR)
    print(os.path.join(BASE_DIR,"render\\favicon.ico"))
    ico = open(os.path.join(BASE_DIR,"render\\favicon.ico"), 'r') 
    return FileResponse(ico)

def generate(request, slug):
    return HttpResponse(svgResponse(request), content_type='image/svg+xml')
    
def index(request):    
    return HttpResponse(svgResponse(request), content_type='image/svg+xml')

# def db(request):

#     greeting = Greeting()
#     greeting.save()

#     greetings = Greeting.objects.all()

#     return render(request, "db.html", {"greetings": greetings})