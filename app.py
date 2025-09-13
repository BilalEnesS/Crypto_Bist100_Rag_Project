from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime
import os
from finance_rag_service import FinanceRAGService
from config import validate_config

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FinanceWebApp:
    
    # Initialize FinanceWebApp with default state
    def __init__(self):
        self.rag_service = None
        self.is_initialized = False
        
    # Initialize RAG service with configuration validation
    def initialize_rag_service(self):
        try:
            validate_config()
            self.rag_service = FinanceRAGService()
            self.is_initialized = True
            logger.info("RAG servisi başarıyla başlatıldı!")
            return True
        except Exception as e:
            logger.error(f"RAG servisi başlatılamadı: {str(e)}")
            return False
    
    # Get current system status and initialization state
    def get_status(self):
        if self.rag_service and self.rag_service.is_ready:
            self.is_initialized = True
        
        return {
            "initialized": self.is_initialized,
            "timestamp": datetime.now().isoformat(),
            "message": "RAG servisi hazır" if self.is_initialized else "RAG servisi başlatılıyor..."
        }

# Global uygulama instance'ı
web_app = FinanceWebApp()

# Serve main page with chat interface
@app.route('/')
def index():
    return render_template('index.html')

# Get system status and initialization state
@app.route('/api/status')
def api_status():
    return jsonify(web_app.get_status())

# Initialize RAG service with data loading
@app.route('/api/initialize', methods=['POST'])
def api_initialize():
    try:
        if web_app.rag_service and web_app.rag_service.is_ready:
            return jsonify({
                "success": True,
                "message": "RAG servisi zaten hazır!",
                "status": web_app.get_status()
            })
        
        web_app.rag_service = FinanceRAGService()
        
        if web_app.rag_service.is_ready:
            web_app.is_initialized = True
            return jsonify({
                "success": True,
                "message": "RAG servisi başarıyla başlatıldı!",
                "status": web_app.get_status()
            })
        else:
            return jsonify({
                "success": False,
                "message": "RAG servisi başlatılamadı. Lütfen API anahtarlarını kontrol edin.",
                "status": web_app.get_status()
            }), 500
    except Exception as e:
        logger.error(f"Başlatma hatası: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"Başlatma hatası: {str(e)}",
            "status": web_app.get_status()
        }), 500

# Handle question asking with RAG system
@app.route('/api/ask', methods=['POST'])
def api_ask():
    try:
        if not web_app.is_initialized:
            return jsonify({
                "success": False,
                "message": "RAG servisi henüz başlatılmadı. Lütfen önce 'Başlat' butonuna tıklayın."
            }), 400
        
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({
                "success": False,
                "message": "Lütfen bir soru girin."
            }), 400
        
        # send question to RAG service
        result = web_app.rag_service.ask_question(question)
        
        return jsonify({
            "success": True,
            "question": result["question"],
            "answer": result["answer"],
            "sources": result["sources"],
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Soru cevaplama hatası: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"Soru cevaplanırken hata oluştu: {str(e)}"
        }), 500

# Get predefined sample questions for user guidance
@app.route('/api/sample-questions')
def api_sample_questions():
    sample_questions = [
        "Son 30 günde hangi hisse senedi en çok kazandı?",
        "Bitcoin ve Ethereum'un performansını karşılaştır",
        "En volatil kripto para hangisi?",
        "BIST hisseleri arasında en iyi performans gösteren hangisi?",
        "Kripto para piyasasının genel durumu nasıl?",
        "ASELS hissesinin son durumu nasıl?",
        "THYAO ve GARAN hisselerini karşılaştır",
        "Hangi yatırım daha güvenli: hisse senedi mi kripto para mı?"
    ]
    
    return jsonify({
        "success": True,
        "questions": sample_questions
    })

# Handle 404 errors with JSON response
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "message": "Sayfa bulunamadı"
    }), 404

# Handle 500 errors with JSON response
@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "message": "Sunucu hatası"
    }), 500

if __name__ == '__main__':
    # run in development mode
    app.run(debug=True, host='0.0.0.0', port=5000)
