# Customer Assistant Agent for Denmark's Largest Retail Organization

This repository contains the code for an automated customer service agent developed for one of Denmark’s largest retail organizations. This assistant handles more than 350 queries daily using Azure Functions, OpenAI's GPT models, and Zendesk APIs. It is designed to address a wide range of customer queries related to orders, tracking, returns, and more.

## Features

- **Handles Over 350 Queries Daily**: Automates responses to frequent customer inquiries, improving response times and accuracy.
- **Order Tracking**: Uses Selenium to fetch real-time tracking information from logistics providers and provide updates on order status.
- **Order Issues Resolution**: Handles cases where customers receive the wrong or broken items and generates appropriate responses, including image comparison using OpenAI Vision API.
- **Claimlane Integration**: Automatically generates responses for returns, defective items, missing parts, and allergic reactions using Claimlane.
- **Multilingual Support**: Supports Danish and English queries, dynamically responding in the same language as the user's query.
- **Macro-based Responses**: Uses pre-defined macros to ensure consistent, high-quality responses for various customer scenarios.
- **Scalable and Serverless**: Deployed as an Azure Function and containerized using Docker for easy scaling and portability.
- **Zendesk Integration**: Fully integrated with Zendesk API to retrieve customer queries and submit responses.

## Technologies Used

### 1. **OpenAI GPT-4 (Vision-enabled)**
- **LLM for Text**: GPT-4 models generate dynamic responses based on the customer query. The system intelligently categorizes and responds to various types of customer queries.
- **Vision API**: For queries involving image attachments, GPT-4 Vision API is used to analyze and compare product images provided by the customer with the retailer’s product database (e.g., wrong item or broken product).

### 2. **Selenium for Web Scraping**
- Selenium WebDriver is used to extract order tracking information from third-party logistics providers' websites, such as **Burd**, **DAO**, **PostNord**, and **GLS**. This allows the agent to provide real-time updates on the status of a package, even when a carrier API is unavailable.

### 3. **Zendesk API**
- The system retrieves customer queries from Zendesk tickets using the Zendesk API. It also submits the generated responses back to Zendesk, ensuring a seamless integration with the support team’s workflow.

### 4. **Azure Function App**
- The application is deployed as an **Azure Function** which is triggered whenever a customer query is received. The serverless architecture of Azure Functions allows the system to scale automatically based on query volume.

### 5. **Docker Containerization**
- The entire function is containerized using **Docker** to ensure consistency across different environments (development, testing, production). This ensures that all necessary dependencies such as **Selenium** and **Chrome WebDriver** are packaged together and easily deployable.

### 6. **Azure Logic Apps**
- **Azure Logic Apps** automate the process by triggering the Azure Function whenever a new Zendesk query is received. It orchestrates the workflow, ensuring smooth automation and integration with the Zendesk ticketing system.

### 7. **Claimlane Integration**
- The agent handles return requests and defective product claims through **Claimlane**, a third-party platform that simplifies the returns process. Customers receive Claimlane links to submit their return or claim requests.

## Query Types Handled

### 1. **Order Tracking**
   - Provides updates on order status, package location, and estimated delivery times.
   
### 2. **Order Cancellation**
   - Handles requests to cancel an order based on its current status.

### 3. **Wrong Item or Broken Product**
   - Automatically analyzes images sent by the customer and compares them with the retailer's product images using the Vision API. Generates appropriate responses based on the results.

### 4. **Missing Items**
   - Investigates missing items in the customer's order by reviewing the order details and tracking history.

### 5. **Returns and Claims (Claimlane)**
   - Guides customers through the return process or defective item claims via Claimlane.

### 6. **Pre-Purchase Inquiries**
   - Responds to customer questions regarding product availability and recommendations before making a purchase.

### 7. **Change of Address**
   - Assists customers who want to update the shipping address for their order.

## Deployment Steps

### 1. **Set up Azure Function App**
   - The core of the system runs as an Azure Function. This serverless architecture ensures that the function scales automatically based on incoming traffic.

### 2. **Containerize with Docker**
   - The entire app is packaged into a **Docker container**, which includes all necessary dependencies such as Selenium, Chrome WebDriver, and the OpenAI API SDK. This ensures that the function can be easily deployed in any environment with consistent results.

### 3. **Connect to Zendesk API**
   - The function connects to Zendesk to retrieve customer queries and submit responses. Ensure that the **Zendesk API** keys are set up properly in your environment configuration.

### 4. **Configure Azure Logic Apps**
   - Use **Azure Logic Apps** to automate the flow of customer queries to the function app. Whenever a new query is received in Zendesk, the Logic App triggers the Azure Function to process the query and generate a response.

### 5. **OpenAI API Integration**
   - The function is integrated with **OpenAI's API** to generate responses for customer queries and handle image-based tasks. The OpenAI credentials should be set up using the Azure environment variables.

### 6. **Selenium for Web Scraping**
   - Selenium is set up in the Docker container to fetch order tracking data from third-party courier websites when direct API access is not available.

## Example Workflow

1. A customer submits a query to Zendesk (e.g., "Where is my package?").
2. Azure Logic App triggers the Azure Function, which retrieves the query using Zendesk API.
3. The function identifies the query category (e.g., tracking request, missing item, or wrong product).
4. Depending on the category:
   - For order tracking, it uses Selenium to fetch real-time tracking details from the logistics provider.
   - For product issues, it uses OpenAI's Vision API to analyze customer-uploaded images.
   - For claims or returns, it sends a Claimlane link for the customer to follow up.
5. A response is generated, incorporating pre-defined macros (templates) or dynamically based on query details.
6. The response is sent back to Zendesk, where it is delivered to the customer.

## Conclusion

This customer assistant agent automates customer service for a large retail organization, handling various user queries efficiently and accurately. With the integration of machine learning models (GPT-4), web scraping (Selenium), and Claimlane, it provides a comprehensive solution for managing customer interactions and improving overall response time and satisfaction.
