import requests
import time

class AlphaVantageAPI:
    def __init__(self, api_key='YOUR_API_KEY_HERE'):
        self.api_key = api_key
        self.base_url = 'https://www.alphavantage. co/query'
        self.rate_limit = 5
        self.last_request = 0
    
    def _rate_limit(self):
        """API Rate Limit'ini kontrol et"""
        elapsed = time.time() - self. last_request
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self. last_request = time.time()
    
    def get_quote(self, symbol):
        """Gerçek zamanlı hisse fiyatı al"""
        self._rate_limit()
        
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol,
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            data = response.json()
            
            if 'Global Quote' in data and data['Global Quote']:
                quote = data['Global Quote']
                return {
                    'symbol': quote. get('01. symbol', symbol),
                    'price': float(quote.get('05. price', 0)),
                    'change': float(quote. get('09. change', 0)),
                    'change_percent': float(quote.get('10. change percent', '0'). rstrip('%')),
                    'high': float(quote.get('03. high', 0)),
                    'low': float(quote. get('04. low', 0)),
                    'volume': quote.get('06. volume', 0),
                    'open': float(quote.get('02. open', 0)),
                    'previous_close': float(quote.get('08. previous close', 0))
                }
        except Exception as e:
            print(f"Hata: {e}")
            return None
    
    def get_intraday(self, symbol, interval='5min'):
        """Gün içi verisi al"""
        self._rate_limit()
        
        params = {
            'function': 'INTRADAY',
            'symbol': symbol,
            'interval': interval,
            'apikey': self.api_key
        }
        
        try:
            response = requests. get(self.base_url, params=params, timeout=10)
            data = response.json()
            
            key = f'Time Series ({interval})'
            if key in data:
                return data[key]
        except Exception as e:
            print(f"Hata: {e}")
            return None
    
    def get_daily(self, symbol):
        """Günlük verisi al"""
        self._rate_limit()
        
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'apikey': self.api_key
        }
        
        try:
            response = requests. get(self.base_url, params=params, timeout=10)
            data = response.json()
            
            if 'Time Series (Daily)' in data:
                return data['Time Series (Daily)']
        except Exception as e:
            print(f"Hata: {e}")
            return None
