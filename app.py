from flask import Flask
app = Flask(__name__)
import os
from flask import jsonify

path = "/etc/ssl/certs/"

def ispem(file):
    if file.endswith(".pem"):
        return True
    return False

def get_info(file):
    try:
        information = {}
        info = str(os.popen("openssl x509 -in " + path + file + " -noout -text").read())  
        information["Not After"] = info.split("Not After : ")[1].split("Subject")[0].strip()
        information["Not Before"] = info.split("Not Before: ")[1].split("Not After")[0].strip()
        information["Authority"] = info.split("O = ")[1].split(",")[0].replace('\"', '')
    except:
        return {}

    return information

@app.route("/")
def hello():
    table = ""
    files_list = []
    files = os.listdir(path)
    for f in files:
        if(ispem(f)):
            files_list.append(get_info(f))
    response = {v: k for v, k in enumerate(files_list)}
    
    for key, value in response.items():
        try:
            print(value["Authority"])
            table = table + "<table id='customers'><tr><th>+"+value["Authority"]+"+</th></tr><tr><td>Not After "+value["Not After"]+"</td></tr><tr><td>Not Before "+value["Not Before"]+"</td></tr></table>"

        except:
            continue
#    return jsonify(response)
    return """  <!DOCTYPE html>
                <html lang="en">

                <head>
                  <meta charset="UTF-8">
                  <meta name="viewport" content="width=device-width, initial-scale=1.0">
                  <meta http-equiv="X-UA-Compatible" content="ie=edge">
                  <title>Index</title>
                  <style>
                    #customers {
                      font-family: Arial, Helvetica, sans-serif;
                      border-collapse: collapse;
                      width: 100%;
                    }
                    
                    #customers td, #customers th {
                      border: 1px solid #ddd;
                      padding: 8px;
                    }
                    
                    #customers tr:nth-child(even){background-color: #f2f2f2;}
                    
                    #customers tr:hover {background-color: #ddd;}
                    
                    #customers th {
                      padding-top: 12px;
                      padding-bottom: 12px;
                      text-align: left;
                      background-color: #04AA6D;
                      color: white;
                    }
                  </style>
                </head>

                <body>
                    <div style="width: 100%;">
                        <h1 style="color: #f5a83f; text-align: center;">Hepsiburada Task</h1>
                        """+table+"""
                    </div>
                  
                  <p>This is an HTML file served up by Flask</p>
                </body>

                </html>"""

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)