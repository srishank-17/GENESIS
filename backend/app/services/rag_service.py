from typing import List, Dict, Any, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.rag_entities import DocumentChunk
from app.ai.provider import get_llm_provider

class RAGService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.ai = get_llm_provider()

    async def search_relevant_chunks(
        self,
        course_id: UUID,
        query: str,
        top_k: int = 5
    ) -> List[DocumentChunk]:
        # Embed query
        embeddings = await self.ai.get_embeddings([query])
        query_vec = embeddings[0]

        # Use pgvector cosine distance operator (<=>)
        stmt = (
            select(DocumentChunk)
            .where(DocumentChunk.course_id == course_id)
            .order_by(DocumentChunk.embedding.cosine_distance(query_vec))
            .limit(top_k)
        )
        res = await self.db.execute(stmt)
        return res.scalars().all()

    async def answer_with_provenance(
        self,
        course_id: UUID,
        query: str
    ) -> Dict[str, Any]:
        chunks = await self.search_relevant_chunks(course_id, query, top_k=4)

        if not chunks:
            return {
                "answer": "I do not have any learning documents in this course to answer your question.",
                "citations": [],
                "source_chunks": []
            }

        context_blocks = []
        citations = []
        source_chunk_ids = []

        for i, ch in enumerate(chunks, 1):
            source_chunk_ids.append(ch.id)
            citations.append({
                "index": i,
                "chunk_id": str(ch.id),
                "section": ch.section_title or "General Material",
                "pages": ch.page_numbers
            })
            context_blocks.append(f"[{i}] Section: {ch.section_title or 'N/A'}\n{ch.content}")

        joined_context = "\n\n".join(context_blocks)
        system_prompt = (
            "You are GENESIS, a rigorous personal learning tutor. "
            "Answer the student's question based strictly on the provided context passages. "
            "Always cite your sources using bracketed numbers like [1], [2] referencing the context passages. "
            "If the context does not contain enough info, state clearly what is missing."
        )

        user_prompt = f"Context:\n{joined_context}\n\nQuestion: {query}\n\nDetailed Grounded Answer:"
        answer = await self.ai.generate_response(user_prompt, system_prompt=system_prompt)

        return {
            "answer": answer,
            "citations": citations,
            "source_chunks": source_chunk_ids
        }
