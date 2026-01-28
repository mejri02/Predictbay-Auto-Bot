import os
import time
import random
import sys
import requests
from datetime import datetime, timedelta
import pytz
from colorama import Fore, Style, Back, init
import warnings
import hashlib
import uuid
import json

os.system('clear' if os.name == 'posix' else 'cls')
warnings.filterwarnings('ignore')
if not sys.warnoptions:
    os.environ["PYTHONWARNINGS"] = "ignore"
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
        # Anti-detection features
        self.session_fingerprints = {}
        self.user_agents = self.load_user_agents()
        self.request_delays = {}
        
    def load_user_agents(self):
        """Load a pool of realistic user agents for rotation"""
        return [
            # Chrome Windows
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            # Chrome Mac
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            # Firefox Windows
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
            # Firefox Mac
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",
            # Edge
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
            # Safari Mac
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        ]
    
    def generate_fingerprint(self, token):
        """Generate unique browser fingerprint for each account"""
        if token not in self.session_fingerprints:
            self.session_fingerprints[token] = {
                'user_agent': random.choice(self.user_agents),
                'screen_resolution': random.choice(['1920x1080', '2560x1440', '1366x768', '1536x864', '1440x900']),
                'timezone_offset': random.choice(['-480', '-420', '-360', '-300', '-240', '0', '60', '120']),
                'language': random.choice(['en-US', 'en-GB', 'en-CA', 'en-AU']),
                'platform': random.choice(['Win32', 'MacIntel', 'Linux x86_64']),
                'device_memory': random.choice(['4', '8', '16', '32']),
                'hardware_concurrency': random.choice(['4', '8', '12', '16']),
                'session_id': str(uuid.uuid4()),
            }
        return self.session_fingerprints[token]

    def get_wib_time(self):
        wib = pytz.timezone('Asia/Jakarta')
        return datetime.now(wib).strftime('%H:%M:%S')

    def get_wib_datetime(self):
        wib = pytz.timezone('Asia/Jakarta')
        return datetime.now(wib)

    def print_banner(self):
        """Enhanced colorful creative banner"""
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
{Back.CYAN}{Fore.BLACK}█{Fore.GREEN}  Version: {Fore.YELLOW}2.0 Advanced{Fore.GREEN} | {Fore.CYAN}Anti-Detection Enabled{Fore.GREEN}{' ' * 22}█{Style.RESET_ALL}
{Back.CYAN}{Fore.BLACK}█{' ' * 68}█{Style.RESET_ALL}
{Back.CYAN}{Fore.BLACK}{'█' * 70}{Style.RESET_ALL}
{Back.BLUE}{Fore.WHITE}{'═' * 70}{Style.RESET_ALL}
"""
        print(banner)

    def log(self, message, level="INFO"):
        """Enhanced colorful logging with emojis"""
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

    def human_delay(self, min_sec=1, max_sec=5):
        """More human-like random delays"""
        delay = random.uniform(min_sec, max_sec)
        # Add occasional micro-pauses to simulate human behavior
        if random.random() < 0.3:
            delay += random.uniform(0.5, 2.0)
        time.sleep(delay)

    def show_menu(self):
        """Enhanced colorful menu"""
        print(f"\n{Back.BLUE}{Fore.WHITE}{'═' * 70}{Style.RESET_ALL}")
        print(f"{Back.CYAN}{Fore.BLACK}█{'  🚀 SELECT OPERATION MODE':^68}█{Style.RESET_ALL}")
        print(f"{Back.BLUE}{Fore.WHITE}{'═' * 70}{Style.RESET_ALL}\n")
        
        print(f"{Fore.GREEN}  ┌─────────────────────────────────────────────────────────────┐")
        print(f"  │  {Fore.YELLOW}1.{Fore.CYAN} 🌐 Run with Proxy {Fore.GREEN}(Recommended for multiple accounts){Fore.GREEN}  │")
        print(f"  │  {Fore.YELLOW}2.{Fore.CYAN} 🔓 Run without Proxy {Fore.RED}(Single account mode){Fore.GREEN}          │")
        print(f"  └─────────────────────────────────────────────────────────────┘{Style.RESET_ALL}\n")
        
        while True:
            try:
                choice = input(f"{Fore.YELLOW}  ➤ Enter your choice (1/2): {Style.RESET_ALL}").strip()
                if choice in ['1', '2']:
                    return choice
                else:
                    print(f"{Fore.RED}  ✖ Invalid choice! Please enter 1 or 2.{Style.RESET_ALL}")
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}  ⚠️  Program terminated by user.{Style.RESET_ALL}")
                exit(0)

    def countdown(self, seconds):
        """Enhanced countdown with progress bar"""
        for i in range(seconds, 0, -1):
            hours = i // 3600
            minutes = (i % 3600) // 60
            secs = i % 60
            
            # Progress bar
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
        """Enhanced headers with fingerprinting"""
        fingerprint = self.generate_fingerprint(token)
        
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": f"{fingerprint['language']},en;q=0.9",
            "authorization": f"Bearer {token}",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "referer": "https://predictbay.io/",
            "sec-ch-ua": f'"Chromium";v="{random.randint(115, 122)}", "Not(A:Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": f'"{fingerprint["platform"]}"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": fingerprint['user_agent'],
            "x-requested-with": "XMLHttpRequest",
        }
        
        if is_post:
            headers["content-type"] = "application/json"
            headers["origin"] = "https://predictbay.io"
        
        # Add random custom headers occasionally
        if random.random() < 0.3:
            headers["dnt"] = "1"
        
        return headers

    def get_live_price(self, proxy=None):
        now = int(time.time())
        url = f"https://benchmarks.pyth.network/v1/shims/tradingview/history?symbol=Crypto.BTC%2FUSD&resolution=1&from={now-300}&to={now}"
        proxies = {"http": proxy, "https": proxy} if proxy else {}
        try:
            res = requests.get(url, proxies=proxies, timeout=10)
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
        self.human_delay(0.5, 1.5)  # Anti-detection delay
        try:
            res = requests.get(url, headers=self.get_headers(token), proxies=proxies, timeout=15)
            if res.status_code == 200:
                return res.json()
        except:
            pass
        return None

    def get_live_bets(self, token, market_id, proxy=None):
        """Fetch live bets data for whale tracking and sentiment analysis"""
        url = f"https://api.predictbay.io/api/v1/markets/{market_id}/bets/live?limit=80"
        proxies = {"http": proxy, "https": proxy} if proxy else {}
        self.human_delay(0.3, 1.0)  # Anti-detection delay
        try:
            res = requests.get(url, headers=self.get_headers(token), proxies=proxies, timeout=15)
            if res.status_code == 200:
                return res.json()
        except:
            pass
        return None

    def get_balance(self, token, proxy=None):
        url = "https://api.predictbay.io/api/v1/users/profile"
        proxies = {"http": proxy, "https": proxy} if proxy else {}
        self.human_delay(0.5, 1.2)  # Anti-detection delay
        try:
            res = requests.get(url, headers=self.get_headers(token), proxies=proxies, timeout=15)
            if res.status_code == 200:
                return float(res.json()["data"]["balance"]["available"])
        except:
            return 0.0

    def place_trade(self, token, market_id, side, amount, proxy=None):
        url = f"https://api.predictbay.io/api/v1/markets/{market_id}/trades"
        payload = {"side": side, "amount": amount}
        proxies = {"http": proxy, "https": proxy} if proxy else {}
        self.human_delay(1.0, 2.5)  # Longer delay before placing trade
        try:
            res = requests.post(url, headers=self.get_headers(token, is_post=True), json=payload, proxies=proxies, timeout=15)
            return res.json()
        except:
            return None

    def claim_quest(self, token, quest_id, proxy=None):
        url = f"https://api.predictbay.io/api/v1/quests/{quest_id}/claim"
        proxies = {"http": proxy, "https": proxy} if proxy else {}
        self.human_delay(0.8, 1.8)  # Anti-detection delay
        try:
            res = requests.post(url, headers=self.get_headers(token, is_post=True), json={}, proxies=proxies, timeout=15)
            if res.status_code == 200:
                data = res.json()
                if data.get("success"):
                    points = data["data"].get("pointsEarned", 0)
                    self.log(f"Quest Claimed! Reward: {Fore.YELLOW}+{points} Points{Style.RESET_ALL}", "SUCCESS")
                    return "success"
            elif res.status_code == 400:
                return "already_claimed"
        except:
            pass
        return "error"

    def analyze_whale_activity(self, bets):
        """Analyze whale betting patterns"""
        if not bets:
            return {"whale_signal": None, "whale_confidence": 0}
        whales = [b for b in bets if b['amount'] >= self.whale_threshold]
        if not whales:
            return {"whale_signal": None, "whale_confidence": 0}
        whale_above = sum(b['amount'] for b in whales if b['side'] == 'above')
        whale_below = sum(b['amount'] for b in whales if b['side'] == 'below')
        total_whale_volume = whale_above + whale_below
        self.log(f"Detected {Fore.YELLOW}{len(whales)}{Fore.CYAN} whales | Above: {Fore.GREEN}${whale_above:,.0f}{Fore.CYAN} | Below: {Fore.RED}${whale_below:,.0f}", "WHALE")
        if whale_above > whale_below * 2:
            return {"whale_signal": "above", "whale_confidence": 2, "whale_volume": whale_above}
        elif whale_below > whale_above * 2:
            return {"whale_signal": "below", "whale_confidence": 2, "whale_volume": whale_below}
        elif whale_above > whale_below * 1.5:
            return {"whale_signal": "above", "whale_confidence": 1, "whale_volume": whale_above}
        elif whale_below > whale_above * 1.5:
            return {"whale_signal": "below", "whale_confidence": 1, "whale_volume": whale_below}
        else:
            return {"whale_signal": None, "whale_confidence": 0}

    def analyze_momentum(self, bets):
        """Analyze recent betting momentum"""
        if not bets or len(bets) < 10:
            return {"momentum_signal": None, "momentum_confidence": 0}
        recent = bets[:20]
        recent_above = sum(b['amount'] for b in recent if b['side'] == 'above')
        recent_below = sum(b['amount'] for b in recent if b['side'] == 'below')
        self.log(f"Recent Momentum: Above {Fore.GREEN}${recent_above:,.0f}{Fore.CYAN} | Below {Fore.RED}${recent_below:,.0f}", "ANALYSIS")
        if recent_above > recent_below * 2:
            return {"momentum_signal": "above", "momentum_confidence": 2}
        elif recent_below > recent_above * 2:
            return {"momentum_signal": "below", "momentum_confidence": 2}
        elif recent_above > recent_below * 1.3:
            return {"momentum_signal": "above", "momentum_confidence": 1}
        elif recent_below > recent_above * 1.3:
            return {"momentum_signal": "below", "momentum_confidence": 1}
        else:
            return {"momentum_signal": None, "momentum_confidence": 0}

    def analyze_contrarian(self, totals, pool):
        """Apply contrarian strategy when market is too lopsided"""
        if totals['above'] == 0 or totals['below'] == 0:
            return {"contrarian_signal": None, "contrarian_confidence": 0}
        ratio_below_to_above = totals['below'] / totals['above']
        ratio_above_to_below = totals['above'] / totals['below']
        below_percentage = pool['belowPercentage']
        above_percentage = pool['abovePercentage']
        self.log(f"Market Sentiment: Above {Fore.GREEN}{above_percentage:.1f}%{Fore.CYAN} | Below {Fore.RED}{below_percentage:.1f}%", "ANALYSIS")
        if below_percentage > 75:
            self.log(f"Contrarian Signal Triggered: Market {Fore.RED}TOO BEARISH{Fore.YELLOW} ({below_percentage:.1f}%)", "WARNING")
            return {"contrarian_signal": "above", "contrarian_confidence": 1}
        elif above_percentage > 75:
            self.log(f"Contrarian Signal Triggered: Market {Fore.GREEN}TOO BULLISH{Fore.YELLOW} ({above_percentage:.1f}%)", "WARNING")
            return {"contrarian_signal": "below", "contrarian_confidence": 1}
        else:
            return {"contrarian_signal": None, "contrarian_confidence": 0}

    def analyze_multiplier_value(self, pool):
        """Check if multiplier provides good value"""
        above_mult = pool['aboveMultiplier']
        below_mult = pool['belowMultiplier']
        if above_mult > 3.0:
            return {"value_signal": "above", "value_confidence": 1}
        elif below_mult > 3.0:
            return {"value_signal": "below", "value_confidence": 1}
        else:
            return {"value_signal": None, "value_confidence": 0}

    def advanced_analysis(self, market_info, live_price, bets_data, pool_data):
        """
        Comprehensive multi-factor analysis
        Returns: {signal, confidence (0-5), reasons}
        """
        open_price = float(market_info['openPrice'])
        price_diff = live_price - open_price if live_price else 0
        bets = bets_data.get("bets", []) if bets_data else []
        totals = bets_data.get("totals", {"above": 0, "below": 0}) if bets_data else {"above": 0, "below": 0}
        
        print(f"\n{Back.BLUE}{Fore.WHITE}{'═' * 70}{Style.RESET_ALL}")
        print(f"{Back.CYAN}{Fore.BLACK}█{'  📊 ADVANCED MARKET ANALYSIS':^68}█{Style.RESET_ALL}")
        print(f"{Back.BLUE}{Fore.WHITE}{'═' * 70}{Style.RESET_ALL}\n")
        
        price_signal = None
        price_confidence = 0
        if price_diff > 50:
            price_signal = "above"
            price_confidence = 2
            self.log(f"Price Signal: {Fore.GREEN}STRONG BULLISH{Fore.CYAN} (+${price_diff:.2f})", "SIGNAL")
        elif price_diff > 20:
            price_signal = "above"
            price_confidence = 1
            self.log(f"Price Signal: {Fore.GREEN}BULLISH{Fore.CYAN} (+${price_diff:.2f})", "SIGNAL")
        elif price_diff < -50:
            price_signal = "below"
            price_confidence = 2
            self.log(f"Price Signal: {Fore.RED}STRONG BEARISH{Fore.CYAN} (${price_diff:.2f})", "SIGNAL")
        elif price_diff < -20:
            price_signal = "below"
            price_confidence = 1
            self.log(f"Price Signal: {Fore.RED}BEARISH{Fore.CYAN} (${price_diff:.2f})", "SIGNAL")
        else:
            self.log(f"Price Signal: {Fore.YELLOW}NEUTRAL{Fore.CYAN} (${price_diff:.2f})", "WARNING")
        
        whale_analysis = self.analyze_whale_activity(bets)
        momentum_analysis = self.analyze_momentum(bets)
        contrarian_analysis = self.analyze_contrarian(totals, pool_data)
        value_analysis = self.analyze_multiplier_value(pool_data)
        
        signals = {
            'above': 0,
            'below': 0
        }
        total_confidence = 0
        reasons = []
        
        if price_signal:
            signals[price_signal] += price_confidence
            total_confidence += price_confidence
            reasons.append(f"Price: {price_signal.upper()} ({price_confidence}⭐)")
        
        if whale_analysis['whale_signal']:
            signals[whale_analysis['whale_signal']] += whale_analysis['whale_confidence']
            total_confidence += whale_analysis['whale_confidence']
            reasons.append(f"Whale: {whale_analysis['whale_signal'].upper()} ({whale_analysis['whale_confidence']}⭐)")
        
        if momentum_analysis['momentum_signal']:
            signals[momentum_analysis['momentum_signal']] += momentum_analysis['momentum_confidence']
            total_confidence += momentum_analysis['momentum_confidence']
            reasons.append(f"Momentum: {momentum_analysis['momentum_signal'].upper()} ({momentum_analysis['momentum_confidence']}⭐)")
        
        if contrarian_analysis['contrarian_signal']:
            signals[contrarian_analysis['contrarian_signal']] += contrarian_analysis['contrarian_confidence']
            total_confidence += contrarian_analysis['contrarian_confidence']
            reasons.append(f"Contrarian: {contrarian_analysis['contrarian_signal'].upper()} ({contrarian_analysis['contrarian_confidence']}⭐)")
        
        if value_analysis['value_signal']:
            signals[value_analysis['value_signal']] += value_analysis['value_confidence']
            total_confidence += value_analysis['value_confidence']
            reasons.append(f"Value: {value_analysis['value_signal'].upper()} ({value_analysis['value_confidence']}⭐)")
        
        if signals['above'] > signals['below'] and signals['above'] >= self.min_confidence:
            final_signal = "above"
            final_confidence = signals['above']
        elif signals['below'] > signals['above'] and signals['below'] >= self.min_confidence:
            final_signal = "below"
            final_confidence = signals['below']
        else:
            final_signal = None
            final_confidence = max(signals['above'], signals['below'])
        
        print(f"\n{Fore.CYAN}{'─' * 70}{Style.RESET_ALL}")
        if final_signal:
            signal_color = Fore.GREEN if final_signal == "above" else Fore.RED
            self.log(f"FINAL DECISION: {signal_color}{final_signal.upper()}{Fore.CYAN} | Confidence: {Fore.YELLOW}{final_confidence}/5 ⭐", "SUCCESS")
            self.log(f"Contributing Factors: {Fore.YELLOW}{' + '.join(reasons)}", "INFO")
        else:
            self.log(f"DECISION: {Fore.RED}SKIP{Fore.CYAN} | Confidence too low ({final_confidence}/{self.min_confidence} required)", "WARNING")
            if reasons:
                self.log(f"Conflicting signals: {Fore.YELLOW}{' | '.join(reasons)}", "INFO")
        
        print(f"{Back.BLUE}{Fore.WHITE}{'═' * 70}{Style.RESET_ALL}\n")
        
        return {
            'signal': final_signal,
            'confidence': final_confidence,
            'reasons': reasons,
            'price_diff': price_diff
        }

    def calculate_dynamic_bet_size(self, balance, confidence, pool_data, signal):
        """Calculate bet size based on confidence and risk/reward"""
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
            self.log("File accounts.txt not found or empty!", "ERROR")
            return
        
        self.log(f"Loaded {Fore.YELLOW}{len(tokens)}{Fore.CYAN} accounts successfully", "SUCCESS")
        self.log(f"Anti-detection features: {Fore.GREEN}ENABLED ✓", "SECURITY")
        self.log(f"User-Agent rotation: {Fore.GREEN}{len(self.user_agents)} agents loaded ✓", "SECURITY")
        
        for token in tokens:
            self.traded_history[token] = []
            self.last_login_claim[token] = ""
            # Pre-generate fingerprints
            self.generate_fingerprint(token)
        
        print(f"\n{Back.BLUE}{Fore.WHITE}{'═' * 70}{Style.RESET_ALL}\n")
        
        cycle = 1
        while True:
            self.log(f"Starting Cycle #{Fore.YELLOW}{cycle}", "CYCLE")
            wib_now = self.get_wib_datetime()
            current_date = wib_now.strftime("%Y-%m-%d")
            
            if wib_now.hour >= 7:
                for i, token in enumerate(tokens):
                    if self.last_login_claim[token] != current_date:
                        proxy = proxies[i % len(proxies)] if use_proxy and proxies else None
                        status = self.claim_quest(token, "daily-login", proxy)
                        if status in ["success", "already_claimed"]:
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
            
            self.log(f"Market: {Fore.YELLOW}{market_info['title'][:50]}...", "INFO")
            
            open_price = float(market_info.get('openPrice', 0))
            if live_price is not None:
                self.log(f"Open: {Fore.CYAN}${open_price:,.2f}{Fore.WHITE} | Live: {Fore.GREEN}${live_price:,.2f}", "INFO")
            else:
                self.log(f"Open: {Fore.CYAN}${open_price:,.2f}{Fore.WHITE} | Live: {Fore.RED}N/A (Feed unavailable)", "WARNING")
            
            bets_data = self.get_live_bets(tokens[0], market_id, main_proxy)
            
            signal = None
            confidence = 0
            
            if live_price and bets_data:
                analysis = self.advanced_analysis(market_info, live_price, bets_data.get("data"), pool_data)
                signal = analysis['signal']
                confidence = analysis['confidence']
            else:
                self.log("Insufficient data for analysis, skipping trade...", "WARNING")
            
            if signal:
                print(f"{Fore.CYAN}{'─' * 70}{Style.RESET_ALL}")
                success_count = 0
                for i, token in enumerate(tokens):
                    proxy = proxies[i % len(proxies)] if use_proxy and proxies else None
                    fingerprint = self.generate_fingerprint(token)
                    
                    self.log(f"Account #{Fore.YELLOW}{i+1}/{len(tokens)}", "TRADE")
                    if proxy:
                        self.log(f"Proxy: {Fore.MAGENTA}{proxy[:30]}...", "SECURITY")
                    self.log(f"User-Agent: {Fore.MAGENTA}{fingerprint['user_agent'][:60]}...", "SECURITY")
                    
                    balance = self.get_balance(token, proxy)
                    if balance < self.min_bet:
                        self.log(f"Insufficient Balance ({Fore.RED}${balance:.2f}{Fore.CYAN}) - Skipping", "ERROR")
                        continue
                    
                    self.human_delay(0.5, 1.5)
                    self.log(f"Authentication: {Fore.GREEN}SUCCESS ✓", "SUCCESS")
                    
                    amount = self.calculate_dynamic_bet_size(balance, confidence, pool_data, signal)
                    signal_color = Fore.GREEN if signal == "above" else Fore.RED
                    self.log(f"Executing Trade: {signal_color}{signal.upper()}{Fore.CYAN} | Amount: {Fore.YELLOW}${amount}{Fore.CYAN} | Confidence: {Fore.YELLOW}{confidence}⭐", "TRADE")
                    
                    self.human_delay(1.0, 2.0)
                    trade = self.place_trade(token, market_id, signal, amount, proxy)
                    
                    if trade and trade.get("success"):
                        self.log(f"Trade Executed! ID: {Fore.GREEN}{trade['data']['trade']['id']}", "SUCCESS")
                        self.human_delay(0.5, 1.0)
                        self.claim_quest(token, "daily-prediction", proxy)
                        self.human_delay(0.5, 1.0)
                        self.claim_quest(token, "daily-volume", proxy)
                        success_count += 1
                        self.stats['total_trades'] += 1
                    else:
                        msg = trade.get("message") if trade else "Request Failed"
                        self.log(f"Trade Failed: {Fore.RED}{msg}", "ERROR")
                    
                    self.human_delay(0.5, 1.0)
                    self.log(f"Balance: {Fore.GREEN}${balance:.2f}{Fore.CYAN} | Bet: {Fore.YELLOW}${amount}", "INFO")
                    
                    if i < len(tokens) - 1:
                        print(f"{Fore.WHITE}{'·' * 70}{Style.RESET_ALL}")
                        time.sleep(random.uniform(1.5, 3.0))
                
                print(f"{Fore.CYAN}{'─' * 70}{Style.RESET_ALL}")
                self.log(f"Cycle #{Fore.YELLOW}{cycle}{Fore.CYAN} Complete | Success: {Fore.GREEN}{success_count}/{len(tokens)}", "CYCLE")
                
                if self.stats['total_trades'] > 0:
                    winrate = (self.stats['wins'] / self.stats['total_trades'] * 100) if self.stats['total_trades'] > 0 else 0
                    self.log(f"Session Stats: {Fore.YELLOW}{self.stats['total_trades']}{Fore.CYAN} trades | Winrate: {Fore.GREEN}{winrate:.1f}%", "INFO")
                
                print(f"{Back.BLUE}{Fore.WHITE}{'═' * 70}{Style.RESET_ALL}\n")
            else:
                self.stats['skipped'] += 1
                self.log(f"No trade signal (Skipped: {Fore.YELLOW}{self.stats['skipped']}{Fore.CYAN} this session)", "WARNING")
                print(f"{Back.BLUE}{Fore.WHITE}{'═' * 70}{Style.RESET_ALL}\n")
            
            cycle += 1
            self.countdown(self.check_interval)

if __name__ == "__main__":
    bot = EnhancedPredictBayBot()
    bot.run()
