from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from . import invoice_json
from . import textxtract_json
from . import safe_json
import requests
import time
import pandas as pd
import os
import random
import json
import logging
import configparser
import uuid
import threading


logging.basicConfig(level=logging.DEBUG,filename="Invoice_API.log",format="%(asctime)s | %(message)s")
config = configparser.ConfigParser()
config.read(r'property.ini')
def get_feature_extraction_xl(path):
    fname = []
    for root,d_names,f_names in os.walk(path):
        if 'FeatureExtraction' in root:
            for f in f_names:
                fname.append(os.path.join(root, f))
    return fname

def create_path(list_dir_path):
    
    # create_directory = os.path.join(os.getcwd(), os.path.join(*list_dir_path))
    create_directory = os.path.join(os.path.join(*list_dir_path))
    if not os.path.exists(create_directory):
        os.makedirs(create_directory)
    return create_directory
 
def call_back_api_flow(url):
    # str("http://127.0.0.1:5000/callback")
    # time.sleep(12)
    print("URL--->",url)
    # callback_response=requests.get(url)
    # print("get callback_response----\n\n",callback_response.json())
    # return JsonResponse(callback_response.json(),safe=False)

    callback_response = textxtract_json.output
    return callback_response


def Text_extract_flow(url="",data_input="",call_data=""):
    print("url--->",url)
    print("data_input--->",data_input)
    print("call_data--->",call_data)
    # text_extract_response_value=requests.post(str(url))
    # print(text_extract_response_value)
    # text_extract_ack=text_extract_response_value.json()
    # print(text_extract_response_value.status_code==200)
    text_extract_ack = textxtract_json.ack

    return text_extract_ack
extracted_data = {
                        "document_fields": [
                            {
                                "key_name": "Date",
                                "key_value": "12/3/2022",
                                "field_cordinates": [
                                    {
                                        "cordinates": [
                                            "1",
                                            "2",
                                            "3",
                                            "345"
                                        ]
                                    },
                                    {
                                        "cordinates": [
                                            "11",
                                            "22",
                                            "33",
                                            "35"
                                        ]
                                    }
                                ],
                                "confidence_score": "90"
                            },
                            {
                                "key_name": "Date",
                                "key_value": "12/3/2022",
                                "field_cordinates": [
                                    {
                                        "cordinates": [
                                            "1",
                                            "2",
                                            "3",
                                            "345"
                                        ]
                                    },
                                    {
                                        "cordinates": [
                                            "11",
                                            "22",
                                            "33",
                                            "35"
                                        ]
                                    }
                                ],
                                "confidence_score": "90"
                            }
                        ]
                    }
json_object = json.dumps(extracted_data, indent=4)

