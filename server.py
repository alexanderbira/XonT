from flask import Flask, jsonify, render_template, request
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "images/"

@app.route("/") 
def home():

  return render_template('index.html')

@app.route("/form-submission", methods = ["POST"])
def form_submission():
  #objectList = request.form.get("object-list")
  """ styleImage = request.files["style-image"]
  filename = secure_filename(styleImage.filename)
  filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
  print(styleImage.filename)
  styleImage.save("images/Capture.PNG")
  return jsonify({
    "message": "Success!"
  })
   """
  """ if 'style-image' not in request.files:
    return jsonify({"error": "no file part nooo D:"})
  file = request.files['style-image']
  
  if file.filename == '':
    return jsonify({"error": "No file submitted nooo D:"})
  
  os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
  filename = secure_filename(file.filename)
  try:
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return jsonify({"success": "so win"})
  except Exception as e:
    return jsonify({"error": str(e)}), 500 """
  return jsonify(tackleFiles("style-image", request.files))
  
def tackleFiles(inputFile, requestFiles):
  if inputFile not in requestFiles:
    return {
      "error": "no file part noooo D:",
      "file": inputFile
      }
  file = requestFiles[inputFile]

  if file.filename == "":
    return {
      "error": "no file submitted noooo D:"
      }
  
  os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
  
  filename = secure_filename(file.filename)
  try:
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    return {
      "success": "so win"
      }
  except Exception as e:
    return {
      "error": str(e),
      "file": inputFile
    }

@app.route("/example-api")
def secret():
  return jsonify({
    "name": "bob",
    "email": "bob@outlook.com"
  })




app.run()
