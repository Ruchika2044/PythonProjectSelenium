import os
import random
import string
import re
from selenium.webdriver.common.by import By
from seleniumbase import BaseCase

from locators import Locators


class JobApplicationTest(BaseCase):
    """Automated script to register, verify email, and apply for a job."""

    def set_up_script(self):
        """Setup base URL and test preconditions."""
        self.base_url = "https://mcitcareerssd.elevatus.io/"
        self.email_service_url = "https://www.gmail.com/"
        self.email_user = "r.agarwal@elevatus.io"
        self.email_password = "Jimmy_12345678900"
        self.resume_path = os.path.abspath("/users/otf/Downloads/resume.pdf")

    def generate_random_email(self):
        """Generate a random email address for registration."""
        return f"r.agarwal+{random.randint(100, 999)}@elevatus.io"

    def generate_random_password(self):
        """Generate a secure random password."""
        while True:
            password = ''.join(
                random.choices(string.ascii_lowercase, k=4) +
                random.choices(string.ascii_uppercase, k=2) +
                random.choices(string.digits, k=2) +
                random.choices("!@#$%^&*", k=2)
            )
            if self.validate_password(password):
                return ''.join(random.sample(password, len(password)))

    def validate_password(self, password):
        """Validate the password against security requirements."""
        if (
                len(password) >= 8 and
                re.search(r"[A-Z]", password) and
                re.search(r"[0-9]", password) and
                re.search(r"[!@#$%^&*]", password)
        ):
            return True
        return False

    def fill_registration_form(self):
        """Step 1: Fill out the registration form with random data."""
        self.open(self.base_url)
        self.assert_title("Career portal")

        self.click("button:contains('Register')")

        # Generate dynamic user data
        first_name = ''.join(random.choices(string.ascii_letters, k=8))
        last_name = ''.join(random.choices(string.ascii_letters, k=8))
        email = self.generate_random_email()
        password = self.generate_random_password()

        # Fill the registration form
        self.type(Locators.first_name_field, first_name)
        self.type(Locators.last_name_field, last_name)
        self.type(Locators.email_field, email)
        self.type(Locators.password_field, password)
        self.type(Locators.confirm_password_field, password)
        self.type(Locators.phone_number_field, "98912969")

        self.click(Locators.checkbox_label)  # Assuming this is the checkbox ID
        self.click("button:contains('Sign up')")

        print(f"Registered with email: {email} and password: {password}")
        return email, password

    def verify_email(self, email_subject="nidalcc - You have been successfully registered!"):
        """Step 2: Log into Gmail and verify the registration email."""
        self.open(self.email_service_url)
        self.type("#identifierId", self.email_user)
        self.click("#identifierNext")

        self.wait_for_element("input[type='password']", timeout=10)
        self.type("input[type='password']", self.email_password)
        self.click("#passwordNext")

        # Search for the email
        self.wait_for_element("input[aria-label='Search mail']", timeout=10)
        self.type("input[aria-label='Search mail']", email_subject)
        # self.press_enter("input[aria-label='Search mail']")

        # Click the first email in the search results
        self.wait_for_element("//tr[contains(@class, 'zA')]", timeout=20)
        self.click("//tr[contains(@class, 'zA')]")

        # Click the verification link
        self.wait_for_element("a:contains('Click Here')", timeout=20)
        self.click("a:contains('Click Here')")
        print("Verification email clicked successfully.")

    def apply_for_job(self):
        """Step 3: Fill out the job application form and upload a resume."""
        self.click("button:contains('Jobs')")
        self.click("button:contains('View')")
        self.click("button:contains('Apply')")

        # Fill out application details
        self.type(Locators.desc_label, "I am excited to apply for this position.")
        self.type(Locators.date_of_birth_label, "1985-05-22")
        self.type(Locators.gender_label, "Female")
        self.type(Locators.nationality, "Indian")
        self.click("label:contains('Drag and drop or click to upload your CV')")  # Adjust selector if needed

        # Upload resume
        self.choose_file("input[type='file']", self.resume_path)
        self.wait_for_element(".alert-success", timeout=10)
        self.assert_text("File uploaded successfully", ".alert-success")

        # Submit application
        self.click("button:contains('Submit')")
        if self.is_element_visible("button:contains('Confirm')", 10):
            self.click("button:contains('Confirm')")
        if self.is_alert_present():
            self.accept_alert()
        print("Job application submitted successfully.")

    def test_register_verify_and_apply(self):
        """End-to-End Test: Register, verify email, and apply for a job."""
        email, _ = self.fill_registration_form()
        self.verify_email()
        self.apply_for_job()
