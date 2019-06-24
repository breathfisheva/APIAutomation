
from yamlallure.loader import *

def response_validator(resp_obj, expec_obj):

    diff_content = diff_response(resp_obj, expec_obj)
    success = False if diff_content else True
    return success, diff_content


'''
function to analyse the response with expected result
'''

def parse_response_object(resp_obj):
    try:
        resp_body = resp_obj.json()
    except ValueError:
        resp_body = resp_obj.text

    return {
        'status_code': resp_obj.status_code,
        'headers': resp_obj.headers,
        'body': resp_body
    }


def diff_response(resp_obj, expected_resp_json):
    diff_content = {}
    resp_info = parse_response_object(resp_obj)
    for key, expected_value in expected_resp_json.items():
        value = resp_info.get(key, None)
        if str(value)!= str(expected_value):
            diff_content[key] = {
                'value': value,
                'expected': expected_value
            }
    return diff_content


if __name__ == '__main__':
    from yamlallure.Request import *
    data = yaml_load('data2.yml')

    req_kwargs = data[0]['test']['request']
    resp_obj = send_request(req_kwargs)

    expec_obj =  data[0]['test']['response']

    result = response_validator(resp_obj, expec_obj)
    print(result)



