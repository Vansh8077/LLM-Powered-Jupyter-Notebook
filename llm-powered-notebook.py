import subprocess
import re
import requests
import json
import uuid
import jupyter_client
from selenium import webdriver
import pyperclip
import time
from pynput import keyboard
from functools import partial
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
driver = None
technical_memory=None
technical_conversation=None
import pyperclip
from pynput import keyboard
import os
import copy
copied_texts = set()
import platform
import pyautogui
#Check for jupyter server
def jupyter_server():
    result = subprocess.run(["jupyter", "notebook", "list"], capture_output=True, text=True)
    output = result.stdout.strip()
    pattern = r"(http://[^\s]+)\?token=([\w]+)"
    match = re.search(pattern, output)
    
    if not match:
        print("No running Jupyter Notebook found. Starting one...")
        subprocess.Popen(["jupyter", "notebook"])
        time.sleep(5)  # Give Jupyter time to start
        result = subprocess.run(["jupyter", "notebook", "list"], capture_output=True, text=True)
        output = result.stdout.strip()
        match = re.search(pattern, output)
    
        if not match:
            print("Failed to start Jupyter Notebook.")
            exit(1)
    
    host = match.group(1)
    token = match.group(2)
    
    print(f"Jupyter Server Found: {host}")
    print(f"Token: {token}")
    return host,token
#create jupyter notebook 
def create_notebook(host, token):
    headers = {'Authorization': f'Token {token}', 'Content-Type': 'application/json'}
    notebook_name = f"dynamic_notebook_{str(uuid.uuid1())[1:11]}.ipynb"
    notebook_path = f"{host}/api/contents/{notebook_name}"

    # Create the notebook
    notebook_data = {"type": "notebook"}
    response = requests.put(notebook_path, headers=headers, data=json.dumps(notebook_data))

    if response.status_code not in [200, 201]:
        print("Failed to create notebook.")
        exit(1)

    print("Notebook created successfully.")
    return notebook_name,notebook_path
# Step 3: Launch or reload the notebook in a browser
def launch_reload_notebook(notebook_name,token,check=0):
    notebook_url = f"{host}notebooks/{notebook_name}?token={token}"
    global driver
    if check==0: 
        driver=webdriver.Chrome() 
        driver.get(notebook_url)
        print(f"Launched Notebook: {notebook_url}")
    else:
        driver.refresh()


def save_notebook():
    """Simulates keyboard shortcut to save the Jupyter Notebook."""
    os_name = platform.system()  # Detect OS
    time.sleep(1)  # Short delay to ensure focus

    if os_name == "Darwin":  # macOS
        pyautogui.hotkey("command", "s")
    elif os_name == "Windows":  # Windows
        pyautogui.hotkey("ctrl", "s")
    else:
        print("Unsupported OS. Please save manually.")

    print("Notebook save command triggered.")


