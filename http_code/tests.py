from http_code import HttpCode
import pytest


@pytest.mark.parametrize(
    "code, expected_name, expected_label",
    [
        (HttpCode.CONTINUE, "CONTINUE", "Continue"),
        (HttpCode.SWITCH_PROTOCOL, "SWITCH_PROTOCOL", "Switch Protocol"),
        (HttpCode.PROCESSING, "PROCESSING", "Processing"),
        (HttpCode.EARLY_HINTS, "EARLY_HINTS", "Early Hints"),
    ],
    ids=[
        "100 Continue",
        "101 Switch Protocol",
        "102 Processing",
        "103 Early Hints",
    ]
)
def test_informational_codes(code, expected_name, expected_label):
    """Test informational HTTP status codes"""
    assert code == getattr(HttpCode, expected_name)
    assert code.label() == expected_label
    assert str(code) == f"{code.value} {expected_label}"
    

@pytest.mark.parametrize(
    "code, expected_name, expected_label",
    [
        (HttpCode.OK, "OK", "Ok"),
        (HttpCode.CREATED, "CREATED", "Created"),
        (HttpCode.ACCEPTED, "ACCEPTED", "Accepted"),
        (HttpCode.NON_AUTHORITATIVE_INFORMATION, "NON_AUTHORITATIVE_INFORMATION", "Non Authoritative Information"),
        (HttpCode.NO_CONTENT, "NO_CONTENT", "No Content"),
        (HttpCode.RESET_CONTENT, "RESET_CONTENT", "Reset Content"),
        (HttpCode.PARTIAL_CONTENT, "PARTIAL_CONTENT", "Partial Content"),
        (HttpCode.MULTI_STATUS, "MULTI_STATUS", "Multi Status"),
        (HttpCode.ALREADY_REPORTED, "ALREADY_REPORTED", "Already Reported"),
        (HttpCode.IM_USED, "IM_USED", "Im Used"),
    ],
    ids=[
        "200 OK",
        "201 Created",
        "202 Accepted",
        "203 Non-Authoritative Information",
        "204 No Content",
        "205 Reset Content",
        "206 Partial Content",
        "207 Multi-Status",
        "208 Already Reported",
        "226 IM Used",
    ]
)
def test_success_codes(code, expected_name, expected_label):
    """Test informational HTTP status codes"""
    assert code == getattr(HttpCode, expected_name)
    assert code.label() == expected_label
    assert str(code) == f"{code.value} {expected_label}"


@pytest.mark.parametrize(
    "code, expected_name, expected_label",
    [
        (HttpCode.MULTIPLE_CHOICES, "MULTIPLE_CHOICES", "Multiple Choices"),
        (HttpCode.MOVED_PERMANENTLY, "MOVED_PERMANENTLY", "Moved Permanently"),
        (HttpCode.FOUND, "FOUND", "Found"),
        (HttpCode.SEE_OTHER, "SEE_OTHER", "See Other"),
        (HttpCode.NOT_MODIFIED, "NOT_MODIFIED", "Not Modified"),
        (HttpCode.TEMPORARY_REDIRECT, "TEMPORARY_REDIRECT", "Temporary Redirect"),
        (HttpCode.PERMANENT_REDIRECT, "PERMANENT_REDIRECT", "Permanent Redirect"),
    ],
    ids=[
        "300 Multiple Choices",
        "301 Moved Permanently",
        "302 Found",
        "303 See Other",
        "304 Not Modified",
        "307 Temporary Redirect",
        "308 Permanent Redirect",
    ]
)
def test_redirection_codes(code, expected_name, expected_label):
    """Test redirection HTTP status codes"""
    assert code == getattr(HttpCode, expected_name)
    assert code.label() == expected_label
    assert str(code) == f"{code.value} {expected_label}"
    

