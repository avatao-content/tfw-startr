import os

__DEFAULT_WORKDIR = "/tmp/workdir "

STARTER_WORKDIR = os.environ.get("TFW_STARTER_WORKING_DIRECTORY", __DEFAULT_WORKDIR)
