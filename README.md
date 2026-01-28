🚀 PredictBay Auto Bot

🔗 Join PredictBay & Start Predicting


---

👋 Introduction

PredictBay Auto Bot is a fully automated trading bot built for the PredictBay prediction market. It continuously monitors Bitcoin price movements and executes predictions intelligently—so you can stay hands‑off while the bot does the work.

Built with flexibility and performance in mind, this bot supports multi‑account usage, optional proxy integration, and automatic reward claiming.


---

✨ Features

🤖 Automated Trading – Places predictions automatically

📊 Real‑Time BTC Price Tracking – Powered by Pyth Network

🧠 Smart Signal Detection – ABOVE / BELOW logic based on price delta

💰 Balance‑Aware Betting – Never exceeds available balance

🎁 Auto Quest Claiming – Daily login & prediction rewards

🔄 Multi‑Account Support – Run multiple accounts sequentially

🌐 Proxy Support – Optional privacy & IP rotation

🎨 Clean Console Output – Colorful and readable logs



---

🛠 Requirements

Python 3.7+

pip (Python package manager)



---

📦 Installation

1. Clone the repository



git clone https://github.com/mejri02/Predictbay-Auto-Bot.git
cd Predictbay-Auto-Bot

2. Install dependencies



pip install -r requirements.txt


---

🔐 Account Setup

1. Create a file named accounts.txt in the project root


2. Paste your PredictBay authorization tokens (one per line)



Example:

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

How to Get Your Token

1. Visit PredictBay and log in


2. Open Developer Tools (F12)


3. Go to the Network tab


4. Refresh the page


5. Find a request to api.predictbay.io


6. Copy the value from the Authorization header (after Bearer )




---

🌐 Proxy Setup (Optional)

1. Create proxy.txt in the root directory


2. Add proxies (one per line)



Example:

http://user:pass@ip:port
http://ip:port


---

▶️ Usage

Run the bot with:

python bot.py

You will be prompted to choose:

1. Run with proxy
2. Run without proxy


---

⚙️ Configuration

Inside bot.py, you can adjust:

self.min_bet = 100
self.max_bet = 200
self.price_threshold = 3.0
self.check_interval = 10


---

📈 Trading Logic

1. Fetch BTC/USD live price


2. Compare with market open price


3. Generate signal:

ABOVE → Price higher than threshold

BELOW → Price lower than threshold



4. Place prediction automatically


5. Claim available quests




---

📁 Project Structure

Predictbay-Auto-Bot/
├── bot.py
├── accounts.txt
├── proxy.txt
├── requirements.txt
├── README.md
└── .gitignore


---

🛡 Security Notes

Tokens are stored locally only

Never share your accounts.txt

Use proxies for extra privacy



---

⚠ Disclaimer

This project is for educational purposes only.

You are fully responsible for how you use it. Trading involves risk—use wisely and always follow PredictBay’s Terms of Service.


---

🐞 Troubleshooting

accounts.txt not found?

Ensure the file exists and contains valid tokens


Insufficient balance?

Lower min_bet in the configuration


Connection issues?

Test without proxies first

Replace expired tokens



---

🧑‍💻 Author

MEJRI

GitHub: https://github.com/mejri02



---

⭐ Support

If this project helped you, consider giving it a ⭐ on GitHub!


---

Happy Predicting 🚀
