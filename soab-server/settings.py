import os

PORT = 8080

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
DATABASE = "sqlite:////" + PROJECT_ROOT + "/soab.sqlite"
