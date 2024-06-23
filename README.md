## Perceive-Chatbot-Server Setup Guide

To set up the endpoint and run a FastAPI server for your perception chatbot, follow these steps:

To set up the FastAPI endpoint for the perception chatbot server, follow these steps:

### Step 1: Clone the Repository

Clone the repository containing the `perceive_chatbot_server` code from GitHub. You can do this by running the following command in your terminal:

```bash
git clone <repository_url>
```

Replace `<repository_url>` with the URL of the GitHub repository where the `perceive_chatbot_server` code is hosted.

### Step 2: Navigate to the Project Directory

Navigate to the directory where you cloned the repository using the `cd` command:

```bash
cd perceive_chatbot_server
```

### Step 3: Set Up Virtual Environment (Optional but Recommended)

It's recommended to set up a virtual environment to isolate the project dependencies. You can do this using `venv` or `virtualenv`. Here's an example using `venv`:

```bash
python -m venv venv
```

Activate the virtual environment:

- On Windows:

```bash
venv\Scripts\activate
```

- On macOS and Linux:

```bash
source venv/bin/activate
```

### Step 4: Install Dependencies

With your virtual environment activated, install the required dependencies from your requirements.txt file:

```
pip install -r requirements.txt


```

### Step 5: Set Up Environment Variables

Create a `.env` file in the project directory if it doesn't already exist, and add your Azure OpenAI API key to it:

```plaintext
AZURE_OPENAI_KEY=your_api_key_here
```

### Step 6: Run the FastAPI Server

Start the FastAPI server by running the following command:

```bash
uvicorn perceive_chatbot_server:app --reload
uvicorn main:app --reload
```

This command tells uvicorn to run the `perceive_chatbot_server` module (Python file) and use the `app` instance of FastAPI. The `--reload` flag enables automatic reloading of the server when code changes are detected.

### Step 7: Access the API Endpoint

Once the server is running, you can access the API endpoint at `http://localhost:8000/generate/` using an HTTP client like `curl` or by sending POST requests programmatically.

That's it! You've successfully set up and run the FastAPI endpoint for the perception chatbot server. You can now interact with the API to generate responses based on user input.

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
   AZURE_OPENAI_KEY=your_openai_api_key_here

   ```

4. **Install Dependencies**

   With your virtual environment activated, install the required dependencies from your requirements.txt file:

   ```
   pip freeze > requirements.txt

   ```

5. **Run the Application**

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
