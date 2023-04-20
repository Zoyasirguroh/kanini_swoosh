input={
    "job_params":{
        "jobid": "JID-jan101630",
        "service":"safee"
    },
    "service_params":{
        "safee_id": "SAFEE_SWOOSH_001",
        "doc_detail_list":[
            {
                "doc_output_path": "/data/Safee_v4_test/safee_service",
                "doc_file_name":"00282BB6-0000-C512.pdf",
                "fet_input":[
                    {
                        "doc_type":"Invoice",
                        "fet_file_name":[
                            "00282BB6-0000-C512.pdf_page1_feature_extraction.xlsx"
                        ],
                        "fet_file_base_path":"/data/Safee_v4_test/safee_service"
                    }
                ]
            }
        ],
        "version":"v1",
        "priority":"1",
        "call_back_url":"NA",
        "output_folder":"/data/Safee_v4_test/safee_service"
    }
}

ack = {
    "job_params":{
        "jobid":"JID-jan101630",
        "taskid":"SFT-fd7ddc68-7b7f-481d-b9a2-ecb864c22144",
        "service_name":None
    },
    "service_output":{
        "status":"acknowledged",
        "doc_trace_id_list":[
            {
                "doc_file_name":"00282BB-0000-C512-8132-173CD5662EA9.pdf",
                "doc_trace_id":"SFD-83a18c00-a732-43ed-8f7a-0f4d3d781bb3"
            }
        ]
    }
}

output ={
    "job_params":
    {
        "jobid":"JID-jan101630",
        "taskid":"SFT-93f4f6fe-02b9-45bf-a4b5-4132317210e3",
        "service_name":"None"
    },
    "service_output":
    {
        "status":"completed",
        "message":"Task execution completed successfully",
        "safee_id":"SAFEE_SWOOSH_001",
        "doc_trace_id_list":[
            {
                "doc_trace_id":"SFD-fd7ddc68-7350-4da4-afab-b5ce99bafa6b",
                "status":"completed",
                "error_code":"",
                "error_message":"",
                "doc_output_path":"/data/Safee_v4_test/safee_service",
                "safee_output_file":"/data/Safee_v4_test/safee_service"

            }
        ]

    }
}