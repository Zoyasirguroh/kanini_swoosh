input={
    "job_params":{
        "jobid":"111-33-333-nq_test_new_tiff",
        "service_name":"text_extract"
    },
    "service_params":{
            "doc_input_path_list":[
                {
                    "doc_path":"data/Safee_v4_test/Textxtract/00282B867-0000C512-8132-173CD5662EA9.pdf",
                    "doc_type":"pdf",
                    "doc_output_path":"data/Safee_v4_test/Textxtract"
                }
            ],
            "output_folder":"data/Safee_v4_test/Textxtract",
            "version":"v.10",
            "priority":"10",
            "call_back_url": "http://10.22.243.113.8001/callback",
            "properties":{
                "priority_queue_required":"True",
                "priority_page_count_threshold":"50"
            }
        
    }
}

ack = {
    "job_params":{
        "jobid":"111-33-333-nq_test_new_tiff",
        "taskid":"TXT-2b72aa3f-f8a7-40e4-b615-3d02bd1ecdbb",
        "service_name":"text_extract"
    },
    "service_output":{
        "doc_trace_id_list":[
            {
                "doc_path":"data/Safee_v4_test/Textxtract/00282BB6-0000-C512-8132.pdf",
                "doc_trace_id": "TXD-81b9140a-e64a-be93-2783366697"
            }
            
        ]
    }
    
}

output =  {'job_params': {'jobid': '111-33-333-nq_test_new_tiff',
  'taskid': 'TXT-efcf689f-8671-4552-8a97-ca6b1590e676',
  'service_name': 'text_extract'},
 'service_output': {'status': 'completed',
  'message': 'Task execution completed successfully',
  'safee_output_path': 'data/Safee_v4_test/Textxtract/00282BB6-0000-C512-8132.pdf.json/safee_output',
  'output_path': 'data/Safee_v4_test/Textxtract/00282B86-0000-C512-8132.pdf.json',
  'doc_trace_id_list': [{'doc_path': 'test/1234\\abcde.pdf',
    'doc_trace_id': 'TXD-12143f53-df54-4f3a-ba4d-a4cc6a735bbf',
    'status': 'completed',
    'error_code': 200,
    'error_message': ''},
   {'doc_path': 'test/1234\\abcfg.pdf',
    'doc_trace_id': 'TXD-12143f53-df54-4f3a-ba4d-a4cc6a735bbf',
    'status': 'completed',
    'error_code': 200,
    'error_message': ''},
   {'doc_path': 'test/1234\\abchi.pdf',
    'doc_trace_id': 'TXD-12143f53-df54-4f3a-ba4d-a4cc6a735bbf',
    'status': 'completed',
    'error_code': 200,
    'error_message': ''}]}}