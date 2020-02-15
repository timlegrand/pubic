import logging


def setup_logger(cli_args):
    logging.basicConfig(
        format="[%(levelname)s] %(message)s",
        level=getattr(logging, cli_args.log_level.upper()))
    logger = logging.getLogger("pubic")
    logger.setLevel(getattr(logging, cli_args.log_level.upper()))
    return logger
