from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import time
import loginInfo as login_info

screenshot_count = 1
html_count = 1


def remove_files_with_extensions(extensions):
    directory = os.path.dirname(os.path.realpath(__file__))
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"Removed: {file_path}")


def get_current_time():
    # Get the current time
    current_time = time.strftime("%H:%M:%S", time.localtime())
    return current_time


def take_screenshot(driver):
    global screenshot_count
    filename = f"screenshot{get_current_time()}_{screenshot_count}.png"
    driver.save_screenshot(filename)
    screenshot_count += 1
    print(f"Screenshot saved to {filename}")


def save_html(driver):
    global html_count
    filename = f"html{get_current_time()}_{html_count}.html"
    html_content = driver.page_source
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(html_content)
    html_count += 1
    print(f"HTML content saved to {filename}")


class MissingInputError(Exception):
    pass


def get_tempKey():
    url = "https://www.mynetid.wisc.edu/mfa-recovery"
    # initilzes new chrome instance
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # goes to https://www.mynetid.wisc.edu/mfa-recovery
        driver.get(url)

        # finds buttons and text fields
        buttons = driver.find_elements(By.TAG_NAME, 'button')
        text_input_fields = driver.find_elements(By.TAG_NAME, 'input')

        # inputs user informatioon and clicks next
        try:
            text_input_fields[0].send_keys(login_info.USERNAME)
            text_input_fields[1].send_keys(login_info.PASSWORD)
        except NameError:
            raise MissingInputError("Add username and password to loginInfo.py")
        buttons[0].click()

        # Finds all questions
        question_divs = driver.find_elements(By.CLASS_NAME, 'question')
        for question in question_divs:
            question_parts = question.find_elements(By.TAG_NAME, 'div')
            question_text = question_parts[0].text
            if question_text not in login_info.ANSWERS:
                raise MissingInputError(f"please enter an answer for the question '{question_text} in loginInfo.py'")
            answer = login_info.ANSWERS[question_text]
            text_input = question_parts[1].find_elements(By.TAG_NAME, 'input')[0]
            text_input.send_keys(answer)

        # submits answers
        buttons = driver.find_elements(By.TAG_NAME, 'input')
        buttons[3].click()

        #copy temp password
        for i in range(1, 300):
            try:
                buttons = driver.find_elements(By.TAG_NAME, 'button')
                buttons[1].click()
                break
            except:
                pass

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    # remove_files_with_extensions(['.png', '.html'])
    get_tempKey()
