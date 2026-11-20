# Lab 13: Creating HTML Interfaces with Flask

Install the lab dependencies from the repository root:

```powershell
python -m pip install -r Lab13\requirements.txt
```

Run one exercise at a time; each development server uses Flask's debug mode at
`http://127.0.0.1:5000`.

- `python Lab13\Ex1.py` serves the welcome message.
- `python Lab13\Ex2.py` serves the login form. Demo credentials: `port` /
  `port123` or `kazman` / `kazman123`.
- `python Lab13\Ex3.py` fetches and displays a meme and subreddit from the meme
  API, then refreshes the page every 10 seconds. It requires an internet
  connection.
- `python Lab13\Ex4.py` serves the quiz-game skeleton.

The HTML pages for all four exercises are in `templates`, as Flask expects.
The quiz mock-up is intentionally a page-flow skeleton: it provides home,
instructions, question, and results pages, but does not yet validate answers
or calculate scores.

## Quiz skeleton reflection

I used approach **(i), mock-up pages**. The skeleton makes the main screens and
navigation visible early, so it is easier to discuss the user experience,
identify missing screens, and divide later implementation into manageable
pieces. It also avoids building scoring and persistence before the page flow is
settled. Its disadvantage is that links and sample content can look like a
finished game even though there is no real answer validation, score handling,
or stored state; those behaviors still need to be designed and tested.

For this small Flask exercise, mock-ups are quick to adapt and make the
application structure easy to understand. The trade-off is that manually
building the page flow does not reuse the existing quiz's question data,
validation, lifelines, or scoring, so it would be wasteful as the final
application. Compared with starting the web application from scratch, the
skeleton was better for establishing routes and getting feedback on the
interface before implementing game logic. It is not a replacement for that
logic: the next step would be to connect these pages to the existing quiz rules
and data, then test the complete experience.
