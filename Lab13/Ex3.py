"""Display a wholesome meme and its subreddit, refreshing every ten seconds."""

import requests
from flask import Flask, render_template

app = Flask(__name__)
MEME_API_URL = "https://meme-api.com/gimme/wholesomememes"


@app.route('/')
def index():
    try:
        response = requests.request("GET", MEME_API_URL, timeout=10)
        response.raise_for_status()
        meme = response.json()
    except requests.RequestException:
        app.logger.exception("The meme API request failed.")
        return render_template(
            "meme.html",
            error="The meme service is unavailable. The page will try again shortly.",
        ), 502

    if not isinstance(meme, dict) or not isinstance(meme.get("url"), str) or not isinstance(
        meme.get("subreddit"), str
    ):
        app.logger.error("The meme API response did not contain a meme URL and subreddit.")
        return render_template(
            "meme.html",
            error="The meme service returned an invalid response. The page will try again shortly.",
        ), 502

    return render_template(
        "meme.html",
        image_url=meme["url"],
        subreddit=meme["subreddit"],
    )


if __name__ == '__main__':
    app.run(debug=True)
