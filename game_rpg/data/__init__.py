import json
import os


def _load(filename):
    return json.load(
        open(
            os.path.dirname(
                os.path.realpath(__file__)
            ) + "\\" + filename
        )
    )