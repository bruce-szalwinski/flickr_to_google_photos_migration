import pickle
import os
import json
import re

"""
This module looks at all of the entries in the list of photos from flickr and attempts to find a matching completed task from celery.
A completed task would indicate that celery was able to read the photo from flickr and transfer it to google.  The url of the photo will
be printed for photos that don't have a matching completed task.
"""

def load_urls():
    urls = []
    p = re.compile("https:[^']*")
    for file in os.listdir("celery/processed/"):
        if file.endswith(".msg"):
            with open(f"celery/processed/{file}") as celery_msg:
                message = json.load(celery_msg)
                r = p.search(message['headers']['argsrepr'])
                url = r.group(0)
                urls.append(url)

    return urls


def check_photoset(urls: list):
    found = 0
    not_found = 0
    for file in os.listdir("photosets-complete/"):
        if file.endswith(".pickle"):

            with open(f"photosets-complete/{file}", "rb") as photo_tasks_file:
                my_photos = pickle.load(photo_tasks_file)

            for photo in my_photos:
                if photo['photoUrl'] in urls:
                    found += 1
                else:
                    print(photo['photoUrl'])
                    not_found += 1

    print(f"found: {found}")
    print(f"not found: {not_found}")


if __name__ == '__main__':
    urls = load_urls()
    check_photoset(urls)
