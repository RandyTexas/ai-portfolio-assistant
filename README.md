# AI Portfolio Assistant

A beginner-friendly local Python project for building a personal AI finance and investing assistant.

This current version is a **watchlist manager MVP** built inside a Linux VM for safe development. It does **not** place real trades and does **not** connect to brokers yet.

## Current Features

- Persistent watchlist saved to `data/watchlist.json`
- View full watchlist
- View available categories
- Filter stocks by category
- Look up a stock by ticker
- Add a stock
- Remove a stock
- Show ticker symbols only

## Current Project Structure

```text
ai-portfolio-assistant/
├── data/
│   └── watchlist.json
├── docs/
├── journals/
├── reports/
├── src/
│   ├── config/
│   │   └── settings.py
│   ├── helpers.py
│   ├── main.py
│   └── watchlist.py
├── tests/
├── .gitignore
├── README.md
└── requirements.txt