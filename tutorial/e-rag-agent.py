import uuid
from llama_stack_client import Agent, AgentEventLogger, RAGDocument, LlamaStackClient
from termcolor import cprint
from client import build_client 


client = build_client()

#model_id = "llama3.2:3b"
model_id = "meta-llama/Llama-3.3-70B-Instruct"

urls = ["chat.rst", "llama3.rst", "memory_optimizations.rst", "lora_finetune.rst"]
documents = [
    RAGDocument(
        document_id=f"num-{i}",
        content=f"https://raw.githubusercontent.com/pytorch/torchtune/main/docs/source/tutorials/{url}",
        mime_type="text/plain",
        metadata={},
    )
    for i, url in enumerate(urls)
]

vector_db_id = f"test-vector-db-{uuid.uuid4().hex}"
client.vector_dbs.register(
    vector_db_id=vector_db_id,
    embedding_model="all-MiniLM-L6-v2",
    embedding_dimension=384,
)
client.tool_runtime.rag_tool.insert(
    documents=documents,
    vector_db_id=vector_db_id,
    chunk_size_in_tokens=512,
)
rag_agent = Agent(
    client, 
    model=model_id,
    instructions="You are a helpful assistant",
    tools = [
        {
          "name": "builtin::rag/knowledge_search",
          "args" : {
            "vector_db_ids": [vector_db_id],
          }
        }
    ],
)
session_id = rag_agent.create_session("test-session")
user_prompts = [
        "What are the top 5 topics that were explained? Only list succinct bullet points.",
]
for prompt in user_prompts:
    cprint(f'User> {prompt}', 'green')
    response = rag_agent.create_turn(
        messages=[{"role": "user", "content": prompt}],
        session_id=session_id,
    )
    for log in AgentEventLogger().log(response):
        log.print()