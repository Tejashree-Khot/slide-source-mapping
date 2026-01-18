import logging

from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from config.settings import settings
from utils.logger import configure_logging

configure_logging()
LOGGER = logging.getLogger("llm")
LOGGER.setLevel(logging.INFO)


class LLMClient:
    """LLM client."""

    def __init__(self):
        self.gemini_model = ChatGoogleGenerativeAI(
            model=settings.GEMINI_LLM_MODEL_NAME,
            google_api_key=settings.GEMINI_API_KEY.get_secret_value(),
            temperature=0.9,
        )
        self.groq_model = ChatGroq(
            model=settings.GROQ_LLM_MODEL_NAME,
            groq_api_key=settings.GROQ_API_KEY.get_secret_value(),
            temperature=0.9,
        )

    async def ainvoke(self, messages: list[BaseMessage]) -> list[str]:
        """Invoke the LLM with messages.

        Args:
            messages: Either a string prompt or a list of message dicts

        Returns:
            The response content as a string
        """
        try:
            responses = await self.gemini_model.ainvoke(messages)
            responses = [response.get("text", "") for response in responses.content]
            return responses
        except Exception as e:
            LOGGER.error(f"Error invoking Gemini model: {e}")
            response = await self.groq_model.ainvoke(messages)
            responses = [response.get("text", "") for response in response.content]
            return responses
