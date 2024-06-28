import os, time
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class image_generator:
    # Default Prompt
    PROMPT = "Tiger jumping through a circle of fire."

    def generate_prompts(theme):
        prompt_generation_prompt = f"""Generate prompts for image generation capturing realistic images of {theme} with various vibes and looks. I am giving you an examples of what the output should look like. I need you to generate 12 prompts in the same way but instead of being about kitchen they sohuld be about {theme}. \n 
        Example output: ["Photo Realistic Kitchen, beautiful, vintage, windows, wooden", "Photo Realistic Kitchen, beautiful, modern, black, sunset", "Photo Realistic Kitchen, beautiful, 80s, disco, colorful", "Photo Realistic Kitchen, winter cabin, show outsite, orange tint] \n Output as python list"""

        prompts = PROMPT

        return prompts
    
    def generate_images(prompts):
        timestamp = time.time()
        # TODO # create folder in images with name timestamp

        for prompt in prompts:
            # call openai api to generate image
            response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            quality="standard",
            n=1,
            )
            # print url with the generated image
            print(response.data[0].url)

        # TODO save image from the url to folder

        return timestamp
    


""" from diffusers import DiffusionPipeline

pipeline = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-3-medium") """



