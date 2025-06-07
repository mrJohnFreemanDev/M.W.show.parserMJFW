# 🎭 MJFWparser — Мужское / Женское Episodes Parser

A precise and resilient episode parser for the Russian TV show “Мужское / Женское” from 1tv.ru, filtering out cuts, fragments, and promos. Created with logic and care by Ivan Mudriakov / MJFW.

## ✨ Features

- Parses the official sitemap (`https://www.1tv.ru/sitemap-160.xml`)
- Extracts full episode links for the show “Мужское / Женское”
- Skips irrelevant fragments, promos, and short inserts
- Retrieves both the `<title>` and a clean description for each episode
- Saves results to a UTF-8 encoded `.txt` file
- Built with pure Python — no external APIs
- Includes error handling and timeout protection

## 🧩 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

Contents of `requirements.txt`:
```
requests
beautifulsoup4
```

Python 3.9+ recommended.

## ⚙️ Usage

Run the script:

```bash
python MJFWparser.py
```

The output will be saved to:

```
man_woman_episodes.txt
```

Each line contains:
```
[ID] 'Episode Title' 'Episode Description' 'URL'
```

## 🧠 About

This parser is designed specifically for extracting **clean, structured episodes** of the show "Мужское / Женское", skipping irrelevant content and creating a filtered archive of real episodes only.

---

🔧 Developed with Python, regex magic and a healthy respect for order.  
💡 Created with love by Ivan Mudriakov / MJFW
