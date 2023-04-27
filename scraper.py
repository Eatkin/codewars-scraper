'''Codewars scraper
Finds all my codewars solutions, saves and organises them
Appends a link to the problems at the end of the code'''

# Set up filetypes dictionary for each language
language_filetypes = {
    "C": ".c",
    "Javascript": ".js",
    "Python": ".py",
    "Shell": ".sh",
}

# Set up comments dictionary for each language
language_comments = {
    "C": "//",
    "Javascript": "//",
    "Python": "#",
    "Shell": "#",
}

from bs4 import BeautifulSoup
'''
Page format:
All solution are contained in a div with class "items-list"
Each individual solution is contained within a div with class "list-item-solutions"
The difficulty is contained in a div of class "item-title", alongside the problem name and link
The language is displayed in a h6 tag with the content of the form "[Language]:" (e.g. "Python:")
We'll need to remove the colon from the end of the language
Finally the problem itself is contained within a code block
This is all formatted nicely using spans, so they need to be removed
Fortunately beautiful soup does this automatically so no problem
'''

# Get the page
filename = "Eatkin_Codewars_toscrape.html"
try:
    with open("Eatkin_Codewars_toscrape.html", "r") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
except FileNotFoundError:
    print("File not found")
    exit()

# Now find the div with class "items-list"
main_content = soup.find("div", class_="items-list")

solutions = main_content.find_all("div", class_="list-item-solutions")

for solution in solutions:
    # Get the difficulty, problem name and link
    head_data = solution.find("div", class_="item-title")
    difficulty = head_data.find("span").text
    print(difficulty)
    problem_name = head_data.find("a").text
    print(problem_name)
    problem_link = head_data.find("a")["href"]
    print(problem_link)

    # The h6 is directly below
    language = solution.find("h6").text[:-1]
    print(language)

    # Now the solution itself
    solution_code = solution.find("code").text
    print(solution_code)

    # Now we need to save the solution to a file with a comment appended to the top with the problem link
    # The filename can be the problem name with spaces replaced with underscores and the filetype appended
    # We'll categorise the solutions by language in subfolders
    # We'll then append the difficulty to the end of the filename
    break
