from flask import Flask, request, jsonify
from utilities_and_helpers import log_info, log_error
from gpt_interactions import get_gpt_response, get_order_number
from api_interactions import get_order_admin_details, get_products_sum_and_matas_image
from macros import get_after_purchase_macros_response, get_before_purchase_macros_response

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="get_customer_assistant_response")
def get_customer_assistant_response(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    ticket_id = req.params.get('ticket_id')
    user_email = req.params.get('user_email')
    
    if not ticket_id:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            ticket_id = req_body.get('ticket_id')

    if ticket_id:

        headers = {
        "Content-Type": "application/json",
        "Authorization": ''
        }

        ticket_url = f"https://zendesk_api/api/v2/tickets/{ticket_id}.json"
        response = requests.get(ticket_url, headers=headers)
        
        if response.status_code == 200:
            logging.info("Ticket ID is: %s", ticket_id)
            ticket_data = response.json()
            prompt = ticket_data['ticket']['description']
            subject = ticket_data['ticket']['subject']
            if subject:
                subject_check = subject.split()[0] if subject.split() else None
            else:
                subject_check = None
            if subject_check == "Claimlane":
                simplified_prompt = prompt
            else:
               simplified_prompt = get_simplified_prompt(prompt)
            response, function_name_2, function_name_1 =  identify_query_category(simplified_prompt, user_email, subject_check, ticket_id)
        else:
            raise Exception(response.text)

        if function_name_2 in ("get_where_is_my_package_response", "get_can_i_cancel_my_order_response", "get_can_i_change_my_address_response", "get_missing_item_or_missing_package", "add_item_to_my_order_response"):
            return func.HttpResponse(response)
        
        else:
            return func.HttpResponse(gpt4_response_translator(simplified_prompt, response, subject_check, function_name_1))
          
    else:
        return func.HttpResponse("No Prompt Given.")
