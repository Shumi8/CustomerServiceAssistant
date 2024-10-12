from flask import Flask, request, jsonify
from utilities_and_helpers import log_info, log_error
from gpt_interactions import get_gpt_response, get_order_number
from api_interactions import get_order_admin_details, get_products_sum_and_matas_image
from macros import get_after_purchase_macros_response, get_before_purchase_macros_response

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    log_info(f"Webhook received: {data}")
    
    try:
        query = data['query']
        category = identify_query_category(query)

        if category == 'after_purchase':
            response = get_after_purchase_macros_response(query)
        elif category == 'before_purchase':
            response = get_before_purchase_macros_response(query)
        else:
            response = get_gpt_response(query, response="Default Response")

        return jsonify({"response": response}), 200

    except Exception as e:
        log_error(f"Error in webhook processing: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
