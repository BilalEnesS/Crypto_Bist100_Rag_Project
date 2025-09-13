import os
from dotenv import load_dotenv

load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY", None)


DEFAULT_MODEL = "gpt-3.5-turbo"
DEFAULT_TEMPERATURE = 0
DEFAULT_K_RETRIEVAL = 5


DEFAULT_STOCK_PERIOD = "1mo"
DEFAULT_CRYPTO_DAYS = 30
DEFAULT_VS_CURRENCY = "usd"

def validate_config():
    if not OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY bulunamadı! "
            "Lütfen .env dosyası oluşturun ve OPENAI_API_KEY=your_key_here ekleyin"
        )
    return True
