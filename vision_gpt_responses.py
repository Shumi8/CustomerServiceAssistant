import openai
import logging

# Setup for GPT-4 Vision
openai.api_type = "azure"
openai.api_base = "YOUR_API_BASE"
openai.api_version = "2024-02-15-preview"
openai.api_key = "YOUR_API_KEY"

logging.basicConfig(level=logging.INFO)

# Function to compare images using GPT-4 Vision
def get_vision_gpt_response(prompt, matas_image_url_dict, user_image_url_dict, scenario):
    logging.info('Getting Vision GPT Response')

    try:
        message_list = [
            {
                "role": "system",
                "content": f"""
                You are receiving images from both the customer and the product ordered. Compare the images and return whether the customer received the correct or incorrect item.
                """
            }
        ]

        for url in matas_image_url_dict.values():
            message_list.append({
                "role": "user",
                "content": {"type": "image_url", "image_url": url}
            })

        for url in user_image_url_dict.values():
            message_list.append({
                "role": "user",
                "content": {"type": "image_url", "image_url": url}
            })

        response = openai.ChatCompletion.create(
            engine="gpt-4-vision",
            messages=message_list,
            max_tokens=1000,
        )

        return response.choices[0].message.content
    
    except Exception as e:
        logging.error(f"Error in Vision API: {e}")
        return "Vision API Error"
