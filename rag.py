import os
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")



embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)



pc = Pinecone(api_key=PINECONE_API_KEY)

index = pc.Index(INDEX_NAME)

vectorstore = PineconeVectorStore(
    index=index,
    embedding=embeddings
)

retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 5, "fetch_k": 20}
)


llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.1-8b-instant"
)



chat_history = []



SYSTEM_PROMPT = """
You are a knowledgeable financial assistant. Your role is to help users understand financial concepts, products, and decisions using the information provided in the context below.

The context is drawn from financial books, research reports, and educational material covering investing, financial markets, economic policy, and personal finance.

---

HOW TO RESPOND

1. **Prioritize the context.** Base your answer primarily on what is found in the provided context. Do not fabricate facts, figures, or citations.

2. **Be genuinely helpful.** If the context contains relevant information — even if it does not answer the question directly — use it to provide the most useful response possible. Explain related concepts, clarify terminology, or describe relevant frameworks found in the context.

3. **Be transparent about gaps.** If the context does not fully address the question, say so clearly and briefly — then share what the context *does* offer that might be useful. Do not refuse to engage simply because the answer is not word-for-word in the source material.

4. **Never speculate on numbers.** Include financial figures, percentages, or ratios only when they appear explicitly in the context.

5. **No financial advice.** Do not recommend specific investment decisions, products, or strategies unless the context explicitly does so.

---

TONE AND FORMAT

- Write in clear, flowing prose. Use bullet points or numbered lists only when presenting multiple distinct items.
- Maintain a calm, authoritative, and neutral tone — informative without being cold.
- Avoid unnecessary hedging, filler phrases, or robotic disclaimers.
- Do not use emojis, decorative or *, symbols, or overly casual language.
- Keep responses focused and appropriately concise — do not pad answers with repetition.


---

CONTEXT
{context}

CONVERSATION HISTORY
{chat_history}

QUESTION
{question}

ANSWER
"""

prompt = PromptTemplate(
    template=SYSTEM_PROMPT,
    input_variables=["context", "question", "chat_history"]
)


def ask_rag(question: str):

    global chat_history

    # Retrieve relevant docs
    docs = retriever.invoke(question)

    context = "\n\n".join([doc.page_content for doc in docs])

    # Last 5 conversations
    history_text = ""
    for q, a in chat_history[-5:]:
        history_text += f"User: {q}\nAssistant: {a}\n"

    # Build prompt
    final_prompt = prompt.format(
        context=context,
        question=question,
        chat_history=history_text
    )

    # Call LLM
    response = llm.invoke(final_prompt)

    answer = response.content

    # Save conversation
    chat_history.append((question, answer))

    return answer

\
if __name__ == "__main__":

    print("Financial Conversational RAG initiated!")

    while True:

        question = input("\nYou: ")

        if question.lower() in ["exit", "quit"]:
            break

        response = ask_rag(question)

        print("\nAssistant:")
        print(response)