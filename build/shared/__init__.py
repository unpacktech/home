import yaml
from jinja2 import Environment, FileSystemLoader


DIVIDER = "#"*80
BASE_FOLDER = "./static"
CONTENT_FOLDER = "./content"

def get_jinja_env():
    file_loader = FileSystemLoader("_templates")
    env = Environment(loader=file_loader)
    return env

def get_context():
    with open('metadata.yml') as f:
        context = yaml.load(f, Loader=yaml.FullLoader)
        return context
