from bottle import Bottle, run

app = Bottle()

@app.route('/hello')
def hello():
    return "Hello World!"

@app.route('/')
def hellotoo():
    return "Hello World too!"