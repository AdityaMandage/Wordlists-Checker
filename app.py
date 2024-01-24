from flask import Flask, render_template, request, redirect, url_for, flash
import os
import threading
import time

app = Flask(__name__)
app.secret_key = 'test01'  # Replace with a secret key for session security


# Replace with the actual path to your SecLists directory
seclists_path = os.path.join(os.getcwd(), "SecLists")

def search_in_seclists(user_input, search_result):
    for root, dirs, files in os.walk(seclists_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r', errors='ignore') as f:
                content = f.read().splitlines()
                if user_input in content:
                    category = os.path.relpath(file_path, seclists_path)
                    search_result.append(f"The name '{user_input}' is in the SecLists. Found in category: {category}")

def perform_search(user_input):
    search_result = []
    search_thread = threading.Thread(target=search_in_seclists, args=(user_input, search_result))
    search_thread.start()

    while search_thread.is_alive():
        time.sleep(0.5)  # Adjust the sleep time as needed

    return search_result

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None

    if request.method == 'POST':
        user_input = request.form['input_name']

        # Flash a loading message before starting the search
        flash("Searching in progress...", 'info')

        # Perform the search in a separate thread to avoid blocking the main thread
        result = perform_search(user_input)

        # Flash the result message
        flash(result, 'info')

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
