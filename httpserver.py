from flask import Flask
import subprocess
app = Flask(__name__)

@app.route('/autonomous')
def webpage():
    process = subprocess.Popen(["./highgoal.bin", "latest"], stdout=subprocess.PIPE)
    response = process.stdout.read()

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='9999')
