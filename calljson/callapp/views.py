from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from . import json

# Create your views here.


@parser_classes([JSONParser])
@api_view(['GET','POST'])
def call_json(request):
    if request.method == 'POST':
        data = request.data
        output = json.result
        return Response(output)
