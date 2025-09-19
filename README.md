# TOEFL Speaking Practice App

A GUI application built with Python and Tkinter to help users practice for the TOEFL independent speaking task. This app provides a practice environment with AI-generated voice, timers, and recording functionality.



---

## ⬇️ Download the App

If you are not a developer and just want to use the program, you can download the ready-to-use application from our Releases page. No installation is needed!

➡️ **[Download the latest .exe from Releases](https://github.com/HJ-Leonardo-Cho/TOEFL-speaker/releases)**
(last update 2025-09-19)
---



<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>


---
## 📖 For Developers: Running from Source Or Add your own questions!

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

####             1. Go to the Google Cloud Platform Console: You will need a Google account.

####             2. Create a New Project: If you don't have one already.

####             3. Enable the Cloud Text-to-Speech API: Use the search bar to find and enable this API for your project.

####             4. Create a Service Account:

            Go to `IAM & Admin` > `Service Accounts`.

            Click `+ CREATE SERVICE ACCOUNT`.

            Give it a name (e.g., `toefl-speaker-key`) and click `CREATE AND CONTINUE`.

            For the role, select `Basic` > `Owner` for simplicity. Click `CONTINUE`, then `DONE`.

#### 5. Download the JSON Key:

            Click on the newly created service account.

            Go to the **KEYS** tab.

            Click `ADD KEY` > `Create new key`.

            Select JSON as the key type and click `CREATE`. A `.json` file will be downloaded immediately.

#### 6. Place the Key and Update the Code:

            Move the downloaded `.json` file into the cloned `TOEFL-speaker` folder.

            Open `speaking.py` with a text editor and update the `GCP_KEY_FILE` variable with your exact filename.

#### Step 2.3: Set Up Google Cloud JSON Key (Very Important!)
            Using a virtual environment (`venv`) is the best practice to keep project dependencies isolated.

#####             1. Create the venv (run this command in the TOEFL-speaker folder):
```bash
python -m venv venv
```

#####             2. Activate the venv:
```bash
# On Windows:
.\venv\Scripts\activate
```
            After activation, your terminal prompt should start with (`venv`).


#### Step 2.4: Install Dependencies with pip
            `pip` is Python's package installer. The `requirements.txt` file lists all the necessary libraries for this project. Install them with a single command:
```bash
pip install -r requirements.txt
```
#####             ▶️ 3. How to Run the Application
            Once you have completed all the setup steps, you can run the application from your terminal (make sure your virtual environment is still activated):
```bash
python speaking.py
```
####             4. Building the .exe from Source (Optional, but convenient)
            If you want to build the standalone `.exe` GUI application yourself, follow these additional steps.

#####             1. Ensure PyInstaller is installed: The `requirements.txt` file should include `pyinstaller`. If not, install it
```bash
pip install pyinstaller
```
#####             2. Run the Build Command:
            Make sure to replace `"your-key-file-name.json"` with your actual key filename.
```bash
pyinstaller --onefile --windowed --add-data "questions_vol1.csv;." --add-data "your-key-file-name.json;." speaking.py
```
            `"questions_vol1.csv"` is pre-provided question list. You can use your own csv files when you build TOEFL-speaker.

#####             3. Find the Executable: The final `speaking.exe` file will be located in the newly created `dist` folder.







