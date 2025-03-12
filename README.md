# LinkedinToMD
Backup your LinkedIn profile as a clean, readable Markdown file using a robust, structure-based parsing approach.

## Features
- Robust Parsing Logic: Unlike common scrapers that rely on fragile HTML IDs or class names, this tool uses a semantic header and text stream approach. It identifies sections (like "Experience" or "Skills") by their display titles and parses the subsequent list structures, making it more resilient to UI updates.
- Session Persistence: Automatically creates a `web_driver_profile` directory to store browser cookies and session data, reducing the need for repeated logins and manual 2FA.
- Nested List Support: Specifically handles complex, multi-level list structures common in the "Experience" section to maintain the hierarchy of your career history.
- Customizable Sections: Easily toggle which profile sections to extract (About, Experience, Education, Projects, Skills, etc.) via the internal configuration.
- Security: Supports .env files for managing credentials to keep sensitive information out of the source code.

## Environment Setup

### Windows
```cmd
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### Linux
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

1. Configure Credentials
Create a .env file in the root directory and fill in your LinkedIn credentials:

```env
LINKEDIN_USERNAME=your_email@example.com
LINKEDIN_PASSWORD=your_password
```

2. Run the Script
### Windows
```cmd
.\.venv\Scripts\activate
python linkedin_to_md.py
```
### Linux
```sh
source .venv/bin/activate
python3 linkedin_to_md.py
```
After execution, a file named linkedin_profile.md will be generated.

## Technical Notes
- 2FA & Verification: If Two-Factor Authentication (2FA) is enabled, the script includes a 15-second delay to allow for manual verification in the browser window.
- Browser Profile: A local directory `web_driver_profile` is used to persist your browser session. Do not delete this if you want to stay logged in.
- Dependencies: Requires Chrome browser and a compatible ChromeDriver. (Latest Selenium versions usually handle ChromeDriver automatically).

---
This tool is for personal backup purposes only. Please comply with LinkedIn's Terms of Service.
