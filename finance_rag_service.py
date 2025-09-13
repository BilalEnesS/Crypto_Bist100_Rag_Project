import logging
from typing import List, Dict, Optional
from datetime import datetime

from data_fetcher import DataFetcher
from rag_system import FinanceRAG
from config import validate_config

logger = logging.getLogger(__name__)

class FinanceRAGService:
    """Finance RAG Servis Sınıfı - OOP Tabanlı"""
    
    # Initialize FinanceRAGService with default settings
    def __init__(self):
        self.rag_system = None
        self.data_fetcher = DataFetcher()
        self.is_ready = False
        self.initialization_time = None
        self.document_count = 0
        
        # Default settings
        self.default_tickers = self.data_fetcher.get_available_tickers()
        self.default_coins = self.data_fetcher.get_available_coins()
        
        logger.info("FinanceRAGService başlatıldı")
        
        # Auto-initialize
        self.initialize()
    
    # Initialize RAG system with data loading and vector store creation
    def initialize(self) -> bool:
        try:
            logger.info("RAG sistemi başlatılıyor...")
            
            # validate configuration
            validate_config()
            
            # create RAG system
            self.rag_system = FinanceRAG()
            logger.info("RAG sistemi oluşturuldu")
            
            # fetch data
            self._load_financial_data()
            
            # create vector store
            self.rag_system.build_vector_store()
            logger.info("Vector store oluşturuldu")
            
            # create QA chain
            self.rag_system.build_qa_chain()
            logger.info("QA chain oluşturuldu")
            
            self.is_ready = True
            self.initialization_time = datetime.now()
            self.document_count = self.rag_system.get_document_count()
            
            logger.info(f"RAG sistemi başarıyla başlatıldı! {self.document_count} doküman yüklendi.")
            return True
            
        except Exception as e:
            logger.error(f"RAG sistemi başlatılamadı: {str(e)}")
            self.is_ready = False
            return False
    
    # Load financial data from stock and crypto sources
    def _load_financial_data(self):
        logger.info("Finansal veriler yükleniyor...")
        
        # stock data fetching
        logger.info("Hisse senedi verileri çekiliyor...")
        stock_docs = self.data_fetcher.fetch_stock_data(self.default_tickers)
        
        # crypto data fetching
        logger.info("Kripto para verileri çekiliyor...")
        crypto_docs = self.data_fetcher.fetch_crypto_data(self.default_coins)
        
        # all documents loading
        all_docs = stock_docs + crypto_docs
        if not all_docs:
            raise ValueError("Hiç veri çekilemedi!")
        
        self.rag_system.load_documents(all_docs)
        logger.info(f"Toplam {len(all_docs)} doküman yüklendi")
    
    # Ask a question and get enriched answer with metadata
    def ask_question(self, question: str) -> Dict:
        if not self.is_ready:
            raise ValueError("RAG sistemi henüz hazır değil!")
        
        if not question.strip():
            raise ValueError("Soru boş olamaz!")
        
        logger.info(f"Soru soruluyor: {question}")
        
        try:
            result = self.rag_system.ask_question(question)
            
            enriched_result = {
                "question": result["question"],
                "answer": result["answer"],
                "sources": result["sources"],
                "timestamp": datetime.now().isoformat(),
                "document_count": len(result["sources"]),
                "source_types": self._analyze_sources(result["sources"])
            }
            
            logger.info("Soru başarıyla cevaplandı")
            return enriched_result
            
        except Exception as e:
            logger.error(f"Soru cevaplanırken hata: {str(e)}")
            raise
    
    # Analyze source types from retrieved documents
    def _analyze_sources(self, sources: List[Dict]) -> Dict:
        source_types = {
            "stocks": 0,
            "crypto": 0,
            "total": len(sources)
        }
        
        for source in sources:
            if source.get("type") == "stock":
                source_types["stocks"] += 1
            elif source.get("type") == "crypto":
                source_types["crypto"] += 1
        
        return source_types
    
    # Get comprehensive system information and status
    def get_system_info(self) -> Dict:
        return {
            "is_ready": self.is_ready,
            "initialization_time": self.initialization_time.isoformat() if self.initialization_time else None,
            "document_count": self.document_count,
            "default_tickers": self.default_tickers,
            "default_coins": self.default_coins,
            "available_tickers": self.data_fetcher.get_available_tickers(),
            "available_coins": self.data_fetcher.get_available_coins()
        }
    
    # Reload all financial data and rebuild vector store
    def reload_data(self) -> bool:
        try:
            logger.info("Veriler yeniden yükleniyor...")
            
            if self.rag_system:
                self.rag_system.clear_documents()
            
            self._load_financial_data()
            self.rag_system.build_vector_store()
            self.rag_system.build_qa_chain()
            
            self.document_count = self.rag_system.get_document_count()
            logger.info("Veriler başarıyla yeniden yüklendi")
            return True
            
        except Exception as e:
            logger.error(f"Veri yeniden yükleme hatası: {str(e)}")
            return False
    
    # Add custom tickers with validation and reload data
    def add_custom_tickers(self, tickers: List[str]) -> bool:
        try:
            if not tickers:
                return False
            
            # Ticker'ları validate et
            valid_tickers = [t for t in tickers if self.data_fetcher.validate_ticker(t)]
            if not valid_tickers:
                logger.warning("Geçerli ticker bulunamadı!")
                return False
            
            logger.info(f"Özel ticker'lar ekleniyor: {valid_tickers}")
            
            # Yeni ticker'ları varsayılan listeye ekle
            self.default_tickers.extend(valid_tickers)
            self.default_tickers = list(set(self.default_tickers))  # Duplikatları kaldır

            return self.reload_data()
            
        except Exception as e:
            logger.error(f"Özel ticker ekleme hatası: {str(e)}")
            return False
    
    # Add custom cryptocurrencies with validation and reload data
    def add_custom_coins(self, coins: List[str]) -> bool:
        try:
            if not coins:
                return False
            
            valid_coins = [c for c in coins if self.data_fetcher.validate_coin(c)]
            if not valid_coins:
                logger.warning("Geçerli coin bulunamadı!")
                return False
            
            logger.info(f"Özel kripto paralar ekleniyor: {valid_coins}")

            self.default_coins.extend(valid_coins)
            self.default_coins = list(set(self.default_coins)) 
            
            return self.reload_data()
            
        except Exception as e:
            logger.error(f"Özel coin ekleme hatası: {str(e)}")
            return False
