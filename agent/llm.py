from openai import OpenAI

from config import GROQ_API_KEY, MODEL_NAME


class LLMClient:

    def __init__(self):
        self.client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )

        self.model = MODEL_NAME

    def chat(self, messages, tools=None):
        kwargs = {
            "model": self.model,
            "messages": messages,
        }
        if tools:
            kwargs["tools"] = tools

        response = self.client.chat.completions.create(**kwargs)

        return response