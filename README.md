# TOEFL-speaker
you can add TOEFL speaking examples and playing audio with timer

---

## 📦 Building the .exe from Source (Optional)

If you want to build the standalone `.exe` application yourself from the source code, follow these steps.

### 1. Complete the Initial Setup
First, follow all the steps in the **[🚀 Installation & Setup](#-installation--setup)** section above. This includes:
-   Cloning the repository.
-   Setting up your own Google Cloud JSON key and updating the filename in `speaking.py`.
-   Creating and activating the virtual environment (`venv`).
-   Installing all dependencies with `pip install -r requirements.txt`.

**Important**: Make sure `pyinstaller` is included in your `requirements.txt` file. If not, install it in your virtual environment and update the file:
```bash
pip install pyinstaller
pip freeze > requirements.txt
