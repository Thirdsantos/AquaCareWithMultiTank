import os
import json
import base64
import io
import re
from PIL import Image
import google.generativeai as genai
from app.utils.firebase import firebase_db
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load Gemini API key from environment variable
def load_gemini_config():
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("GEMINI_API_KEY not found in environment variables")
            return False
        
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        print(f"Error loading Gemini config: {e}")
        return False

# Initialize Gemini Model
def initialize_gemini():
    if not load_gemini_config():
        return None
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        return model
    except Exception as e:
        print(f"Error initializing Gemini model: {e}")
        return None

model = initialize_gemini()

# Decode base64 image string into a PIL Image
def decode_base64_image(base64_str):
    try:
        if "," in base64_str:
            base64_str = base64_str.split(",", 1)[1]
        image_bytes = base64.b64decode(base64_str)
        return Image.open(io.BytesIO(image_bytes))
    except Exception as e:
        print(f"Error decoding image: {e}")
        return None

# Main function to handle Gemini AI prompts
def ask_gemini(text=None, image=None, ai_enabled=False, aquarium_id=None):
    if not model:
        return {"Error": "Gemini AI not properly initialized. Check API key configuration."}, 500
    
    if not text and not image:
        return {"Error": "At least give a question or an image"}, 400

    # Text only
    if text and not image:
        instruction = (
            "Your name is Aquabot. If a question is not related to aquatic life or aquarium and fish, "
            "please respond like 'Oops, I can only answer questions about aquatic life and the wonders of the water world. "
            "Let's talk fish, oceans, lakes, or anything aquatic!' "
            "Also, start your response like 'Hi, I'm Aquabot, happy to serve you!' "
            "Do not use bold text. "
            "User: "
        )
        modified_question = instruction + text
        try:
            response = model.generate_content([modified_question])
            return {"AI_Response": response.text}, 200
        except Exception as e:
            return {"Error": f"Gemini API error: {str(e)}"}, 500

    # Image only
    elif image and not text:
        detection_prompt = (
            'You are an expert in aquatic life. Your name is Aquabot Finder. '
            'From the provided image, identify the fish species. Then, provide ideal water parameters for this fish '
            'in the following JSON format: '
            '{"Fish": "Type of fish", "PH": {"MIN": 6.0, "MAX": 7.5}, "Temperature": {"MIN": 24, "MAX": 28}, "Turbidity": {"MIN": 0, "MAX": 1.5}}. '
            'Do not explain anything else. Return only the JSON format.'
        )

        image_data = decode_base64_image(image)
        if not image_data:
            return {"Error": "Failed to decode image"}, 400

        try:
            response = model.generate_content([detection_prompt, image_data])
            raw = response.candidates[0].content.parts[0].text.strip()
        except Exception as e:
            return {"Error": f"Gemini API failed: {str(e)}"}, 500

        try:
            fish_match = re.search(r'"?Fish"?\s*:\s*"([^"]+)"', raw)
            ph_min_match = re.search(r'"?PH"?[^}]*"MIN"\s*:\s*([\d.]+)', raw)
            ph_max_match = re.search(r'"?PH"?[^}]*"MAX"\s*:\s*([\d.]+)', raw)
            temp_min_match = re.search(r'"?Temperature"?[^}]*"MIN"\s*:\s*([\d.]+)', raw)
            temp_max_match = re.search(r'"?Temperature"?[^}]*"MAX"\s*:\s*([\d.]+)', raw)
            turb_min_match = re.search(r'"?Turbidity"?[^}]*"MIN"\s*:\s*([\d.]+)', raw)
            turb_max_match = re.search(r'"?Turbidity"?[^}]*"MAX"\s*:\s*([\d.]+)', raw)

            if not all([fish_match, ph_min_match, ph_max_match, temp_min_match, temp_max_match, turb_min_match, turb_max_match]):
                raise ValueError("One or more parameters could not be found in Gemini response.")

            fish = fish_match.group(1)
            PH = {"MIN": float(ph_min_match.group(1)), "MAX": float(ph_max_match.group(1))}
            Temperature = {"MIN": float(temp_min_match.group(1)), "MAX": float(temp_max_match.group(1))}
            Turbidity = {"MIN": float(turb_min_match.group(1)), "MAX": float(turb_max_match.group(1))}

            parameters = {
                "Fish": fish,
                "PH": PH,
                "Temperature": Temperature,
                "Turbidity": Turbidity
            }

            summary = (
                f"The fish is {fish}. "
                f"Recommended pH: {PH['MIN']} - {PH['MAX']}, "
                f"Temperature: {Temperature['MIN']}°C - {Temperature['MAX']}°C, "
                f"Turbidity: {Turbidity['MIN']} - {Turbidity['MAX']} NTU."
            )

            return {
                "Water_Parameters": parameters,
                "Summary": summary
            }, 200

        except Exception as e:
            return {"Error": f"Failed to extract values: {str(e)}", "RawResponse": raw}, 500

    # Text + Image
    else:
        instruction = (
            "Your name is Aquabot. If a question is not related to aquatic life or aquarium and fish, "
            "please respond like 'Oops, I can only answer questions about aquatic life and the wonders of the water world. "
            "Let's talk fish, oceans, lakes, or anything aquatic!' "
            "Also, start your response like 'Hi, I'm Aquabot, happy to serve you!' "
            "Do not use bold text. "
            "User: "
        )
        modified_question = instruction + text
        image_data = decode_base64_image(image)
        if not image_data:
            return {"Error": "Failed to decode image"}, 400
            
        try:
            response = model.generate_content([modified_question, image_data])
            return {"AI_Response": response.text}, 200
        except Exception as e:
            return {"Error": f"Gemini API error: {str(e)}"}, 500
