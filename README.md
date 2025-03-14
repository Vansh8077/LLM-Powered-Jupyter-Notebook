# 🔮 LLM-Powered Jupyter Notebook

An intelligent Jupyter Notebook powered by the **Groq API** that automatically sets up an LLM-powered session, extracts user inputs, and provides **real-time code explanations, debugging, and solutions**.

## ✨ Features

✅ **Automatic Session Management**: Checks for an active Jupyter session and creates one if not found.  
✅ **LLM Integration**: Uses **Groq API** for AI-assisted coding, debugging, and explanations.  
✅ **Keyboard Shortcuts**:  
   - **Cmd + Shift + Z (Mac)** or **Ctrl + Shift + Z (Windows)** → Copy multiple contents  
   - **Cmd + Shift + X (Mac)** or **Ctrl + Shift + X (Windows)** → Process user input for errors, questions, or code  
✅ **Auto-Extract API Key**: Automatically retrieves and saves the **Groq API key** for seamless access.  
✅ **One-Click App Execution**: Converts the Python script into an **executable** (`.app` for Mac, `.exe` for Windows - under development).  

---

## 🛠️ How It Works

1️⃣ **Launches Jupyter Notebook** automatically.  
2️⃣ **Prompts the user** to enter a **Groq API key** (auto-extracted for ease).  
3️⃣ **User interacts** with the notebook, entering **code, debugging queries, or questions**.  
4️⃣ **AI-powered assistant** processes inputs and provides **solutions, explanations, and debugging help**.  
5️⃣ **Shortcut-based workflow** for seamless usage.  

---

## 📌 Usage Instructions

1. **Start Jupyter** by running the script or opening the app.  
2. **Enter the Groq API Key** when prompted.  
3. **Use keyboard shortcuts for quick actions:**  
   - **Cmd + Shift + Z** → Copy content  
   - **Cmd + Shift + X** → Process input and receive AI-generated explanations  

---

## 🚧 Windows Support Notice

⚠️ **Currently, this project is fully functional on macOS.**  
Windows support is still under development and will be available in future updates.  

---

## 🔗 Contributions & Issues

Feel free to **raise an issue** or **contribute** to this project! 🚀  


## 🚀 Setup and Run the LLM-Powered Jupyter Notebook

### 1️⃣ Clone the Repository
   - **A)** `git clone https://github.com/Vansh8077/LLM-Powered-Jupyter-Notebook`
   - **B)** `cd LLM-Powered-Jupyter-Notebook`

### 2️⃣ Install Dependencies
   Ensure you have Python installed, then install the required dependencies using:
   - **A)** `pip install -r requirements.txt`

### 3️⃣ Run the LLM-Powered Notebook
   - **A)** `python llm-powered-notebook.py`

### 4️⃣ (Optional) Run in a Virtual Environment
   To avoid conflicts, you can use a virtual environment:
   - **A)** `python -m venv venv`
   - **B)** `source venv/bin/activate`  *(On Windows use: `venv\Scripts\activate`)*
   - **C)** `pip install -r requirements.txt`
   - **D)** `python llm-powered-notebook.py`
