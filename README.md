# CustomerServiceAssistant

This code represents a sophisticated customer service agent developed for one of the largest retail organizations in Denmark, designed to handle more than 350 queries daily via the Zendesk platform. It integrates Azure Functions, containerization via Docker, OpenAI's large language models (LLMs), and Zendesk API, with the automation being deployed and managed using Azure Logic Apps. Here’s a detailed breakdown of the functionality, technologies, and models used in the code.

Core Functionalities:
Query Categorization and Response Generation: The core functionality of this code is to process customer queries in both Danish and English by using OpenAI GPT-based models to generate responses based on the category of the user query. The code categorizes queries into several types:

After Purchase Issues: Handles complaints about received orders (e.g., missing items, wrong or broken products, returns).
Before Purchase Issues: Handles pre-purchase inquiries such as availability and product recommendations.
Order Status/Tracking: Determines the current status of an order using order numbers and the tracking history.
Returns and Claims (Claimlane): Specialized for handling return requests, defective products, missing parts, damaged goods, lost deliveries, and allergic reactions.
Order Tracking: For queries regarding order status, the function extracts the order number from user queries, retrieves details via API from an order administration system, and checks the shipping status using the carrier’s website. Selenium WebDriver is used to automate tracking history extraction from shipping providers like Burd, DAO, PostNord, and GLS.

Response Customization and Templates: The code utilizes multiple response macros (predefined templates) for both After Purchase and Before Purchase scenarios, allowing for consistent and fast responses tailored to customer queries. Depending on the type of query, the macros are integrated into the response.

Handling Vision Tasks with OpenAI Vision API: The agent handles more complex queries involving images using OpenAI's Vision API. When a customer sends images, such as those showing a wrong or broken item, the Vision API compares them with product images from the retailer’s database. For example:

Wrong Item Received: Compares product images the customer received vs. what they ordered.
Broken Item Received: Analyzes images for defects (e.g., broken packaging, product cracks).
Claimlane Integration: If a query is identified as falling under Claimlane categories (Return, Defective Item, Missing Parts, etc.), the code generates a specific response instructing the customer to submit a claim via the provided Claimlane link. Claimlane handles customer claims and returns efficiently by collecting the necessary details.

API and Web Scraping with Selenium: The code uses the Selenium WebDriver to interact with carrier tracking pages to extract tracking history and status for packages. This automates the tracking process without relying on direct API access from all the courier services.

Automated Categorization and Function Invocation: The OpenAI model is used to intelligently classify queries into categories such as "Where is My Package?", "Wrong Item Received", or "Missing Item", and calls the appropriate function to generate a response based on the category.

Azure Function App: The core of the system runs as an Azure Function which is exposed via an HTTP endpoint. When a query is received from Zendesk, Azure Logic Apps trigger the function by calling this HTTP endpoint. The function processes the query, interacts with external APIs, generates a response, and sends it back to Zendesk.

Technologies Used:
OpenAI GPT Models:

The system utilizes GPT-4 (Vision-enabled) for text-based responses and image-based query handling. GPT-4 processes both customer queries and generates responses, and in the case of image-based queries, the Vision API analyzes the images sent by users.
OpenAI Azure Integration: OpenAI’s API is configured with Azure's service to integrate with the function app, making it a scalable solution.
Selenium:

Selenium is used for web scraping to fetch real-time tracking information from third-party logistics providers' websites like DAO, Burd, PostNord, and GLS. Since not all carriers provide tracking APIs, Selenium automates browser interaction to extract tracking statuses.
Azure Functions and Docker:

The code is hosted within an Azure Function App, which provides serverless hosting and scales based on demand. The function is containerized using Docker, which allows for easy deployment, scaling, and isolation of the app's environment.
Docker ensures that the environment dependencies (Selenium, Chrome WebDriver, OpenAI, etc.) are consistently maintained across all deployments. The Azure Function App is integrated with the Docker image, making it portable and easily managed.
Zendesk API:

Zendesk API is used to interact with the ticketing system. The code uses it to retrieve user queries and ticket data (such as order numbers or images) and to send generated responses back to customers.
Azure Logic Apps:

Azure Logic Apps act as the orchestrator, triggering the Azure Function whenever a new customer query is received. This enables automation without manual intervention.
Tracking History Parsing: The function also includes logic for month mapping between Danish and English, which allows it to convert tracking details into a customer-friendly format, supporting both Danish and English languages.

User Query Types Handled:
Order Tracking: Customers asking "Where is my package?"
Order Cancellation: Handling requests to cancel an order.
Address Changes: Address modification requests post-order.
Wrong Item Received: Comparing images and generating solutions.
Broken/Damaged Products: Handling issues with defective products.
Missing Items: Investigating missing products from an order.
Pre-Purchase Queries: Responding to product availability or recommendations.
Returns and Claims: Initiating the return process using Claimlane.
Model Integration:
LLM (GPT-4): The core language model used for generating responses based on user input.
Vision-enabled GPT-4: Utilized to analyze and compare images (product photos) and provide visual-based analysis for issues like wrong or damaged products.
Containerization with Docker:
The function app is containerized using Docker, ensuring consistency between development, testing, and production environments. The container includes all dependencies such as the Chrome WebDriver (for Selenium) and the OpenAI SDK, making the function highly portable and scalable.

Docker also allows easy scaling on Azure and supports rapid deployment of updates or patches by simply updating the Docker image.

Conclusion:
This system automates customer service for a large retail organization, handling various user queries with the help of GPT-4 models, Zendesk API, Selenium for tracking, and Azure for deployment. It provides a robust, scalable solution for managing high volumes of customer interactions efficiently and accurately, using machine learning models, web scraping, and API integrations. The use of Docker ensures environment consistency, while Azure Functions allows for serverless, scalable deployment.
