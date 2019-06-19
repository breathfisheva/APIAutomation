# import importlib
# import types
#
# def is_function(tup):
#     """ Takes (name, object) tuple, returns True if it is a function.
#     """
#     name, item = tup
#     return isinstance(item, types.FunctionType)
#
# def dynamic_import(module):
#     return importlib.import_module(module)
#
# def import_module_functions(module):
#
#    imported = importlib.import_module(module)
#    imported_functions_dict = dict(filter(is_function, vars(imported).items()))
#    return imported_functions_dict
#
#
# if __name__ == "__main__":
#     module = import_module_functions('foo')
#     print(vars(module))
#     module.fun1()
#     module.fun2()
#

import re
# regex = r"^\$\{(\w+)\((.*)\)\}$"
# regex2 = r"^\$\{(\w+)\(([\$\w =,]*)\)\}$"  #匹配参数部分的时候是采用.*的形式，也就是任意字符匹配，匹配的方式不是很严谨。考虑到正常的函数参数部分可能使用到的字符，我们可以采用如下更严谨的正则表达式。
# matched = re.match(regex, string="${func(3,a=1)}")
# print(matched.group(1))
# print(matched.group(2))

import ast
def parse_string_value(str_value):
    """ parse string to number if possible
    e.g. "123" => 123
         "12.2" => 12.3
         "abc" => "abc"
         "$var" => "$var"
    """
    try:
        return ast.literal_eval(str_value)
    except ValueError:
        return str_value
    except SyntaxError:
        # e.g. $var, ${func}
        return str_value

#handle function
function_regexp = re.compile(r"^\$\{(\w+)\(([\$\w =,]*)\)\}$")

def is_functon(content):
    matched = function_regexp.match(content)
    return True if matched else False

def parse_function(content):
    function_meta = {
        "args": [],
        "kwargs": {}
    }
    matched = function_regexp.match(content)
    function_meta["func_name"] = matched.group(1)

    args_str = matched.group(2).replace(" ", "")
    if args_str == "":
        return function_meta

    args_list = args_str.split(',')
    for arg in args_list:
        if '=' in arg:
            key, value = arg.split('=')
            function_meta["kwargs"][key] = parse_string_value(value)
        else:
            function_meta["args"].append(parse_string_value(arg))

    return function_meta

#handle variable
variable_regex = re.compile(r"\$(\w+)")
def is_variable(content):
    matched = variable_regex.match(content)
    return True if matched else False

def parse_variable(content):
    matched = variable_regex.match(content)
    var = matched.group(1)
    return var

testcase_variables_mapping = {
                "varA": "1234563",
                "varB": "4563",
                "varC": "3",
                "a": 1,
                "b": 2,
                "c": {"key": 2},
                "d": [1, 3]
            }

def get_eval_value(data):
   """ evaluate data recursively, each variable in data will be evaluated.
   """
   if isinstance(data, (list, tuple)):
       return [get_eval_value(item) for item in data]

   if isinstance(data, dict):
       evaluated_data = {}
       for key, value in data.items():
           evaluated_data[key] = get_eval_value(value)

       return evaluated_data

   if isinstance(data, (int, float)):
       return data

   # data is in string format here
   data = "" if data is None else data.strip()
   if is_variable(data):
       # variable marker: $var
       variable_name = parse_variable(data)
       value = testcase_variables_mapping[variable_name]
       if value is None:
           print( "%s is not defined in bind variables!" % variable_name)
           # raise exception.ParamsError(
           #     "%s is not defined in bind variables!" % variable_name)
       return value

   elif is_functon(data):
       # function marker: ${func(1, 2, a=3, b=4)}
       fuction_meta = parse_function(data)
       func_name = fuction_meta['func_name']
       args = fuction_meta.get('args', [])
       kwargs = fuction_meta.get('kwargs', {})
       args = get_eval_value(args)
       kwargs = get_eval_value(kwargs)
       # return testcase_config["functions"][func_name](*args, **kwargs)
       print(func_name, args, kwargs)
   else:
       return data

get_eval_value("$varA")