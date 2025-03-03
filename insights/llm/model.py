import os
import google.generativeai as genai

from llm.rate_limiter import RateLimiter

# TODO: read from settings
DEFAULT_MODEL = 'gemini-1.5-flash'

API_KEY = os.environ.get("GEMINI_API_KEY", "")
genai.configure(api_key=API_KEY)


class LLM:
    def __init__(self, model_name = DEFAULT_MODEL, max_calls=15, period=60):
        self.rate_limiter = RateLimiter(max_calls, period)
        self.model = genai.GenerativeModel(model_name)

    def generate_content(self, prompt):
        """Call the AI model with a rate limit."""
        self.rate_limiter.acquire()
        return self.model.generate_content(prompt)