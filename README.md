## Perceive-Chatbot Setup Guide

This document outlines the steps required to set up and run the Perceive-Chatbot project. The Perceive-Chatbot is a Python-based chatbot application that integrates Azure and OpenAI services.

### Prerequisites

Before setting up the Perceive-Chatbot project, ensure you have the following prerequisites installed:

- Python (version 3.6 or higher)
- `pip` package manager

### Installation Steps

1. **Clone the Repository**

   Clone the Perceive-Chatbot repository from GitHub using the following command:

   ```
   git clone <repository_url>
   ```

   Replace `<repository_url>` with the URL of the Perceive-Chatbot repository.

2. **Navigate to the Project Directory**

   Move to the directory containing the Perceive-Chatbot project:

   ```
   cd Perceive-Chatbot
   ```

3. **Create `.env` File**

   Create a file named `.env` in the root directory of the project. This file will store the environment variables required for the application. Ensure to add the necessary configuration details in this file.

   Here's a sample `.env` file structure:
   
   ```
   # .env file
   
   # Azure OpenAI API Key
   OPENAI_API_KEY=your_openai_api_key_here
   
   ```


5. **Install Dependencies**

   Install the required Python dependencies using `pip`. Run the following commands:

   ```
   pip install AzureOpenAI
   pip install python-dotenv
   ```

6. **Run the Application**

   To start the Perceive-Chatbot application, execute the following command:

   ```
   python perceive_chatbot.py
   ```

   This command will run the main Python script of the chatbot application.

### Usage

Once the application is running, you can interact with the Perceive-Chatbot through a command-line interface or integrate it into your existing Python projects.

### Additional Notes

- Ensure that you have proper permissions and access rights to the Azure and OpenAI services used by the Perceive-Chatbot.
- Refer to the official documentation of Azure and OpenAI for detailed information on configuring and using their services.

By following these steps, you should be able to set up and run the Perceive-Chatbot project successfully.
