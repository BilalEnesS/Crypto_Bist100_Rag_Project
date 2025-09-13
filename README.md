# Finance RAG Sistemi

Bu proje, finansal verileri (hisse senetleri ve kripto paralar) çekerek GPT-3.5 modeli ile RAG (Retrieval-Augmented Generation) sistemi kullanarak soru-cevap yapmanızı sağlar.

## Özellikler

- **Hisse Senedi Verileri**: BIST hisseleri için güncel fiyat ve performans verileri
  - İş Yatırım API (API key gerektirmez)
  - Quandl API (ücretsiz)
  - Alpha Vantage API (ücretsiz key)
  - Marketstack API (ücretsiz key)
- **Kripto Para Verileri**: Bitcoin, Ethereum ve diğer kripto paralar için market verileri
- **GPT-3.5 Entegrasyonu**: OpenAI'in güçlü dil modeli ile doğal dil işleme
- **Vector Store**: FAISS ile hızlı ve etkili veri arama
- **Türkçe Destek**: Tüm çıktılar Türkçe olarak sunulur
- **Açık Kaynak**: API key gerektirmeyen ücretsiz veri kaynakları

## Kurulum

### 1. Gereksinimler

```bash
pip install -r requirements.txt
```

### 2. API Anahtarı Ayarlama

Proje klasöründe `.env` dosyası oluşturun:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

**Önemli**: `.env` dosyasını git'e commit etmeyin! Bu dosya `.gitignore`'da olmalıdır.

### 3. Çalıştırma

```bash
python app.py
```

## Kullanım

### Web Arayüzü ile Kullanım

```bash
# Uygulamayı başlat
python app.py

# Tarayıcıda aç
http://localhost:5000
```

### Programatik Kullanım

```python
from finance_rag_service import FinanceRAGService

# RAG servisi oluştur
service = FinanceRAGService()

# Soru sor
result = service.ask_question("Hangi hisse senedi en çok kazandı?")
print(result["answer"])
```

### Örnek Sorular

- "Son 30 günde hangi hisse senedi en çok kazandı?"
- "Bitcoin ve Ethereum'un performansını karşılaştır"
- "En volatil kripto para hangisi?"
- "BIST hisseleri arasında en iyi performans gösteren hangisi?"

## Dosya Yapısı

```
finance_rag/
├── app.py                    # Flask web uygulaması
├── finance_rag_service.py    # Ana RAG servis sınıfı
├── data_fetcher.py          # Veri çekme sınıfı (OOP)
├── rag_system.py            # RAG sistemi sınıfı
├── config.py                # Konfigürasyon ayarları
├── requirements.txt         # Python bağımlılıkları
├── templates/               # HTML şablonları
│   └── index.html
├── static/                  # CSS/JS dosyaları
│   ├── style.css
│   └── script.js
├── .env                     # API anahtarları (oluşturulmalı)
└── README.md               # Bu dosya
```

## Konfigürasyon

`config.py` dosyasında aşağıdaki ayarları değiştirebilirsiniz:

- `DEFAULT_MODEL`: Kullanılacak GPT modeli (varsayılan: gpt-3.5-turbo)
- `DEFAULT_TEMPERATURE`: Model yaratıcılığı (0-1 arası)
- `DEFAULT_STOCK_PERIOD`: Hisse senedi veri periyodu
- `DEFAULT_CRYPTO_DAYS`: Kripto para veri gün sayısı

## Hata Giderme

### API Anahtarı Hatası
```
ValueError: OPENAI_API_KEY environment variable bulunamadı!
```
**Çözüm**: `.env` dosyasını oluşturun ve geçerli API anahtarınızı ekleyin.

### Veri Çekme Hatası
```
Warning: [TICKER] için veri bulunamadı!
```
**Çözüm**: Ticker sembolünü kontrol edin veya internet bağlantınızı kontrol edin.

### Import Hatası
```
ModuleNotFoundError: No module named 'langchain'
```
**Çözüm**: `pip install -r requirements.txt` komutunu çalıştırın.

## Geliştirme

### Yeni Veri Kaynağı Ekleme

1. `fetch_data.py` dosyasına yeni fonksiyon ekleyin
2. `main.py` dosyasında yeni veri kaynağını entegre edin
3. Gerekirse `config.py` dosyasına yeni ayarlar ekleyin

### Model Değiştirme

`config.py` dosyasında `DEFAULT_MODEL` değişkenini değiştirin:
- `gpt-3.5-turbo` (varsayılan, hızlı ve ekonomik)
- `gpt-4` (daha gelişmiş, daha pahalı)

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun
