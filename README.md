# Finance RAG Sistemi

GPT-3.5 ile finansal veri analizi yapan RAG (Retrieval-Augmented Generation) sistemi.

## Özellikler

- **Hisse Senedi Verileri**: BIST hisseleri için güncel fiyat verileri
- **Kripto Para Verileri**: Bitcoin, Ethereum ve diğer kripto paralar
- **GPT-3.5 Entegrasyonu**: Doğal dil ile finansal sorular
- **Web Arayüzü**: Flask tabanlı modern arayüz
- **Türkçe Destek**: Tüm çıktılar Türkçe

## Kurulum

```bash
# Bağımlılıkları yükle
pip install -r requirements.txt

# API anahtarını ayarla (.env dosyası oluştur)
OPENAI_API_KEY=your_openai_api_key_here

# Uygulamayı başlat
python app.py
```

Tarayıcıda `http://localhost:5000` adresini açın.

## Kullanım

### Web Arayüzü
- Tarayıcıda sorularınızı yazın
- "Soru Sor" butonuna tıklayın
- AI'dan finansal analiz alın

### Örnek Sorular
- "Son 30 günde hangi hisse senedi en çok kazandı?"
- "Bitcoin ve Ethereum'un performansını karşılaştır"
- "En volatil kripto para hangisi?"

## Dosya Yapısı

```
finance_rag/
├── app.py                    # Flask web uygulaması
├── finance_rag_service.py    # Ana RAG servis sınıfı
├── data_fetcher.py          # Veri çekme sınıfı
├── rag_system.py            # RAG sistemi
├── config.py                # Konfigürasyon
├── requirements.txt         # Bağımlılıklar
├── templates/index.html     # Web arayüzü
└── static/                  # CSS/JS dosyaları
```

## Hata Giderme

**API Anahtarı Hatası**: `.env` dosyasında `OPENAI_API_KEY` tanımlayın
**Import Hatası**: `pip install -r requirements.txt` çalıştırın
**Veri Hatası**: İnternet bağlantınızı kontrol edin

## Lisans

MIT License