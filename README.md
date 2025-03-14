🔮 LLM-Powered Jupyter Notebook

An intelligent Jupyter Notebook powered by Groq API that automatically sets up an LLM-powered session, extracts user inputs, and provides real-time code explanations, debugging, and solutions.

✨ Features

✅ Automatic Session Management: Checks for an active Jupyter session and creates one if not found.
✅ LLM Integration: Uses Groq API for AI-assisted coding, debugging, and explanations.
✅ Keyboard Shortcuts:

Cmd + Shift + Z (Mac) or Ctrl + Shift + Z (Windows) → Copy multiple contents
Cmd + Shift + X (Mac) or Ctrl + Shift + X (Windows) → Process user input for errors, questions, or code
✅ Auto-Extract API Key: Automatically retrieves and saves the Groq API key for seamless access.
✅ One-Click App Execution: Converts the Python script into an executable (.exe for Windows, .app for Mac) for easy use.



🛠️ How It Works

1️⃣ Launches Jupyter Notebook automatically.
2️⃣ Prompts the user to enter a Groq API key (auto-extracted for ease).
3️⃣ User interacts with the notebook, entering code, debugging queries, or questions.
4️⃣ AI-powered assistant processes inputs and provides solutions, explanations, and debugging help.
5️⃣ Shortcut-based workflow for seamless usage.


📌 Usage Instructions

Start Jupyter by running the script or opening the app.
Enter the Groq API Key when prompted.
Use Cmd + Shift + Z to copy content.
Use Cmd + Shift + X to process input and receive AI-generated explanations.

🔗 Contributions & Issues
Feel free to raise an issue or contribute to this project! 🚀


🚀 **Setup and Run the LLM-Powered Notebook**

1️⃣ Clone the Repository
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/Vansh8077/LLM-Powered-Jupyter-Notebook)
cd LLM-Powered-Jupyter-Notebook
2️⃣ Install Dependencies
Ensure you have Python installed, then install required dependencies using:
pip install -r requirements.txt

3️⃣ Run the LLM-Powered Notebook
Start the Python script:
python llm-powered-notebook.py

4️⃣ (Optional) Run in a Virtual Environment
To avoid conflicts, you can use a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
python llm-powered-notebook.py
