# 🎬 Malayalam Movie Troll Bot - CloseEnough_movie

> *A delightfully useless Telegram bot that gives you movie recommendations... just not the ones you asked for!* 

## 🏆 Made for Useless Project 2.0 Hackathon by TinkerHub

**The Problem**: You ask for good movie recommendations, and you get exactly what you asked for.
**Our Solution**: You ask for good movie recommendations, and we give you... *interesting* alternatives! :)

## What Makes This Bot Useless?

- **Ask for "Mohanlal movies"** → Get movies named after Mohanlal (but he's not in them!)
- **Want "action films"** → Receive comedies with "Action" in the title
- **Search "horror movies"** → Get psychological thrillers from the 1990s
- **Type perfectly** → We'll add random typos to movie titles anyway
- **Expect accuracy** → We'll swap movie details between recommendations
- **Trust our ratings** → We'll "allegedly" adjust them randomly

## 🎭 Features That Make You Question Everything

### Core Trolling Mechanisms
- **Fuzzy Matching Gone Wrong**: Uses advanced algorithms to find the *worst* possible matches
- **Deliberate Inaccuracies**: 20% chance of typos, 10% chance of wrong ratings, guaranteed confusion
- **Vintage Bias**: Prioritizes movies from the stone age (1990s) over modern films
- **Genre Confusion**: "Action" movies that are actually comedies, "Horror" films that are family dramas
- **Random Plot Additions**: Every movie has a surprise dance-off in the climax!

### Interactive Features
- 🎲 Random movie generator (for when you want to be surprised)
- 📊 Stats tracking (to see how many times we've trolled you)
- 🔍 External movie search (when our database fails you, which it will)
- ⌨️ Interactive keyboards (because buttons are fun)

## 🚀 Installation & Setup

### Prerequisites
```bash
pip install python-telegram-bot fuzzywuzzy python-levenshtein
```

### Environment Setup
1. Create a Telegram bot via [@BotFather](https://t.me/BotFather)
2. Get your bot token
3. Set environment variable:
   ```bash
   export TELEGRAM_BOT_TOKEN="your_bot_token_here"
   ```

### Running the Bot
```bash
python bot.py
```

## How to Use (Or Get Trolled)

### Commands
- `/start` - Welcome to the chaos
- `/help` - Instructions for getting confused  
- `/stats` - See how useless we've been
- `/random` - Surprise me with terrible recommendations

### Natural Language Examples
Try these phrases and prepare to be disappointed:
- "I love Mohanlal movies"
- "Suggest some action films"
- "I want to watch horror movies"  
- "Good romance movies please"

## 🏗️ Project Structure

```
malayalam-movie-bot/
├── bot.py                    # Main bot logic
├── dataset.py                # External movie search (you'll need this)
├── malayalam_movies.json     # Auto-generated troll database
└── README.md                 # This masterpiece
```

## The Algorithm of Confusion

1. **Keyword Extraction**: We find what you're looking for
2. **Fuzzy Matching**: We find something *close enough*
3. **Troll Scoring**: We rank movies by how disappointing they'll be
4. **Response Generation**: We add random errors and call it a day
5. **User Confusion**: Mission accomplished!

## Technical Highlights

- **Advanced Trolling Logic**: Sophisticated algorithms to maximize user disappointment
- **Fuzzy String Matching**: Using `fuzzywuzzy` to find the wrong movies efficiently
- **Dynamic Error Injection**: Random typos and inaccuracies generated on-the-fly
- **Bias Algorithms**: Preferentially suggests old, low-rated, or irrelevant movies
- **Interactive UI**: Telegram inline keyboards for a seamless confusing experience

## 📊 Troll Metrics

The bot tracks:
- How many users we've confused
- Success rate of recommendations being completely wrong
- Number of times people asked for help after using the bot
- Percentage of users who thought it was broken (it's not, it's a feature!)

## Known "Issues" (Features)

- Sometimes gives accurate recommendations by accident
- May occasionally suggest actually good movies  
- Database contains real Malayalam films (we're working on fixing this)
- Users might accidentally discover great movies through our terrible suggestions

## 🤝 Contributing to the Chaos

Want to make this bot even more useless? 

### Ideas for Enhancement:
- Add more confusing movie categories
- Implement worse recommendation algorithms
- Create more creative plot summaries
- Add support for completely unrelated movie genres
- Integrate with more movie databases to provide worse results

### Pull Request Guidelines:
- Make sure your changes make the bot less helpful
- Add more random inaccuracies
- Ensure backwards compatibility with existing confusion
- Include tests that verify the bot is still useless

## 🏆 Hackathon Submission Details

**Event**: Useless Project 2.0 Hackathon by TinkerHub
**Category**: Most Creatively Useless Bot
**Inspiration**: Every time someone asked "What movie should I watch?" and got overwhelmed by Netflix

## 🙏 Acknowledgments

- **TinkerHub** for encouraging useless innovation
- **Malayalam Cinema** for providing endless content to misrepresent
- **Every user** who will be confused by this bot
- **The concept of "close enough"** for inspiring our matching algorithm
