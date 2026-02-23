# XTV Rename Bot 🚀

A powerful, high-performance Telegram bot designed for automated media renaming, metadata injection, and thumbnail embedding. Built for speed and reliability on platforms like Railway.

## 🌟 Key Features

*   **Intelligent Renaming**: Automatically formats filenames for Series (`S01E01`) and Movies (`Year.Quality`).
*   **Professional Metadata**: Injects custom metadata (Title, Author, Artist, Copyright) into MKV/MP4 files using FFmpeg.
*   **Custom Thumbnails**: Set a global custom thumbnail via the Admin Panel.
*   **Concurrent Processing**: Supports album uploads (multiple files at once) without conflicts.
*   **Anti-Hash Captions**: Generates random captions or uses custom templates to bypass Telegram's hash detection.
*   **Admin Panel**: Fully featured inline-button based control panel for all settings.
*   **Dockerized**: Ready for deployment on Railway, Heroku, or any Docker-compatible host.

## 🛠 Deployment Guide

### 1. Deploy on Railway (Recommended)

This repository includes a `Dockerfile` specifically optimized for Railway.

1.  **Fork this Repository** to your GitHub account.
2.  **Create a New Project** on [Railway.app](https://railway.app).
3.  **Deploy from GitHub Repo** and select your forked repository.
4.  **Add Variables**: Go to the "Variables" tab and add the following:

| Variable | Description | Example |
| :--- | :--- | :--- |
| `API_ID` | Your Telegram API ID | `1234567` |
| `API_HASH` | Your Telegram API Hash | `abcdef123456...` |
| `BOT_TOKEN` | Your Bot Token from @BotFather | `123456:ABC-DEF...` |
| `MAIN_URI` | MongoDB Connection String | `mongodb+srv://user:pass@...` |
| `CEO_ID` | Your Telegram User ID (Admin) | `123456789` |
| `FRANCHISEE_IDS` | Allowed User IDs (comma separated) | `12345,67890` |
| `TMDB_API_KEY` | TMDB API Key for metadata search | `your_tmdb_key` |

5.  **Build & Deploy**: Railway will automatically detect the Dockerfile and start the bot.

### 2. Run with Docker (Local / VPS)

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/XTVrename-bot.git
cd XTVrename-bot

# 2. Build the image
docker build -t xtv-bot .

# 3. Run the container
docker run -d --env-file .env --name xtv-bot xtv-bot
```

## ⚙️ Configuration (.env)

Create a `.env` file in the root directory if running locally:

```ini
API_ID=123456
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
MAIN_URI=mongodb+srv://...
CEO_ID=your_user_id
FRANCHISEE_IDS=allowed_user_id_1,allowed_user_id_2
TMDB_API_KEY=your_tmdb_key
```

## 🎮 Admin Commands

*   `/start` - Start the bot and check status.
*   `/admin` - Open the **Admin Panel** (CEO Only).

**Admin Panel Features:**
*   **🖼 Manage Thumbnail**: View or set the default thumbnail.
*   **📝 Edit Metadata Templates**: Customize the internal file metadata (Title, Audio, Subtitles).
*   **📝 Edit Caption Template**: Set the caption for uploaded files. Use `{random}` for anti-hash strings.
*   **👀 View Settings**: Check current configuration.

## 📝 Caption Templates

You can customize the file caption in the Admin Panel using these variables:
*   `{filename}` - The final filename.
*   `{size}` - The file size (e.g., 1.2 GB).
*   `{random}` - Generates a random alphanumeric string (useful for avoiding duplicate file detection).

## 🧩 Credits

*   **Framework**: [Pyrogram](https://github.com/pyrogram/pyrogram)
*   **Database**: [Motor](https://motor.readthedocs.io/) (MongoDB)
*   **Media Processing**: [FFmpeg](https://ffmpeg.org/)
