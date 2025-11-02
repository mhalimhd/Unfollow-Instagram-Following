# Simple Instagram Unfollower

This tool automatically unfollows Instagram accounts using your session ID for authentication. It's designed for users who want to quickly reduce their following count without manually clicking each account.

## ⚠️ Important Notice

This tool is for educational purposes only. Use at your own risk:
- Instagram may temporarily lock accounts that unfollow too many users too quickly
- Rate limits may block further unfollowing during a session
- This tool attempts to mimic human behavior but is not guaranteed to avoid detection

## 🛠️ Prerequisites

### 1. Python Installation

1. Download Python 3.8 or higher from [python.org](https://www.python.org/downloads/)
2. During installation:
   - Check "Add Python to PATH"
   - Choose "Install for all users" if prompted
3. Verify installation by opening Command Prompt and typing:
   ```bash
   python --version
   ```

### 2. Chrome Browser

Download Google Chrome from [google.com/chrome](https://www.google.com/chrome/)

### 3. ChromeDriver (Automatically Installed)

This tool uses Selenium which will automatically download ChromeDriver. No manual installation required.

## 📦 Installation

1. Download or clone this repository
2. Open Command Prompt as Administrator
3. Navigate to the folder containing the script:
   ```bash
   cd C:\path\to\your\downloaded\folder
   ```
4. Install required packages:
   ```bash
   pip install selenium
   ```

## 🔧 Setup & Usage

### 1. Get Your Instagram Session ID

1. Log into Instagram in Chrome
2. Press `F12` to open Developer Tools
3. Go to Application tab → Cookies → https://www.instagram.com
4. Find `sessionid` cookie and copy its value

### 2. Run the Script

1. Open Command Prompt
2. Navigate to the script folder:
   ```bash
   cd C:\path\to\your\folder
   ```
3. Run the script:
   ```bash
   python unfollow.py
   ```

### 3. Enter Information When Prompted

1. Paste your `sessionid` when prompted
2. Enter your Instagram username
3. Type `UNFOLLOW` to confirm

### 4. Choose How Many to Unfollow

- Enter a number to unfollow that many accounts
- Press Enter to unfollow all accounts

## ⚙️ Troubleshooting

### If the Tool Doesn't Open the Following List

If the tool fails to navigate to your following list:
1. Manually go to `https://www.instagram.com/[your-username]/following/`
2. Press Enter in the tool to continue

### If the Tool Doesn't Scroll Properly

If the tool stops finding accounts to unfollow:
1. Manually scroll down the following list
2. The tool will continue processing as you scroll
3. Ensure accounts with "Following" buttons are visible

### If Buttons Are Not Clicked

If unfollow buttons aren't clicked:
1. Manually click the "Following" buttons
2. The tool will count these as processed

## 📝 Notes

- Processing speed: ~12 unfollows per second
- Auto-scrolls every 12 accounts processed
- Keeps track of processed accounts to avoid duplicates
- Shows live count of unfollowed accounts and remaining
- Safe exit with `Ctrl+C`

## ⚖️ Legal Disclaimer

This tool is not affiliated with Instagram or Meta. Use responsibly according to Instagram's Terms of Service. Automated unfollowing may violate Instagram's policies and could result in account restrictions.


## 🚀 Connect With Me!

| Platform | Handle/Link |
| :--- | :--- |
| **WhatsApp** | `+961 81 145 410` |
| **Website** | [![Website](https://img.shields.io/badge/My_Website-Visit%20Now-29B6F6?style=for-the-badge&logo=google-chrome&logoColor=white)](https://mhalimhd-2025.web.app) |
