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
    
    current_directory = config['Invoice_DATA']['Cur_dir']
    call_directory = config['Invoice_DATA']['Call_dir']
    create_directory = os.path.join(current_directory, os.path.join(*list_dir_path))
    call_directory = os.path.join(call_directory, os.path.join(*list_dir_path))
    print(create_directory)
    if not os.path.exists(create_directory):
        os.makedirs(create_directory)
    print(call_directory)
    return call_directory
 
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






@parser_classes([JSONParser])
@api_view(['GET','POST'])
def call_json(request):
    if request.method == 'POST':
        inv_input = request.data
        logging.debug("{} |Status of {} : {}".format(inv_input["job_params"]["ui_id"],"Invoice","Request recieved"))  
        txt_input = textxtract_json.input
        safee_input = safe_json.input
        txt_output = textxtract_json.output
        invoice_output=invoice_json.result

        # # txt_ack=Text_extract_flow(url="http://127.0.0.1:5000/textxtract",data_input=txt_input,call_data="")
        # # time.sleep(12)
        # # txt_callback =call_back_api_flow
        # random_page_no = [ i + 1 for i in range(random.randint(3, 8)) ]
        print (uuid.uuid1())
        jobid = str(uuid.uuid1())
        txt_input["job_params"]["jobid"]=jobid
        print(txt_input["job_params"]["jobid"])

        txt_input["service_params"]["output_folder"]= create_path([inv_input["job_params"]["ui_id"],inv_input["job_params"]["documenttype"],txt_input["job_params"]["service_name"]])

        txt_input["service_params"]["doc_input_path_list"] = []

        for i in inv_input["service_params"]["doc_details"]:
            print(i["document_name"])
            # print(os.path.join(i["document_path"],i["document_name"]))
            # feature_extraction_path = create_path([inv_input["job_params"]["ui_id"],inv_input["job_params"]["documenttype"],txt_input["job_params"]["service_name"]])
            # feature_extraction_directory = os.path.join(feature_extraction_path,"FeatureExtraction")
            # if not os.path.exists(feature_extraction_directory):
            #     os.makedirs(feature_extraction_directory)
            # print("feature_extraction_directory",feature_extraction_directory)
            # for randin in random_page_no:
            #     print()
            #     feature_extraction_filename = os.path.basename(i["document_name"])+"_page"+str(randin)+"_feature_extraction.xlsx"
            #     pd.ExcelWriter(os.path.join(feature_extraction_directory,feature_extraction_filename))
            txt_input["service_params"]["doc_input_path_list"].append({
                            "doc_path":os.path.join(i["document_path"],i["document_name"]),
                            "doc_type":"pdf",
                            "doc_output_path":txt_input["service_params"]["output_folder"]
                        })
        print("\n\n\n\n\n TextXtract ACK")

        txt_ack=Text_extract_flow(url=config['Invoice_DATA']['Textextract_url'],data_input=txt_input,call_data="")
        logging.debug("{} |Status of {} : {}".format(txt_input["job_params"]["jobid"],"Textxtract","ACK recieved"))  
        print("\n\n\n\n\n TextXtract Callback")
        txt_output=call_back_api_flow(config['Invoice_DATA']['Textextract_callback_url'])
        print(txt_output)
        logging.debug("{} |Status of {} : {}".format(txt_input["job_params"]["jobid"],"Textxtract","Callback response recieved"))  

        print(txt_output["service_output"]["doc_trace_id_list"])
        # txt_output["service_output"]["doc_trace_id_list"] = []

        # for i in txt_input["service_params"]["doc_input_path_list"]:
        #     print(i["doc_path"])
        #     txt_output["service_output"]["doc_trace_id_list"].append({
        #                 "doc_path":i["doc_path"],
        #                 "doc_trace_id":"TXD-12143f53-df54-4f3a-ba4d-a4cc6a735bbf",
        #                 "status":"completed",
        #                 "error_code":200,
        #                 "error_message":""
        #             })
        safee_input["job_params"]["jobid"]=str(uuid.uuid1())
        print(safee_input["service_params"]["doc_detail_list"])
        safee_input["service_params"]["doc_detail_list"]=[]
        invoice_output_filename = []
        for i in txt_output["service_output"]["doc_trace_id_list"]:
            print(os.path.basename(i["doc_path"]))
            invoice_output_filename.append(os.path.basename(i["doc_path"]))
            feature_extraction_filelist = get_feature_extraction_xl(txt_input['service_params']['doc_input_path_list'][0]['doc_output_path'])
            print(feature_extraction_filelist)
            safee_fet_file = [os.path.basename(string) for string in feature_extraction_filelist if os.path.basename(i["doc_path"]) in string]
            print(safee_fet_file)
            safee_fet_file_path = os.path.dirname(feature_extraction_filelist[0])
            print(safee_fet_file_path)
            safee_output_path = create_path([inv_input["job_params"]["ui_id"],inv_input["job_params"]["documenttype"],safee_input["job_params"]["service"]])
            print(safee_output_path)
            safee_input["service_params"]["doc_detail_list"].append({
                        "doc_output_path":safee_output_path,
                        "doc_file_name":os.path.basename(i["doc_path"]),
                        "fet_input":[
                            {
                                "doc_type":"Invoice",
                                "fet_file_name":safee_fet_file,
                                "fet_file_base_path":safee_fet_file_path
                            }
                        ]
                    })  
            # safe_output_files = [os.path.basename(string) for string in feature_extraction_filelist]
            # for safe_output_file in safe_output_files:
            #     print(os.path.join(safee_output_path,safe_output_file+".txt"))
            #     with open(os.path.join(safee_output_path,safe_output_file+".txt"), 'w') as f:
            #         f.write(json_object)

            invoice_output["service_params"]['doc_output_details']=[]
            print("\n\n\n\n\n TextXtract ACK")
            safee_ack=Text_extract_flow(url=config['Invoice_DATA']['Safee_url'],data_input=safee_input,call_data="")
            logging.debug("{} |Status of {} : {}".format(safee_input["job_params"]["jobid"],"SafeE","ACK recieved"))  
            print("\n\n\n\n\n TextXtract Callback")
            safee_output=call_back_api_flow(config['Invoice_DATA']['Safee_callback_url'])
            logging.debug("{} |Status of {} : {}".format(safee_input["job_params"]["jobid"],"SafeE","Callback response recieved"))  

            for invoice_filename in invoice_output_filename:
                print(invoice_filename)
                invoice_output["service_params"]['doc_output_details'].append({
                "document_path": "test/1234",
                "doc_output_path": "outputpath/",
                "document_name": invoice_filename,
                "pages": [
                    {
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
                ]
            })
        return Response(invoice_output)
