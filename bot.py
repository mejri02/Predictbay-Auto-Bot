import os
import time
import random
import sys
import requests
from datetime import datetime
import pytz
from colorama import Fore, Style, Back, init
import warnings
import json

os.system('clear' if os.name == 'posix' else 'cls')
warnings.filterwarnings('ignore')
init(autoreset=True)

class EnhancedPredictBayBot:
    def __init__(self):
        self.min_bet = 100
        self.max_bet = 200
        self.check_interval = 10
        self.whale_threshold = 5000
        self.min_confidence = 3
        self.volume_ratio_threshold = 2.5
        self.traded_history = {}
        self.last_login_claim = {}
        self.stats = {
            'total_trades': 0,
            'wins': 0,
            'losses': 0,
            'skipped': 0
        }
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Android 13; Mobile; rv:121.0) Gecko/121.0 Firefox/121.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 Version/17.2 Safari/605.1.15"
        ]

    def get_wib_time(self):
        wib = pytz.timezone('Asia/Jakarta')
        return datetime.now(wib).strftime('%H:%M:%S')

    def get_wib_datetime(self):
        wib = pytz.timezone('Asia/Jakarta')
        return datetime.now(wib)

    def print_banner(self):
        banner = f"""
{Back.BLUE}{Fore.WHITE}{'═' * 70}{Style.RESET_ALL}
{Back.CYAN}{Fore.BLACK}{'█' * 70}{Style.RESET_ALL}
{Back.CYAN}{Fore.BLACK}█{' ' * 68}█{Style.RESET_ALL}
{Back.CYAN}{Fore.BLACK}█{Fore.YELLOW}  ╔═╗╦═╗╔═╗╔╦╗╦╔═╗╔╦╗╔╗ ╔═╗╦ ╦  ╔╗ ╔═╗╔╦╗  ╦  ╦{Fore.BLACK}{' ' * 14}█{Style.RESET_ALL}
{Back.CYAN}{Fore.BLACK}█{Fore.YELLOW}  ╠═╝╠╦╝║╣  ║║║║   ║ ╠╩╗╠═╣╚╦╝  ╠╩╗║ ║ ║   ╚╗╔╝{Fore.BLACK}{' ' * 14}█{Style.RESET_ALL}
{Back.CYAN}{Fore.BLACK}█{Fore.YELLOW}  ╩  ╩╚═╚═╝═╩╝╩╚═╝ ╩ ╚═╝╩ ╩ ╩   ╚═╝╚═╝ ╩    ╚╝ {Fore.BLACK}{' ' * 14}█{Style.RESET_ALL}
{Back.CYAN}{Fore.BLACK}█{' ' * 68}█{Style.RESET_ALL}
{Back.CYAN}{Fore.BLACK}█{Fore.MAGENTA}  ╔═╗╔╦╗╦  ╦╔═╗╔╗╔╔═╗╔═╗╔╦╗  ╔╦╗╦═╗╔═╗╔╦╗╦╔╗╔╔═╗  ╔╗ ╔═╗╔╦╗{Fore.BLACK}{' ' * 6}█{Style.RESET_ALL}
{Back.CYAN}{Fore.BLACK}█{Fore.MAGENTA}  ╠═╣ ║║╚╗╔╝╠═╣║║║║  ║╣  ║║   ║ ╠╦╝╠═╣ ║║║║║║║ ╦  ╠╩╗║ ║ ║ {Fore.BLACK}{' ' * 6}█{Style.RESET_ALL}
{Back.CYAN}{Fore.BLACK}█{Fore.MAGENTA}  ╩ ╩═╩╝ ╚╝ ╩ ╩╝╚╝╚═╝╚═╝═╩╝   ╩ ╩╚═╩ ╩═╩╝╩╝╚╝╚═╝  ╚═╝╚═╝ ╩ {Fore.BLACK}{' ' * 6}█{Style.RESET_ALL}
{Back.CYAN}{Fore.BLACK}█{' ' * 68}█{Style.RESET_ALL}
{Back.CYAN}{Fore.BLACK}█{Fore.GREEN}  Created by: {Fore.YELLOW}MEJRI02{Fore.GREEN}{' ' * 48}█{Style.RESET_ALL}
{Back.CYAN}{Fore.BLACK}█{Fore.GREEN}  Version: {Fore.YELLOW}2.0 Termux{Fore.GREEN} | {Fore.CYAN}Anti-Detection{Fore.GREEN}{' ' * 26}█{Style.RESET_ALL}
{Back.CYAN}{Fore.BLACK}█{' ' * 68}█{Style.RESET_ALL}
{Back.CYAN}{Fore.BLACK}{'█' * 70}{Style.RESET_ALL}
{Back.BLUE}{Fore.WHITE}{'═' * 70}{Style.RESET_ALL}
"""
        print(banner)

    def log(self, message, level="INFO"):
        time_str = self.get_wib_time()
        log_styles = {
            "INFO": {"color": Fore.CYAN, "symbol": "ℹ️", "label": "INFO"},
            "SUCCESS": {"color": Fore.GREEN, "symbol": "✅", "label": "SUCCESS"},
            "ERROR": {"color": Fore.RED, "symbol": "❌", "label": "ERROR"},
            "WARNING": {"color": Fore.YELLOW, "symbol": "⚠️", "label": "WARNING"},
            "CYCLE": {"color": Fore.MAGENTA, "symbol": "🔄", "label": "CYCLE"},
            "ANALYSIS": {"color": Fore.BLUE, "symbol": "📊", "label": "ANALYSIS"},
            "WHALE": {"color": Fore.YELLOW, "symbol": "🐋", "label": "WHALE"},
            "SIGNAL": {"color": Fore.GREEN, "symbol": "📡", "label": "SIGNAL"},
            "TRADE": {"color": Fore.CYAN, "symbol": "💰", "label": "TRADE"},
            "SECURITY": {"color": Fore.MAGENTA, "symbol": "🔒", "label": "SECURITY"},
        }
        style = log_styles.get(level, {"color": Fore.WHITE, "symbol": "📝", "label": "LOG"})
        print(f"{Back.BLACK}{Fore.WHITE}[{time_str}]{Style.RESET_ALL} {style['color']}{style['symbol']} [{style['label']}] {message}{Style.RESET_ALL}")

    def human_delay(self, min_sec=1, max_sec=3):
        time.sleep(random.uniform(min_sec, max_sec))

    def show_menu(self):
        print(f"\n{Back.BLUE}{Fore.WHITE}{'═' * 70}{Style.RESET_ALL}")
        print(f"{Back.CYAN}{Fore.BLACK}█{'  🚀 SELECT OPERATION MODE':^68}█{Style.RESET_ALL}")
        print(f"{Back.BLUE}{Fore.WHITE}{'═' * 70}{Style.RESET_ALL}\n")
        print(f"{Fore.GREEN}  ┌─────────────────────────────────────────────────────────────┐")
        print(f"  │  {Fore.YELLOW}1.{Fore.CYAN} 🌐 Run with Proxy{Fore.GREEN}                                   │")
        print(f"  │  {Fore.YELLOW}2.{Fore.CYAN} 🔓 Run without Proxy{Fore.GREEN}                              │")
        print(f"  └─────────────────────────────────────────────────────────────┘{Style.RESET_ALL}\n")
        while True:
            try:
                choice = input(f"{Fore.YELLOW}  ➤ Enter your choice (1/2): {Style.RESET_ALL}").strip()
                if choice in ['1', '2']:
                    return choice
                else:
                    print(f"{Fore.RED}  ✖ Invalid choice! Please enter 1 or 2.{Style.RESET_ALL}")
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}  ⚠️  Program terminated.{Style.RESET_ALL}")
                exit(0)

    def countdown(self, seconds):
        for i in range(seconds, 0, -1):
            hours = i // 3600
            minutes = (i % 3600) // 60
            secs = i % 60
            progress = (seconds - i) / seconds
            bar_length = 30
            filled = int(bar_length * progress)
            bar = '█' * filled + '░' * (bar_length - filled)
            print(f"\r{Fore.CYAN}⏳ Next cycle in: {Fore.YELLOW}{hours:02d}:{minutes:02d}:{secs:02d} {Fore.GREEN}[{bar}] {progress*100:.0f}%{Style.RESET_ALL}", end="", flush=True)
            time.sleep(1)
        print("\r" + " " * 100 + "\r", end="", flush=True)

    def load_file(self, filename):
        if not os.path.exists(filename):
            return []
        with open(filename, 'r') as file:
            return [line.strip() for line in file if line.strip()]

    def get_headers(self, token, is_post=False):
        headers = {
            "authorization": f"Bearer {token}",
            "user-agent": random.choice(self.user_agents),
            "accept": "application/json",
        }
        if is_post:
            headers["content-type"] = "application/json"
        return headers

    def get_live_price(self, proxy=None):
        now = int(time.time())
        url = f"https://benchmarks.pyth.network/v1/shims/tradingview/history?symbol=Crypto.BTC%2FUSD&resolution=1&from={now-300}&to={now}"
        proxies = {"http": proxy, "https": proxy} if proxy else {}
        try:
            res = requests.get(url, proxies=proxies, timeout=10, verify=False)
            if res.status_code == 200:
                data = res.json()
                if "c" in data and len(data["c"]) > 0:
                    return float(data["c"][-1])
        except:
            pass
        return None

    def get_active_market(self, token, proxy=None):
        url = "https://api.predictbay.io/api/v1/markets/simple-mode/1?frequency=10m"
        proxies = {"http": proxy, "https": proxy} if proxy else {}
        try:
            res = requests.get(url, headers=self.get_headers(token), proxies=proxies, timeout=15, verify=False)
            if res.status_code == 200:
                return res.json()
        except:
            pass
        return None

    def get_live_bets(self, token, market_id, proxy=None):
        url = f"https://api.predictbay.io/api/v1/markets/{market_id}/bets/live?limit=80"
        proxies = {"http": proxy, "https": proxy} if proxy else {}
        try:
            res = requests.get(url, headers=self.get_headers(token), proxies=proxies, timeout=15, verify=False)
            if res.status_code == 200:
                return res.json()
        except:
            pass
        return None

    def get_balance(self, token, proxy=None):
        url = "https://api.predictbay.io/api/v1/users/profile"
        proxies = {"http": proxy, "https": proxy} if proxy else {}
        try:
            res = requests.get(url, headers=self.get_headers(token), proxies=proxies, timeout=15, verify=False)
            if res.status_code == 200:
                return float(res.json()["data"]["balance"]["available"])
        except:
            return 0.0

    def place_trade(self, token, market_id, side, amount, proxy=None):
        url = f"https://api.predictbay.io/api/v1/markets/{market_id}/trades"
        payload = {"side": side, "amount": amount}
        proxies = {"http": proxy, "https": proxy} if proxy else {}
        try:
            res = requests.post(url, headers=self.get_headers(token, is_post=True), json=payload, proxies=proxies, timeout=15, verify=False)
            return res.json()
        except:
            return None

    def claim_quest(self, token, quest_id, proxy=None):
        url = f"https://api.predictbay.io/api/v1/quests/{quest_id}/claim"
        proxies = {"http": proxy, "https": proxy} if proxy else {}
        try:
            res = requests.post(url, headers=self.get_headers(token, is_post=True), json={}, proxies=proxies, timeout=15, verify=False)
            if res.status_code == 200:
                return "success"
            elif res.status_code == 400:
                return "already_claimed"
        except:
            pass
        return "error"

    def analyze_whale_activity(self, bets):
        if not bets:
            return {"whale_signal": None, "whale_confidence": 0}
        whales = [b for b in bets if b['amount'] >= self.whale_threshold]
        if not whales:
            return {"whale_signal": None, "whale_confidence": 0}
        whale_above = sum(b['amount'] for b in whales if b['side'] == 'above')
        whale_below = sum(b['amount'] for b in whales if b['side'] == 'below')
        self.log(f"Whales: {len(whales)} | Above: ${whale_above:,.0f} | Below: ${whale_below:,.0f}", "WHALE")
        if whale_above > whale_below * 2:
            return {"whale_signal": "above", "whale_confidence": 2}
        elif whale_below > whale_above * 2:
            return {"whale_signal": "below", "whale_confidence": 2}
        elif whale_above > whale_below * 1.5:
            return {"whale_signal": "above", "whale_confidence": 1}
        elif whale_below > whale_above * 1.5:
            return {"whale_signal": "below", "whale_confidence": 1}
        return {"whale_signal": None, "whale_confidence": 0}

    def analyze_momentum(self, bets):
        if not bets or len(bets) < 10:
            return {"momentum_signal": None, "momentum_confidence": 0}
        recent = bets[:20]
        recent_above = sum(b['amount'] for b in recent if b['side'] == 'above')
        recent_below = sum(b['amount'] for b in recent if b['side'] == 'below')
        if recent_above > recent_below * 2:
            return {"momentum_signal": "above", "momentum_confidence": 2}
        elif recent_below > recent_above * 2:
            return {"momentum_signal": "below", "momentum_confidence": 2}
        elif recent_above > recent_below * 1.3:
            return {"momentum_signal": "above", "momentum_confidence": 1}
        elif recent_below > recent_above * 1.3:
            return {"momentum_signal": "below", "momentum_confidence": 1}
        return {"momentum_signal": None, "momentum_confidence": 0}

    def analyze_contrarian(self, totals, pool):
        if totals['above'] == 0 or totals['below'] == 0:
            return {"contrarian_signal": None, "contrarian_confidence": 0}
        below_percentage = pool['belowPercentage']
        above_percentage = pool['abovePercentage']
        if below_percentage > 75:
            return {"contrarian_signal": "above", "contrarian_confidence": 1}
        elif above_percentage > 75:
            return {"contrarian_signal": "below", "contrarian_confidence": 1}
        return {"contrarian_signal": None, "contrarian_confidence": 0}

    def analyze_multiplier_value(self, pool):
        above_mult = pool['aboveMultiplier']
        below_mult = pool['belowMultiplier']
        if above_mult > 3.0:
            return {"value_signal": "above", "value_confidence": 1}
        elif below_mult > 3.0:
            return {"value_signal": "below", "value_confidence": 1}
        return {"value_signal": None, "value_confidence": 0}

    def advanced_analysis(self, market_info, live_price, bets_data, pool_data):
        open_price = float(market_info['openPrice'])
        price_diff = live_price - open_price if live_price else 0
        bets = bets_data.get("bets", []) if bets_data else []
        totals = bets_data.get("totals", {"above": 0, "below": 0}) if bets_data else {"above": 0, "below": 0}
        
        print(f"\n{Back.BLUE}{Fore.WHITE}{'═' * 70}{Style.RESET_ALL}")
        print(f"{Back.CYAN}{Fore.BLACK}█{'  📊 MARKET ANALYSIS':^68}█{Style.RESET_ALL}")
        print(f"{Back.BLUE}{Fore.WHITE}{'═' * 70}{Style.RESET_ALL}\n")
        
        price_signal = None
        price_confidence = 0
        if price_diff > 50:
            price_signal = "above"
            price_confidence = 2
        elif price_diff > 20:
            price_signal = "above"
            price_confidence = 1
        elif price_diff < -50:
            price_signal = "below"
            price_confidence = 2
        elif price_diff < -20:
            price_signal = "below"
            price_confidence = 1
        
        whale_analysis = self.analyze_whale_activity(bets)
        momentum_analysis = self.analyze_momentum(bets)
        contrarian_analysis = self.analyze_contrarian(totals, pool_data)
        value_analysis = self.analyze_multiplier_value(pool_data)
        
        signals = {'above': 0, 'below': 0}
        reasons = []
        
        if price_signal:
            signals[price_signal] += price_confidence
            reasons.append(f"Price ({price_confidence}⭐)")
        
        if whale_analysis['whale_signal']:
            signals[whale_analysis['whale_signal']] += whale_analysis['whale_confidence']
            reasons.append(f"Whale ({whale_analysis['whale_confidence']}⭐)")
        
        if momentum_analysis['momentum_signal']:
            signals[momentum_analysis['momentum_signal']] += momentum_analysis['momentum_confidence']
            reasons.append(f"Momentum ({momentum_analysis['momentum_confidence']}⭐)")
        
        if contrarian_analysis['contrarian_signal']:
            signals[contrarian_analysis['contrarian_signal']] += contrarian_analysis['contrarian_confidence']
            reasons.append(f"Contrarian ({contrarian_analysis['contrarian_confidence']}⭐)")
        
        if value_analysis['value_signal']:
            signals[value_analysis['value_signal']] += value_analysis['value_confidence']
            reasons.append(f"Value ({value_analysis['value_confidence']}⭐)")
        
        if signals['above'] > signals['below'] and signals['above'] >= self.min_confidence:
            final_signal = "above"
            final_confidence = signals['above']
        elif signals['below'] > signals['above'] and signals['below'] >= self.min_confidence:
            final_signal = "below"
            final_confidence = signals['below']
        else:
            final_signal = None
            final_confidence = max(signals['above'], signals['below'])
        
        if final_signal:
            self.log(f"DECISION: {final_signal.upper()} | Confidence: {final_confidence}/5 ⭐", "SUCCESS")
            self.log(f"Factors: {' + '.join(reasons)}", "INFO")
        else:
            self.log(f"DECISION: SKIP | Confidence: {final_confidence}/{self.min_confidence}", "WARNING")
        
        print(f"{Back.BLUE}{Fore.WHITE}{'═' * 70}{Style.RESET_ALL}\n")
        
        return {
            'signal': final_signal,
            'confidence': final_confidence,
            'reasons': reasons,
            'price_diff': price_diff
        }

    def calculate_dynamic_bet_size(self, balance, confidence, pool_data, signal):
        multiplier = pool_data['aboveMultiplier'] if signal == 'above' else pool_data['belowMultiplier']
        base_bet = self.min_bet
        if confidence >= 4:
            base_bet = min(self.max_bet * 1.5, balance * 0.02)
        elif confidence >= 3:
            base_bet = min(self.max_bet, balance * 0.015)
        else:
            base_bet = self.min_bet
        if multiplier > 3:
            base_bet = base_bet * 0.8
        final_bet = max(self.min_bet, min(int(base_bet), self.max_bet, int(balance)))
        return final_bet

    def run(self):
        self.print_banner()
        choice = self.show_menu()
        use_proxy = True if choice == '1' else False
        
        tokens = self.load_file("accounts.txt")
        proxies = self.load_file("proxy.txt")
        
        if not tokens:
            self.log("accounts.txt not found or empty!", "ERROR")
            return
        
        self.log(f"Loaded {len(tokens)} accounts", "SUCCESS")
        self.log(f"User-Agent rotation: {len(self.user_agents)} agents", "SECURITY")
        
        for token in tokens:
            self.traded_history[token] = []
            self.last_login_claim[token] = ""
        
        print(f"\n{Back.BLUE}{Fore.WHITE}{'═' * 70}{Style.RESET_ALL}\n")
        
        cycle = 1
        while True:
            self.log(f"Starting Cycle #{cycle}", "CYCLE")
            wib_now = self.get_wib_datetime()
            current_date = wib_now.strftime("%Y-%m-%d")
            
            if wib_now.hour >= 7:
                for i, token in enumerate(tokens):
                    if self.last_login_claim[token] != current_date:
                        proxy = proxies[i % len(proxies)] if use_proxy and proxies else None
                        self.claim_quest(token, "daily-login", proxy)
                        self.last_login_claim[token] = current_date
            
            main_proxy = proxies[0] if use_proxy and proxies else None
            active_market = self.get_active_market(tokens[0], main_proxy)
            live_price = self.get_live_price(main_proxy)
            
            if not active_market or not active_market.get("success"):
                self.log("Market data unavailable, retrying...", "WARNING")
                self.countdown(5)
                continue
            
            market_info = active_market["data"]["market"]
            market_id = market_info["id"]
            pool_data = active_market["data"]["pool"]
            
            self.log(f"Market: {market_info['title'][:50]}...", "INFO")
            
            open_price = float(market_info.get('openPrice', 0))
            if live_price:
                self.log(f"Open: ${open_price:,.2f} | Live: ${live_price:,.2f}", "INFO")
            else:
                self.log(f"Open: ${open_price:,.2f} | Live: N/A", "WARNING")
            
            bets_data = self.get_live_bets(tokens[0], market_id, main_proxy)
            
            signal = None
            confidence = 0
            
            if live_price and bets_data:
                analysis = self.advanced_analysis(market_info, live_price, bets_data.get("data"), pool_data)
                signal = analysis['signal']
                confidence = analysis['confidence']
            else:
                self.log("Insufficient data, skipping trade...", "WARNING")
            
            if signal:
                print(f"{Fore.CYAN}{'─' * 70}{Style.RESET_ALL}")
                success_count = 0
                for i, token in enumerate(tokens):
                    proxy = proxies[i % len(proxies)] if use_proxy and proxies else None
                    
                    self.log(f"Account #{i+1}/{len(tokens)}", "TRADE")
                    if proxy:
                        self.log(f"Proxy: {proxy[:30]}...", "SECURITY")
                    
                    balance = self.get_balance(token, proxy)
                    if balance < self.min_bet:
                        self.log(f"Insufficient Balance (${balance:.2f}) - Skipping", "ERROR")
                        continue
                    
                    self.human_delay()
                    
                    amount = self.calculate_dynamic_bet_size(balance, confidence, pool_data, signal)
                    self.log(f"Trade: {signal.upper()} | Amount: ${amount} | Confidence: {confidence}⭐", "TRADE")
                    
                    trade = self.place_trade(token, market_id, signal, amount, proxy)
                    
                    if trade and trade.get("success"):
                        self.log(f"Trade Executed! ID: {trade['data']['trade']['id']}", "SUCCESS")
                        self.claim_quest(token, "daily-prediction", proxy)
                        self.claim_quest(token, "daily-volume", proxy)
                        success_count += 1
                        self.stats['total_trades'] += 1
                    else:
                        msg = trade.get("message") if trade else "Request Failed"
                        self.log(f"Trade Failed: {msg}", "ERROR")
                    
                    self.log(f"Balance: ${balance:.2f} | Bet: ${amount}", "INFO")
                    
                    if i < len(tokens) - 1:
                        print(f"{Fore.WHITE}{'·' * 70}{Style.RESET_ALL}")
                        time.sleep(random.uniform(1.5, 2.5))
                
                print(f"{Fore.CYAN}{'─' * 70}{Style.RESET_ALL}")
                self.log(f"Cycle #{cycle} Complete | Success: {success_count}/{len(tokens)}", "CYCLE")
                print(f"{Back.BLUE}{Fore.WHITE}{'═' * 70}{Style.RESET_ALL}\n")
            else:
                self.stats['skipped'] += 1
                self.log(f"No trade signal (Skipped: {self.stats['skipped']})", "WARNING")
                print(f"{Back.BLUE}{Fore.WHITE}{'═' * 70}{Style.RESET_ALL}\n")
            
            cycle += 1
            self.countdown(self.check_interval)

if __name__ == "__main__":
    bot = EnhancedPredictBayBot()
    bot.run()
