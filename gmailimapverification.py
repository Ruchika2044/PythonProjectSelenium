import imaplib
import email
from email.header import decode_header
from seleniumbase import BaseCase
import time

class GmailIMAPVerification(BaseCase):
    def fetch_latest_email(self, imap_host, email_user, app_password, email_subject):
        """Fetch the latest email matching a specific subject."""
        # Connect to the IMAP server
        mail = imaplib.IMAP4_SSL(imap_host)
        mail.login(email_user, app_password)

        # Select the inbox
        mail.select("inbox")

        # Search for the specific email by subject
        status, messages = mail.search(None, f'(SUBJECT "{email_subject}")')
        if status != "OK" or not messages[0]:
            raise ValueError(f"No email found with subject: {email_subject}")

        # Get the latest email ID
        latest_email_id = messages[0].split()[-1]

        # Fetch the email by ID
        status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
        if status != "OK":
            raise ValueError("Failed to fetch email.")

        # Parse the email content
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                # Decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # If it's a bytes object, decode to str
                    subject = subject.decode(encoding if encoding else "utf-8")

                # Get the email body
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))

                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            # Get the email body
                            body = part.get_payload(decode=True).decode()
                            return body
                else:
                    # If the email is not multipart, get the payload
                    return msg.get_payload(decode=True).decode()

        mail.logout()
        raise ValueError("Failed to extract email body.")

    def test_verify_email(self):
        # IMAP Configuration
        imap_host = "imap.gmail.com"
        email_user = "r.agarwal@elevatus.io"  # Replace with your Gmail address
        app_password = "vzxb vvdv dvkw dpim"  # Replace with your Gmail App Password
        email_subject = "Your Email Subject Here"  # Replace with the email's subject

        # Step 1: Fetch the latest email
        email_body = self.fetch_latest_email(imap_host, email_user, app_password, email_subject)

        # Step 2: Parse the email body to find the verification link
        print("Email Body:", email_body)  # For debugging purposes
        verification_link = None
        for line in email_body.splitlines():
            if "Click Here" in line or "http" in line:
                verification_link = line.strip()
                break

        if not verification_link:
            raise ValueError("Verification link not found in the email.")

        # Step 3: Open the verification link using Selenium
        self.open(verification_link)
        time.sleep(5)  # Allow time for the page to load

        # Step 4: Validate successful navigation (optional)
        assert "Expected Page Title" in self.get_title(), "Failed to navigate to the expected page."
