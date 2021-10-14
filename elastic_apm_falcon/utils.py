from elasticapm.utils import get_url_dict
from falcon import Request, Response


def get_data_from_request(request: Request) -> dict:
    """Collect relevant information from a Falcon request.

    Parameters
    ----------
    request : Request
        The Falcon request object to get information from.

    Returns
    -------
    dict
        The gathered information.
    """
    # collect relevant information from the request
    data = {
        "headers": request.headers,
        "method": request.method,
        "socket": {"remote_address": request.remote_addr, "encrypted": request.scheme == "https"},
        "cookies": request.cookies,
        "url": get_url_dict(request.url),
        "forwarded_uri": request.forwarded_uri,
    }

    # remove Cookie header since the same data is in request["cookies"] as well
    data["headers"].pop("Cookie", None)

    return data


def get_data_from_response(response: Response) -> dict:
    """Collect relevant information from a Falcon response.

    Parameters
    ----------
    response : Response
        The Falcon response object to get information from.

    Returns
    -------
    dict
        The gathered information.
    """
    # collect relevant information from the response
    return {"status_code": response.status, "headers": response.headers}
