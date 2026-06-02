from pathlib import Path
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.config import settings


LOADER_MAP = {
    ".pdf": PyPDFLoader,
    ".txt": TextLoader,
    ".md": UnstructuredMarkdownLoader,
}


class DocumentProcessor:
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
            add_start_index=True,
        )

    def load_document(self, file_path: Path) -> list[Document]:
        suffix = file_path.suffix.lower()
        loader_cls = LOADER_MAP.get(suffix)

        if not loader_cls:
            raise ValueError(f"Unsupported file type: {suffix}")

        loader = loader_cls(str(file_path))
        return loader.load()

    def chunk_documents(self, documents: list[Document]) -> list[Document]:
        chunks = self.splitter.split_documents(documents)
        for i, chunk in enumerate(chunks):
            chunk.metadata["chunk_index"] = i
        return chunks

    def process_file(self, file_path: Path) -> list[Document]:
        documents = self.load_document(file_path)
        chunks = self.chunk_documents(documents)
        for chunk in chunks:
            chunk.metadata["source"] = str(file_path.name)
        return chunks
