# Codewars Scraper

## About

I wrote this script as a way of retrieving all my coding problems I'd solved from Codewars.

It will categorise your solutions into neat folders, organised by the problem name, with the difficulty appended to the end of the filename. Each file will have the coding problem's URL included as a comment at the top.

## Limitations

This does not scrape the live page. Content is dynamically loaded on Codewars and this exclusively uses Beautiful Soup which can't perform any actions beyond reading the html.

## Usage

This script includes support for the languages I've been using - C, JavaScript, Python and Shell.

There are two dictionaries you will need to fill in values for if you want to add additional languauges:
- language_filetypes, which contains the file extentsion
- language_comments, which contains the comment syntax for the language (so the coding problem's URL can be added to the file as a comment)

Since this script does not scrape a live page, you will need to save your Codewars solutions page locally (here: https://www.codewars.com/users/[YOUR USERNAME]/completed_solutions). Solutions are dynamically loaded so scroll to the very bottom of the page, then save the page.

You will need to change the first occurance of "filename" in the program so that it references the .html file you've saved.
