from bottle import Bottle, run, get, post, request

app = Bottle()

@app.route('/hello')
def hello():
    return "hello get route"

@app.route('/')
def hellotoo():
    return "base route"


@get('/login') # or @route('/login')
def login():
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>
    '''

@post('/login') # or @route('/login', method='POST')
def login():
    body = request.json
    return {'puppet': str(body)}