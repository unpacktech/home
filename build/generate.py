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

source_files = sorted(glob.glob(f"./{CONTENT_FOLDER}/*.json"))
dailies = []
for i, daily_file in enumerate(source_files):
    with open(daily_file, "r") as f:
        parsed = json.loads(f.read())
    date = parsed.get("date").replace("/", "-")
    permalink = f"https://unpack.tech/{date}"
    freshness = 0.25 + 0.75*i/len(source_files)
    dailies.append(parsed)
    for destination, template, publish in [
        [f"{date}.html", "daily.html", True],
        [f"{date}-email.html", "email.html", False],
    ]:
        path = f"{BASE_FOLDER}/{destination}"
        print("Generating:", destination, "->", path, freshness)
        with open(path, "w") as f:
            template = ENV.get_template(template)
            f.write(template.render(content=parsed, permalink=permalink, **CONTEXT))
            if publish:
                SITEMAP_URLS.append((destination, freshness))
print("Parsed", len(dailies), "days")

# SITEMAP
print("Generating sitemap.xml with %d items" % len(SITEMAP_URLS))
now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
with open(f"{BASE_FOLDER}/sitemap.xml", "w") as f:
    template = ENV.get_template("sitemap.xml")
    f.write(template.render(urls=SITEMAP_URLS, now=now))
