'''Codewars scraper
Finds all my codewars solutions, saves and organises them
Appends a link to the problems at the end of the code'''

from bs4 import BeautifulSoup
import string
import os

# Set up filetypes dictionary for each language
# Ensure the languages are lowercase
language_filetypes = {
    "c": ".c",
    "javascript": ".js",
    "python": ".py",
    "shell": ".sh",
}

# Set up comments dictionary for each language
language_comments = {
    "c": "//",
    "javascript": "//",
    "python": "#",
    "shell": "#",
}

# Create a translator which will remove all punctuation and replace spaces with underscores
translator = str.maketrans("", "", string.punctuation)
translator[ord(" ")] = "_"
translator[ord("-")] = "-"
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
The only remaining problem to be solved is when there are multiple solutions
Which I'm sure we can just solve using a loop through each code element found
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
    problem_name = head_data.find("a").text
    problem_link = head_data.find("a")["href"]

    # The h6 is directly below
    language = solution.find("h6").text[:-1]

    # Now the solution itself
    # There may be multiple solutions, so reverse the order going from oldest first
    # This means we can save the refactors as v2, v3, etc.
    solution_code = solution.find_all("code")
    solution_code.reverse()
    for version, code_block in enumerate(solution_code):
        # Now we need to save the solution to a file with a comment appended to the top with the problem link
        # The filename can be the problem name with spaces replaced with underscores and the filetype appended
        # We'll categorise the solutions by language in subfolders
        # We'll then append the difficulty to the end of the filename
        # We can also append a version number if version > 0
        # I'm having a migraine so and I can't really see what I'm typing but let's try anyway

        # Construct the filename
        filename = problem_name
        if version > 0:
            filename += f"-v{version + 1}"
        filename += f"-{difficulty}"
        filename = filename.translate(translator)
        filename += language_filetypes[language.lower()]

        # Construct the filepath
        directory = f"{language}"
        filepath = f"{language}/{filename}"

        # Construct the comment
        comment = f"{language_comments[language.lower()]} {problem_link}"

        # Now write the file
        # Create directory if necessary
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Check for file existence first
        if not os.path.exists(filepath):
            with (open(filepath, "w")) as f:
                f.write(comment + "\n")
                f.write(code_block.text)
