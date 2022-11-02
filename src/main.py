#!/usr/bin/env python3

import flask
import praw
import os
from dotenv import load_dotenv

# Read Environment Variables From Env File.
load_dotenv()

# Obtain a `Reddit` Instance (read-only).
reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT")
)

# Create a Flask application.
app = flask.Flask(__name__)

# Scrape a random post from the subreddit specified in the usl of the API.
def ScrapPost(sub=None):
    if sub is not None:
        try:
            subreddit = reddit.subreddit(sub)
            post = subreddit.random()
            try:
                post.preview
                return {
                    "code":200,
                    "post_link": post.shortlink,
                    "subreddit": sub,
                    "title": post.title,
                    "url": post.url,
                    "ups": post.ups,
                    "author": post.author.name,
                    "spoilers_enabled": subreddit.spoilers_enabled,
                    "nsfw": subreddit.over18,
                    "image_previews": [i["url"] for i in post.preview.get("images")[0].get("resolutions")]
                }
            except Exception as error:
                return {
                    "code":200,
                    "post_link": post.shortlink,
                    "subreddit": sub,
                    "title": post.title,
                    "url": post.url,
                    "ups": post.ups,
                    "author": post.author.name,
                    "spoilers_enabled": subreddit.spoilers_enabled,
                    "nsfw": subreddit.over18,
                    "image_previews": ["No image preview found for this post"]
                }
        except Exception as error:
            return {
                "code": 400,
                "message": str(type(error)) + str(error),
                "help": "Unable to find the subbreddit `" + str(subreddit) + "` specified."
            }
    else:
        return {
            "code": 400,
            "message": "Please specify a subreddit."
        }

# The home page that will be shown when no subreddit is specified.
@app.route('/')
def home():
    result = {
        "code": 400,
        "message": "Please specify a subreddit."
    }
    return flask.jsonify(result)

# Page that shows the information collected by the API.
@app.route('/<string:subreddit>/')
def api_subreddit(subreddit):
    result = ScrapPost(subreddit)
    return flask.jsonify(result)

# Main function to start the Flask application.
if __name__ == "__main__":
    app.run(threaded=True)

