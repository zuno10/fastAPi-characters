from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import json
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Google AI API with your key
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Create an instance of the GenerativeModel
model = genai.GenerativeModel('gemini-2.0-flash')

app = FastAPI()

origins = [
    "https://zuno10.github.io/bahrupiya/",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/characters", response_model=List[Dict])
def read_characters():
    with open("characters.json", "r") as f:
        characters = json.load(f)
    return characters

conversation_sessions = {}

# We'll use this Pydantic model to validate the incoming data for the summary endpoint
class ChatHistory(BaseModel):
    history: List[Dict[str, str]]
    character_id: str

# A new function to generate the summary using the AI model
def summarize_text(text_to_summarize: str) -> str:
    # This is an example of prompt engineering for summarization
    prompt = (f"Please create an abstractive summary of the following conversation. "
              "Focus on the key topics, decisions, and outcomes. Keep the summary concise and no more than two sentences. "
              "Conversation:\n\n{text_to_summarize}")
    
    try:
        response = model.generate_content(prompt.format(text_to_summarize=text_to_summarize))
        return response.text
    except Exception as e:
        print(f"Error during summarization: {e}")
        return "Failed to generate summary."

# A new POST endpoint to handle the summarization request
@app.post("/chat/summary")
async def create_chat_summary(data: ChatHistory):
    try:
        # We need to format the chat history into a single string for the AI
        formatted_history = ""
        for message in data.history:
            formatted_history += f"{message['role']}: {message['parts']}\n"
        
        summary_text = summarize_text(formatted_history)
        
        # We are not storing this in a database yet, but in a real-world app, you would save it here
        # For now, we'll just return the summary
        return {"summary": summary_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

# inside main.py - replace the websocket_endpoint function with this

@app.websocket("/ws/{character_id}")
async def websocket_endpoint(websocket: WebSocket, character_id: str):
    await websocket.accept()

    if character_id not in conversation_sessions:
        character_data = next((c for c in read_characters() if c['id'] == character_id), None)
        if not character_data:
            await websocket.send_text(json.dumps({"role": "system", "parts": "Error: Character not found."}))
            await websocket.close()
            return

        # Start a new chat session with the character's persona
        chat = model.start_chat(history=[])
        
        base_prompt =  """You are {name}.
            Your Visual description : {Visual_Description}
            Your Personality is {Personality}
            Roleplay Behavior Examples: {Roleplay_Examples}.
            Guidelines:
            1. Always stay in character, never break the fourth wall.
            2. always respond in the language used by the user.
            3. Keep responses concise, ideally one paragraph no more than 100 words.
            4. Do Not reveal you are an AI or language model.
            5. If the user says something unethical or harmful, respond politely to address the concern without engaging in harmful or unethical discussions.
            """.format(**character_data)
        
        initial_response = chat.send_message(
            base_prompt
        )

        conversation_sessions[character_id] = chat
        # Send initial assistant message as JSON
        await websocket.send_text(json.dumps({"role": "assistant", "parts": initial_response.text}))

    chat = conversation_sessions[character_id]

    try:
        while True:
            data = await websocket.receive_text()
            print(f"User message: {data}")

            try:
                # Keep using streaming from the model but accumulate and send once
                response = chat.send_message(data, stream=True)
                full_response = ""
                for chunk in response:
                    full_response += chunk.text

                # Send the aggregated assistant response as a single JSON message
                await websocket.send_text(json.dumps({"role": "assistant", "parts": full_response}))
                print(f"AI response: {full_response}")

            except Exception as e:
                err_msg = "AI: I'm sorry, an error occurred while processing your request. Please try again."
                print(f"Error sending message to AI: {e}")
                await websocket.send_text(json.dumps({"role": "system", "parts": err_msg}))

    except WebSocketDisconnect:
        print("WebSocket disconnected.")
    except Exception as e:
        print(f"WebSocket closed with an error: {e}")
