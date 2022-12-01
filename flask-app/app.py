from shutil import move, rmtree
from flask import Flask, request , send_file
from flask_cors import CORS
from contour import render
from os import mkdir, path, remove
from random import randint, choices
import string

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['MAX_CONTENT_LENGTH'] = 10 * 1000 * 1000


@app.route("/upload/<filename>", methods = ['POST', 'GET'])
def receive(filename):
    
    if request.method == 'POST':
        while True:
            dir = ''.join(choices(string.ascii_uppercase + string.digits, k=randint(6, 16)))
            try:
                mkdir(dir)
                break
            except:
                pass

        filename = dir + filename

        file = request.files['file']
        file.save(filename)
        render(filename, dir)
        remove(filename)
        move(dir + 'red.vtp', path.join(dir, 'red.vtp'))
        move(dir + 'blue.vtp', path.join(dir, 'blue.vtp'))
        move(dir + 'green.vtp', path.join(dir, 'green.vtp'))
        
        return dir

    if request.method == 'GET':
        return ''


@app.route('/download/<dir>/<color>')
def download(dir,color):
        
    download_name = color + '.vtp'
    path_ = path.join(dir, download_name)
    
    response =  send_file(as_attachment=False, path_or_file=path_, download_name=download_name)
    
    #'blue.vtp' is the last file to be read, delete the directory after that.
    if color == 'blue':
        rmtree(dir)

    return response

    

if __name__ == "__main__":
    app.run()
