# TOEFL Speaking Practice App

A GUI application built with Python and Tkinter to help users practice for the TOEFL independent speaking task. This app provides a realistic practice environment with AI-generated voice, timers, and recording functionality.



---

## ⬇️ Download the App

If you are not a developer and just want to use the program, you can download the ready-to-use application from our Releases page. No installation is needed!

➡️ **[Download the latest .exe from Releases](https://github.com/HJ-Leonardo-Cho/TOEFL-speaker/releases)**

---

## 📖 For Developers: Running from Source

If you are a developer and want to run or modify the source code, please follow the detailed instructions below.

### 🛠️ 1. Prerequisites

Before you begin, ensure you have the following installed on your system:
-   **Python 3.9+**: [Download from python.org](https://www.python.org/downloads/)
-   **Git**: [Download from git-scm.com](https://git-scm.com/downloads)

---

### 🚀 2. Step-by-Step Setup Guide

#### Step 2.1: Clone the Repository
First, clone this repository to your local machine. Open your terminal (Command Prompt, PowerShell, or Git Bash) and run the following command:
```bash
git clone [https://github.com/HJ-Leonardo-Cho/TOEFL-speaker.git](https://github.com/HJ-Leonardo-Cho/TOEFL-speaker.git)
cd TOEFL-speaker
```


#### Step 2.2: Set Up Google Cloud JSON Key (Very Important!)
This application requires a Google Cloud Platform service account key to use the Text-to-Speech API. This key is your private credential and should NEVER be shared publicly.

#### 1. Go to the Google Cloud Platform Console: You will need a Google account.

#### 2. Create a New Project: If you don't have one already.

#### 3. Enable the Cloud Text-to-Speech API: Use the search bar to find and enable this API for your project.

#### 4. Create a Service Account:

Go to IAM & Admin > Service Accounts.

Click + CREATE SERVICE ACCOUNT.

Give it a name (e.g., toefl-speaker-key) and click CREATE AND CONTINUE.

For the role, select Basic > Owner for simplicity. Click CONTINUE, then DONE.

Download the JSON Key:

Click on the newly created service account.

Go to the KEYS tab.

Click ADD KEY > Create new key.

Select JSON as the key type and click CREATE. A .json file will be downloaded immediately.

Place the Key and Update the Code:

Move the downloaded .json file into the cloned TOEFL-speaker folder.

Open speaking.py with a text editor and update the GCP_KEY_FILE variable with your exact filename.


