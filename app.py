import flask
import subprocess
import os
import secrets

app = flask.Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/')
def index():
    # HTML content with JavaScript to check for popup blocker
    html_content = '''
    <!DOCTYPE html>
    <html>
    <head>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Web Page Title</title>
        <style>
            body {
                text-align: center; /* Center aligns the content */
                margin-top: 20px; /* Adds some space at the top */
            }

            h1 {
                color: #333; /* Dark grey color for the title */
                margin-bottom: 10px; /* Space between title and pink line */
            }

            .pink-line {
                height: 1px; /* Thickness of the line */
                background-color: pink; /* Pinkish color for the line */
                margin: 20px auto; /* Centers the line and adds space above and below */
                width: 50%; /* Width of the line */
            }

            button {
                background-color: #007bff; /* Bootstrap primary button color */
                color: white; /* Text color */
                border: none; /* Removes the border */
                padding: 10px 20px; /* Padding inside the button */
                margin-top: 20px; /* Space between the line and the button */
                cursor: pointer; /* Changes cursor to pointer on hover */
                border-radius: 5px; /* Slightly rounded corners for the button */
            }

            button:hover {
                background-color: #0056b3; /* Darkens the button on hover */
            }
        </style>
        <title>Email Sorter</title>
        <script type="text/javascript">
        function checkPopupsEnabled() {
            var testPopup = window.open('', '_blank', 'width=100,height=100');
            if (!testPopup) {
                alert('Popups are blocked. Please enable popups for this site.');
            } else {
                testPopup.close();
                // Redirect to the script execution endpoint
                window.location.href = '/run-script';
        
                // Or, for an asynchronous request:
                fetch('/run-script')
                    .then(response => response.json())
                    .then(data => {
                        console.log(data);
                        // Process and display the response data on the webpage
                    })
                    .catch(error => console.error(error));
            }
        }
        </script>
    </head>
    <body>
        <h1>Welcome to Email Sorter</h1>
        <div class="pink-line"></div>
        <button onclick="checkPopupsEnabled()">Check Popups to continue ahead</button>
    </body>
    </html>
    '''
    return flask.render_template_string(html_content)

@app.route('/run-script', methods=['GET'])
def run_script():
    print("I am here")
    try:
        # Assuming quickstart2.py is in the same directory as this Flask app
        script_path = os.path.join(os.getcwd(), 'quickstart2.py')
        result = subprocess.run(['python', script_path], capture_output=True, text=True, check=True)
        return ""
    except subprocess.CalledProcessError as e:
        return flask.Response({"success": False, "error": e.output}), 400

if __name__ == '__main__':
    app.run(debug=True)
