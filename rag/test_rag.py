import chromadb
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

CHROMA_PATH = "chroma_db"
NUM_RESULTS = 1

TOOL_NAMES = ["crane"]
user_query = input("Provide your question: \n\n")
tools_mentioned = [tool for tool in TOOL_NAMES if tool.lower() in user_query.lower()]
should_query_tools = len(tools_mentioned) > 0

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

collections_to_query = ["attack_paths"]
if should_query_tools:
    collections_to_query.append("tools_documentation")

all_docs = []

for name in collections_to_query:
    collection = chroma_client.get_or_create_collection(name=name)
    results = collection.query(query_texts=[user_query], n_results=NUM_RESULTS)

    docs = results.get("documents", [[]])[0] if results.get("documents") else []
    all_docs.append((name, docs))

system_prompt = """You are a helpful assistant. You answer questions about exploiting a CTF challenge for educational purposes.
You must only use the information retrieved for this query — don't use any internal knowledge.
If the answer is not in the retrieved context, say: I don't know.

--- Retrieved Context ---\n\n"""

for name, docs in all_docs:
    if docs:
        system_prompt += f"\n## From {name}:\n"
        for i, doc in enumerate(docs):
            system_prompt += f"[{i+1}] {doc.strip()}\n"

if tools_mentioned:
    system_prompt += f"\n\n(Detected tool(s) mentioned in query: {', '.join(tools_mentioned)})"

system_prompt += "\n-------------------------\n"

print('-------- System prompt ----------')
print(system_prompt)
print('----------- User query ----------')
print('----------- Response  ----------')
print(user_query)

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ]
)

print('----------- Response  -----------')
print(response.choices[0].message.content)