@pytest.mark.parametrize(
    "code, expected_name, expected_label",
    [
        (HttpCode.BAD_REQUEST, "BAD_REQUEST", "Bad Request"),
        (HttpCode.UNAUTHORIZED, "UNAUTHORIZED", "Unauthorized"),
        (HttpCode.PAYMENT_REQUIRED, "PAYMENT_REQUIRED", "Payment Required"),
        (HttpCode.FORBIDDEN, "FORBIDDEN", "Forbidden"),
        (HttpCode.NOT_FOUND, "NOT_FOUND", "Not Found"),
        (HttpCode.METHOD_NOT_ALLOWED, "METHOD_NOT_ALLOWED", "Method Not Allowed"),
        (HttpCode.NOT_ACCEPTABLE, "NOT_ACCEPTABLE", "Not Acceptable"),
        (HttpCode.PROXY_AUTHENTICATION_REQUIRED, "PROXY_AUTHENTICATION_REQUIRED", "Proxy Authentication Required"),
        (HttpCode.REQUEST_TIMEOUT, "REQUEST_TIMEOUT", "Request Timeout"),
        (HttpCode.CONFLICT, "CONFLICT", "Conflict"),
        (HttpCode.GONE, "GONE", "Gone"),
        (HttpCode.LENGTH_REQUIRED, "LENGTH_REQUIRED", "Length Required"),
        (HttpCode.PRECONDITION_FAILED, "PRECONDITION_FAILED", "Precondition Failed"),
        (HttpCode.PAYLOAD_TOO_LARGE, "PAYLOAD_TOO_LARGE", "Payload Too Large"),
        (HttpCode.URI_TOO_LONG, "URI_TOO_LONG", "Uri Too Long"),
        (HttpCode.UNSUPPORTED_MEDIA_TYPE, "UNSUPPORTED_MEDIA_TYPE", "Unsupported Media Type"),
        (HttpCode.RANGE_NOT_SATISFIABLE, "RANGE_NOT_SATISFIABLE", "Range Not Satisfiable"),
        (HttpCode.EXPECTATION_FAILED, "EXPECTATION_FAILED", "Expectation Failed"),
        (HttpCode.IM_A_TEAPOT, 'IM_A_TEAPOT', 'Im A Teapot'),  # RFC 7168
        (HttpCode.MISDIRECTED_REQUEST, 'MISDIRECTED_REQUEST', 'Misdirected Request'),
        (HttpCode.UNPROCESSABLE_CONTENT, 'UNPROCESSABLE_CONTENT', 'Unprocessable Content'),
        (HttpCode.LOCKED, 'LOCKED', 'Locked'),
        (HttpCode.FAILED_DEPENDENCY, 'FAILED_DEPENDENCY', 'Failed Dependency'),
    ],
    ids=[
        "400 Bad Request",
        "401 Unauthorized",
        "402 Payment Required",
        "403 Forbidden",
        "404 Not Found",
        "405 Method",
        "406 Not Acceptable",
        "407 Proxy Authentication Required",
        "408 Request Timeout",
        "409 Conflict",
        "410 Gone",
        "411 Length Required",
        "412 Precondition Failed",
        "413 Payload Too Large",
        "414 URI Too Long",
        "415 Unsupported Media Type",
        "416 Range Not Satisfiable",
        "417 Expectation failed",
        "418 Im A Teapot",
        "421 Misdirected Request",
        "422 Unprocessable Content",
        "423 Locked",
        "424 Failed Dependency"
    ]
)
def test_client_error_codes(code, expected_name, expected_label):
    """Test client error HTTP status codes"""
    assert code == getattr(HttpCode, expected_name)
    assert code.label() == expected_label
    assert str(code) == f"{code.value} {expected_label}"


@pytest.mark.parametrize(
    "code, expected_name, expected_label",
    [
        (HttpCode.INTERNAL_SERVER_ERROR, "INTERNAL_SERVER_ERROR", "Internal Server Error"),
        (HttpCode.NOT_IMPLEMENTED, "NOT_IMPLEMENTED", "Not Implemented"),
        (HttpCode.BAD_GATEWAY, "BAD_GATEWAY", "Bad Gateway"),
        (HttpCode.SERVICE_UNAVAILABLE, "SERVICE_UNAVAILABLE", "Service Unavailable"),
        (HttpCode.GATEWAY_TIMEOUT, "GATEWAY_TIMEOUT", "Gateway Timeout"),
        (HttpCode.HTTP_VERSION_NOT_SUPPORTED, "HTTP_VERSION_NOT_SUPPORTED", "Http Version Not Supported"),
        (HttpCode.VARIANT_ALSO_NEGOTIATES, "VARIANT_ALSO_NEGOTIATES", "Variant Also Negotiates"),
        (HttpCode.INSUFFICIENT_STORAGE, "INSUFFICIENT_STORAGE", "Insufficient Storage"),
        (HttpCode.LOOP_DETECTED, "LOOP_DETECTED", "Loop Detected"),
        (HttpCode.NOT_EXTENDED, "NOT_EXTENDED", "Not Extended"),
        (HttpCode.NETWORK_AUTHENTICATION_REQUIRED, 'NETWORK_AUTHENTICATION_REQUIRED', 'Network Authentication Required'),
    ],
    ids=[
        "500 Internal Server Error",
        "501 Not Implemented",
        "502 Bad Gateway",
        "503 Service Unavailable",
        "504 Gateway Timeout",
        "505 Http Version Not Supported",
        "506 Variant Also Negotiates",
        "507 Insufficient Storage",
        "508 Loop Detected",
        "510 Not Extended",
        '511 Network Authentication Required'
    ]
)
def test_server_error_codes(code, expected_name, expected_label):
    """Test server error HTTP status codes"""
    assert code == getattr(HttpCode, expected_name)
    assert code.label() == expected_label
    assert str(code) == f"{code.value} {expected_label}"
