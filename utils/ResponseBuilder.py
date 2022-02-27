from datetime import datetime 
def response_builder(protocol, version, status_code, mesage):
    return f'{protocol}/{version} {status_code} - {mesage}\r\n\r\n'

def request_builder_log(method_name, path, status_code):
    return f'{datetime.now()} {method_name} {path} - {status_code}'