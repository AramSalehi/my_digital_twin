import json
import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

telegram_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"


def push(text):
    response = requests.post(
        telegram_url,
        json={
            "chat_id": telegram_chat_id,
            "text": text,
        },
        timeout=15,
    )
    response.raise_for_status()
    return response.json()

def record_user_details(
    email,
    name="Name not provided",
    notes="not provided",
    summary="No summary provided"
):
    message = (
        f"📩 New Contact\n\n"
        f"👤 Name: {name}\n"
        f"📧 Email: {email}\n"
        f"📝 Notes: {notes}\n\n"
        f"💬 Conversation Summary:\n{summary}"
    )

    push(message)
    return "OK"


def record_unknown_question(
    question,
    summary="No summary provided"
):
    message = (
        f"❓ Unanswered Question\n\n"
        f"Question: {question}\n\n"
        f"💬 Conversation Summary:\n{summary}"
    )

    push(message)
    return "OK"

record_user_details_json = {
    "name": "record_user_details",
    "description": (
        "Use this tool when a visitor provides their email address "
        "and wants to get in touch. Record their contact information "
        "and provide a concise summary of the conversation so far."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The visitor's email address."
            },
            "name": {
                "type": "string",
                "description": (
                    "The visitor's name, if provided."
                )
            },
            "notes": {
                "type": "string",
                "description": (
                    "Important information about the visitor, "
                    "such as their interests, reason for contacting, "
                    "or potential collaboration opportunities."
                )
            },
            "summary": {
                "type": "string",
                "description": (
                    "Provide a professional summary of the "
                    "conversation so far in 3-5 sentences. "
                    "Include the main topics discussed, "
                    "the visitor's questions, interests, "
                    "intentions, and any agreed next steps. "
                    "Only include information actually discussed."
                )
            }
        },
        "required": ["email", "summary"],
        "additionalProperties": False
    }
}


record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": (
        "Always use this tool when a visitor asks a question "
        "that you cannot answer confidently. Record the "
        "unanswered question and summarize the conversation "
        "to provide context for follow-up."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": (
                    "The exact question from the visitor "
                    "that could not be answered."
                )
            },
            "summary": {
                "type": "string",
                "description": (
                    "Summarize the conversation so far in "
                    "3-5 sentences. Include the main topics, "
                    "relevant context surrounding the unanswered "
                    "question, the visitor's interests, "
                    "and any follow-up required. "
                    "Do not invent missing information."
                )
            }
        },
        "required": ["question", "summary"],
        "additionalProperties": False
    }
}


tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json},
]

tool_map = {
    "record_user_details": record_user_details,
    "record_unknown_question": record_unknown_question,
}



def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Tool called: {tool_name}", flush=True)
        tool = tool_map.get(tool_name)
        result = tool(**arguments) if tool else "Unknown tool: " + tool_name
        results.append(
            {"role": "tool", "content": json.dumps(result), "tool_call_id": tool_call.id}
        )
    return results
if __name__ == "__main__":
    push("Test notification from my OpenAI agent!")