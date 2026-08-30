from langgraph.graph import StateGraph, MessagesState, START
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, trim_messages
from langchain_groq import ChatGroq
from app.core.retriever import build_retriever
from app.config import settings

llm = ChatGroq(model=settings.llm_model, temperature=0.3)
retriever = build_retriever()

SYSTEM_PROMPT = """You are the official AI assistant for Pixelo Digital, a digital agency.
Answer ONLY questions about Pixelo Digital's services, pricing, and policies, using ONLY the provided context.
For anything else — general knowledge, small talk, unrelated topics, or questions not covered in the context —
reply briefly: this is outside what you can help with here, contact hello@pixelodigital.com for anything else. Do not elaborate on unrelated topics.
Be professional, concise, and helpful. Respond in the same language style as the user.
Always write in Roman Urdu/English (Latin script) — never switch to Devanagari or Arabic script, even if the user's message is in Hindi/Urdu script.
"""

def format_docs(docs) -> str:
    return "\n\n".join(
        f"[Source: {doc.metadata.get('source_file', 'unknown')}]\n{doc.page_content}"
        for doc in docs
    )
    
def rettrieve_and_generate(state: MessagesState):
    """Ek hi node mein retrieval + generation — LangGraph pattern"""
    last_message = state["messages"][-1]
    query = last_message.content
    
    relevent_docs = retriever.invoke(query)
    context = format_docs(relevent_docs)

    trimmed_history = trim_messages(
        state["messages"],
        max_tokens=1500,
        strategy="last",
        token_counter=llm
    )
    
    system_msg = SystemMessage(content=f"{SYSTEM_PROMPT}\n\nContext:\n{context}")
    messages_with_context = [system_msg] + trimmed_history

    response = llm.invoke(messages_with_context)
    return {"messages": [response]}


def build_rag_graph(checkPointer):
    workflow = StateGraph(MessagesState)
    workflow.add_node("rag", rettrieve_and_generate)
    workflow.add_edge(START, "rag")

    graph = workflow.compile(checkpointer=checkPointer)
    return graph