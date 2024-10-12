def gpt_response_generator(prompt, user_email, ticket_id):
    after_purchase_titles_string = get_macros_and_titles('AutomatedMacroTitles', 'Titles', 'Efter køb', 'title')
    before_purchase_titles_string = get_macros_and_titles('AutomatedMacroTitles', 'Titles', 'Før køb', 'title')
    club_matas_titles_string = get_macros_and_titles('AutomatedMacroTitles', 'Titles', 'Club Matas', 'title')
    other_titles_string = get_macros_and_titles('AutomatedMacroTitles', 'Titles', 'Andet', 'title')

    message_list = [{"role": "system", "content": f"""We have 12 different categories into which users' queries fall: After Purchase, Before Purchase, Other, Club Matas, Where is My Package, Can I Cancel My Order, Can I Change My Address, Wrong Item Received, Broken Product Received, Missing Item In My Order, Adding Items to an Order and Order Confirmation Not Received.

      Macro titles for After Purchase queries are:
      {after_purchase_titles_string}
    
      Macro titles for Before Purchase queries are:
      {before_purchase_titles_string}
    
      Macro titles for Where is My Package queries are:
      "Removed because of organization policy"
    
      Macro titles for Can I Cancel My Order queries are:
      "Removed because of organization policy"
    
      Macro titles for Can I Cancel My Order queries are:
      "Removed because of organization policy"
    
      Macro titles for Wrong Item Received:
      "Removed because of organization policy"
    
      Macro titles for Broken Product Received:
      "Removed because of organization policy"
    
      Macro titles for Missing Item In My Order:
      "Removed because of organization policy"
    
      Macro titles for Adding Items to an Order:
      "Removed because of organization policy"
    
      Macro titles for Order Confirmation Not Received:
      "Removed because of organization policy"
    
      You will receive customer queries in Danish or English. Your task is to intelligently determine the category to which the user's query belongs using the above macro titles and by following the process outlined in the examples below and then activate the relevant function according to the determined Macro category from the user's query:
    
      Q: "Removed because of organization policy"
      Category Determination: This particular query belongs to the 'After Purchase' category, as the customer is inquiring about missing items in the received order. Therefore, the function that should be activated is get_after_purchase_macros_response.
    
      Q: "Removed because of organization policy"
      Category Determination: This particular query belongs to the 'Before Purchase' category, as the customer is inquiring about the reavailability of a previously sold-out item. Therefore, the function that should be activated is get_before_purchase_macros_response.
    
      Q: "Removed because of organization policy"
      Category Determination: This particular query belongs to the 'Others' category, as the customer is inquiring about the process of renewing expired gift card. Therefore, the function that should be activated is get_other_macros_response.
    
      Note: If the query is related to Wrong Item Received, Broken Product Received, Missing Item In My Order, Adding Items to an Order or Order Confirmation Not Received. do not activate get_after_purchase_macros_response; instead, activate the appropriate function: wrong_item_has_been_received, broken_product_has_been_received, item_missing_in_order, add_item_to_my_order_response or order_confirmation_not_received. If the query is related to not receiving the whole package, activate get_where_is_my_package_response instead of item_missing_in_order, as the latter is for specific products missing in the package.
      
      IMPORTANT: YOU MUST ALWAYS ACTIVATE A FUNCTION WITH REGARDS TO THE USER'S QUERY, EVEN FOR AMBIGUOUS AND WITHOUT CONTEXT QUERIES. ALSO, ALWAYS PASS THE FULL PROMPT TO THE FUNCTION AS INPUT. DO NOT REMOVE SENTENCES, SPECIALLY 'DECISION GIVEN' ON YOUR OWN.
      """}]
    
    logging.info("Choosing which function to call")
    new_message = {"role": "user", "content": prompt}
    message_list.append(new_message)
    response_message = openai_answers(message_list)
    response_message = response_message.to_dict()
    if response_message.get("function_call"):
        response_message['function_call'] = response_message['function_call'].to_dict()
        available_functions = {
            "get_after_purchase_macros_response": get_after_purchase_macros_response,
            "get_before_purchase_macros_response": get_before_purchase_macros_response,
            "get_other_macros_response": get_other_macros_response,
            "get_club_matas_macros_response": get_club_matas_macros_response,
            "get_where_is_my_package_response": get_where_is_my_package_response,
            "get_can_i_cancel_my_order_response": get_can_i_cancel_my_order_response,
            "get_can_i_change_my_address_response": get_can_i_change_my_address_response,
            "wrong_item_has_been_received": wrong_item_has_been_received,
            "broken_product_has_been_received": broken_product_has_been_received,
            "get_missing_item_or_missing_package": get_missing_item_or_missing_package,
            "add_item_to_my_order_response": add_item_to_my_order_response,
            "order_confirmation_not_received": order_confirmation_not_received

        }
        function_name = response_message["function_call"]["name"]

        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        if function_name in ("get_where_is_my_package_response", "get_can_i_cancel_my_order_response", "get_can_i_change_my_address_response", "add_item_to_my_order_response", "order_confirmation_not_received"):
            function_response = function_to_call(
                prompt=function_args.get("prompt"),
                user_email=user_email
            )
        elif function_name in ("wrong_item_has_been_received", "broken_product_has_been_received", "get_missing_item_or_missing_package"):
            function_response = function_to_call(
                prompt=function_args.get("prompt"),
                ticket_id = ticket_id,
                user_email=user_email
            )
        else:
            function_response = function_to_call(
                prompt=function_args.get("prompt")
            )

        response_message['content'] = None
        return function_response, function_name
        message_list = []

    else:
        return get_no_category_response(prompt), None

