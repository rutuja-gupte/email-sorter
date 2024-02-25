# from flask import Flask, render_template, session, jsonify
 
import subprocess
import os
import script
from cluster import *
from scipy.cluster.hierarchy import cut_tree
import json
import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
    # Serve an HTML file that includes the JavaScript for popup checking
    # print(result.stdout)
    with open("templates/test.html") as f:
        return (f.read())
#     return flask.render_template('test.html')

@app.route('/run-script', methods=['GET'])
def run_script():
    # Path to your quickstart2.py script
    script_path = os.path.join(os.getcwd(), 'script.py')
    
    try:
        # Attempt to run your Python script
#         result = subprocess.run(['python', script_path], capture_output=True, text=True, check=True)
        creds = script.authenticate()
    # a: header; b: messages; c:pre-process; d:vectors; e:cluster matrix; g:groups; h:grouped headers; i:grouped msges; j:label_maker data
    
#         output = result.stdout
        # Return the script output or a success message
        return "Success"
    except subprocess.CalledProcessError as error:
        # Return an error message if the script fails
        return jsonify({"success": False, "error": str(error.output)}), 500

# the generic image display route for displaying images
# needs a preexisting image in the website-images directory

@app.route('/wait.html')
def wait():
    return "Please wait while we process your request"

@app.route('/result.html')
def folders():
        
    creds = script.authenticate()
    # a: header; b: messages; c:pre-process; d:vectors; e:cluster matrix; g:groups; h:grouped headers; i:grouped msges; j:label_maker data
    a,b, extra = script.check_messages(creds)
    c = cleanup(b)
    d = pre_processing(c)
    # f is the figure
    e = cluster(d)
    g = cut_tree(e, n_clusters=5)
    h = {}
    for idx, item in enumerate(g):
        if item[0] not in h:
            h[int(item[0])] = []
        h[int(item[0])].append(a[idx])


    i = {}
    for idx, item in enumerate(g):
        if item[0] not in i:
            i[item[0]] = []
        i[item[0]].extend(c[idx].split(" "))
    j = list(i.values())
    k = label_maker(j)

    l = {}
    for idx, item in enumerate(g):
        if item[0] not in l:
            l[int(item[0])] = []
        l[int(item[0])].append(b[idx])
        
    extra2 = {}
    for idx, item in enumerate(g):
        if item[0] not in extra2:
            extra2[int(item[0])] = []
        extra2[int(item[0])].append(extra[idx])
        
    with open("result_h.json", "w") as f:
        json.dump(h, f)
    with open("result_k.json", "w") as f:
        json.dump(l, f)
        
    with open("result_extra.json", "w") as f:
        json.dump(extra2,f)
        
    with open("templates/result.html") as f: 
        html = f.read()
    html = html.replace("REPLACEA", k[0])
    html = html.replace("REPLACEB", k[1])
    html = html.replace("REPLACEC", k[2])
    html = html.replace("REPLACED", k[3])
    html = html.replace("REPLACEE", k[4])
    return html   
    
#     return flask.render_template('templates/result.html', folders=j)
#     if True:
#         result = subprocess.run(['python', 'script.py'], capture_output=True, text=True, check=True)
#         # print(result.stdout)
#         with open("templates/result.html") as f:
#             html = f.read()
#         return html

# @app.route('/num_categories.html', methods=['GET'])
# def categories():
#     with open('templates/num_categories.html') as f:
#         html = f.read()
#         num_categories = int(flask.request.form['numCategories'])
#     return html
#     # return render_template('num_categories.html', num_categories=num_categories)

# @app.route('/categories.html', methods=['GET'])
# def process_categories():
#     categories = [request.form[f'category{i}'] for i in range(len(request.form))]
#     print(categories)  # For demonstration; in a real app, you might save this to a database or use it otherwise.
#     return redirect(url_for('index'))  # Redirecting to the initial form as an example

# @app.route('/result.html')
# def folders():
#     # Example list of folders with names and URLs
#     folders = j
#     return render_template('folders.html', folders=folders)

@app.route('/mail.html')
def mail():
    query_string = dict(flask.request.args)
    group = query_string.get("group")
    
    with open("result_h.json") as f:
        h = json.load(f)

#     print(h)
    heads = h[group]
    links = []
    for idx, head in enumerate(heads):
        nice_head = f"""
        <h3>{head['Subject']}</h3></a>
        <ul>
        <li>From: {head['From']} </li>
        <li>To: {head['To']} </li>
        <li>Date: {head['Date']} </li>
        </ul>
        """
        head_string = f'<li><a href="/content.html?group={group}&pos={idx}">{nice_head}</li>'
        links.append(head_string)
    replace_string = "".join(links)
    with open("templates/folder-contents.html") as f:
        html = f.read()
    html = html.replace("???", replace_string)
    
    return html

@app.route("/content.html")
def content():
    query_string = dict(flask.request.args)
    group = query_string.get("group")
    pos = query_string.get("pos")
    
    with open("result_h.json") as f:
        h = json.load(f)
    with open("result_k.json") as f:
        k = json.load(f)
        
    with open("result_extra.json") as f:
        extra = json.load(f)
        
    head = h[group][int(pos)]
    nice_head = f"""
        <h3>{head['Subject']}</h3></a>
        <ul>
        <li>From: {head['From']} </li>
        <li>To: {head['To']} </li>
        <li>Date: {head['Date']} </li>
        </ul>
        """
    head_string = f'<h1>{nice_head}</h1>'
    
    msg = extra[group][int(pos)]
    
    with open("templates/email-output.html") as f:
        html = f.read()
        
    html = html.replace("heads", head_string)
    html = html.replace("message", msg)
        
    
    return html

@app.route('/about.html')
def about():
    with open("templates/about.html") as f:
        return(f.read())
    
@app.route('/contact.html')
def contact():
    with open("templates/contact.html") as f:
        return(f.read())

@app.route('/image')
def dash2():
    query_string = dict(flask.request.args)
    fname = query_string['fname']
#     dirs = query_string['dir']
    ext = fname.split('.')[-1]
    path = os.path.join('website-images', fname)
    print(path)
    
    with open(os.path.join('website-images', fname), "rb") as f:
        return flask.Response(f.read(), headers = {"Content-Type":f"image/{ext}"})


if __name__ == '__main__':
    app.run(debug=True)
