#!/usr/bin/env python3

import datetime
import re
import os
import string
import yaml
from jinja2 import Environment, FileSystemLoader
from jinja_markdown import MarkdownExtension


DIVIDER = "#"*80
SITEMAP_URLS = []
BASE_FOLDER = "./static"

# init the jinja stuff
file_loader = FileSystemLoader("_templates")
env = Environment(loader=file_loader)
env.add_extension(MarkdownExtension)
#env.filters["short_url"] = generate_short_url


# load the context from the metadata file
print(DIVIDER)
print("Loading context")
with open('metadata.yml') as f:
    context = yaml.load(f, Loader=yaml.FullLoader)


# MAIN PAGES
print(DIVIDER)
pages = ["index.html"]
for page in pages:
    with open(BASE_FOLDER + "/" + page, "w") as f:
        print("Generating page:", page)
        template = env.get_template(page)
        f.write(template.render(page=page, **context))

# SITEMAP
print(DIVIDER)
print("Generating sitemap.xml with %d items" % len(SITEMAP_URLS))
now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
with open(BASE_FOLDER + "/sitemap.xml", "w") as f:
    template = env.get_template("sitemap.xml")
    f.write(template.render(urls=SITEMAP_URLS, now=now))
