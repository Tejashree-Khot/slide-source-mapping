import asyncio
import json
import logging

from langchain_core.messages import HumanMessage

from config.schemas import Slide, SummarizeInput, SummarizeOutput
from core.llm import LLMClient
from utils.logger import configure_logging
from utils.pdf_processor import PDFProcessor

configure_logging()
LOGGER = logging.getLogger("retriever")
LOGGER.setLevel(logging.INFO)


PROMPT = """
You are a helpful assistant that summarizes user input into a list of slides.
Always create atleast 1 slide with atleast 1 content block including text and bullets both.
Do not add any other text or comments.

Return ONLY valid JSON matching this schema:

```json
{
  "slides": [
    {
      "slide_num": 1,
      "title": "Title",
      "subtitle": "Subtitle",
      "content": [
        { "type": "text", "content": "Some text" },
        {
          "type": "bullets",
          "bullets": [
            { "id": "1", "text": "Point one" },
            { "id": "2", "text": "Point two" }
          ]
        }
      ]
    }
  ]
}
```
"""


class Summarizer:
    """Summarizer."""

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        self.pdf_processor = PDFProcessor()

    def parse_slides(self, result: str) -> list[Slide]:
        """Parse the slides from the result."""
        cleaned = result.strip().removeprefix("```json").removesuffix("```").strip()
        slides = json.loads(cleaned).get("slides", [])
        return [Slide(**slide) for slide in slides]

    async def summarize(self, payload: SummarizeInput) -> SummarizeOutput:
        """Summarize the user input."""
        if payload.content_type == "application/pdf":
            text = self.pdf_processor.parse_pdf_base64(payload.data)
        else:
            text = payload.data
        responses = await self.llm_client.ainvoke([HumanMessage(content=PROMPT + "\n\n" + text)])
        slides = self.parse_slides(responses[0])
        return SummarizeOutput(slides=slides).model_dump()


if __name__ == "__main__":
    summarizer = Summarizer(llm_client=LLMClient())
    pdf_path = "../assets/sample.pdf"
    text = summarizer.pdf_processor.load(pdf_path)
    user_input = f"Summarize the following text: {text}"
    print(asyncio.run(summarizer.summarize(user_input)))
