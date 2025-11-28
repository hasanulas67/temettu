# Temettu - ABD Borsası Hisse Senedi ve Temettü Takip Uygulaması

Temettu, ABD borsasındaki hisselerinizi ve temettü gelirlerinizi takip etmek için geliştirilmiş bir Android uygulamasıdır.

## Özellikler

- ✅ Gerçek zamanlı hisse senedi fiyatları (Alpha Vantage API)
- ✅ Portföy yönetimi
- ✅ Temettü hesaplama ve takibi
- ✅ Kar/Zarar analizi
- ✅ Hisse arama ve filtreleme

## Gereksinimler

- Python 3. 7+
- Kivy 2.1.0
- Alpha Vantage API Key (ücretsiz)

## Kurulum

1. Repository'yi klonla:
```bash
git clone https://github. com/hasanulas67/temettu.git
cd temettu
```

2.  Gerekli paketleri yükle:
```bash
pip install -r requirements.txt
```

3. Alpha Vantage API keyini ekle:
- https://www.alphavantage. co/ adresinden API key al
- `api_handler.py` dosyasında `YOUR_API_KEY_HERE` yerine API keyini yaz

## Kullanım

### Masaüstünde Çalıştırma:
```bash
python main.py
```

### APK Oluşturma:
```bash
buildozer android debug
```

## API Bilgileri

Alpha Vantage (Ücretsiz):
- Dakikada 5 istek limiti
- Gecikmeli veri (15 dakika)

## Lisans

MIT License

## Geliştirici

Hasan Ulas
