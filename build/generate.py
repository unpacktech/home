import datetime
import json
import glob
from shared import BASE_FOLDER, CONTENT_FOLDER, get_context, get_jinja_env

SITEMAP_URLS = []
ENV = get_jinja_env()
CONTEXT = get_context()


for page in ["index.html"]:
    path = f"{BASE_FOLDER}/{page}"
    print("Generating page:", path)
    with open(path, "w") as f:
        template = ENV.get_template(page)
        f.write(template.render(**CONTEXT))

for daily_file in glob.glob(f"./{CONTENT_FOLDER}/*.json"):
    with open(daily_file, "r") as f:
        parsed = json.loads(f.read())
    date = parsed.get("date").replace("/", "-")
    permalink = f"https://unpack.tech/{date}"
    for path, template, publish in [
        [f"{BASE_FOLDER}/{date}.html", "daily.html", True],
        [f"{BASE_FOLDER}/{date}-email.html", "email.html", False],
    ]:
        print("Generating daily:", path)
        with open(path, "w") as f:
            template = ENV.get_template(template)
            f.write(template.render(content=parsed, permalink=permalink, **CONTEXT))
            if publish:
                SITEMAP_URLS.append((path, 0.7))

# SITEMAP
print("Generating sitemap.xml with %d items" % len(SITEMAP_URLS))
now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
with open(f"{BASE_FOLDER}/sitemap.xml", "w") as f:
    template = ENV.get_template("sitemap.xml")
    f.write(template.render(urls=SITEMAP_URLS, now=now))