def get_claimlane_response(prompt, user_email, subject_check, ticket_id):
  logging.info('Getting Claimlane Response')
  if subject_check != 'Claimlane':
    claimlane_category = get_claimlane_category(prompt)
    if claimlane_category == 'Return':
      response = "Removed because of organization policy"

    elif claimlane_category == 'Claim/Defect':
      response = "Removed because of organization policy"

    elif claimlane_category == 'Missing Parts':
      response = "Removed because of organization policy"
        
    elif claimlane_category == 'Damaged in Transport':
      response = "Removed because of organization policy"

    elif claimlane_category == 'Lost/Incorrect Delivery':
      response = "Removed because of organization policy"
        
    elif claimlane_category == 'Allergic Reaction':
      response = "Removed because of organization policy"
        
    else:
      response = "Removed because of organization policy"
    
    gpt_response = get_gpt_response(prompt, response, general=True, conditional=False, cancelled=False,
                                            tracking_history=None, logs=None)
    return gpt_response, None

  else:
    function_response, function_name = gpt_response_generator(prompt, user_email, ticket_id)
    return function_response, function_name


def identify_query_category(prompt, user_email, subject_check, ticket_id):
    logging.info('Identifying Query Category - Claimlane or General')
    message_list = [{"role": "system", "content": f"""We have 6 different claimlane categories: Return, Claim/Defect, Missing Parts, Damaged in Transport, Lost or Incorrect Delivery, and Allergic Reaction.

    You will receive customer queries in Danish or English. Your task is to intelligently determine if the query falls into any of these categories. If the query falls into any of the above categories, then the function that should be activated is get_claimlane_response. If it does not fall into any of these categories, activate gpt_response_generator.
    
    Q: "Removed because of organization policy"
    The customer's query falls under the 'Lost/Incorrect Delivery' category of ClaimLane, as it concerns a package that has not been received. Therefore, the appropriate function to activate is: get_claimlane_response

    Q: "Removed because of organization policy"    
    The customer's query falls under the 'Return' category of ClaimLane, as it concerns a request for returning the packahe. Therefore, the appropriate function to activate is: get_claimlane_response

    Q: "Removed because of organization policy"
    The customer's query does not fall into any of the 6 Claimlane categories, as it concerns an issue with update of Matas app. Therefore, the appropriate function to activate is: gpt_response_generator
                    
    Q: "Removed because of organization policy"
    The customer's query does not fall into any of the 6 Claimlane categories, as it concerns with the cancellation of an order. Therefore, the appropriate function to activate is: gpt_response_generator

    IMPORTANT: YOU MUST ALWAYS ACTIVATE A FUNCTION WITH REGARDS TO THE USER'S QUERY, EVEN FOR AMBIGUOUS AND WITHOUT CONTEXT QUERIES. ALSO, ALWAYS PASS THE FULL PROMPT TO THE FUNCTION AS INPUT. DO NOT REMOVE SENTENCES, SPECIALLY 'DECISION GIVEN' ON YOUR OWN."""}]
    
    new_message = {"role": "user", "content": prompt}
    message_list.append(new_message)
    response_message = openai_check_for_claimlane(message_list)
    response_message = response_message.to_dict()
    if response_message.get("function_call"):
        response_message['function_call'] = response_message['function_call'].to_dict()
        available_functions = {
            "get_claimlane_response": get_claimlane_response,
            "gpt_response_generator": gpt_response_generator
        }
        function_name_1 = response_message["function_call"]["name"]

        function_to_call = available_functions[function_name_1]
        function_args = json.loads(response_message["function_call"]["arguments"])
        if function_name_1 in ("get_claimlane_response"):
            function_response, function_name_2 = function_to_call(
                prompt=function_args.get("prompt"),
                user_email=user_email,
                subject_check = subject_check,
                ticket_id = ticket_id
            )
        else:
            function_response, function_name_2 = function_to_call(
                prompt=function_args.get("prompt"),
                user_email=user_email,
                ticket_id = ticket_id
            )
        response_message['content'] = None
        return function_response, function_name_2, function_name_1
        message_list = []

    else:
        return gpt_response_generator(prompt, user_email, ticket_id), None, None
