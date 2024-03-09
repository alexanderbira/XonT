from flask import Flask, jsonify, send_from_directory, render_template, request
import os
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO

### global variables (im sorry there has to be a better way but im tired)
objectDict = {}


### flask stuff

app = Flask(__name__, 
            template_folder="frontend/build", 
            static_folder="frontend/build/static",
            static_url_path=''
            )
app.config["UPLOAD_FOLDER"] = "images/"
socketio = SocketIO(app)

@app.route("/") 
def serve():
  return send_from_directory(app.static_folder, 'index.html')

@app.route("/submit-form", methods = ["POST"])
def form_submission():
  # dealing with the object list
  global objectDict
  for key in request.form:
    if key.startswith("object-"):
      objectDict[key] = request.form[key]
  
  # dealing with the style image
  tackleFiles("style-image", request.files)
  return 
  
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
  
  try:
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], "style_image.png"))
    return {
      "success": "so win"
      }
  except Exception as e:
    return {
      "error": str(e),
      "file": inputFile
    }

""" @app.route("/example-api")
def secret():
  return jsonify({
    "name": "bob",
    "email": "bob@outlook.com"
  })

 """

### socket stuff

@socketio.on("evaluate-image"):
  ### RUN SANIS FUNCTION

@socketio.on("3d-object"):
  ### RUN SANIS FUNCTION ON THE REST OF THE OBJECTS (IF APPLICABLE)
  ### RUN MO N LAWAN SO THAT 3D OBJECT IS RETURNED

### running

socketio.run(app)

##### from sani, assume we have functions:
## generateInitialObject(object: str, styleImage: imagefile = null): imagefile (im so kotlin brained)
#### this function should be given the input object, i.e., the first object in the object list,
#### and the style image if one exists, and then should generate an image of an object a game dev could use