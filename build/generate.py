import datetime
import json
import glob
from shared import *


SITEMAP_URLS = []
ENV = get_jinja_env()
CONTEXT = get_context()


# MAIN PAGES
print(DIVIDER)
pages = ["index.html"]
for page in pages:
    with open(f"{BASE_FOLDER}/{page}", "w") as f:
        print("Generating page:", page)
        template = ENV.get_template(page)
        f.write(template.render(page=page, **CONTEXT))

# DAILY ITEMS
print(DIVIDER)
files = glob.glob(f"./{CONTENT_FOLDER}/*.json")
for file in files:
    with open(file, "r") as f:
        content = f.read()
    parsed = json.loads(content)
    date = parsed.get("date").replace("/", "-")
    permalink = f"https://unpack.tech/{date}"
    # write the regular version for browsing
    for path, template, publish in [
        [f"{BASE_FOLDER}/{date}.html", "daily.html", True],
        [f"{BASE_FOLDER}/{date}-email.html", "email.html", False],
    ]:
        with open(path, "w") as f:
            template = ENV.get_template(template)
            f.write(template.render(page=page, content=parsed, permalink=permalink, **CONTEXT))
            print("Generated", path)
            if publish:
                SITEMAP_URLS.append((path, 0.7))

# SITEMAP
print(DIVIDER)
print("Generating sitemap.xml with %d items" % len(SITEMAP_URLS))
now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
with open(f"{BASE_FOLDER}/sitemap.xml", "w") as f:
    template = ENV.get_template("sitemap.xml")
    f.write(template.render(urls=SITEMAP_URLS, now=now))
