# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
#
# # Automatically download and use the correct ChromeDriver
# service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service)
#
# # Test the setup
# driver.get("https://www.google.com")
# driver.quit()
import email
import random
import string
import re
import imaplib
import time
import webbrowser
from datetime import datetime

from bs4 import BeautifulSoup
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from seleniumbase import BaseCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class JobApplicationTest(BaseCase):
    imap_host = "imap.gmail.com"
    email_user = "r.agarwal@elevatus.io"  # Replace with your Gmail address
    app_password = "vzxb vvdv dvkw dpim"  # Replace with your Gmail App Password
    email_subject = "nidalcc - You have been successfully registered!"  # Replace with the email's subject
    def generate_random_password(self):
        """Generate a secure random password with uppercase, special character, and numbers."""
        while True:
            password = ''.join(
                random.choices(string.ascii_lowercase, k=4) +
                random.choices(string.ascii_uppercase, k=2) +
                random.choices(string.digits, k=2) +
                random.choices("!@#$%^&*", k=2)
            )
            if self.validate_password(password):
                return ''.join(random.sample(password, len(password)))  # Shuffle characters for randomness

    def validate_password(self, password):
        """Validate that the password meets the required criteria."""
        if (
                len(password) >= 8 and
                re.search(r"[A-Z]", password) and  # At least one uppercase letter
                re.search(r"[0-9]", password) and  # At least one number
                re.search(r"[!@#$%^&*]", password)  # At least one special character
        ):
            return True
        raise ValueError(
            "Password must be at least 8 characters long, contain an uppercase letter, a number, and a special character.")

    def generate_random_email(self, first_name, last_name):
        """Generate a random email address."""
        return f"{'r.agarwal+'}{random.randint(100, 999)}@elevatus.io"


    def validate_email(self, email):
        """Validate that the email address is in a correct format."""
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if re.fullmatch(email_regex, email):
            return True
        raise ValueError(f"Invalid email format: {email}")

    def close_cookie_popup(self):
        """
        Locate and click the cookie pop-up button using self.
        """
        try:
            cookie_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH,
                     "//button[contains(text(), 'Accept') or contains(text(), 'Agree') or contains(text(), 'Close')]")
                )
            )
            cookie_button.click()
            print("Cookie pop-up closed successfully.")
        except Exception as e:
            print(f"No cookie pop-up found or error occurred: {e}")

    def test_register_and_apply(self):
        # Step 1: Navigate to the website
        self.open("https://mcitcareerssd.elevatus.io/")
        self.close_cookie_popup()
        #
        # cookie_button = WebDriverWait(self.driver, 10).until(
        #     EC.element_to_be_clickable(
        #         (By.XPATH,
        #          "//button[contains(text(), 'Accept') or contains(text(), 'Agree') or contains(text(), 'Close')]")
        #     )
        # )
        # # Click the cookie button
        # cookie_button.click()

        self.assert_title("Career portal")  # Validation 1: Ensure correct page title

        # Step 2: Start registration process
        self.click("button:contains('Register')")  # Assuming button text contains 'Register'

        # Dynamically generate user data
        first_name = ''.join(random.choices(string.ascii_letters, k=8))
        last_name = ''.join(random.choices(string.ascii_letters, k=8))
        # email='r.agarwal+106@elevatus.io'
        # password='Oman@1234'
        email = self.generate_random_email(first_name, last_name)
        self.validate_email(email)
        password = self.generate_random_password()  # Generate secure password

        # password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        phone_number = "98912969"  # Example phone number

        # Fill out the registration form
        self.type("/html/body/div[1]/div/div/div/div[1]/div/form/div[1]/div[1]/input", first_name)  # Validation 2: Ensure first name is entered
        assert first_name.isalpha()  # Validation 7: First name contains only letters

        self.type("/html/body/div[1]/div/div/div/div[1]/div/form/div[2]/div[1]/input", last_name)  # Validation 3: Ensure last name is entered
        assert last_name.isalpha()  # Validation 7: First name contains only letters

        self.type("/html/body/div[1]/div/div/div/div[1]/div/form/div[3]/div/input", email)  # Validation 4: Ensure email is entered
        self.type("/html/body/div[1]/div/div/div/div[1]/div/form/div[4]/div/input", password)
        self.type("/html/body/div[1]/div/div/div/div[1]/div/form/div[5]/div[1]/input", password)
        # Validation: Ensure password and confirm password match
        confirm_password = self.get_value("/html/body/div[1]/div/div/div/div[1]/div/form/div[5]/div[1]/input")
        self.assert_equal(password, confirm_password, "Password and Confirm Password do not match!")

        self.type("/html/body/div[1]/div/div/div/div[1]/div/form/div[6]/div/div/div/input", phone_number)  # Enter phone number
        self.click("/html/body/div[1]/div/div/div/div[1]/div/form/div[7]/label")  # Assuming this is the checkbox ID

        self.click("button:contains('Sign up')")  # Submit registration form
        self.verify_email()


        # self.click_element("//button[text()='Fill in manually']", By.XPATH)
        # self.wait_for_element_visible("//button[text()='Fill in manually']", timeout=10)
        # self.click("//button[text()='Fill in manually']")

    def click_element(self, selector, by):
        """Click the specified element."""
        try:
            element = self.wait_for_element(selector, by)
            element.click()
            print("Button clicked successfully.")
        except Exception as e:
            print(f"Error clicking button: {e}")


    def get_body_from_email(self, msg):
        """Extract the body of the email, handling both plain text and HTML parts"""
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                # Extract text or HTML body
                if "attachment" not in content_disposition:
                    if content_type == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        break
                    elif content_type == "text/html":
                        body = part.get_payload(decode=True).decode()
                        break
        else:
            body = msg.get_payload(decode=True).decode()
        return body

    def extract_click_here_link(self, body):
        """Extract the link behind 'Click here' or any other anchor tags"""
        soup = BeautifulSoup(body, "html.parser")
        # Debug: Print all anchor tags in the email
        print("Debug: List of all anchor tags in the email:")
        for link in soup.find_all("a"):
            print(f"Anchor Text: {link.text.strip()}, HREF: {link.get('href')}")

        # Attempt to find the link with "Click here" text
        link = soup.find("a", string=lambda text: text and "Click Here" in text)
        if link and link.get("href"):
            return link["href"]

        # Debug: Fallback if "Click here" is not found
        print("No 'Click here' link found. Trying other links...")
        all_links = soup.find_all("a")
        if all_links:
            return all_links[0].get("href")  # Return the first available link as a fallback

        return None

    def fill_in_details(self):
        """Step 3: Fill in the candidate details after email verification"""
        print("Candidate details should be filled in manually on the webpage.")
        # You can add code for filling the form if required with other tools.

    def close_browser(self):
        """Since we're not using a browser, this is redundant"""
        print("No browser to close, process is complete.")

    def get_latest_email_id(self, mail, message_ids):
        """Sort emails by INTERNALDATE and return the ID of the most recent email"""
        latest_email_id = None
        latest_date = None

        for msg_id in message_ids:
            status, msg_data = mail.fetch(msg_id, "(BODY[HEADER.FIELDS (DATE)])")
            if status == "OK":
                email_date = email.utils.parsedate_to_datetime(
                    email.message_from_bytes(msg_data[0][1]).get("Date")
                )
                if latest_date is None or email_date > latest_date:
                    latest_date = email_date
                    latest_email_id = msg_id

        return latest_email_id

    def verify_email(self):
        """Fetch the latest email with the specified subject"""
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(self.email_user, self.app_password)
        mail.select("inbox")

        # Search for emails matching the subject
        status, messages = mail.search(None, f'(SUBJECT "{self.email_subject}")')

        if status == "OK":
            message_ids = messages[0].split()
            if message_ids:
                # Fetch all emails matching the subject
                latest_email_id = self.get_latest_email_id(mail, message_ids)
                if latest_email_id:
                    status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
                    raw_email = msg_data[0][1]

                    # Parse the email content
                    msg = email.message_from_bytes(raw_email)
                    body = self.get_body_from_email(msg)

                    # Extract the verification link
                    verification_link = self.extract_click_here_link(body)

                    if verification_link:
                        print("Verification link found:", verification_link)
                        self.driver.get(verification_link)

                        # Wait for the verification page to load and look for the button
                        WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//button[text()='Fill in manually']"))
                        )

                        # Click the verification button (example action on the opened page)
                        self.driver.find_element(By.XPATH, "//button[text()='Fill in manually']").click()
                        # Wait for the element to be present
                        wait = WebDriverWait(self.driver, 10)
                        description_input = wait.until(EC.presence_of_element_located((By.ID, "description")))

                        # Interact with the element
                        description_input.send_keys("Your description here. I want to apply here")
                        date_input = self.driver.find_element(By.ID,
                                                         "date-picker-dialog--0---0-0-undefined")  # Replace with the actual ID of the date field
                        date_input.clear()
                        date_input.send_keys("1985-05-22")

                        gender_input = self.driver.find_element(By.XPATH,
                                                           "//input[@id='gender']")  # Replace with the actual ID of the date field
                        gender_input.click()

                        # Select an option by its text
                        option = self.driver.find_element(By.ID,
                                                     "gender-option-1")  # Replace with the actual locator
                        option.click()

                        # # Select an option by its text
                        # option = driver.find_element(By.ID,
                        #                              "gender-option-1")  # Replace with the actual locator
                        # option.click()

                        nationality_input = self.driver.find_element(By.ID,
                                                                "nationality")  # Replace with the actual ID of the date field
                        nationality_input.click()
                        # Select an option by its text
                        option = self.driver.find_element(By.ID,
                                                          "nationality-option-79")  # Replace with the actual locator
                        option.click()

                        address_input = self.driver.find_element(By.ID,"address")
                        address_input.send_keys("AlGhubra")



                        city_input = self.driver.find_element(By.ID,
                                                         "city")  # Replace with the actual ID of the date field
                        city_input.send_keys("Muscat")

                        # Wait for the file input element to appear
                        file_input = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/div/div[13]/div/div/div"))
                        )

                        # Send the file path to the input element
                        file_input.send_keys("/users/otf/resume.pdf")
                        # resume_upload = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/div/div[13]/div/div/div")
                        # self.driver.execute_script("arguments[0].click();", resume_upload)
                        #
                        # resume_file_path = "/users/otf/resume.pdf"  # Replace with the absolute path to your resume
                        # # self.choose_file("input[type='file']", resume_file_path)
                        # # Send the file path to the input element
                        # resume_upload.send_keys(resume_file_path)



                        # # Wait for the file input element to appear
                        # file_input = WebDriverWait(self.driver, 10).until(
                        #     EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/div/div[13]/div/div/div/input"))
                        # )

                        # Send the file path to the file input element
                        # file_input.send_keys(file_path)

                        # Step 1: Click the button that triggers the alert
                        submit_button = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div[7]/button[2]"))
                        )

                        self.driver.execute_script("arguments[0].click();", submit_button)
                        time.sleep(3)

                        # Step 2: Wait for the alert to appear and switch to it
                        alert = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div[7]/button[2]")

                        self.driver.execute_script("arguments[0].click();", alert)

                        jobs = self.driver.find_element(By.XPATH,
                                                   "/html/body/div[1]/div[1]/div[2]/div[2]/div[2]/button/div")
                        self.driver.execute_script("arguments[0].click();", jobs)
                        time.sleep(3)

                        view = self.driver.find_element(By.XPATH,
                                                   "/html/body/div[1]/div[4]/div/div/div/div/div/div/div[3]/button")
                        self.driver.execute_script("arguments[0].click();", view)
                        time.sleep(3)
                        apply = self.driver.find_element(By.XPATH,
                                                    "/html/body/div[1]/div[3]/div/div[2]/div/div[6]/button")
                        self.driver.execute_script("arguments[0].click();", apply)
                        time.sleep(3)

                        # Accept the alert (you can use alert.dismiss() to cancel)
                        apply_submit = self.driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div[2]/div[7]/button[2]")
                        self.driver.execute_script("arguments[0].click();", apply_submit)
                        time.sleep(3)



                    else:
                        print("No verification link found in the email body.")
                else:
                    print("No emails found with the specified subject.")
            else:
                print(f"No email found with the subject: {self.email_subject}")
        else:
            print("Error searching for emails.")

        mail.logout()

