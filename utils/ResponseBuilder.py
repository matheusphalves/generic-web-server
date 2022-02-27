def response_builder(protocol, version, status_code, mesage):
    return f'{protocol}/{version} {status_code} - {mesage}\r\n\r\n'