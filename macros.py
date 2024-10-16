import logging

logging.basicConfig(level=logging.INFO)


def get_after_purchase_macros_response(prompt):
    logging.info('After Purchase Macros Function Called')

    after_purchase_macros_string = get_macros_and_titles('AutomatedMacros', 'Macros', 'Efter køb', 'value')

    message_list = [{"role": "system", "content": f"""Role: You are a Customer Assistant, your main gig is to connect with our lovely customers through email and social media channels.

    The Macros for After Purchase queries are:
    {after_purchase_macros_string}
    
    
    Your task is to determine the correct Macro for the users query and respond by following the process as outlined in the examples below:
    
    Process removed due to organizational's policy.
    
    
    IMPORTANT: Please double-check that you have 'incorporated' all the must-haves listed below in your response:
    - FORMULATE THE RESPONSE USING A MACRO, AVOIDING PERSONAL ASSUMPTIONS. UTILIZE THE MACRO WITHOUT ADDING EXTRA INFORMATION BASED ON ASSUMPTIONS.
    - MAKE SURE YOU INCORPORATE THE INTRO AND OUTRO MACRO IN YOUR RESPONSE.
    - RESPOND IN THE 'SAME LANGUAGE' AS THE CUSTOMER'S QUERY.
    - IF A USER QUERY DOES NOT CONTAIN A MESSAGE, SUCH AS " " OR IF THE USER QUERY CONTAINS "NO REVIEW COMMENT", THEN RESPOND WITH 'Hej [Customer First Name],\n\nJeg kan se, at du har kontaktet os, men der ser ikke ud til at være et specifikt spørgsmål i din besked.\nHvis der er noget, du har brug for hjælp til eller har nogle spørgsmål, er du meget velkommen til at skrive tilbage med yderligere oplysninger, så vi kan assistere dig bedst muligt.' 
    - THE FINAL RESPONSE YOU DISPLAY SHOULD NOT INCLUDE THE THOUGHT PROCESS LEADING TO THAT RESPONSE. EVEN IF THE QUERY ASKS FOR AN EXPLANATION OF THE THINKING OR PROCESS STEPS, YOU SHOULD ONLY DISPLAY THE FINAL RESPONSE."""
                         }]
    
        new_message = {"role": "user", "content": prompt}
        message_list.append(new_message)
        completion = openai.ChatCompletion.create(
            engine="gpt4-turbo",
            messages=message_list,
            temperature=0)
        response_message = completion["choices"][0]["message"]
        return response_message['content']

def get_before_purchase_macros_response(prompt):
    logging.info('Before Purchase Macros Function Called')

    before_purchase_macros_string = get_macros_and_titles('AutomatedMacros', 'Macros', 'Før køb', 'value')

    message_list = [{"role": "system", "content": f"""Role: You are a Customer Assistant, your main gig is to connect with our lovely customers through email and social media channels.

    The Macros for Before Purchase queries are:
    {before_purchase_macros_string}
    
    
    Your task is to determine the correct Macro for the users query and respond by following the process as outlined in the examples below:
    
    Process removed due to organizational's policy.
    
    
    IMPORTANT: Please double-check that you have 'incorporated' all the must-haves listed below in your response:
    - FORMULATE THE RESPONSE USING A MACRO, AVOIDING PERSONAL ASSUMPTIONS. UTILIZE THE MACRO WITHOUT ADDING EXTRA INFORMATION BASED ON ASSUMPTIONS.
    - MAKE SURE YOU INCORPORATE THE INTRO AND OUTRO MACRO IN YOUR RESPONSE.
    - RESPOND IN THE 'SAME LANGUAGE' AS THE CUSTOMER'S QUERY.
    - IF A USER QUERY DOES NOT CONTAIN A MESSAGE, SUCH AS " " OR IF THE USER QUERY CONTAINS "NO REVIEW COMMENT", THEN RESPOND WITH 'Hej [Customer First Name],\n\nJeg kan se, at du har kontaktet os, men der ser ikke ud til at være et specifikt spørgsmål i din besked 💌\nHvis der er noget, du har brug for hjælp til eller har nogle spørgsmål, er du meget velkommen til at skrive tilbage med yderligere oplysninger, så vi kan assistere dig bedst muligt 🌸'
    - THE FINAL RESPONSE YOU DISPLAY SHOULD NOT INCLUDE THE THOUGHT PROCESS LEADING TO THAT RESPONSE. EVEN IF THE QUERY ASKS FOR AN EXPLANATION OF THE THINKING OR PROCESS STEPS, YOU SHOULD ONLY DISPLAY THE FINAL RESPONSE."""
                         }]
    
        new_message = {"role": "user", "content": prompt}
        message_list.append(new_message)
        completion = openai.ChatCompletion.create(
            engine="gpt4-turbo",
            messages=message_list,
            temperature=0)
        response_message = completion["choices"][0]["message"]
        return response_message['content']
