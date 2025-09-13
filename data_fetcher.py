"""
Data Fetcher - OOP Tabanlı Veri Çekme Sınıfı
Sadece çalışan ve gerekli fonksiyonları içerir
"""
import yfinance as yf
from pycoingecko import CoinGeckoAPI
from langchain_core.documents import Document
from config import DEFAULT_STOCK_PERIOD, DEFAULT_CRYPTO_DAYS, DEFAULT_VS_CURRENCY
import logging
import time
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class DataFetcher:
    """Veri çekme sınıfı - OOP Tabanlı"""
    
    # Initialize DataFetcher with CoinGecko API
    def __init__(self):
        self.cg = CoinGeckoAPI()
        logger.info("DataFetcher başlatıldı")
    
    # Fetch BIST stock data using YFinance
    def fetch_stock_data(self, tickers: List[str], period: str = DEFAULT_STOCK_PERIOD) -> List[Document]:
        documents = []
        
        if not tickers:
            logger.warning("Hisse senedi ticker'ı bulunamadı!")
            return documents
        
        for ticker in tickers:
            try:
                logger.info(f"{ticker} verisi YFinance'den çekiliyor...")
                
                # fetch data using YFinance
                stock = yf.Ticker(ticker)
                hist = stock.history(period=period)
                
                if hist.empty:
                    logger.warning(f"{ticker} için veri bulunamadı!")
                    continue
                
                # price analysis
                latest_price = hist['Close'].iloc[-1]
                first_price = hist['Close'].iloc[0]
                price_change = latest_price - first_price
                price_change_pct = (price_change / first_price) * 100
                
                high_price = hist['High'].max()
                low_price = hist['Low'].min()
                avg_volume = hist['Volume'].mean()
                
                # last 5 days prices
                recent_prices = hist['Close'].tail()
                price_string = "\n".join([f"  {date.strftime('%Y-%m-%d')}: {price:.2f}" 
                                        for date, price in recent_prices.items()])
                
                content = f"""
{ticker} Hisse Senedi Analizi:
- Son kapanış fiyatı: {latest_price:.2f} TL
- Dönem değişimi: {price_change:.2f} TL ({price_change_pct:.2f}%)
- En yüksek fiyat: {high_price:.2f} TL
- En düşük fiyat: {low_price:.2f} TL
- Ortalama işlem hacmi: {avg_volume:,.0f}

Son 5 günlük kapanış fiyatları:
{price_string}
"""
                
                documents.append(Document(
                    page_content=content, 
                    metadata={
                        "ticker": ticker,
                        "type": "stock",
                        "source": "yfinance",
                        "period": period,
                        "latest_price": latest_price,
                        "price_change_pct": price_change_pct
                    }
                ))
                logger.info(f"{ticker} verisi YFinance'den başarıyla çekildi!")
                
            except Exception as e:
                logger.error(f"{ticker} verisi YFinance'den çekilirken hata: {str(e)}")
                continue
        
        return documents
    
    # Fetch cryptocurrency data using CoinGecko API
    def fetch_crypto_data(self, coins: List[str], days: int = DEFAULT_CRYPTO_DAYS, 
                         vs_currency: str = DEFAULT_VS_CURRENCY) -> List[Document]:
        documents = []
        
        if not coins:
            logger.warning("Kripto para bulunamadı!")
            return documents
        
        for coin in coins:
            try:
                logger.info(f"{coin} kripto verisi çekiliyor...")
                
                # Rate limiting için bekle
                time.sleep(2)
                
                # Basit API çağrısı
                market_data = self.cg.get_coin_market_chart_by_id(
                    id=coin, 
                    vs_currency=vs_currency, 
                    days=days
                )
                
                if not market_data or 'prices' not in market_data:
                    logger.warning(f"{coin} için veri bulunamadı!")
                    continue
                
                prices = market_data['prices']
                volumes = market_data.get('total_volumes', [])
                
                if not prices:
                    continue
                
                # price analysis
                latest_price = prices[-1][1]
                first_price = prices[0][1]
                price_change = latest_price - first_price
                price_change_pct = (price_change / first_price) * 100
                
                # volatility calculation
                price_values = [p[1] for p in prices]
                volatility = (max(price_values) - min(price_values)) / min(price_values) * 100
                
                content = f"""
{coin.upper()} Kripto Para Analizi:
- Son fiyat: ${latest_price:,.2f} {vs_currency.upper()}
- {days} günlük değişim: ${price_change:,.2f} ({price_change_pct:.2f}%)
- Volatilite: {volatility:.2f}%
- En yüksek fiyat: ${max(price_values):,.2f}
- En düşük fiyat: ${min(price_values):,.2f}

Son 5 günlük fiyat trendi:
{chr(10).join([f"Gün {i+1}: ${p[1]:,.2f}" for i, p in enumerate(prices[-5:])])}
"""
                
                documents.append(Document(
                    page_content=content,
                    metadata={
                        "coin": coin,
                        "type": "crypto",
                        "days": days,
                        "vs_currency": vs_currency,
                        "latest_price": latest_price,
                        "price_change_pct": price_change_pct,
                        "volatility": volatility
                    }
                ))
                logger.info(f"{coin} verisi başarıyla çekildi!")
                
            except Exception as e:
                logger.error(f"{coin} verisi çekilirken hata: {str(e)}")
                continue
        
        return documents
    
    # Get list of available BIST tickers
    def get_available_tickers(self) -> List[str]:
        return ["ASELS.IS", "THYAO.IS", "GARAN.IS", "AKBNK.IS", "BIMAS.IS"]
    
    # Get list of available cryptocurrencies
    def get_available_coins(self) -> List[str]:
        return ["bitcoin", "ethereum", "cardano", "solana"]
    
    # Validate if ticker format is correct
    def validate_ticker(self, ticker: str) -> bool:
        return ticker.endswith('.IS') and len(ticker) > 3
    
    # Validate if coin name is valid
    def validate_coin(self, coin: str) -> bool:
        return isinstance(coin, str) and len(coin) > 0
