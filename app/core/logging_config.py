import logging

import structlog


def setup_logging():
    logging.basicConfig(
        format='%(message)s',
        stream=None,
        level=logging.INFO,
    )

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt='iso'),
            structlog.processors.KeyValueRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
