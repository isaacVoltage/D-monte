# 🚀 How to Run This Project on Any Laptop

Share these instructions with anyone who wants to run this project on their computer.

---

## 📋 Prerequisites
Make sure **Python (version 3.8 or higher)** is installed on the laptop:
- Download from: [python.org/downloads](https://www.python.org/downloads/)
- ⚠️ **Important during installation:** Check the box that says **"Add Python to PATH"**.

---

## 💻 Step-by-Step Instructions

### Step 1: Get the Code
Open **Terminal** (Mac/Linux) or **Command Prompt / PowerShell** (Windows):

```bash
git clone https://github.com/isaacVoltage/D-monte.git
cd D-monte
```

*(Alternatively, if they received the project as a `.zip` file, extract the folder, open Command Prompt or Terminal, and `cd` into that folder).*

---

### Step 2: (Optional but Recommended) Create a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

---

### Step 3: Install Required Dependencies
Run:
```bash
pip install -r requirements.txt
```
*(This installs `streamlit`, `pandas`, and `pytest`).*

---

### Step 4: Run the Application
Start the Streamlit web dashboard:
```bash
python -m streamlit run app.py
```
*(On Mac/Linux, use `python3 -m streamlit run app.py` if needed).*

---

### Step 5: Open in Browser
Once launched, the terminal will display:
```
Local URL: http://localhost:8501
```
Open your web browser and go to **`http://localhost:8501`**.

---

## 🧪 (Optional) Run Automated Tests
To run the automated test suite and verify everything is working correctly:
```bash
python -m pytest -v
```
All 17 tests should pass.

---

## ❓ Common Troubleshooting Tips

1. **`'python' is not recognized as an internal or external command`**:
   - Python is not added to the system PATH. Re-run the Python installer, select **Modify**, and check **"Add Python to PATH"**.

2. **`'streamlit' is not recognized`**:
   - Run the command using the python module flag:
     ```bash
     python -m streamlit run app.py
     ```

3. **Port 8501 is already in use**:
   - Run on an alternative port:
     ```bash
     python -m streamlit run app.py --server.port 8502
     ```
