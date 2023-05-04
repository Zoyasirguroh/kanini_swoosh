from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from django.core.files import File
import request
import os
import logging
import configparser
import uuid
import threading
import json
# Create your views here.

logging.basicConfig(level=logging.DEBUG,filename="CompareX_API.log",format="%(asctime)s | %(message)s")
config = configparser.ConfigParser()
config.read(r'property.ini')
url = config["CompareX_DATA"]["URL"]
headers= {}
format_output= {
    "job_params":{
        "user_id":"",
        "middleware_id":"provided by SCB",
    "experiment_id":"comp123456",
    "snapshot_id":"sn1234565",
    "documenttype":"compare_document"
    },
    "service_params":{
        "doc_output_details":{
            "document_path":"data/comp123456/sn1234565/input",
            "document_output_path":"data/comp123456/sn1234565/output",
            "document_name_1":"abc.pdf",
            "document_name_2":"abc.pdf",
            "document_content_1":" ",
            "document_content_2":"",
            "score":"0.003%",
            
        }
    }
}
compare_Ack = {
    "user_id":"",
"experiment_id":"comp123456",
"snapshot_id":"sn1234565",
"documenttype":"compare_document",
"status":"Processing"
}

def compare_processing(compareX_input,jobid,onlyfiles):
    print("compareX_input,jobid--->",compareX_input,jobid)
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
    format_output["job_params"]["user_id"]=jobid
    format_output["job_params"]["middleware_id"]=jobid
    format_output["job_params"]["experiment_id"]=compareX_input["experiment_id"]
    format_output["job_params"]["snapshot_id"]=compareX_input["snapshot_id"]
    format_output["job_params"]["documenttype"]=compareX_input["documenttype"]

    format_output["service_params"]["doc_output_details"]["document_path"]=compareX_input["service_params"]["doc_details"]["document_path"]
    format_output["service_params"]["doc_output_details"]["document_output_path"]=compareX_input["service_params"]["doc_details"]["document_output_path"]
    format_output["service_params"]["doc_output_details"]["score"]=response["similarity_score"]
    format_output["service_params"]["doc_output_details"]["document_name_1"]=compareX_input["service_params"]["doc_details"]["document_name_1"]
    format_output["service_params"]["doc_output_details"]["document_name_1"]=compareX_input["service_params"]["doc_details"]["document_name_2"]
    format_output["service_params"]["doc_output_details"]["document_content_1"]=response["document_content_1"]
    format_output["service_params"]["doc_output_details"]["document_content_2"]=response["document_content_2"]

    
    callback = request.post(compareX_input["callback_url"],data=json.loads(json.dumps(format_output)))
    # callback_response=requests.get(url)
    # print("get callback_response----\n\n",callback_response.json())
    # return JsonResponse(callback_response.json(),safe=False)

    # callback_response = textxtract_json.output
    # return callback_response
@parser_classes([JSONParser])
@api_view(['GET','POST'])
def call_json(request):
    if request.method == 'POST':
        data = request.data
        print(data.json())
        compareX_input = data.json()
        onlyfiles = [os.path.join(compareX_input["service_params"]["doc_details"]["document_path"],compareX_input["service_params"]["doc_details"]["document_name_1"]),os.path.join(compareX_input["service_params"]["doc_details"]["document_path"],compareX_input["service_params"]["doc_details"]["document_name_2"])]
        # onlyfiles = [os.path.join(compareX_input["service_params"]["doc_details"]["document_path"],f) for f in onlyfiles]
        jobid = str(uuid.uuid1())
        for i in onlyfiles:
            print(os.path.isfile(i)) 
            if os.path.isfile(i) == False:
                print(i)
                compare_Ack["user_id"]=jobid
                compare_Ack["experiment_id"]=compareX_input["experiment_id"]
                compare_Ack["snapshot_id"]=compareX_input["snapshot_id"]
                compare_Ack["documenttype"]=compareX_input["documenttype"]
                compare_Ack["status"]="Failed"
                print(compare_Ack)
                return JsonResponse(compare_Ack, status=400)
        compare_Ack["user_id"]=jobid
        compare_Ack["experiment_id"]=compareX_input["experiment_id"]
        compare_Ack["snapshot_id"]=compareX_input["snapshot_id"]
        compare_Ack["documenttype"]=compareX_input["documenttype"]
        compare_Ack["status"]="Processing"
        print(compare_Ack)
        Threading_links = threading.Thread(target=compare_processing, args=(compareX_input,jobid,onlyfiles,)).start()
        return JsonResponse(compare_Ack, status=200)
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
