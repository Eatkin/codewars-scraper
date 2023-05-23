'''Codewars scraper
Finds all my codewars solutions, saves and organises them
Appends a link to the problems at the beginning of the code'''

from bs4 import BeautifulSoup
import string
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Constants
SCROLL_PAUSE_TIME = 1
MAX_SCROLL_ATTEMPTS = 20

# Set up filetypes dictionary for each language
# Ensure the languages are lowercase
language_filetypes = {
    "c": ".c",
    "javascript": ".js",
    "python": ".py",
    "shell": ".sh",
    "c#": ".cs",
    "sql": ".sql",
    "bf": ".bf",
    "prolog": ".pl",
}

# Set up comments dictionary for each language
language_comments = {
    "c": "//",
    "javascript": "//",
    "python": "#",
    "shell": "#",
    "c#": "//",
    "sql": "--",
    "bf": "",
    "prolog": "%",
}

# Create a translator which will remove all punctuation and replace spaces with underscores
# Retains any hyphens
translator = str.maketrans("", "", string.punctuation)
translator[ord(" ")] = "_"
translator[ord("-")] = "-"


def offline_scraper(filename):
    '''
    HTML page format:
    All solution are contained in a div with class "items-list"
    Each individual solution is contained within a div with class "list-item-solutions"
    The difficulty is contained in a div of class "item-title", alongside the problem name and link
    The language is displayed in a h6 tag with the content of the form "[Language]:" (e.g. "Python:")
    We'll need to remove the colon from the end of the language
    Finally the problem itself is contained within a code block
    '''

    # Get the page
    try:
        with open(filename, "r") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
    except FileNotFoundError:
        print(
            "File not found, please make sure you have downloaded the page and placed it in the same directory as this script and set the filename variable correctly"
        )
        exit()

    parse_page(soup)


def online_scraper(github_signin, username, password):
    # Start webdriver in headless mode
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.codewars.com/users/sign_in")

    if github_signin:
        button = button = driver.find_element(
            By.CSS_SELECTOR, "button[data-action='auth#githubSignIn']")
        button.click()

        # This redirects to github, so wait for it to load and fill in login details
        wait = WebDriverWait(driver, 10)
        wait.until(EC.title_contains("Sign in to GitHub · GitHub"))

        # Fill in username and password
        username_form = driver.find_element(By.ID, "login_field")
        username_form.send_keys(username)
        password_form = driver.find_element(By.ID, "password")
        password_form.send_keys(password)

        # Press login button
        submit_button = driver.find_element(By.CSS_SELECTOR,
                                            "input[type='submit']")
        submit_button.click()
    else:
        # Fill in username and password
        username_form = driver.find_element(By.ID, "user_email")
        username_form.send_keys(username)
        password_form = driver.find_element(By.ID, "user_password")
        password_form.send_keys(password)

        # Press sign in button
        submit_button = driver.find_element(By.CSS_SELECTOR,
                                            "input[type='submit']")
        submit_button.click()

    # We should now be logged in and get redirected to the dashboard
    # But we don't want to be there, so let's go to the solutions page
    driver.get(
        f"https://www.codewars.com/users/{username}/completed_solutions")

    # Scroll to the bottom of the page to load all solutions
    # Get scroll height
    # (Ref: https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python/27760083#27760083)
    last_height = driver.execute_script("return document.body.scrollHeight")

    scroll_attempts = 0
    while True:
        # Scroll down to bottom
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            scroll_attempts += 1
            if scroll_attempts >= MAX_SCROLL_ATTEMPTS:
                break
        else:
            last_height = new_height
            scroll_attempts = 0

    # Create soup and parse page
    soup = BeautifulSoup(driver.page_source, "html.parser")
    parse_page(soup)


def parse_page(page):
    # Now find the div with class "items-list"
    main_content = page.find("div", class_="items-list")

    # Get the solutions
    solutions = main_content.find_all("div", class_="list-item-solutions")

    problem_count = 0

    # Loop through all solutions
    for solution in solutions:
        problem_count += 1
        # Get the difficulty, problem name and link
        head_data = solution.find("div", class_="item-title")
        difficulty = head_data.find("span").text
        problem_name = head_data.find("a").text
        problem_link = head_data.find("a")["href"]

        # Fix for relative URL in live scraper
        if "codewars.com" not in problem_link:
            problem_link = "https://www.codewars.com" + problem_link

        # Languages are stored in h6, solutions are stored in code blocks
        # Date and time are stored in time-ago tags
        # Loop through all the elements in "solution"
        language = None
        solution_code = None
        datetime = None

        solution_details = []

        for element in solution.descendants:
            if element.name == "h6":
                language = element.text[:-1]
            elif element.name == "code":
                solution_code = element.text
            elif element.name == "time-ago":
                # Datetime is the last attribute before a new solution
                datetime = element["datetime"]
                solution_details.append((language, solution_code, datetime))

        # Now reverse the order of the solutions so that the oldest is first
        solution_details.reverse()
        revision = 1
        current_language = None

        # Loop through all the solutions found
        for language, solution_code, datetime in solution_details:
            if language != current_language:
                revision = 1
                current_language = language
            else:
                revision += 1

            # Construct filename
            filename = problem_name
            if revision > 1:
                filename += f"-v{revision}"
            filename += f"-{difficulty}"
            filename = filename.translate(translator)
            filename += language_filetypes[language.lower()]

            # Filepath
            directory = f"{language}"
            filepath = f"{language}/{filename}"

            # Comment
            comment = f"{language_comments[language.lower()]} {problem_link}"
            comment += f"\n{language_comments[language.lower()]} {datetime}"

            # Now write the file
            # Create directory if necessary
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Check for file existence first
            if not os.path.exists(filepath):
                with (open(filepath, "w")) as f:
                    f.write(comment + "\n")
                    f.write(solution_code)

    print("Scraped {} solutions".format(problem_count))


def main():
    # Ask if user wants to use online or offline scraper
    scraper_type = input("Use the (l)ive (online) or (o)ffline scraper? ")
    while scraper_type.lower() not in ["l", "o"]:
        scraper_type = input("Please enter l or o: ")

    if scraper_type == "l":
        github = input("Do you want to sign in with GitHub? (y/n) ")
        while github.lower() not in ["y", "n"]:
            github = input("Please enter y or n: ")
        github = True if github == "y" else False
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        print(
            "Thanks! Now sit back and relax while I do the hard work...bleep bloop I am a computer"
        )
        online_scraper(github, username, password)
    else:
        # Run the scraper
        print("I need the HTML file you downloaded from Codewars")
        print("Put it in the same directory as this script")
        filename = input(
            "And tell me what the filename is including the file extension (e.g. codewars.html): "
        )
        print(
            "Thanks! Now sit back and relax while I do the hard work...bleep bloop I am a computer"
        )
        offline_scraper(filename)

    print("All done! And nothing went wrong! Enjoy your solutions!")


if __name__ == "__main__":
    main()
