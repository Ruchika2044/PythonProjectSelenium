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
from nntplib import decode_header

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
                        # webbrowser.open(verification_link)


                        # Step 1: Set up WebDriver
                        driver_path = "/opt/homebrew/bin/chromedriver"  # Replace with your ChromeDriver path
                        driver = webdriver.Chrome(service=Service(driver_path))

                        try:
                            # Step 2: Open the target webpage
                            driver.get(verification_link)  # Replace with your target URL

                            cookie_button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH,
                                                            "//button[contains(text(), 'Accept') or contains(text(), 'Agree') or contains(text(), 'Close')]"))
                            )

                            # Click the button to close the pop-up
                            cookie_button.click()
                            # Step 3: Wait for the button to be clickable
                            button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, "//button[text()='Fill in manually']"))
                                # Replace XPath as needed
                            )

                            # Step 4: Click the button
                            button.click()
                            # Fill application form
                            # self.driver.find_element(By.XPATH, "//textarea[@id = 'description']").send_keys("I am excited to apply for this position.")
                            # Wait for the element to be present
                            wait = WebDriverWait(driver, 10)
                            description_input = wait.until(EC.presence_of_element_located((By.ID, "description")))

                            # Interact with the element
                            description_input.send_keys("Your description here. I want to apply here")
                            date_input = driver.find_element(By.ID ,"date-picker-dialog--0---0-0-undefined")  # Replace with the actual ID of the date field
                            date_input.clear()
                            date_input.send_keys("1985-05-22")

                            gender_input = driver.find_element(By.XPATH,
                                                               "//input[@id='gender']")  # Replace with the actual ID of the date field
                            gender_input.click()

                            # Select an option by its text
                            option = driver.find_element(By.ID,
                                                         "gender-option-1")  # Replace with the actual locator
                            option.click()
                            # gender_input.send_keys("Female")

                            # # Select an option by its text
                            # option = driver.find_element(By.ID,
                            #                              "gender-option-1")  # Replace with the actual locator
                            # option.click()

                            nationality_input = driver.find_element(By.ID,
                                                             "nationality")  # Replace with the actual ID of the date field
                            nationality_input.click()

                            # Select an option by its text
                            option = driver.find_element(By.ID,"nationality-option-79")  # Replace with the actual locator
                            option.click()



                            city_input = driver.find_element(By.ID,
                                                                    "city")  # Replace with the actual ID of the date field
                            city_input.send_keys("Muscat")

                            # Step 1: Click the button that triggers the alert
                            submit_button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div[7]/button[2]"))
                            )
                            driver.execute_script("arguments[0].click();", submit_button)

                            # submit_button.click()

                            # Step 2: Wait for the alert to appear and switch to it
                            alert = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div[7]/button[2]")
                            driver.execute_script("arguments[0].click();", alert)

                            jobs = driver.find_element(By.XPATH,
                                                        "/html/body/div[1]/div[1]/div[2]/div[2]/div[2]/button/div")
                            driver.execute_script("arguments[0].click();", jobs)
                            time.sleep(3)

                            view = driver.find_element(By.XPATH,
                                                       "/html/body/div[1]/div[4]/div/div/div/div/div/div/div[3]/button")
                            driver.execute_script("arguments[0].click();", view)
                            time.sleep(3)
                            apply = driver.find_element(By.XPATH,
                                                       "/html/body/div[1]/div[3]/div/div[2]/div/div[6]/button")
                            driver.execute_script("arguments[0].click();", apply)
                            time.sleep(3)


                            # Step 3: Accept the alert (Click "OK" or "Confirm")
                            # submit_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div[7]/button[2]")  # Replace with the actual locator
                            #
                            # # Step 4: Click the button
                            # driver.execute_script("arguments[0].click();", submit_button)


                            # resume_file_path = "/users/otf/Downloads/resume.pdf"  # Replace with the absolute path to your resume
                            # # Wait for the file input element to be present and visible
                            # file_input = driver.find_element(By.XPATH,"//div[contains(@class,'mt-1 mb-3 row')]//div[contains(@class,'col-lg-12')]//div//div[contains(@role,'button')]"
                            #                                 )
                            #
                            # file_input.click()
                            #
                            # # Provide the file path to the file input element
                            # file_input.send_keys(resume_file_path)
                            # Wait for the button to be clickable



                            # self.type("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/div/div[2]/div/textarea[1]", "I am excited to apply for this position.")
                            # # self.type("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/div/div[3]/div[2]/div/div/div/div/div/div/input","1985-05-22")
                            # # self.type("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/div/div[3]/div[3]/div/div/div/input","Female")
                            # # self.type("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/div/div[4]/div/div/input","Indian")
                            # self.click("label:contains('Drag and drop or click to upload your CV')")  # Adjust selector if needed
                            # #         #
                            # #         #  # / html / body / div[1] / div[2] / div / div[2] / div[1] / div[2] / div / div[13] / div / div / div
                            # resume_file_path = "/users/otf/Downloads/resume.pdf"  # Replace with the absolute path to your resume
                            # self.choose_file("input[type='file']", resume_file_path)  # Make sure this matches the <input> element
                            # self.assert_text("File uploaded successfully", ".alert-success")  # Adjust text/selector if needed
                            # #         #
                            # #         # self.choose_file("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/div/div[13]/div/div/div/p/span/span", resume_file_path)  # Dynamic resume if needed
                            # self.click("button:contains('Submit')")
                            # self.click("button:contains('Confirm')")
                            # self.accept_alert()
                            # #         #
                            # self.click("button:contains('Jobs')")
                            # self.click("button:contains('View')")
                            # self.click("button:contains('Apply')")
                            # #         #
                            # #         print("Submit button clicked successfully.")
                            # print("Button clicked successfully.")

                        finally:
                            # Step 5: Close the browser
                            driver.quit()

                        # / opt / homebrew / bin / chromedriver
                        # self.wait_for_element_visible("//button[text()='Fill in manually']", timeout=10)
                        # self.click("button:contains('Fill in manually')")
                        # self.click("//button[text()='Fill in manually']")
                    else:
                        print("No verification link found in the email body.")
                else:
                    print("No emails found with the specified subject.")
            else:
                print(f"No email found with the subject: {self.email_subject}")
        else:
            print("Error searching for emails.")

        mail.logout()

    # def open_link_and_click_submit(link, self):
    #     """Open the verification link in a browser and click the submit button."""
    #     # Setup WebDriver
    #     chrome_options = Options()
    #     chrome_options.add_argument("--start-maximized")
    #     driver = webdriver.Chrome(service=Service("/path/to/chromedriver"), options=chrome_options)
    #
    #     try:
    #         # Open the verification link
    #         driver.get(link)
    #
    #         # Wait for the submit button to become visible
    #         submit_button = WebDriverWait(driver, 20).until(
    #             EC.visibility_of_element_located((By.XPATH, "//button[text()='Fill in manually']"))  # Adjust XPath as needed
    #         )
    #
    #         # Click the submit button
    #         submit_button.click()
    #         # Fill application form
    #         self.type("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/div/div[2]/div/textarea[1]", "I am excited to apply for this position.")
    #         self.type("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/div/div[3]/div[2]/div/div/div/div/div/div/input","1985-05-22")
    #         self.type("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/div/div[3]/div[3]/div/div/div/input","Female")
    #         self.type("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/div/div[4]/div/div/input","Indian")
    #         self.click("label:contains('Drag and drop or click to upload your CV')")  # Adjust selector if needed
    #         #
    #         #  # / html / body / div[1] / div[2] / div / div[2] / div[1] / div[2] / div / div[13] / div / div / div
    #         resume_file_path = "/users/otf/Downloads/resume.pdf"  # Replace with the absolute path to your resume
    #         self.choose_file("input[type='file']", resume_file_path)  # Make sure this matches the <input> element
    #         self.assert_text("File uploaded successfully", ".alert-success")  # Adjust text/selector if needed
    #         #
    #         # self.choose_file("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/div/div[13]/div/div/div/p/span/span", resume_file_path)  # Dynamic resume if needed
    #         self.click("button:contains('Submit')")
    #         self.click("button:contains('Confirm')")
    #         self.accept_alert()
    #         #
    #         self.click("button:contains('Jobs')")
    #         self.click("button:contains('View')")
    #         self.click("button:contains('Apply')")
    #         #
    #         print("Submit button clicked successfully.")
    #
    #         # Keep the browser open for observation
    #         input("Press Enter to close the browser...")
    #
    #     finally:
    #         driver.quit()

