import elasticapm
from elasticapm.utils.disttracing import TraceParent
from falcon import HTTP_INTERNAL_SERVER_ERROR, Request, Response
from falcon import __version__ as falcon_version

from elastic_apm_falcon.utils import get_data_from_request, get_data_from_response


class ElasticApmMiddleware:
    """Middleware for tracking requests in Elastic APM."""

    def __init__(self, **config):
        # add framework name and version if missing
        if "framework_name" not in config:
            config["framework_name"] = "falcon"
            config["framework_version"] = falcon_version

        # create APM client
        self.client = elasticapm.Client(**config)

    def process_request(self, req: Request, resp: Response):
        if not self.client.should_ignore_url(req.path):
            trace_parent = TraceParent.from_headers(req.headers)

            # begin APM transaction
            self.client.begin_transaction("request", trace_parent=trace_parent)

            # provide request data as callable (so it is only called if the request is sampled)
            elasticapm.set_context(lambda: get_data_from_request(req), "request")

    def process_response(self, req: Request, resp: Response, resource, req_succeeded: bool):
        # the result of the transaction is the HTTP status code
        transaction_result = resp.status

        # if request did not succeed, set result to internal server error
        if not req_succeeded:
            transaction_result = HTTP_INTERNAL_SERVER_ERROR

        # provide response data as callable (so it is only called if the request is sampled)
        elasticapm.set_context(lambda: get_data_from_response(resp), "response")

        # end APM transaction
        self.client.end_transaction(" ".join((req.method, req.path)), transaction_result)
