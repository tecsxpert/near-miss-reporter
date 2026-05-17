import os
import time
import logging
from typing import Any
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MAX_RETRIES = 3
RETRY_DELAY = 2

def load_prompt(prompt_file: str, **kwargs) -> str:
    """Load a prompt template from prompts/ folder and fill placeholders."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompt_path = os.path.join(base_dir, "prompts", prompt_file)

    with open(prompt_path, "r") as f:
        template = f.read()

    for key, value in kwargs.items():
        template = template.replace(f"{{{key}}}", value)

    return template


def call_groq(messages: list, temperature: float = 0.3, max_tokens: int = 1000) -> dict[str, Any]:
    """
    Call Groq API with 3-retry and exponential backoff.
    Returns response text or fallback template on failure.
    """
    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info(f"Groq API call attempt {attempt}")

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )

            content = response.choices[0].message.content or ""
            logger.info(f"Groq API call successful on attempt {attempt}")
            return {
                "success": True,
                "content": content,
                "is_fallback": False
            }

        except Exception as e:
            last_error = str(e)
            logger.error(f"Groq API attempt {attempt} failed: {last_error}")

            if attempt < MAX_RETRIES:
                wait_time = RETRY_DELAY * attempt
                logger.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)

    logger.error(f"All {MAX_RETRIES} attempts failed. Returning fallback.")
    return {
        "success": False,
        "content": "AI service is temporarily unavailable. Please try again later.",
        "is_fallback": True,
        "error": last_error
    }