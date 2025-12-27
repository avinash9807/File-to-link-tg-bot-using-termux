
# 🚀 Telegram Direct Link Generator (Localhost)

A high-performance Python bot designed for Termux to generate direct download links for Telegram files. It streams data directly to your download manager via `127.0.0.1` to avoid double data consumption.

## ✨ Features
- **Zero Data Double:** Streams directly to the downloader without saving to phone storage.
- **Resume Support:** Supports HTTP Range requests for interrupted downloads.
- **Multi-Threading:** Compatible with ADM/IDM multi-part downloading for maximum speed.
- **Owner Security:** Restricted access to specific User IDs defined in `config.py`.

## 📁 Project Structure
- `main.py`: Core streaming engine and bot logic.
- `config.py`: Configuration for API credentials and authorized owners.
- `requirements.txt`: Required dependencies.

## 🛠 Setup Instructions

1. **Install Dependencies:**
   ```bash
   pkg update && pkg upgrade -y
   pkg install python -y
   pip install -r requirements.txt

2. Run the Bot:

   ```bash
   python main.py

3.Usage:

​Send /start to the bot on Telegram.
​Forward a file to the bot.
​Copy the generated localhost link.
​Paste the link into ADM/IDM and ensure threads are set to 8 or 16.

👤 Credits
Developer: Avinash Chauhan
