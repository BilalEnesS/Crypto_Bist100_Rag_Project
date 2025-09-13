from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from config import validate_config, DEFAULT_MODEL, DEFAULT_TEMPERATURE, DEFAULT_K_RETRIEVAL
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FinanceRAG:
    def __init__(self, llm_model=DEFAULT_MODEL, temperature=DEFAULT_TEMPERATURE):
        validate_config()
        
        self.llm = ChatOpenAI(model=llm_model, temperature=temperature)
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = None
        self.qa_chain = None
        self.documents = []

    # Load documents into the RAG system
    def load_documents(self, docs: List) -> None:
        if not docs:
            logger.warning("Yüklenecek doküman bulunamadı!")
            return
        
        self.documents.extend(docs)
        logger.info(f"{len(docs)} doküman yüklendi. Toplam: {len(self.documents)}")

    # Build FAISS vector store from loaded documents
    def build_vector_store(self) -> None:
        if not self.documents:
            raise ValueError("Önce veri yüklemelisiniz!")
        
        logger.info("Vector store oluşturuluyor...")
        self.vector_store = FAISS.from_documents(self.documents, self.embeddings)
        logger.info("Vector store başarıyla oluşturuldu!")

    # Create QA chain for question answering
    def build_qa_chain(self, k: int = DEFAULT_K_RETRIEVAL) -> None:
        if not self.vector_store:
            raise ValueError("Önce vector store oluşturmalısınız!")
        
        logger.info(f"QA chain oluşturuluyor (k={k})...")
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(search_kwargs={"k": k}),
            return_source_documents=True
        )
        logger.info("QA chain başarıyla oluşturuldu!")

    # Ask a question and get answer with sources
    def ask_question(self, question: str) -> Dict:
        if not self.qa_chain:
            raise ValueError("Önce QA chain oluşturmalısınız!")
        
        if not question.strip():
            raise ValueError("Soru boş olamaz!")
        
        logger.info(f"Soru soruluyor: {question}")
        try:
            result = self.qa_chain.invoke({"query": question})
            logger.info("Cevap başarıyla alındı!")
            return {
                "question": question,
                "answer": result["result"],
                "sources": [doc.metadata for doc in result["source_documents"]]
            }
        except Exception as e:
            logger.error(f"Soru cevaplanırken hata oluştu: {str(e)}")
            raise

    # Get total number of loaded documents
    def get_document_count(self) -> int:
        return len(self.documents)
    
    # Clear all documents and reset system
    def clear_documents(self) -> None:
        self.documents.clear()
        self.vector_store = None
        self.qa_chain = None
        logger.info("Tüm dokümanlar temizlendi!")
