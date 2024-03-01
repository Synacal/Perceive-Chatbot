**Setting Up Perceive-Chatbot**

To set up the Perceive-Chatbot, follow these steps:

### Step 1: Clone the Repository
Clone the Perceive-Chatbot repository from the source.

### Step 2: Add .env File
Create a .env file in the root directory of the project. This file will contain environment variables such as API keys. Ensure that you do not expose this file to the public.

Here's a sample `.env` file structure:
```
# .env file

# Azure OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Other environment variables
```

Replace `your_openai_api_key_here` with your actual Azure OpenAI API key.

### Step 3: Install Dependencies
Install the required Python dependencies using pip. Run the following commands in your terminal or command prompt:

```bash
pip install AzureOpenAI
pip install python-dotenv
pip install streamlit
```

### Step 4: Run the Application
After installing the dependencies, you can run the Perceive-Chatbot using Streamlit. Execute the following command in your terminal:

```bash
streamlit run perceive_chatbot.py
```

This command will start the Streamlit server and launch the Perceive-Chatbot application in your default web browser.

### Additional Notes:
- Make sure you have Python installed on your system.
- Ensure that you have an active internet connection to download the dependencies and access the Azure OpenAI API.
- For any issues or errors during the setup process, refer to the documentation or seek assistance from the community or project maintainers.

Follow these steps carefully to set up the Perceive-Chatbot successfully and enjoy using its features!