def modify_notebook(host, token, notebook_name, initial=0, gen_ai_cells=[],error_message='yes'):
    global driver
    notebook_path = f"{host}/api/contents/{notebook_name}"
    session_path = f"{host}/api/sessions"
    headers = {'Authorization': f'Token {token}', 'Content-Type': 'application/json'}
    # Step 2: Fetch session information if initial is set
    session_id = None
    if initial:
        response = requests.get(session_path, headers=headers)
        if response.status_code != 200:
            print("❌ Failed to fetch session information.")
            return False

        sessions = response.json()
        for session in sessions:
            if session['notebook']['path'] == notebook_name:
                session_id = session['id']
                break
        print(f"Session ID: {session_id}")
        if not session_id:
            print("❌ No active session found for the notebook. Ensure the notebook is open and running.")
            return False

    # Step 3: Force a checkpoint/save operation to persist outputs to disk
    checkpoint_path = f"{host}/api/contents/{notebook_name}/checkpoints"
    print(f"Checkpoint Path: {checkpoint_path}")
    response = requests.post(checkpoint_path, headers=headers)
    print(f"Checkpoint Response: {response.text}")
    if response.status_code not in [200, 201]:
        print("❌ Failed to create checkpoint/save notebook.")
        return False

    # Wait briefly to ensure the checkpoint is processed
    time.sleep(1)

    # Step 4: Fetch the current notebook content
    response = requests.get(notebook_path, headers=headers)
    if response.status_code != 200:
        print("❌ Failed to fetch notebook content.")
        return False
    notebook_content = response.json()

    # Debug: Print the fetched content to check if outputs are present
    print("Fetched Notebook Content Before Modification:")
    print(json.dumps(notebook_content, indent=2))

    # Step 5: Create a deep copy of the current content (including outputs) for backup
    original_content = copy.deepcopy(notebook_content)

    # Step 6: Set kernel metadata (if needed)
    notebook_content['content']['metadata']['kernelspec'] = {
        'display_name': 'Python 3',
        'language': 'python',
        'name': 'python3'
    }

    # Step 7: Define the dynamic cells to append
    print(error_message,len(notebook_content['content']['cells']))
    if initial == 0 and gen_ai_cells==[]:
        dynamic_cells = [
            {
                'cell_type': 'markdown',
                'metadata': {},
                'source': "# 🚀 Hello, This is an LLM-supported Jupyter Notebook\n\n"
            },
            {
                'cell_type': 'markdown',
                'metadata': {},
                'source': "[🔗 Visit Groq Dev Console](https://console.groq.com/playground)"
            },
            {
                'cell_type': 'code',
                'metadata': {'tags': ['input-cell']},
                'execution_count': None,
                'source': '''import json\n\n# Set API key and save it to a JSON file\napi_key = input("Enter your Groq API key. To generate one, visit the above link: ")\nconfig = {"groq_api_key": api_key}\n\nwith open("/tmp/config.json", "w") as f:\n    json.dump(config, f)\n\nprint("API Key saved successfully!")''',
                'outputs': []
            }
        ]
    elif initial ==0 and gen_ai_cells!=[]:
        if error_message=='yes' and len(notebook_content['content']['cells'])<=3:
            dynamic_cells=[gen_ai_cells]
        elif len(notebook_content['content']['cells'])>3 and error_message=='no':
            notebook_content['content']['cells'][3]['source']='Everything seems fine ,You can start working now'
            dynamic_cells=''
        elif len(notebook_content['content']['cells'])>3 and error_message=='yes':
            dynamic_cells=''
        elif error_message=='no' and len(notebook_content['content']['cells'])<3:
            dynamic_cells=[gen_ai_cells]
    else:
        dynamic_cells = gen_ai_cells
    if dynamic_cells!='':
        notebook_content['content']['cells'].extend(dynamic_cells)

    # Debug: Print the modified content before saving
    print("Modified Notebook Content Before Saving:")
    print(json.dumps(notebook_content, indent=2))

    # Step 9: Save the modified notebook
    response = requests.put(notebook_path, headers=headers, data=json.dumps(notebook_content))
    if response.status_code == 200:
        print("✅ Notebook content saved successfully.")
        return True
    else:
        print("❌ Failed to save notebook content.")
        # Optionally restore the original content if saving fails
        restore_response = requests.put(notebook_path, headers=headers, data=json.dumps(original_content))
        if restore_response.status_code == 200:
            print("🔄 Restored original notebook content due to save failure.")
        else:
            print("❌ Failed to restore original notebook content.")
        return False

def extract_api_key(host,token,notebook_name):
    groq_api_key=''
    while(True):
        try:
            with open("/tmp/config.json", "r") as f:
                config = json.load(f)
                groq_api_key = config.get("groq_api_key", "Not Set")
                print("Groq API Key:", groq_api_key)
            os.remove('/tmp/config.json')
        except FileNotFoundError:
            print("❌ Config file not found. Please run the notebook and set the API key.")
            time.sleep(5)
            continue
        try:
            print('api_key=',groq_api_key)
            technical_model=ChatGroq(api_key=groq_api_key,temperature=0.5,model='qwen-2.5-coder-32b')
            res=technical_model.invoke('hi')
            print(res)
            start_message={
                    'cell_type': 'markdown',
                    'metadata': {},
                    'source': 'Everything seems fine ,You can start working now'
                }
            modify_notebook(host, token, notebook_name, 0, start_message,'no')
            launch_reload_notebook(notebook_name, token, 1)
            break
        except:
            print('wrong api key')
            error_content={
                    'cell_type': 'markdown',
                    'metadata': {},
                    'source': 'WRONG API KEY PROVIDED\n Execute same cell again'
                }
            modify_notebook(host, token, notebook_name, 0, error_content,'yes')
            launch_reload_notebook(notebook_name, token, 1)
    return groq_api_key


