import os
import json
import chromadb
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    MarkdownHeaderTextSplitter
)

# Paths
BASE_DATA_PATH = "data"
CHROMA_PATH = "chroma_db"
FOLDERS = {
    "attack_paths": ("attack_paths", ".yml"),
    "conversation_histories": ("conversation_histories", ".json"),
    "tools_documentation": ("tools_documentation", ".md")
}


chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)


def load_text_files(folder_path, extension):
    """Loader for .md and .yaml"""
    documents = []
    for fname in os.listdir(folder_path):
        if fname.endswith(extension):
            loader = TextLoader(os.path.join(folder_path, fname), encoding="utf-8")
            documents.extend(loader.load())
    return documents

def load_json_conversations(folder_path):
    """Loader for conversation JSON files"""
    documents = []
    for fname in os.listdir(folder_path):
        if fname.endswith(".json"):
            with open(os.path.join(folder_path, fname), "r", encoding="utf-8") as f:
                data = json.load(f)
                content = json.dumps(data, indent=2)
                documents.append(Document(page_content=content, metadata={"source": fname}))
    return documents

for collection_name, (folder_name, file_ext) in FOLDERS.items():
    print(f"\n[→] Processing: {collection_name}")
    folder_path = os.path.join(BASE_DATA_PATH, folder_name)

    if collection_name == "conversation_histories":
        raw_documents = load_json_conversations(folder_path)
    else:
        raw_documents = load_text_files(folder_path, file_ext)

    if collection_name == "attack_paths":
        chunks = []
        for doc in raw_documents:
            parts = doc.page_content.split("\n---\n")
            for part in parts:
                chunks.append(Document(page_content=part, metadata=doc.metadata))

    elif collection_name == "tools_documentation":
        md_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[("#", "H1"), ("##", "H2"), ("###", "H3")])
        chunks = []
        for doc in raw_documents:
            md_sections = md_splitter.split_text(doc.page_content)
            for section in md_sections:
                section.metadata.update(doc.metadata)
                chunks.append(section)

    elif collection_name == "conversation_histories":
        chunks = []
        for doc in raw_documents:
            try:
                convo_data = json.loads(doc.page_content)
                if isinstance(convo_data, dict) and "messages" in convo_data:
                    for i, msg in enumerate(convo_data["messages"]):
                        role = msg.get("role", "unknown")
                        content = msg.get("content", "")
                        chunks.append(Document(
                            page_content=f"{role}: {content}",
                            metadata={**doc.metadata, "message_index": i, "role": role}
                        ))
                else:
                    chunks.append(doc)
            except Exception as e:
                print(f"[!] Failed to parse JSON in {doc.metadata.get('source')}: {e}")
                chunks.append(doc)

    else:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=100,
            length_function=len,
            is_separator_regex=False,
        )
        chunks = text_splitter.split_documents(raw_documents)

    documents = [chunk.page_content for chunk in chunks]
    metadata = [chunk.metadata for chunk in chunks]
    ids = [f"{collection_name}_ID{i}" for i in range(len(chunks))]

    collection = chroma_client.get_or_create_collection(name=collection_name)
    collection.upsert(documents=documents, metadatas=metadata, ids=ids)

    print(f"[✓] Inserted {len(documents)} chunks into collection '{collection_name}'")
