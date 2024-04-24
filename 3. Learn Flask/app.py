from flask import Flask

app = Flask(__name__) # set up out application


@app.route('/')
def  index():
    return 'Hello, world'

if __name__ == '__main__':
    app.run(debug=True)
