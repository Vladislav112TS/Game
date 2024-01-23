from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/qw')
def odd_even():
    return render_template('odd_even.html', number=2)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')