def invoice_processing(inv_inp_json):
    txt_input = textxtract_json.input
    safee_input = safe_json.input
    txt_output = textxtract_json.output
    invoice_output=invoice_json.result
    print (uuid.uuid1())
    jobid_text_safe = str(uuid.uuid1())
    invoice_output_filename = []

    for i in inv_inp_json["service_params"]["doc_details"]:
        text_output_path = create_path(["data",inv_inp_json["experiment_id"],inv_inp_json["snapshot_id"],"input",jobid,i["document_name"],"textXtract"])
        txt_input["job_params"]["jobid"]=jobid_text_safe
        txt_input["service_params"]["doc_input_path_list"][0]["doc_path"] = os.path.join(i["document_path"],i["document_name"])
        txt_input["service_params"]["doc_input_path_list"][0]["doc_output_path"] = text_output_path
        txt_input["service_params"]["output_folder"]= text_output_path
        txt_input["service_params"]["doc_input_path_list"][0]["doc_type"] = os.path.splitext(i["document_name"])[1].replace('.', '')
        txt_ack=Text_extract_flow(url=config['Invoice_DATA']['Textextract_url'],data_input=txt_input,call_data="")
        logging.debug("{} |Status of {} : {}".format(txt_input["job_params"]["jobid"],"Textxtract","ACK recieved"))  
        print("\n\n\n\n\n TextXtract Callback")
        txt_output=call_back_api_flow(config['Invoice_DATA']['Textextract_callback_url'])
        print(txt_output)
        logging.debug("{} |Status of {} : {}".format(txt_input["job_params"]["jobid"],"Textxtract","Callback response recieved"))  

        print(txt_output["service_output"]["doc_trace_id_list"])
        safee_input["job_params"]["jobid"]=jobid_text_safe
        safee_input["service_params"]["doc_detail_list"][0]["doc_output_path"]= create_path(["data",inv_inp_json["experiment_id"],inv_inp_json["snapshot_id"],"input",jobid,i["document_name"],"SafeE"])
        safee_input["service_params"]["doc_detail_list"][0]["doc_file_name"]=i["document_name"]
        feature_extraction_filelist = get_feature_extraction_xl(text_output_path)
        safee_fet_file = [os.path.basename(string) for string in feature_extraction_filelist if os.path.basename(txt_input["service_params"]["doc_input_path_list"][0]["doc_path"]) in string]
        safee_fet_file_path = os.path.dirname(feature_extraction_filelist[0])
        safee_input["service_params"]["doc_detail_list"][0]["fet_input"][0]["fet_file_name"]=safee_fet_file
        safee_input["service_params"]["doc_detail_list"][0]["fet_input"][0]["fet_file_base_path"]=safee_fet_file_path
        safee_input["service_params"]["output_folder"]=safee_fet_file_path

        invoice_output_filename.append(os.path.basename(txt_input["service_params"]["doc_input_path_list"][0]["doc_path"]))
        print(json.dumps(safee_input,sort_keys=False, indent=4))
        safee_ack=Text_extract_flow(url=config['Invoice_DATA']['Safee_url'],data_input=safee_input,call_data="")
        logging.debug("{} |Status of {} : {}".format(safee_input["job_params"]["jobid"],"SafeE","ACK recieved"))  
        print("\n\n\n\n\n SAFEE Callback")
        safee_output=call_back_api_flow(config['Invoice_DATA']['Safee_callback_url'])
        logging.debug("{} |Status of {} : {}".format(safee_input["job_params"]["jobid"],"SafeE","Callback response recieved"))  
    safe_output_files = [os.path.basename(string) for string in feature_extraction_filelist]
    print(safe_output_files)
    print(invoice_output_filename)

    document  = {
                    "document_path": "test/1234",
                    "doc_output_path": "outputpath/",
                    "document_name": "abc.pdf",
                    "pages": [
                        {
                            "document_fields": []}]}
    print(document["pages"][0]["document_fields"])
    for file in invoice_output_filename:
        
        for root,d_names,f_names in os.walk(safee_input["service_params"]["doc_detail_list"][0]["doc_output_path"]):
        #     if 'FeatureExtraction' in root:
            print(root)
            document[ "document_path"]=root
            document[ "doc_output_path"]=root
            
            for f in f_names:
                if file in f:
                    document[ "document_name"]=f
                    print("\n\n\n\n\n\ndocument----->",document)
                    print("\n\n\n\ndocument\n\n\n\n",document["pages"])
                    with open(os.path.join(root, f) , 'r') as myfile:
                        data=myfile.read()
                        extracted_data = json.loads(data)
    #                     print(extracted_data)
                        doc=[]
                        document_fields={}
                        for i in extracted_data["entityExtraction"]:
                            if len(i["values"])!=0:
    #                             print(i["values"])

                                document_fields["key_name"]=i["name"]
                                document_fields["key_value"]=i["values"][0]["value"]

                                document_fields["field_cordinates"]=[]
                                for value in i["values"]:
                                    document_fields["field_cordinates"].append({'cordinates':value["coordinates"][0]})
                                    document_fields["confidence_score"] = value["score"][0]
                                doc.append(document_fields.copy())
                                print("\n\n\ndoc\n\n\n\n",doc)
                                document["pages"][0]["document_fields"] = doc.copy()
                                print("\n\n\ndocument\n\n\n\n",document)
            print("invoice+++++++++++\n\n\n\n\n",invoice_output["service_params"]["doc_output_details"])
            invoice_output["service_params"]["doc_output_details"].append(document["pages"][0]["document_fields"])
                    
    print(invoice_output)
    invoice_output_object = json.dumps(invoice_output, indent=4)

    print(os.path.join(create_path(["data",inv_inp_json["experiment_id"],inv_inp_json["snapshot_id"],"output"]),inv_inp_json["experiment_id"]+"_output.json"))
    with open(os.path.join(create_path(["data",inv_inp_json["experiment_id"],inv_inp_json["snapshot_id"],"output"]),inv_inp_json["experiment_id"]+"_output.json"), 'w') as f:
        f.write(invoice_output_object)
    return {}





@parser_classes([JSONParser])
@api_view(['GET','POST'])
def call_json(request):
    if request.method == 'POST':
        inv_inp_json = request.data
        logging.debug("{} |Status of {} : {}".format(inv_inp_json["job_params"]["ui_id"],"Invoice","Request recieved"))  
        jobid = str(uuid.uuid1())

        for i in inv_inp_json["service_params"]["doc_details"]:
            check_file_type=os.path.join(i["document_path"],i["document_name"]).lower().endswith(tuple(config["Invoice_DATA"]["filetype"]))
            check_file = os.path.isfile(os.path.join(i["document_path"],i["document_name"]))
            if not (check_file and check_file_type):
                 print({'status':'false','jobid':jobid})
            return JsonResponse({'status':'false','jobid':jobid}, status=400)
        else:
            print({'status':'true','jobid':jobid})
            Threading_links = threading.Thread(target=invoice_processing, args=(inv_inp_json,)).start()
            return JsonResponse({'status':'true','jobid':jobid}, status=200)
            
        #return Response(invoice_output)