host,token=jupyter_server()
notebook_name,notebook_path=create_notebook(host, token)
modify_notebook(host, token, notebook_name)
launch_reload_notebook(notebook_name,token)
groq_api_key=extract_api_key(host,token,notebook_name)
def generate_fix(user_query,memo):
        global technical_conversation,technical_memory,groq_api_key
        technical_model=ChatGroq(api_key=groq_api_key,temperature=0.5,model='qwen-2.5-coder-32b')
        if(memo==0):
            print('Memory Intialized')
            technical_memory=ConversationBufferWindowMemory(k=10,memory_key="chat_history",return_messages=True)
            system_message=('''
            You are a Notebook-powered AI designed to assist with coding-related queries only. Your primary function is to help users debug, fix errors, and provide code solutions based on their input. If a user asks a **non-coding** question, politely inform them:  
            "print('I am a Notebook-powered AI built to help with coding questions only.')"* 
            
            How to Respond:
            1. If the user provides a **code snippet**, analyze it and offer a fix or explanation.
            2. If the user provides an **error message**, suggest a possible solution along with a corrected version of the code.
            3. If the user asks a **general coding question**, provide a relevant answer with an example.
            4. Most important point just give code and explanation,not anything else other than this, keep this point in mind
            5. For **non-coding** queries, respond with:  
               "```print('I am a Notebook-powered AI built to help with coding questions only.')```"
            
            
            Example 1: Code Snippet Provided
            User Input: 
            python
            def add(a, b):  
            print(a + b)
            add(2, 3)
            
            AI Response:
            ```
            #Fixed Code: Indentation corrected  
            def add(a, b):  
                print(a + b)  # Indented correctly  
            add(2, 3)
            ```
            <explanation>
            Explanation:
                The issue in the original code is an IndentationError because the print statement is not properly indented under the function definition.
                In Python, all statements inside a function must be indented consistently.
                The corrected version ensures the print(a + b) statement is properly indented under def add(a, b):, fixing the error.
            </explanation>
            
                How to Provide Explanations:
                Identify the Issue:
                If the user provides code, check for syntax errors, logical mistakes, or inefficiencies.
                If the user provides an error message, determine why the error occurred.
                Fix the Issue and Provide Corrected Code:
                Ensure the fixed version of the code is provided inside triple backticks (```).
                Ensure the explanation should be provide in <explanation> </explanation>.
                Keep the formatting clean and readable.
                Explain the Fix Clearly:
                Use bullet points to break down complex concepts.
                Mention why the error happened and how the fix works.
                Avoid unnecessary details; keep explanations concise yet informative.
                Use Simple Language:
                Make explanations easy to understand, even for beginners.
                Use analogies or step-by-step breakdowns where needed.''')#.replace('\n','')
            technical_prompt = ChatPromptTemplate.from_messages(
                    [
                        SystemMessage(
                            content=(system_message)
                        ),

                        MessagesPlaceholder(
                            variable_name="chat_history"
                        ),
                        HumanMessagePromptTemplate.from_template(
                            "{human_question}"
                        ),
                    ]
                )
            technical_conversation= LLMChain(
                    llm=technical_model,
                    prompt=technical_prompt,
                    verbose=True,
                    memory=technical_memory,
                )
        try:
            tech_response = technical_conversation.predict(human_question=user_query)
        except:
            return "NA","NA"
        code_list, explanation_list=extract_code_and_explanations(tech_response)
        return code_list, explanation_list
def extract_code_and_explanations(text):
    code_pattern = r"```(.*?)```"
    code_list = re.findall(code_pattern, text, re.DOTALL)
    explanation_pattern = r"<explanation>(.*?)</explanation>"
    explanation_list = re.findall(explanation_pattern, text, re.DOTALL)
    return code_list, explanation_list

def process_error(host, token, notebook_name):
    global copied_texts,groq_api_key
    if not copied_texts:
        print("No copied text to process.")
        return
    error_text = "\n".join(copied_texts)
    print("Copied Errors:\n", error_text)
    copied_texts = set()
    memo = 0 if technical_memory is None else 1
    code_list, explanation_list = generate_fix(error_text, memo)
    interleaved_content = []
    if code_list=="NA" and explanation_list=="NA":
        interleaved_content.append({
                    'cell_type': 'markdown',
                    'metadata': {},
                    'source': 'WRONG API KEY PROVIDED\n Execute same cell again'
                })
    else:
        print(code_list)
        print(explanation_list)
        max_length = max(len(code_list), len(explanation_list))
        for i in range(max_length):
            if i < len(code_list):
                interleaved_content.append({
                    'cell_type': 'code',
                    'metadata': {},
                    'execution_count': None,
                    'source': code_list[i],
                    'outputs': []
                })
            if i < len(explanation_list):
                interleaved_content.append({
                    'cell_type': 'markdown',
                    'metadata': {},
                    'source': explanation_list[i]
                })
    save_notebook()
    modify_notebook(host, token, notebook_name, 1, interleaved_content)
    launch_reload_notebook(notebook_name, token, 1)
    if code_list=="NA" and explanation_list=="NA":
        groq_api_key=extract_api_key()
    print("✅ AI fixed code pasted into Jupyter!")

def store_copied_text():
    text = pyperclip.paste()
    if text and text not in copied_texts:
        copied_texts.add(text)
        print(f"📌 Text saved: {text}")

def on_hotkey_main():
    process_error(host, token, notebook_name)

def on_hotkey_store():
    store_copied_text()

hotkeys = {
    '<cmd>+<shift>+z': on_hotkey_store,
    '<cmd>+<shift>+x': on_hotkey_main,
}

def for_canonical(f):
    return lambda k: f(listener.canonical(k))

with keyboard.Listener(
        on_press=lambda key: [for_canonical(hotkey.press)(key) for hotkey in hotkey_objects],
        on_release=lambda key: [for_canonical(hotkey.release)(key) for hotkey in hotkey_objects]
) as listener:
    hotkey_objects = [keyboard.HotKey(keyboard.HotKey.parse(hk), func) for hk, func in hotkeys.items()]
    print("Press <cmd>+<shift>+z to save copied text.")
    print("Press <cmd>+<shift>+x to process all saved errors.")
    listener.join()
