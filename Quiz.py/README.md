# Filipino 101 Quiz website

The original terminal quiz is unchanged. To run the browser-based version:

1. Open a terminal in this folder.
2. Install dependencies with `python -m pip install -r requirements.txt`.
3. Start the local web server with `python quiz_web.py`.
4. Open `http://127.0.0.1:5000` in a browser and register an account.

Accounts and best scores are stored in `quiz_users.sqlite3`. The leaderboard
ranks each user's best percentage; the grand champion is the player at the top.
The quiz awards one point for a correct answer and one additional point when
the answer is submitted within 10 seconds. Each quiz run has one 50/50 lifeline.

## Image and video questions

Put media files in `static/media/` (subfolders are allowed), then add a `media`
object to a question in `questions.json`:

```json
{
  "media": {
    "type": "image",
    "filename": "paintings/example.jpg",
    "alt": "A painting with a blue sky"
  }
}
```

Use `"type": "video"` for a video file such as `clips/example.mp4`. The
`filename` is relative to `static/media/`; files outside that folder are not
served. The media object is optional, so existing text-only questions continue
to work. The app reports a missing referenced file rather than silently
displaying an empty media area.

## Deployment note

The generated secret key is convenient for local use, but it changes whenever
the server restarts. For a deployed site, set a persistent, random
`QUIZ_SECRET_KEY` environment variable shared by all app workers, use HTTPS, and
set `QUIZ_HTTPS=1` so the session cookie is marked secure. Keep the SQLite
database and question-media files on persistent storage. This starter app binds
to localhost by default and is not configured as a hardened public production
service.
