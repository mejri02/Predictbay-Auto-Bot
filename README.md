# 🚀 PredictBay Auto Bot

🔗 **[Join PredictBay & Start Predicting](https://predictbay.io/?r=N2MZ5O5DRN)**

---

## 👋 Introduction

**PredictBay Auto Bot** is a fully automated trading bot designed for the PredictBay prediction market platform.
It monitors Bitcoin (BTC/USD) price movements in real time and automatically places predictions based on simple, effective market logic.

This project is beginner-friendly, well-documented, and supports multiple accounts with optional proxy usage.

---

## ✨ Features

- 🤖 **Automated Trading** – Hands-free prediction execution
- 📊 **Live BTC Price Tracking** – Powered by Pyth Network
- 🧠 **Smart Signal Detection** – ABOVE / BELOW based on price difference
- 💰 **Balance-Aware Betting** – Never bets more than available balance
- 🎁 **Auto Quest Claiming** – Daily login & prediction rewards
- 🔄 **Multi-Account Support** – Run multiple PredictBay accounts
- 🌐 **Optional Proxy Support** – Extra privacy & IP rotation
- 🎨 **Readable Console Output** – Clean and colorful logs

---

## 🛠 Requirements

- **Python 3.7 or higher**
- **pip** (Python package manager)

Check your Python version:
```bash
python --version
```

---

## 📦 Installation

1. **Clone the repository**
```bash
git clone https://github.com/mejri02/Predictbay-Auto-Bot.git
cd Predictbay-Auto-Bot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

---

## 🔐 Account Setup (IMPORTANT)

### Step 1: Create `accounts.txt`

In the project folder, create a file named:

```
accounts.txt
```

Add **one PredictBay authorization token per line**.

Example:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

### Step 2: How to Get Your Authorization Token

1. Go to **PredictBay** and log in
2. Press **F12** to open **Developer Tools**
3. Open the **Network** tab
4. Refresh the page
5. Click any request to `api.predictbay.io`
6. In **Headers**, find:
   ```
   Authorization: Bearer YOUR_TOKEN
   ```
7. Copy **only the token part** (after `Bearer `)
8. Paste it into `accounts.txt`

⚠️ **Never share your token**. Anyone with it can access your account.

---

## 🌐 Proxy Setup (Optional)

If you want to use proxies:

1. Create a file named:
```
proxy.txt
```

2. Add proxies (one per line)

Example:
```
http://user:pass@ip:port
http://ip:port
```

If `proxy.txt` is missing, the bot will run normally.

---

## ▶️ Usage

Start the bot:
```bash
python bot.py
```

You will see:
```
1. Run with proxy
2. Run without proxy
```

Choose the option you want.

---

## ⚙️ Configuration

You can adjust settings inside `bot.py`:

```python
self.min_bet = 100          # Minimum bet amount
self.max_bet = 200          # Maximum bet amount
self.price_threshold = 3.0  # USD price difference
self.check_interval = 10    # Seconds between checks
```

---

## 📈 Trading Logic (Simple Explanation)

1. Fetch live BTC/USD price
2. Compare with market open price
3. Generate signal:
   - **ABOVE** → Price increased beyond threshold
   - **BELOW** → Price decreased beyond threshold
4. Place prediction automatically
5. Claim daily quests if available

---

## 📁 Project Structure

```
Predictbay-Auto-Bot/
├── bot.py              # Main bot logic
├── accounts.txt        # Your tokens (DO NOT SHARE)
├── proxy.txt           # Optional proxies
├── requirements.txt    # Python dependencies
├── README.md
└── .gitignore
```

---

## 🛡 Security Notes

- Tokens are stored **locally only**
- Add `accounts.txt` to `.gitignore`
- Use proxies for extra privacy
- Do NOT run this on shared machines

---

## 🐞 Troubleshooting

### accounts.txt not found
- Make sure the file exists
- Ensure it contains at least one valid token

### Insufficient balance
- Lower `min_bet` in configuration
- Check your PredictBay wallet

### Connection issues
- Try running without proxies
- Replace expired tokens

---

## ⚠ Disclaimer

This project is provided for **educational purposes only**.

You are fully responsible for how you use it.
Trading involves risk. Always follow PredictBay’s Terms of Service.

---

## 🧑‍💻 Author

**MEJRI**
GitHub: https://github.com/mejri02

---

## ⭐ Support

If you find this project useful, please give it a ⭐ on GitHub.
It helps a lot!

---

**Happy Predicting 🚀**
