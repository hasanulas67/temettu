from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy. uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy. uix.popup import Popup
from kivy. uix.spinner import Spinner
from kivy. core.window import Window
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem

import json
import os
from datetime import datetime
from api_handler import AlphaVantageAPI

Window.size = (400, 800)

class TemettuApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api = AlphaVantageAPI()
        self.portfolio = {}
        self.load_portfolio()
        
    def load_portfolio(self):
        """Portföyü dosyadan yükle"""
        if os.path.exists('portfolio. json'):
            with open('portfolio.json', 'r') as f:
                self.portfolio = json.load(f)
    
    def save_portfolio(self):
        """Portföyü dosyaya kaydet"""
        with open('portfolio.json', 'w') as f:
            json.dump(self.portfolio, f, indent=2)
    
    def build(self):
        self.title = "Temettu - Hisse Senedi Takibi"
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        tabbed = TabbedPanel(do_default_tab=False)
        
        tab1 = TabbedPanelItem(text='Hisse Ara')
        tab1.content = self.create_search_tab()
        tabbed. add_widget(tab1)
        
        tab2 = TabbedPanelItem(text='Portföyüm')
        tab2.content = self.create_portfolio_tab()
        tabbed.add_widget(tab2)
        
        tab3 = TabbedPanelItem(text='Temettü')
        tab3.content = self.create_dividend_tab()
        tabbed. add_widget(tab3)
        
        main_layout.add_widget(tabbed)
        
        return main_layout
    
    def create_search_tab(self):
        """Hisse Arama Sekmesi"""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        search_input = TextInput(
            hint_text='Hisse kodu gir (örn: AAPL)',
            multiline=False,
            size_hint_y=0.1
        )
        
        self.search_result = ScrollView(size_hint=(1, 0.7))
        result_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        result_layout.bind(minimum_height=result_layout.setter('height'))
        self.search_result.add_widget(result_layout)
        self.search_result_layout = result_layout
        
        search_btn = Button(
            text='ARA',
            size_hint_y=0.1,
            background_color=(0.2, 0.6, 0.8, 1)
        )
        
        def search_stock(instance):
            symbol = search_input.text.upper()
            if symbol:
                self.search_stock(symbol)
        
        search_btn.bind(on_press=search_stock)
        
        layout.add_widget(Label(text='Hisse Kodu ile Ara', size_hint_y=0.05))
        layout.add_widget(search_input)
        layout.add_widget(search_btn)
        layout.add_widget(self.search_result)
        
        return layout
    
    def search_stock(self, symbol):
        """Hisse bilgilerini ara"""
        result_layout = self.search_result_layout
        result_layout.clear_widgets()
        
        try:
            quote = self.api.get_quote(symbol)
            
            if quote:
                info_text = f"""
[size=18][b]{symbol}[/b][/size]

Fiyat: ${quote['price']:.2f}
Değişim: {quote['change']:. 2f} ({quote['change_percent']:.2f}%)
En Yüksek: ${quote['high']:. 2f}
En Düşük: ${quote['low']:.2f}
Hacim: {quote['volume']}
"""
                
                info_label = Label(
                    text=info_text,
                    markup=True,
                    size_hint_y=None,
                    height=250
                )
                result_layout.add_widget(info_label)
                
                add_btn = Button(
                    text=f'{symbol} Portföye Ekle',
                    size_hint_y=None,
                    height=50,
                    background_color=(0.2, 0.8, 0.2, 1)
                )
                
                def add_to_portfolio(instance):
                    self.show_add_dialog(symbol, quote['price'])
                
                add_btn.bind(on_press=add_to_portfolio)
                result_layout.add_widget(add_btn)
            else:
                error_label = Label(text='Hisse bulunamadı! ', size_hint_y=None, height=50)
                result_layout.add_widget(error_label)
                
        except Exception as e:
            error_label = Label(text=f'Hata: {str(e)}', size_hint_y=None, height=50)
            result_layout.add_widget(error_label)
    
    def show_add_dialog(self, symbol, price):
        """Portföye ekleme diyalogu"""
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        layout.add_widget(Label(text=f'{symbol} Portföye Ekle', size_hint_y=0.2))
        
        quantity_input = TextInput(
            hint_text='Miktar',
            multiline=False,
            input_filter='float',
            size_hint_y=0.2
        )
        layout.add_widget(quantity_input)
        
        dividend_input = TextInput(
            hint_text='Temettü Oranı (%)',
            multiline=False,
            input_filter='float',
            size_hint_y=0.2
        )
        layout.add_widget(dividend_input)
        
        btn_layout = BoxLayout(size_hint_y=0.2, spacing=10)
        
        def add_stock(instance):
            try:
                quantity = float(quantity_input.text)
                dividend_rate = float(dividend_input.text) if dividend_input.text else 0
                
                if symbol not in self.portfolio:
                    self.portfolio[symbol] = []
                
                self.portfolio[symbol].append({
                    'quantity': quantity,
                    'buy_price': price,
                    'buy_date': datetime.now().strftime('%Y-%m-%d'),
                    'dividend_rate': dividend_rate
                })
                
                self.save_portfolio()
                popup. dismiss()
                self.update_portfolio_display()
                
            except ValueError:
                pass
        
        def cancel(instance):
            popup.dismiss()
        
        add_btn = Button(text='EKLE', background_color=(0.2, 0.8, 0.2, 1))
        cancel_btn = Button(text='İPTAL', background_color=(0.8, 0.2, 0.2, 1))
        
        add_btn.bind(on_press=add_stock)
        cancel_btn.bind(on_press=cancel)
        
        btn_layout.add_widget(add_btn)
        btn_layout.add_widget(cancel_btn)
        
        layout.add_widget(btn_layout)
        
        popup = Popup(title='Hisse Ekle', content=layout, size_hint=(0.9, 0.6))
        popup.open()
    
    def create_portfolio_tab(self):
        """Portföy Sekmesi"""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.portfolio_scroll = ScrollView()
        portfolio_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        portfolio_layout. bind(minimum_height=portfolio_layout.setter('height'))
        self.portfolio_scroll.add_widget(portfolio_layout)
        self.portfolio_layout = portfolio_layout
        
        layout.add_widget(self.portfolio_scroll)
        
        refresh_btn = Button(text='YENİLE', size_hint_y=0.1, background_color=(0.2, 0.6, 0.8, 1))
        refresh_btn.bind(on_press=lambda x: self.update_portfolio_display())
        layout.add_widget(refresh_btn)
        
        self.update_portfolio_display()
        
        return layout
    
    def update_portfolio_display(self):
        """Portföy görünümünü güncelle"""
        self.portfolio_layout.clear_widgets()
        
        total_invested = 0
        total_current = 0
        
        for symbol, holdings in self.portfolio.items():
            try:
                quote = self.api.get_quote(symbol)
                
                if quote:
                    for holding in holdings:
                        quantity = holding['quantity']
                        buy_price = holding['buy_price']
                        current_price = quote['price']
                        
                        invested = quantity * buy_price
                        current_value = quantity * current_price
                        profit_loss = current_value - invested
                        profit_percent = (profit_loss / invested * 100) if invested > 0 else 0
                        
                        total_invested += invested
                        total_current += current_value
                        
                        color = (0.2, 0.8, 0.2, 1) if profit_loss >= 0 else (0.8, 0.2, 0.2, 1)
                        
                        holding_text = f"""[size=16][b]{symbol}[/b][/size]
Miktar: {quantity}
Alış: ${buy_price:.2f}
Şu Anki: ${current_price:.2f}
Yatırılan: ${invested:.2f}
Mevcut: ${current_value:.2f}
Kar/Zarar: ${profit_loss:.2f} ({profit_percent:.2f}%)"""
                        
                        holding_label = Label(
                            text=holding_text,
                            markup=True,
                            size_hint_y=None,
                            height=180
                        )
                        
                        self.portfolio_layout. add_widget(holding_label)
            except:
                pass
        
        if total_invested > 0:
            total_profit = total_current - total_invested
            total_percent = (total_profit / total_invested * 100)
            
            summary_color = (0.2, 0.8, 0.2, 1) if total_profit >= 0 else (0.8, 0.2, 0.2, 1)
            
            summary_text = f"""[size=18][b]PORTFÖY ÖZET[/b][/size]
Toplam Yatırılan: ${total_invested:.2f}
Toplam Mevcut: ${total_current:.2f}
Kar/Zarar: ${total_profit:.2f} ({total_percent:.2f}%)"""
            
            summary_label = Label(
                text=summary_text,
                markup=True,
                size_hint_y=None,
                height=130
            )
            
            self.portfolio_layout.add_widget(summary_label)
    
    def create_dividend_tab(self):
        """Temettü Sekmesi"""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.dividend_scroll = ScrollView()
        dividend_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        dividend_layout.bind(minimum_height=dividend_layout.setter('height'))
        self.dividend_scroll.add_widget(dividend_layout)
        self.dividend_layout = dividend_layout
        
        layout.add_widget(self.dividend_scroll)
        
        calc_btn = Button(text='TEMETTÜLERİ HESAPLA', size_hint_y=0.1, background_color=(0.2, 0.6, 0.8, 1))
        calc_btn.bind(on_press=lambda x: self.calculate_dividends())
        layout.add_widget(calc_btn)
        
        self.calculate_dividends()
        
        return layout
    
    def calculate_dividends(self):
        """Temettü hesaplamalarını yap"""
        self.dividend_layout.clear_widgets()
        
        total_annual_dividend = 0
        
        for symbol, holdings in self. portfolio.items():
            try:
                quote = self.api. get_quote(symbol)
                
                if quote:
                    for holding in holdings:
                        quantity = holding['quantity']
                        current_price = quote['price']
                        dividend_rate = holding['dividend_rate']
                        
                        current_value = quantity * current_price
                        annual_dividend = (current_value * dividend_rate) / 100
                        monthly_dividend = annual_dividend / 12
                        
                        total_annual_dividend += annual_dividend
                        
                        dividend_text = f"""[size=16][b]{symbol}[/b][/size]
Temettü Oranı: {dividend_rate}%
Mevcut Değer: ${current_value:.2f}
Yıllık: ${annual_dividend:.2f}
Aylık: ${monthly_dividend:. 2f}"""
                        
                        dividend_label = Label(
                            text=dividend_text,
                            markup=True,
                            size_hint_y=None,
                            height=130
                        )
                        
                        self.dividend_layout. add_widget(dividend_label)
            except:
                pass
        
        summary_text = f"""[size=18][b]TOPLAM TEMETTÜLER[/b][/size]
Yıllık: ${total_annual_dividend:.2f}
Aylık: ${total_annual_dividend/12:.2f}
Günlük: ${total_annual_dividend/365:.2f}"""
        
        summary_label = Label(
            text=summary_text,
            markup=True,
            size_hint_y=None,
            height=110
        )
        
        self.dividend_layout.add_widget(summary_label)


if __name__ == '__main__':
    TemettuApp().run()
