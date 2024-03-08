from flask import Flask, jsonify, render_template
app = Flask(__name__)

@app.route("/") 
def home():
  return render_template('index.html')

@app.route('/example-api')
def secret():
  return jsonify({
    'name': 'bob',
    'email': 'bob@outlook.com'
  })


app.run()
