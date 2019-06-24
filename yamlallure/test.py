from yamlallure.Request import *
from yamlallure.validator import *


data = yaml_load('data2.yml')

casename = data[0]['test']['casename']

req_kwargs = data[0]['test']['request']
resp_obj = send_request(req_kwargs)

expec_obj = data[0]['test']['response']

result = response_validator(resp_obj, expec_obj)
print(casename, result)