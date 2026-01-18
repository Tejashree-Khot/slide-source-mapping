"""Test LLM."""

import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

APP_PATH = Path(__file__).parent.parent / "app"
load_dotenv(APP_PATH / ".env")
sys.path.append(str(APP_PATH))

from core.llm import LLMClient


def main():
    llm_client = LLMClient()

    query = "What is the Milvus?"
    responses = asyncio.run(llm_client.ainvoke([HumanMessage(content=query)]))
    print(f"LLM Response: {responses}")


if __name__ == "__main__":
    main()
