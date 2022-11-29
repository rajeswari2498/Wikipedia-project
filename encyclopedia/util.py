import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def list_entries():
    _, listnames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", listname)
                for listname in listnames if listname.endswith(".md")))


def save_entry(title,content):
    listname=f"entries/{title}.md"
    if default_storage.exists(listname):
        default_storage.delete(listname)
    default_storage.save(listname, ContentFile(content))


def get_entry(title):
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
