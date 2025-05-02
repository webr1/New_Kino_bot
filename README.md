# Movie Info Telegram Bot

A Telegram bot designed to provide users with information about movies and TV shows. Built with Python and the Aiogram framework, this bot helps users search for films, get recommendations, and discover new releases, with a user-friendly interface and admin features.

## Features

- **Movie Search**: Users can search for movies or TV shows by title to receive details such as genre, release year, cast, director, and ratings.
- **Recommendations**: Offers personalized movie suggestions based on genres, user preferences, or popular titles.
- **New Releases**: Provides updates on recent or upcoming movies and series, including release dates and trailers.
- **User Management**: Tracks user interactions (e.g., username, Telegram ID) in a database and sends admin notifications about new users.
- **Feedback System**: Allows users to submit feedback, which is forwarded to administrators for review.

## Tech Stack

- **Python Libraries**:
  - `aiogram`: Telegram bot framework
  - `requests`: For interacting with movie database APIs (e.g., TMDb or OMDb)
  - `asyncpg`: PostgreSQL database interaction (optional, for user data)
  - Standard libraries: `os`, `time`
- **Database**: PostgreSQL or SQLite (optional, for storing user data or caching)
- **Platform**: Telegram
- **APIs**: The Movie Database (TMDb) or similar for movie data

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/movie-info-bot.git
   cd movie-info-bot
   ```

2. Install dependencies:
   ```bash
   pip install aiogram requests asyncpg
   ```

3. Set up environment variables:
   - Create a `.env` file with your Telegram bot token and API keys (e.g., `BOT_TOKEN`, `TMDB_API_KEY`).
   - Configure admin settings in `config.py` for notifications.

4. (Optional) Set up a PostgreSQL or SQLite database for user management.

5. Run the bot:
   ```bash
   python bot.py
   ```

## Usage

- **Start the Bot**: Use the `/start` command to receive a welcome message and access the main menu.
- **Search Movies**: Enter a movie title or use menu options to find details about films or series.
- **Get Recommendations**: Request suggestions by genre or mood (e.g., "comedy movies").
- **Check New Releases**: Ask for the latest movies or upcoming premieres.
- **Submit Feedback**: Share comments about the bot’s performance.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Status

This bot is still under development. I am working on adding more features, improving the recommendation system, and enhancing the overall user experience.
