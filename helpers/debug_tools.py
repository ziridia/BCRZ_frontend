
from os import getenv

def debugPrint(string):
    env = getenv("BCRZ_DEBUG")
    if env and env.lower() == "true":
        print(f"DEBUG: {string}")