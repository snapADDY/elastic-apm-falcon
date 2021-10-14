# elastic-apm-falcon
Middleware for tracking Falcon requests/responses with Elastic APM.

This package provides a middleware for monitoring [Falcon](https://falconframework.org/)
applications with [Elastic APM](https://www.elastic.co/apm/). The middleware hooks into Falcon's
request and response processing and maintains an Elastic APM client to track transactions and
metadata.

## Installation
You can install the latest stable version from
[PyPI](https://pypi.org/project/elastic-apm-falcon/):

```
$ pip install elastic-apm-falcon
```

## Usage
You can add `elastic_apm_falcon` like any other middleware to your Falcon application. However,
you should make sure to import and instrument `elasticapm` as early as possible.

```python
# import and instrument elasticapm as early as possible
import elasticapm
elasticapm.instrument()

# import remaining modules
import falcon
from elastic_apm_falcon import ElasticApmMiddleware


# initialize Elastic APM middleware
elastic_apm_middleware = ElasticApmMiddleware(service_name="your_service")

# initialize Falcon application
application = falcon.App(middleware=elastic_apm_middleware)

# add routes and resources to your application below
...
```

## License
This package is licensed under the terms of the MIT license.

Made with ♥ at [snapADDY](https://snapaddy.com/).
