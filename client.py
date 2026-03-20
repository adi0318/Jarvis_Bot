from google import genai
import os

YOUR_API_KEY = "Your API KEY"
client = genai.Client(api_key=YOUR_API_KEY)

chat = client.chats.create(
    model="gemini-2.5-flash"  # or another valid model
)

# 2. Send user input to the chat
response = chat.send_message("What is coding?")

# Print the AI’s answer
print(response.text)

