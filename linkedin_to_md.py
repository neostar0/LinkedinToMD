import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

from linkedinparser.linkedin_parser import LinkedinParser


def get_webdriver() -> WebDriver:
    # Set up the webdriver (You need to have ChromeDriver installed)
    options = Options()
    profile_path = os.path.join(os.getcwd(), "web_driver_profile")
    options.add_argument(r"user-data-dir={}".format(profile_path))

    return webdriver.Chrome(options)


def login_linkedin(web_driver: WebDriver, username: str, password: str, linkedin_url: str) -> None:
    linkedin_login_url = 'https://www.linkedin.com/login'
    # Navigate to the profile page
    web_driver.get(linkedin_url)

    if linkedin_url == web_driver.current_url:
        return

    web_driver.get(linkedin_login_url)
    if linkedin_login_url in web_driver.current_url:
        try:
            is_hint_user_fill_id_pw = not password
            web_driver.find_element(By.ID, 'username').send_keys('Please type yours.' if is_hint_user_fill_id_pw else username)
            web_driver.find_element(By.ID, 'password').send_keys(password)
            if is_hint_user_fill_id_pw:
                time.sleep(10)
            web_driver.find_element(By.XPATH, "//button[@type='submit']").click()

            time.sleep(15)  # You may need sometime to do some extra login stuff which not cover in this project
            web_driver.get(linkedin_url)
        except Exception as e:
            print(e)


def format_to_markdown(profile: dict) -> str:
    markdown = f"{profile[LinkedinParser.USER_NAME]}\n===\n\n\n"
    for header, content in profile[LinkedinParser.RESUME].items():
        markdown += f'## {header}\n\n'
        markdown += "\n\n".join(content)
        markdown += '\n\n\n'
    return markdown


def save_profile_to_md_file(username, password, url, filename="linkedin_profile.md"):
    web_driver = get_webdriver()
    login_linkedin(web_driver, username, password, url)
    profile = LinkedinParser().get_profile(web_driver.page_source)
    profile_md = format_to_markdown(profile)
    # Close the browser
    web_driver.quit()

    # Write the markdown content to a file
    with open(filename, 'w') as file:
        file.write(profile_md)

    print(f"Profile saved to {filename}")


def main():
    load_dotenv()
    save_profile_to_md_file(os.getenv('LINKEDIN_USERNAME'), os.getenv('LINKEDIN_PASSWORD'), 'https://www.linkedin.com/in/me/')


if __name__ == "__main__":
    main()
