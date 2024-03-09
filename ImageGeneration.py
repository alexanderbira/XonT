import os
import io
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import requests
import base64
import rembg
import numpy as np


def ImageGenerator(in_img, in_prompts, save_paths, ret_fun):

    # Set your OpenAI API key
    api_key = 'API Key here'

    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')


    # Getting the base64 string
    base64_image = encode_image(in_img)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"}
    
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "Describe the style of this image as much as possible summarizing in 5 key words separated by commas"
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
                }
            ]
            }
        ],
        "max_tokens": 300
        }
    
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)


    # Our Host URL should not be prepended with "https" nor should it have a trailing slash.
    os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'

    # Sign up for an account at the following link to get an API Key.
    # https://platform.stability.ai/

    # Click on the following link once you have created an account to be taken to your API Key.
    # https://platform.stability.ai/account/keys

    # Paste your API Key below.

    os.environ['STABILITY_KEY'] = 'sk-lKadva3CI31g12p2piPTTrcHoCA8BPvCE3odMQCw54CpnBd9'


    # Set up our connection to the API.
    stability_api = client.StabilityInference(
        key=os.environ['STABILITY_KEY'], # API Key reference.
        verbose=True, # Print debug messages.
        engine="stable-diffusion-xl-1024-v1-0", # Set the engine to use for generation.
        # Check out the following link for a list of available engines: https://platform.stability.ai/docs/features/api-parameters#engine
    )

    for i in range(0,len(in_prompts)):

        answers2 = stability_api.generate(
            prompt=in_prompts[i] + "one, individual, singular, isolated," + response.json()['choices'][0]['message']['content'] + "3d model, pure white background, flat base, in frame, isolated, top-down view",
            init_image=Image.open(in_img), # Assign our previously generated img as our Initial Image for transformation.
            start_schedule=0.99, # Set the strength of our prompt in relation to our initial image.
            end_schedule=0.99,
            steps=50, # Amount of inference steps performed on image generation. Defaults to 30.
            cfg_scale=20.0, # Influences how strongly your generation is guided to match your prompt.
                        # Setting this value higher increases the strength in which it tries to match your prompt.
                        # Defaults to 7.0 if not specified.
            width=1024, # Generation width, defaults to 512 if not included.
            height=1024, # Generation height, defaults to 512 if not included.
            sampler=generation.SAMPLER_K_DPMPP_2M # Choose which sampler we want to denoise our generation with.
                                                        # Defaults to k_dpmpp_2m if not specified. Clip Guidance only supports ancestral samplers.
                                                        # (Available Samplers: ddim, plms, k_euler, k_euler_ancestral, k_heun, k_dpm_2, k_dpm_2_ancestral, k_dpmpp_2s_ancestral, k_lms, k_dpmpp_2m, k_dpmpp_sde)
        )

        # Set up our warning to print to the console if the adult content classifier is tripped.
        # If adult content classifier is not tripped, save generated image.
        for resp in answers2:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    warnings.warn(
                        "Your request activated the API's safety filters and could not be processed."
                        "Please modify the prompt and try again.")
                if artifact.type == generation.ARTIFACT_IMAGE:
                    global img2
                    img2 = Image.open(io.BytesIO(artifact.binary))
                    # img2.save(save_paths[i]) # Do not need to actually save these, instead save 3D model

        
        input_array = np.array(img2)
        output_array = rembg.remove(input_array)
        output_image = Image.fromarray(output_array)
        output_image.save(save_paths[i])
        ret_fun()
       