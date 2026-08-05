import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Groq API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
