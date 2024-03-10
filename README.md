# Summary
#### Made by Alex, Kai, Lawan, Mo and Sani

XonT is a tool, targeted at game developers, that generates 3D model assets that users can integrate into their own games. 

Using our website, the user can input a text prompt that describes which assets they need, as well as an image that indicates the style that they are going for (though this is optional) [Figure 1]. Using Stable Diffusion XL (provided by Stability AI), the tool creates a 2D representation of what their desired asset may look like. In the case that the user does not provide a style image, they are continuously prompted with suggestions for what their asset could look like, and they can indicate whether this is acceptable or whether changes need to be made, which they can implement via changes to their initial prompt [Figure 2]. 

Then, any other objects that are required are generated in a consistent style, and are presented to the user in the form of a 2D representation of the asset with a transparent background which the user can save - these images serve as the blueprints for the 3D model [Figure 3]. The user can then load these files to Google Colab to generate 3D models of these images, and via a Blender script (which runs in the background) the model is placed onto a tile, which is saved as a .fbx file (as well as a .mtl file used for materials) that can be imported to a game engine, such as Unity. 

We have provided a demo in Unity of how these assets could be used, with a hover script in C# that can be attached to the tiles so that when the cursor is on the object, the object hovers, and it can be selected to take the user playing the game to a different scene, similar to a level selection screen.

# How we used sponsor technology

Stability.ai is at the core of the 3D object generation pipeline, firstly through the developer API and stable-diffusion LX model:
• We used the Text-to-Image service to generate an initial style reference, injecting
the users object word into a prompt specifying basic properties such as the quantity and orientation.
• We then used Image-to-Image to generate the images to be converted to 3D objects, starting with the style image, and combining with the user object words (alongside additional prompting as before) to produce high quality images of 3D
models in consistent style.
Secondly, leveraging the Stability.ai open-source stable-zero123, we locally trained the model allowing us to convert the previously generated images into 3D models.

# Getting started
1. Compile React ([Node and NPM required](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm))
```bash
$ cd frontend
$ npm install
$ npm run build
```
2. Run the Flask server (Python required)
```bash
$ python3 server.py
```
3. Use the web app to get transparent images to turn into 3d models<br/>
[127.0.0.1:8000](https://127.0.0.1:8000)
4. Save the transparent images to your local disc
5. Open the [Jupyter notebook](https://github.com/alexanderbira/XonT/blob/main/image_to_model.ipynb) in [Google Colab](https://colab.research.google.com), and follow the provided instructions
6. Take the triples of 3d model (.obj), material file (.mtl), and texture file (.jpg), placing each triple in a directory of its own under `images/models/`
7. Process and place the resulting 3d models in `images/tiles/` (you will need to have Blender installed with the command-line configured)
```bash
$ blender -b --python compose_objects/modules/function_chest.py
```


# Demonstration Images
##### Figure 1: The initial prompt screen
![](https://github.com/alexanderbira/XonT/blob/main/demos/imgs/Figure%201.png)

##### Figure 2: Deciding on the style that objects will be generated in
![](https://github.com/alexanderbira/XonT/blob/main/demos/imgs/Figure%202.png)

##### Figure 3: Screen providing transparent images that can be sent to Google Colab
![](https://github.com/alexanderbira/XonT/blob/main/demos/imgs/Figure%203.png)

##### Figure 4: Unity Scene view of the demo, with example tiles in scene
![](https://github.com/alexanderbira/XonT/blob/main/demos/imgs/Figure%204.png)

