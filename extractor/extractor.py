import os
import re
import json

import praw
import requests

from dotenv import load_dotenv


load_dotenv()
reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("CLIENT_USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
)

subreddit = reddit.subreddit("dalle2")

openai_ids = set()

# Crawl OpenAI DALL-E links from dalle2 subreddit
for submission in subreddit.search("*", sort="new", time_filter="hour"):
    openai_links = set()

    url = submission.url
    permalink = submission.permalink
    comments = submission.comments.list()

    if "labs.openai" in url:
        openai_links.add(url)

    for comment in comments:
        links = [
            link
            for link in re.findall(r"(https?://[^\s]+)", comment.body)
            if "labs.openai.com" in link
        ]
        for link in links:
            openai_links.add(link)

    for link in openai_links:
        openai_id = re.findall(r"s\/(\w+)", link)[0]
        openai_ids.add(openai_id)

# Scrape generation data from DALLE public API
for _id in openai_ids:
    openai_endpoint = (
        f"https://labs.openai.com/api/labs/public/generations/generation-{_id}"
    )
    result = requests.get(openai_endpoint).json()
    with open("output.jsonl", "a") as f:
        f.write(json.dumps(result))
        f.write("\n")


# Verify if item is in Firestore
import firebase_admin
import firebase_admin.firestore as firestore
from firebase_admin import credentials as firebase_credentials

admin_sdk_path = os.getenv("FIREBASE_CREDENTIAL_CERTIFICATE_PATH")
cred = firebase_credentials.Certificate(admin_sdk_path)
app = firebase_admin.initialize_app(cred)
db = firestore.client()

image_collection = db.collection("images")
image_document = {}
image_collection.add(image_document)

