from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from django.core.files import File
import requests
import os
# Create your views here.


format_output= {
    "job_params":{
        "ui_id":"4447aac-abf5-11ec-942-0a58c0a80816",
        "middleware_id":"SAFEE-32929-29",
        "service_name":"compareX",
    },
    "service_params":{
        "doc_output_details":{
            "document_path1":"text/1234",
            "document_path2":"text/1234",
            "similarity_score":99.16,
            "scoring_algorithm":"default",
            "common_texts":[
                "some other text chunks",
                "some text"
            ]
        }
    }
}

@parser_classes([JSONParser])
@api_view(['GET','POST'])
def call_json(request):
    if request.method == 'POST':
        data = request.data
        print(data.json())
        compareX_input = data.json()
        onlyfiles = [f for f in os.listdir(compareX_input["service_params"]["doc_details"]["document_folderpath"]) if os.path.isfile(os.path.join(compareX_input["service_params"]["doc_details"]["document_folderpath"], f))]
        onlyfiles = [os.path.join(compareX_input["service_params"]["doc_details"]["document_folderpath"],f) for f in onlyfiles]
        file_reader_dict = {}
        if len(onlyfiles)==2:
            for i in  range(1,len(onlyfiles)+1):
                print(i)
                file_reader_dict["file"+str(i)]=(os.path.basename(onlyfiles[i-1]),open(onlyfiles[i-1],'rb'),'text/plain')
        print(file_reader_dict)
        form_data = {
            "key":"scoring_algorithm",
            "value":"elmo",
            "type":"default",
        }
        form_data = {**form_data, **file_reader_dict}
        response = request.post(url,headers=headers, files = form_data)
        response = response.json()
        format_output["job_params"]["ui_id"]=compareX_input["job_params"]["ui_id"]
        format_output["service_params"]["doc_output_details"]["document_path1"]=os.path.dirname(onlyfiles[0])
        format_output["service_params"]["doc_output_details"]["document_path2"]=os.path.dirname(onlyfiles[1])
        format_output["service_params"]["doc_output_details"]["similarity_score"]=response["similarity_score"]
        format_output["service_params"]["doc_output_details"]["scoring_algorithm"]=response["scoring_algorithm"]
        format_output["service_params"]["doc_output_details"]["common_texts"]=response["common_texts"]

        return Response(format_output)
