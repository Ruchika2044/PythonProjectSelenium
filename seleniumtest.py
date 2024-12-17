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
import random
import string
import re
import time

from selenium.webdriver.common.by import By
from seleniumbase import BaseCase


class JobApplicationTest(BaseCase):


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

    def test_register_and_apply(self):
        # Step 1: Navigate to the website
        self.open("https://mcitcareerssd.elevatus.io/")
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

        # Step 3: Verify Email (Log in to webmail and click the verification link)
        self.open("https://www.gmail.com/")
        # self.click("button:contains('Sign In')")
        self.type("#identifierId", 'r.agarwal@elevatus.io')  # Enter the email used for registration
        self.click("#identifierNext")
        time.sleep(2)  # Wait for the password field to load
        self.type("input[type='password']", 'Jimmy_12345678900')  # Replace with your email password
        self.click("#passwordNext")

        # # Wait for the inbox to load and search for the verification email
        self.assert_text("Inbox", "body","",50)
        self.type("input[aria-label='Search mail']", "nidalcc - You have been successfully registered!")
        """Clicks the first email in the search results and clicks the verification link."""
        # Wait for the first email to appear in the search results
        self.wait_for_element("//tr[contains(@class, 'zA')]", timeout=20, by=By.XPATH)
        self.click("//tr[contains(@class, 'zA')]", by=By.XPATH)

        # Wait for the email content to load and click the verification link
        self.wait_for_element(f"a:contains('Click Here')", timeout=20)
        self.click(f"a:contains('Click Here')")


        # Step 5: Validate successful navigation (Optional)
        # time.sleep(5)  # Wait for the new page to load
        # print("Verification process completed successfully.")
        # # # Step 3: Fill the profile manually
        # # self.click("button:contains('Fill Profile Manually')")
        # # self.type("#address", "123 Test Street")
        # # self.type("#phone", "0123456789")
        # # self.type("#qualification", "Bachelor's Degree")
        # # self.type("#experience", "3 years of software development")
        # # self.click("button:contains('Save Profile')")
        # #
        # # # Validation 5: Assert profile save success message
        # # self.assert_text("Profile saved successfully", ".alert-success")
        # #
        # Step 4: Apply for a job

        self.click("button:contains('Jobs')")  # Navigate to job listings
        self.click("button:contains('View')")  # Navigate to job listings
        self.click("button:contains('Apply')")  # Navigate to job listings
        # / html / body / div[1] / div[3] / div / div[2] / div / div[6] / button / span


        # Wait to observe the behavior

        # # Fill application form
        self.type("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/div/div[2]/div/textarea[1]", "I am excited to apply for this position.")
        self.type("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/div/div[3]/div[2]/div/div/div/div/div/div/input","1985-05-22")
        self.type("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/div/div[3]/div[3]/div/div/div/input","Female")
        self.type("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/div/div[4]/div/div/input","Indian")
        self.click("label:contains('Drag and drop or click to upload your CV')")  # Adjust selector if needed

        # / html / body / div[1] / div[2] / div / div[2] / div[1] / div[2] / div / div[13] / div / div / div
        resume_file_path = "/users/otf/Downloads/resume.pdf"  # Replace with the absolute path to your resume
        self.choose_file("input[type='file']", resume_file_path)  # Make sure this matches the <input> element
        self.assert_text("File uploaded successfully", ".alert-success")  # Adjust text/selector if needed

        # self.choose_file("/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/div/div[13]/div/div/div/p/span/span", resume_file_path)  # Dynamic resume if needed
        self.click("button:contains('Submit')")
        self.click("button:contains('Confirm')")
        self.accept_alert()

        self.click("button:contains('Jobs')")
        self.click("button:contains('View')")
        self.click("button:contains('Apply')")




         # Step 6: Generate Test Report
        # self.create_report()  # SeleniumBase automatically generates an HTML report in the 'reports/' directory
