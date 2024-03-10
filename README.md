# Summary
#### Made by Alex, Kai, Lawan, Mo and Sani

XonT is a tool, targeted at game developers, that generates 3D model assets that users can integrate into their own games. 

Using our website, the user can input a text prompt that describes which assets they need, as well as an image that indicates the style that they are going for (though this is optional) [Figure 1]. Using Stable Diffusion XL (provided by Stability AI), the tool creates a 2D representation of what their desired asset may look like. In the case that the user does not provide a style image, they are continuously prompted with suggestions for what their asset could look like, and they can indicate whether this is acceptable or whether changes need to be made, which they can implement via changes to their initial prompt [Figure 2]. 

Then, any other objects that are required are generated in a consistent style, and are presented to the user in the form of a 2D representation of the asset with a transparent background which the user can save - these images serve as the blueprints for the 3D model [Figure 3]. The user can then load these files to Google Colab to generate 3D models of these images, and via a Blender script (which runs in the background) the model is placed onto a tile, which is saved as a .fbx file (as well as a .mtl file used for materials) that can be imported to a game engine, such as Unity. 

We have provided a demo in Unity of how these assets could be used, with a hover script in C# that can be attached to the tiles so that when the cursor is on the object, the object hovers, and it can be selected to take the user playing the game to a different scene, similar to a level selection screen.

# Demonstration Images
##### Figure 1: The initial prompt screen
![[Pasted image 20240310101901.png]]

##### Figure 2: Deciding on the style that objects will be generated in
![[Pasted image 20240310102021.png]]

##### Figure 3: Screen providing transparent images that can be sent to Google Colab
![[Pasted image 20240310102259.png]]

