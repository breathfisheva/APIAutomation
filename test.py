# import requests
# response = requests.post('http://127.0.0.1:7890/api/users/1000', json={'name': 'user1', 'password': '123456'})
#
# print(response)
# resp = requests.get('http://127.0.0.1:7890/api/users/1000')
#
# print(resp.content)


'''
test cases
'''

testcase = {
   "name": "create user which does not exist",
   "request": {
       "url": "http://127.0.0.1:7890/api/users/1000",
       "method": "POST",
       "headers": {
           "content-type": "application/json"
       },
       "json": {
           "name": "user1",
           "password": "123456"
       }
   },
   "response": {
       "status_code": 201,
       "headers": {
           "Content-Type": "application/json"
       },
       "body": {
           "success": True,
           "msg": "user created successfully."
       }
   }
}


'''
common send request and recieve response function
'''
import requests

def run_single_testcase(testcase):
   req_kwargs = testcase['request']

   try:
       url = req_kwargs.pop('url')
       method = req_kwargs.pop('method')
   except KeyError as e:
       raise e.ParamsError("Params Error")

   resp_obj = requests.request(url=url, method=method, **req_kwargs)
   diff_content = diff_response(resp_obj, testcase['response'])
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
    print(run_single_testcase(testcase))