# # below code was commented
       #
       #  self.open("https://mail.google.com/")
       #  # self.click("button:contains('Sign In')")
       #  self.type("#identifierId", 'r.agarwal@elevatus.io')  # Enter the email used for registration
       #  self.click("#identifierNext")
       #  time.sleep(2)  # Wait for the password field to load
       #  self.type("input[type='password']", 'vzxb vvdv dvkw dpim')  # Replace with your email password
       #  self.click("#passwordNext")
       #
       #  # # Wait for the inbox to load and search for the verification email
       #  self.assert_text("Inbox", "body","",50)
       #  self.type("input[aria-label='Search mail']", "nidalcc - You have been successfully registered!")
       #  """Clicks the first email in the search results and clicks the verification link."""
       #  # Wait for the first email to appear in the search results
       #  self.wait_for_element("//tr[contains(@class, 'zA')]", timeout=20, by=By.XPATH)
       #  self.click("//tr[contains(@class, 'zA')]", by=By.XPATH)
       #
       #  # Wait for the email content to load and click the verification link
       #  self.wait_for_element(f"a:contains('Click Here')", timeout=20)
       #  self.click(f"a:contains('Click Here')")
       #
       #
       #  # Step 5: Validate successful navigation (Optional)
       #  # time.sleep(5)  # Wait for the new page to load
       #  # print("Verification process completed successfully.")
       #  # # # Step 3: Fill the profile manually
       #  # # self.click("button:contains('Fill Profile Manually')")
       #  # # self.type("#address", "123 Test Street")
       #  # # self.type("#phone", "0123456789")
       #  # # self.type("#qualification", "Bachelor's Degree")
       #  # # self.type("#experience", "3 years of software development")
       #  # # self.click("button:contains('Save Profile')")
       #  # #
       #  # # # Validation 5: Assert profile save success message
       #  # # self.assert_text("Profile saved successfully", ".alert-success")
       #  # #
       #  # Step 4: Apply for a job
       #
       #  self.click("button:contains('Jobs')")  # Navigate to job listings
       #  self.click("button:contains('View')")  # Navigate to job listings
       #  self.click("button:contains('Apply')")  # Navigate to job listings
       #  # / html / body / div[1] / div[3] / div / div[2] / div / div[6] / button / span
       #
       #
       #  # Wait to observe the behavior
       #
       #  # # Fill application form
       #  self.type("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/div/div[2]/div/textarea[1]", "I am excited to apply for this position.")
       #  self.type("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/div/div[3]/div[2]/div/div/div/div/div/div/input","1985-05-22")
       #  self.type("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/div/div[3]/div[3]/div/div/div/input","Female")
       #  self.type("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/div/div[4]/div/div/input","Indian")
       #  self.click("label:contains('Drag and drop or click to upload your CV')")  # Adjust selector if needed
       #
       #  # / html / body / div[1] / div[2] / div / div[2] / div[1] / div[2] / div / div[13] / div / div / div
       #  resume_file_path = "/users/otf/Downloads/resume.pdf"  # Replace with the absolute path to your resume
       #  self.choose_file("input[type='file']", resume_file_path)  # Make sure this matches the <input> element
       #  self.assert_text("File uploaded successfully", ".alert-success")  # Adjust text/selector if needed
       #
       #  # self.choose_file("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/div/div[13]/div/div/div/p/span/span", resume_file_path)  # Dynamic resume if needed
       #  self.click("button:contains('Submit')")
       #  self.click("button:contains('Confirm')")
       #  self.accept_alert()
       #
       #  self.click("button:contains('Jobs')")
       #  self.click("button:contains('View')")
       #  self.click("button:contains('Apply')")
       #
       #
       #
       #
       #   # Step 6: Generate Test Report
       #  # self.create_report()  # SeleniumBase automatically generates an HTML report in the 'reports/' directory
