import subprocess


class CommandTimeout(Exception):
    pass


class InvalidReqTypeException(Exception):
    pass


class InvalidRestVerbException(Exception):
    pass


REST_VERB_TO_REQ_TYPE_MAPPING = {
    "PUT": 0,
    "GET": 1,
    "DELETE": 2,
    "POST": 3,
    "PATCH": 4,
    "OPTIONS": 5
}

EXECUTE_TIMEOUT_SEC = 5

REQ_TYPE_TO_REST_VERB_MAPPING = {v: k for k, v in REST_VERB_TO_REQ_TYPE_MAPPING.items()}


def get_rest_verb_from_req_type(req_type):
    if req_type not in REQ_TYPE_TO_REST_VERB_MAPPING:
        raise InvalidReqTypeException

    return REQ_TYPE_TO_REST_VERB_MAPPING[req_type]


def get_req_type_from_rest_verb(rest_verb):
    if rest_verb not in REST_VERB_TO_REQ_TYPE_MAPPING:
        raise InvalidRestVerbException
    return REST_VERB_TO_REQ_TYPE_MAPPING[rest_verb]


def execute_cmd(command):
    try:
        output = subprocess.check_output(command.split(" "), timeout=EXECUTE_TIMEOUT_SEC)
        res = output.decode('utf-8')
    except subprocess.TimeoutExpired:
        raise CommandTimeout

    return res.strip()
