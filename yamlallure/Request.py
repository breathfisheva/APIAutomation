import requests
from yamlallure.loader import *

def send_request(req_kwargs):
    try:
        url = req_kwargs.pop('url')
        method = req_kwargs.pop('method')
    except KeyError as e:
        raise e.ParamsError("Params Error")

    resp_obj = requests.request(url=url, method=method, **req_kwargs)
    return resp_obj


if __name__ == '__main__':
    data = yaml_load('data.yml')
    req_kwargs = data[0]['test']['request']
    response = send_request(req_kwargs)

    print(response)

