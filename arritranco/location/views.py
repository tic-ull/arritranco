# Create your views here.
from django.shortcuts import render_to_response

def algo(request):

    algo = Location
    return render_to_response('index.html')

