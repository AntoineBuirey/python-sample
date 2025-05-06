from enum import IntEnum

class HttpCode(IntEnum):
    """HTTP status codes, compatible with Flask"""
    # Informational
    CONTINUE = 100                          # continue processing
    SWITCH_PROTOCOL = 101                   # switch protocol
    PROCESSING = 102                        # tell the client that the server is processing the request, but no response is available yet
    EARLY_HINTS = 103                       # allow to start the preloading of resources before the server has finished processing the request

    # Success
    OK = 200                                # request was successful, significant response depends on the method:
                                            # - GET: the resource has been fetched and is transmitted in the message body
                                            # - HEAD: the entity headers are in the message body
                                            # - PUt & POST: the result of the action is transmitted in the message body
                                            # - TRACE: the message body contains the request message as received by the server
    CREATED = 201                           # request was successful and a new resource was created (Usually for POST and PUT requests)
    ACCEPTED = 202                          # request was accepted for processing, but the processing has not been completed
    NON_AUTHORITATIVE_INFORMATION = 203     # request was successful, but the returned information is from a third-party source
    NO_CONTENT = 204                        # request was successful, but no content is returned (headers may still be useful)
    RESET_CONTENT = 205                     # request was successful, but the client should reset the document view
    PARTIAL_CONTENT = 206                   # request was successful, but only a part of the resource is returned (used for range requests)
    MULTI_STATUS = 207                      # used in WebDAV to provide information about multiple resources in a single response
    ALREADY_REPORTED = 208                  # used in WebDAV to indicate that the members of a collection have already been reported in a previous response
    IM_USED = 226                           # indicates that the server is returning a delta in response to a GET request. It is used in the context of HTTP delta encodings

    # Redirection
    MULTIPLE_CHOICES = 300                  # client must take additional action to complete the request
    MOVED_PERMANENTLY = 301                 # resource has been moved permanently to a new location
    FOUND = 302                             # resource has been found, but the location has been temporarily moved
    SEE_OTHER = 303                         # resource can be found under a different URI and should be retrieved using a GET method
    NOT_MODIFIED = 304                      # resource has not been modified since the last request, and the client should use the cached copy
    TEMPORARY_REDIRECT = 307                # resource has been temporarily moved to another URI, but the client should continue to use same method to access it
    PERMANENT_REDIRECT = 308                # resource has been permanently moved to another URI, and the client should use the new URI for all future requests

    # Client Error
    BAD_REQUEST = 400                       # server could not understand the request due to invalid syntax
    UNAUTHORIZED = 401                      # client must authenticate itself to get the requested response
    PAYMENT_REQUIRED = 402                  # nonstandard response status code reserved for future use.
    FORBIDDEN = 403                         # client does not have permission to access the requested resource
    NOT_FOUND = 404                         # server cannot find the requested resource. (May be used to hide the existence of a resource; in this case, it replace 403 Forbidden)
    METHOD_NOT_ALLOWED = 405                # request method is not supported for the requested resource
    NOT_ACCEPTABLE = 406                    # server cannot generate a response that the client will accept
    PROXY_AUTHENTICATION_REQUIRED = 407     # client must authenticate itself with the proxy (similar to 401 Unauthorized)
    REQUEST_TIMEOUT = 408                   # server timed out waiting for the request
    CONFLICT = 409                          # request could not be processed because of conflict in the request
    GONE = 410                              # requested resource is no longer available and will not be available again
    LENGTH_REQUIRED = 411                   # server requires a content-length header
    PRECONDITION_FAILED = 412               # one or more conditions in the request header fields evaluated to false
    PAYLOAD_TOO_LARGE = 413                 # request is larger than the server is willing or able to process
    URI_TOO_LONG = 414                      # request URI is longer than the server is willing to interpret
    UNSUPPORTED_MEDIA_TYPE = 415            # request entity has a media type which the server or resource does not support
    RANGE_NOT_SATISFIABLE = 416             # server cannot provide the requested range (used in range requests)
    EXPECTATION_FAILED = 417                # expectation given in the request's Expect header field cannot be met by the server
    IM_A_TEAPOT = 418                       # server refuses to brew coffee because it is a teapot
    MISDIRECTED_REQUEST = 421               # request was directed at a server that is not able to produce a response (e.g., due to connection reuse)
    UNPROCESSABLE_CONTENT = 422             # request was well-formed, but was unable to be followed due to semantic errors
    LOCKED = 423                            # resource that is being accessed is locked
    FAILED_DEPENDENCY = 424                 # request failed due to failure of a previous request (used in WebDAV)
#   TOO_EARLY = 425                         # server is unwilling to risk processing a request that might be replayed (firefox only)
    UPGRADE_REQUIRED = 426                  # client should switch to a different protocol (e.g., TLS/1.0)
    PRECONDITION_REQUIRED = 428             # origin server requires the request to be conditional (used in WebDAV)
    TOO_MANY_REQUESTS = 429                 # client has sent too many requests in a given amount of time
    REQUEST_HEADER_FIELDS_TOO_LARGE = 431   # server is unwilling to process the request because its header fields are too large
    UNAVAILABLE_FOR_LEGAL_REASONS = 451      # resource is unavailable for legal reasons (e.g., censorship)

    # Server Error
    INTERNAL_SERVER_ERROR = 500             # server has encountered a situation it doesn't know how to handle (only if no other error code applies)
    NOT_IMPLEMENTED = 501                   # request method is not supported by the server and cannot be handled
    BAD_GATEWAY = 502                       # server, while acting as a gateway or proxy, received an invalid response from the upstream server
    SERVICE_UNAVAILABLE = 503               # server is not ready to handle the request (commonly used for maintenance)
    GATEWAY_TIMEOUT = 504                   # server is acting as a gateway and cannot get a response in time from the upstream server
    HTTP_VERSION_NOT_SUPPORTED = 505        # server does not support the HTTP protocol version used in the request
    VARIANT_ALSO_NEGOTIATES = 506           # server has an internal configuration error: transparent content negotiation for the request results in a circular reference
    INSUFFICIENT_STORAGE = 507              # server is unable to store the representation needed to complete the request
    LOOP_DETECTED = 508                     # server detected an infinite loop while processing a request (used in WebDAV)
    NOT_EXTENDED = 510                      # server requires further extensions to fulfill the request
    NETWORK_AUTHENTICATION_REQUIRED = 511   # client needs to authenticate to gain network access (used in captive portals)

    def label(self) -> str:
        """
        Get the label of the HTTP status code.
        :return: Label of the HTTP status code.
        """
        return self.name.replace('_', ' ').title()

    def __str__(self) -> str:
        """
        Get the string representation of the HTTP status code.
        :return: String representation of the HTTP status code.
        """
        return f"{self.value} {self.label()}"
