import os
from openai import OpenAI
import requests
from datetime import datetime

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Predefined styles
STYLES = [
    "photorealistic",
    "anime style",
    "watercolor painting",
    "oil painting",
    "pencil sketch",
    "3D rendered",
    "pop art",
    "minimalist",
    "steampunk"
]

def generate_and_save_image(prompt, style, index):
    # Combine user prompt with style
    full_prompt = f"{prompt}, in {style} style"
    
    try:
        # Generate image using DALL-E 3
        response = client.images.generate(
            model="dall-e-3",
            prompt=full_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        # Get image URL
        image_url = response.data[0].url
        
        # Download image
        img_response = requests.get(image_url)
        
        # Create timestamp for unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save image
        filename = f"image_{timestamp}_{index}_{style.replace(' ', '_')}.png"
        with open(filename, 'wb') as f:
            f.write(img_response.content)
            
        print(f"Generated and saved: {filename}")
        
    except Exception as e:
        print(f"Error generating {style} image: {str(e)}")

def main():
    # Get user prompt
    user_prompt = input("Enter your image prompt: ")
    
    # Generate 9 variations
    for i, style in enumerate(STYLES, 1):
        print(f"Generating {style} version...")
        generate_and_save_image(user_prompt, style, i)

if __name__ == "__main__":
    main()
