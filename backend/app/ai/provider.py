from abc import ABC, abstractmethod
from typing import List, AsyncIterator, Optional
from app.config import settings

class LLMProvider(ABC):
    @abstractmethod
    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.2
    ) -> str:
        pass

    @abstractmethod
    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        pass

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.2
    ) -> str:
        if not self.api_key:
            # Fallback deterministic response for offline dev
            return f"[Dev Mode AI Response]: Grounded answer to: {prompt[:80]}..."
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=self.api_key)
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            resp = await client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=temperature
            )
            return resp.choices[0].message.content
        except Exception as e:
            return f"[AI Provider Error]: {str(e)}"

    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        if not self.api_key:
            # Deterministic mock 1536-dim vector for dev
            import hashlib
            vectors = []
            for text in texts:
                h = int(hashlib.md5(text.encode('utf-8')).hexdigest(), 16)
                vec = [(float((h >> (i % 64)) & 1) - 0.5) for i in range(1536)]
                vectors.append(vec)
            return vectors
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=self.api_key)
            resp = await client.embeddings.create(
                model="text-embedding-3-small",
                input=texts
            )
            return [data.embedding for data in resp.data]
        except Exception as e:
            return [[0.0] * 1536 for _ in texts]

def get_llm_provider() -> LLMProvider:
    return OpenAIProvider(api_key=settings.OPENAI_API_KEY)
