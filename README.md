Selenium Python Script: Job Application Automation
This project automates the following steps for a job application process:

User Registration on a career portal.
Email Verification via Gmail.
Job Application Submission with a resume upload.
Features
Dynamic user registration with randomized credentials.
Automated Gmail login and email verification.
Automated job application form submission.
Prerequisites
1. Python
Install Python 3.10 or higher. Download Python

2. Selenium Web Driver
This project uses SeleniumBase, which automatically manages web drivers for supported browsers (e.g., Chrome).

3. Browser
Google Chrome must be installed. Download Chrome

Installation
Step 1: Clone the Repository
bash
Copy code
git clone https://github.com/your-repo-name/selenium-job-application.git  
cd selenium-job-application  
Step 2: Set Up Virtual Environment
bash
Copy code
python3 -m venv venv  
source venv/bin/activate  # On Windows, use venv\Scripts\activate  
Step 3: Install Dependencies
bash
Copy code
pip install seleniumbase  
pip install -r requirements.txt  
Configuration
Update Login Details and File Paths
Edit the script (e.g., selenium_test.py) to update the following:

Gmail Login Credentials:

python
Copy code
GMAIL_USERNAME = "your-email@example.com"  
GMAIL_PASSWORD = "your-password"  
Resume File Path:

python
Copy code
resume_file_path = "/absolute/path/to/your/resume.pdf"  
Running the Script
Execute the Script
Run the following command in your terminal:

bash
Copy code
pytest selenium_test.py --browser=chrome --headed  
Parameters
--browser=chrome: Specifies the browser to use (Chrome is default).
--headed: Runs the browser in a visible mode (omit for headless mode).
selenium_test.py: Replace with the actual script name if different.
Sample Output
The script will:

Register a new user on the career portal.
Log into Gmail, search for the verification email, and click the confirmation link.
Navigate to the career portal, apply for a job, and submit the application.
