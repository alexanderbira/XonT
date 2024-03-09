from flask import Flask, jsonify, send_from_directory, request, send_file, redirect
import os
from flask_socketio import SocketIO
from StyleGeneration import StyleGenerator

app = Flask(__name__, 
            static_folder="frontend/build",
            static_url_path=''
            )
app.config["UPLOAD_FOLDER"] = "images/"
socketio = SocketIO(app)

# this list stores the strings of names of objects we want to generate
objectList = []

@app.route("/") 
def serve():
  return send_from_directory(app.static_folder, 'index.html')

@app.route("/submit-form", methods = ["POST"])
def submit_form():
  global objectList

  objectList = []

  # get the names of the objects which should be made
  for key in request.form:
    if key.startswith("object-"):
      objectList.append(request.form[key])
  if len(objectList) == 0:
    return "List of objects to generate cannot be empty", 400 
  
  # process the input style image file
  res = save_style_image(request.files)

  if "error" in res:
    return res["error"], 500
  
  # if the user has not provided a style image, generate one
  if res["success"] == "generating style image...":
    socketio.start_background_task(target=generate_style_image, word=objectList[0])
  
  return jsonify(res)
  
# the src property of the img element containing the style image
@app.route("/evaluate-img.png")
def give_evaluated_image():
  if os.path.exists("images/style_image.png"):
    return send_file("images/style_image.png", mimetype='image/png')
  return "Error", 404

@app.route("/reject-image", methods = ["POST"])
def reject_image():
  content = request.json
  socketio.start_background_task(target=generate_style_image, word=objectList[0]+" which is "+content['prompt'])
  return jsonify({
    "success": "generating style image..."
  })

# TODO
@socketio.on("create_results")
def handle_connect():
  print('Starting 3d...')
  # call the 3d model generation scripts

  # send web socket "next_completed" after each completion
  # add a function to serve the 3d models

  # send web socket "all_completed" when all completed




def generate_style_image(word):
  # make the images folder if it doesn't already exist
  if not os.path.exists("images"):
    os.makedirs("images")
  
  # generate the style image
  StyleGenerator(word, "images/style_image.png")

  # send a message to the user saying the image is ready
  with app.app_context():
    socketio.emit('evaluate_image', {
      "status": "success",
      "message": "ready to evaluate generated style image"
    }, include_self=True)

def save_style_image(request_files):
  # if the user doesn't upload a style image, we still expect it to exist as a
  # key, but just be blank
  if "style-image" not in request_files:
    return {
      "error": "style image not present in request",
    }
  file = request_files["style-image"]

  if file.filename == "":
    return {
      "success": "generating style image..."
    }
  
  os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
  
  try:
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], "style_image.png"))
    return {
      "success": "generating assets"
    }
  except Exception as e:
    return {
      "error": str(e)
    }

socketio.run(app, log_output=True, port=8000)
