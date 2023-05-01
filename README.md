# Codewars Scraper

## About

I wrote this script as a way of retrieving all my coding problems I'd solved from Codewars.

It will categorise your solutions into neat folders, organised by the problem name, with the difficulty appended to the end of the filename. Each file will have the coding problem's URL included as a comment at the top.

### Solution categorisation

Solutions are placed in folders based on their language. The filenames are of the form [Problem_name]-[difficulty].

If there are multiple of the same solution, they will have v2, v3, etc. appended.

Solutions will have a link to the problem as a comment on the first line.

## Usage

This script includes support for the languages I've been using on Codewars - C, JavaScript, Python and Shell.

There are two dictionaries you will need to fill in values for if you want to add additional languauges:
- language_filetypes, which contains the file extentsion
- language_comments, which contains the comment syntax for the language (so the coding problem's URL can be added to the file as a comment)

These are located at the top of the page.

### Requirements

Requires bs4 for the offline scraper. Requires Selenium and Chromedriver for the live scraper.

The live scraper uses Google Chrome.

You can install them as necessary using Pip in your console of choice.

```
pip install bs4
pip install selenium
pip install chromedriver-binary-auto
```

### Offline scraping

The simplest way of scraping is to download your solutions page and drop it into the same directory as scraper.py.

To save your solutions, go here (after filling in your username): https://www.codewars.com/users/[YOUR USERNAME]/completed_solutions.

Solutions are dynamically loaded so scroll to the very bottom of the page, then save the page.

Run python scraper.py and choose the offline scraper.

### Live scraping

To scrape live, run python scraper.py and choose the live scraper.

It will ask whether you want to sign in with Github, then ask for your username and password. This is only used for filling in your login details.

Then you can just sit back whilst the scraper does it's work.

If you find that the full solution set isn't loaded, you can adjust SCROLL_PAUSE_TIME to a higher number at the top of scraper.py.

Note: I use sign in with Github so non-Github signin hasn't been tested.
