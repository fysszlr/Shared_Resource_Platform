import json

success_template = {
    "status_code": 200,
    "content": {
        "success": True,
        "code": 0,
        "message": "",
        "data": {}
    }
}

failed_template = {
    "status_code": 404,
    "content": {
        "success": False,
        "code": 100,
        "message": "",
        "data": {}
    }
}

def gen_success_template(message="", data=None):
    ret_template = success_template.copy()
    ret_template["content"]["message"] = message
    ret_template["content"]["data"] = data
    return ret_template

def gen_failed_template(code, message="", data=None):
    ret_template = failed_template.copy()
    ret_template["content"]["code"] = code
    ret_template["content"]["message"] = message
    ret_template["data"] = data
    return ret_template
