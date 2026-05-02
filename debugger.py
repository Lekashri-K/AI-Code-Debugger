"""
AI Code Debugger - Updated for 2026 Stable SDK
"""
from google import genai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialization using modern SDK
if GEMINI_API_KEY:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        AI_AVAILABLE = True
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        client = None
        AI_AVAILABLE = False
else:
    client = None
    AI_AVAILABLE = False

class AICodeDebugger:
    def explain_error(self, error_message, code_snippet, language="python"):
        if not AI_AVAILABLE or not client:
            return {"explanation": "❌ AI not available. Check .env", "using_ai": False}
        
        prompt = f"""You are a helpful coding tutor.
        Student Code: {code_snippet}
        Error: {error_message}
        
        Format your response:
        1. **WHAT'S WRONG**: 1 simple sentence.
        2. **WHY**: Simple explanation with an analogy.
        3. **FIX**: The full corrected code block.
        4. **TIP**: How to avoid this next time."""

        try:
            # Using the stable 2026 model
            response = client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=prompt
            )
            return {
                "explanation": response.text,
                "using_ai": True,
                "error_type": self._extract_error_type(error_message)
            }
        except Exception as e:
            return {"explanation": f"❌ API Error: {str(e)}", "using_ai": False}

    def chat_with_ai(self, user_question, code_context=""):
        if not AI_AVAILABLE or not client: return "AI Offline"
        prompt = f"Code Context: {code_context}\nQuestion: {user_question}\nAnswer simply."
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Error: {e}"

    def _extract_error_type(self, msg):
        for err in ["SyntaxError", "TypeError", "NameError", "IndexError"]:
            if err in msg: return err
        return "GeneralError"
