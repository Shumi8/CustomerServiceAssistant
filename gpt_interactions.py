import openai
import logging

# OpenAI setup
openai.api_type = "azure"
openai.api_base = "YOUR_API_BASE"
openai.api_version = "2024-02-15-preview"
openai.api_key = "YOUR_API_KEY"

logging.basicConfig(level=logging.INFO)

# Function to extract order number using GPT
def get_order_number(prompt):
    logging.info("Extracting Order Number")
    message_list = [
        {
            "role": "system",
            "content": """
            Extract only the 7 or 8-digit order number from the user's query.
            """
        }
    ]

    new_message = {"role": "user", "content": prompt}
    message_list.append(new_message)

    completion = openai.ChatCompletion.create(
        engine="gpt-4-turbo",
        messages=message_list,
        temperature=0
    )
    
    response_message = completion["choices"][0]["message"]
    return response_message['content']


# Function to generate GPT-based responses based on context
def get_gpt_response(prompt, response, general=False, conditional=False, cancelled=False, tracking_history=None, logs=None):
    if general:
        message_list = [
            {
                "role": "system",
                "content": f"""
                You will receive a query from a customer and a response to that query. 
                Your task is to tailor the response using the appropriate guidelines.
                """
            }
        ]
    else:
        message_list = [
            {
                "role": "system",
                "content": f"""
                Query received: {prompt}
                Respond using the response: {response}
                """
            }
        ]

    new_message = {"role": "user", "content": prompt}
    message_list.append(new_message)

    completion = openai.ChatCompletion.create(
        engine="gpt-4-turbo",
        messages=message_list,
        temperature=0
    )
    
    response_message = completion["choices"][0]["message"]
    return response_message['content']
