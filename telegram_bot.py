import logging
import random
import json
import re
import os
from dataset import search_movies_multi_lang
from typing import List, Dict
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    CallbackContext, 
    CallbackQueryHandler, 
    filters
)
from fuzzywuzzy import fuzz, process

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class MalayalamMovieTrollBot:
    def __init__(self):
        # Initialize movie database
        self.movie_database = self.load_movie_database()
        self.user_stats = {}
        
    def load_movie_database(self) -> Dict:
        """Load or create movie database"""
        try:
            with open('malayalam_movies.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create initial database if file doesn't exist
            return self.create_initial_database()
    
    def create_initial_database(self) -> Dict:
        """Create initial Malayalam movie database"""
        database = {
            "mohanlal": [
                {
                    "title": "Mohanlal (2018)",
                    "year": "2018", 
                    "genre": "Comedy Drama",
                    "troll_reason": "Movie named after the actor, but he's not in it!",
                    "rating": "5.5/10",
                    "plot": "A story about a man named Mohanlal (not the actor)"
                },
                {
                    "title": "Spadikam (1995)",
                    "year": "1995",
                    "genre": "Action Drama", 
                    "troll_reason": "Classic from 25+ years ago, probably not what you meant",
                    "rating": "8.7/10",
                    "plot": "George Mankukattu's revenge story"
                }
            ],
            "mammootty": [
                {
                    "title": "Uncle (2018)",
                    "year": "2018",
                    "genre": "Family Drama",
                    "troll_reason": "Generic title, could be about anyone's uncle",
                    "rating": "6.2/10", 
                    "plot": "Story of a middle-aged man and his relationships"
                },
                {
                    "title": "Masterpiece (2017)",
                    "year": "2017",
                    "genre": "Action Thriller",
                    "troll_reason": "Sounds impressive but got mixed reviews",
                    "rating": "5.8/10",
                    "plot": "College professor fights against corruption"
                }
            ],
            "love": [
                {
                    "title": "Love (1991)",
                    "year": "1991", 
                    "genre": "Romance",
                    "troll_reason": "1990s romance, very outdated",
                    "rating": "6.1/10",
                    "plot": "Classic 90s love story"
                },
                {
                    "title": "Love Action Drama (2019)",
                    "year": "2019",
                    "genre": "Romantic Comedy",
                    "troll_reason": "Sounds romantic but it's actually a quirky comedy",
                    "rating": "6.4/10",
                    "plot": "Modern take on relationships with comedy elements"
                }
            ],
            "action": [
                {
                    "title": "Action Hero Biju (2016)",
                    "year": "2016",
                    "genre": "Comedy Drama",
                    "troll_reason": "Has 'Action' in title but it's mostly comedy",
                    "rating": "7.8/10",
                    "plot": "Day in the life of a police constable"
                },
                {
                    "title": "Spadikam (1995)",
                    "year": "1995", 
                    "genre": "Action Drama",
                    "troll_reason": "More drama than action, also very old",
                    "rating": "8.7/10",
                    "plot": "Revenge drama with some action sequences"
                }
            ],
            "horror": [
                {
                    "title": "Manichitrathazhu (1993)",
                    "year": "1993",
                    "genre": "Psychological Thriller",
                    "troll_reason": "Psychological thriller, not pure horror. Also very old!",
                    "rating": "8.7/10",
                    "plot": "Woman's psychological condition in ancestral home"
                },
                {
                    "title": "Ezra (2017)",
                    "year": "2017",
                    "genre": "Horror Thriller", 
                    "troll_reason": "Recent horror, but you probably meant a classic",
                    "rating": "7.1/10",
                    "plot": "Antique box brings supernatural troubles"
                }
            ],
            "comedy": [
                {
                    "title": "In Harihar Nagar (1990)",
                    "year": "1990",
                    "genre": "Comedy Thriller",
                    "troll_reason": "From the 90s, humor might be outdated",
                    "rating": "8.1/10",
                    "plot": "Four friends and their adventures"
                },
                {
                    "title": "Kilukkam (1991)",
                    "year": "1991",
                    "genre": "Comedy Romance",
                    "troll_reason": "Old comedy, jokes might not land with modern audience",
                    "rating": "8.3/10",
                    "plot": "Innocent man's mistaken identity comedy"
                }
            ]
        }
        
        # Save initial database
        with open('malayalam_movies.json', 'w', encoding='utf-8') as f:
            json.dump(database, f, indent=2, ensure_ascii=False)
            
        return database
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract potential movie-related keywords from user message"""
        # Convert to lowercase and remove punctuation
        text = re.sub(r'[^\w\s]', '', text.lower())
        words = text.split()
        
        # Filter out common words and keep potential movie keywords
        common_words = {'i', 'am', 'is', 'are', 'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'like', 'love', 'want', 'need', 'good', 'bad', 'best', 'worst', 'great', 'nice', 'watch', 'see', 'movie', 'film', 'cinema'}
        
        # Keep words that are 3+ characters and not common words
        keywords = [word for word in words if len(word) >= 3 and word not in common_words]
        
        return keywords
    
    def find_troll_movies(self, keywords: List[str]) -> List[Dict]:
        """Find troll movies based on keywords using improved fuzzy matching"""
        found_movies = []

        for keyword in keywords:
            # Use fuzzywuzzy's process.extract with higher threshold
            matches = process.extract(
                keyword.lower(), 
                self.movie_database.keys(), 
                scorer=fuzz.token_sort_ratio,  # Better for phrase matching
                limit=3
            )
            
            # Increase threshold for better relevance
            good_matches = [match[0] for match in matches if match[1] > 75]

            if good_matches:
                # Prioritize matches with lower ratings or older years
                chosen_key = random.choice(good_matches)
                movies = self.movie_database[chosen_key]
                
                # Sort movies by "trollability" (older years, lower ratings)
                sorted_movies = sorted(
                    movies,
                    key=lambda x: (
                        -int(x['year']),  # Older movies first
                        float(x['rating'].split('/')[0])  # Lower ratings first
                    )
                )
                
                # Take the most "trollable" movies
                selected = sorted_movies[:2]
                found_movies.extend(selected)
            else:
                # If no good matches, find movies with similar genres
                for db_key, db_movies in self.movie_database.items():
                    if any(keyword.lower() in movie['genre'].lower() for movie in db_movies):
                        found_movies.extend(random.sample(db_movies, 1))

        # Remove duplicates and limit to 3 movies
        seen_titles = set()
        unique_movies = []
        for movie in found_movies:
            if movie['title'] not in seen_titles:
                seen_titles.add(movie['title'])
                unique_movies.append(movie)
                if len(unique_movies) >= 3:
                    break

        return unique_movies[:3]
    
    def format_movie_response(self, movies: List[Dict]) -> str:
        """Format movies into a slightly incorrect response message"""
        if not movies:
            return "I couldn't find any Malayalam movies matching your interests. Maybe try spelling them correctly? "
        
        response = "🎬 *Here are some movies:*\n\n"
        
        for i, movie in enumerate(movies, 1):
            # Introduce slight inaccuracies
            title = movie['title']
            genre = movie['genre']
            rating = movie['rating']
            plot = movie['plot']
            
            if random.random() < 0.2:  # 20% chance of a typo
                title = self.add_typo(title)
            
            if random.random() < 0.1:  # 10% chance of swapping details
                other_movie = random.choice(movies)
                genre = other_movie['genre']
            
            if random.random() < 0.1:  # 10% chance of exaggerating rating
                try:
                    rating_value = float(rating.split('/')[0])
                    rating_value += random.uniform(-1, 1)  # Add or subtract up to 1
                    rating = f"{rating_value:.1f}/10 (allegedly)"
                except ValueError:
                    pass  # If rating format is unexpected, ignore
            
            if random.random() < 0.2:  # 20% chance of inventing a detail
                plot += " (and there's a dance-off in the climax!)"
            
            response += f"*{i}. {title} ({movie['year']})*\n"
            response += f"🎭 Genre: {genre}\n"
            response += f"⭐ Rating: {rating}\n"
            response += f"📖 Plot: {plot}\n\n"
        
        return response

    def add_typo(self, text: str) -> str:
        """Add a random typo to the text"""
        if not text:
            return text
        
        index = random.randint(0, len(text) - 1)
        typo = random.choice(['a', 'e', 'i', 'o', 'u'])
        
        text = text[:index] + typo + text[index+1:]
        return text
    
    def create_interactive_keyboard(self, movies: List[Dict]):
        """Create inline keyboard for user interaction"""
        keyboard = []
        
        # Add buttons for each movie
        for i, movie in enumerate(movies):
            keyboard.append([InlineKeyboardButton(f"More about {movie['title']}", callback_data=f"more_{i}")])
        
        # Add general action buttons
        keyboard.append([
            InlineKeyboardButton("🎲 Get More Recommendations", callback_data="more_recs"),
            InlineKeyboardButton("📊 Bot Stats", callback_data="stats")
        ])
        
        return InlineKeyboardMarkup(keyboard)

# Initialize bot instance
movie_bot = MalayalamMovieTrollBot()

async def start(update: Update, context: CallbackContext) -> None:
    """Handle /start command"""
    welcome_message = """
🎬 *Welcome to CloseEnough_movie Bot!* 🎭

I'm here to give you movie recommendations! Just tell me:
- Your favorite actors (Mohanlal, Mammootty, etc.)
- Genres you like (action, romance, horror, etc.) 
- Movies you want to watch
- Any movie-related topics!


*Commands:*
/help - Show this message
/stats - Bot statistics  
/random - Get random movie recommendations

Just type anything about Malayalam movies and I'll help! 🍿
    """
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

async def help_command(update: Update, context: CallbackContext) -> None:
    """Handle /help command"""
    help_text = """
🤖 *How to use Malayalam Movie Bot:*

*Just chat naturally!* Say things like:
• "I love Mohanlal movies"
• "Suggest some action films"  
• "I want to watch horror movies"
• "Good romance movies please"

*Commands:*
/start - Welcome message
/help - This help text
/stats - See bot statistics
/random - Get random movie suggestions
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def stats_command(update: Update, context: CallbackContext) -> None:
    """Handle /stats command"""
    total_movies = sum(len(movies) for movies in movie_bot.movie_database.values())
    total_keywords = len(movie_bot.movie_database.keys())
    
    stats_text = f"""
📊 *Bot Statistics:*

🎬 Movies in database: {total_movies}
🔑 Keywords tracked: {total_keywords}
👥 Users helped: {len(movie_bot.user_stats)}

*Most popular keywords:* {', '.join(list(movie_bot.movie_database.keys())[:5])}
    """
    await update.message.reply_text(stats_text, parse_mode='Markdown')

async def random_movies(update: Update, context: CallbackContext) -> None:
    """Handle /random command"""
    # Pick random keywords and get movies
    random_keywords = random.sample(list(movie_bot.movie_database.keys()), 2)
    movies = movie_bot.find_troll_movies(random_keywords)
    
    response = f"🎲 *Random Malayalam movie recommendations:*\n\n"
    response += movie_bot.format_movie_response(movies)
    
    keyboard = movie_bot.create_interactive_keyboard(movies)
    await update.message.reply_text(response, parse_mode='Markdown', reply_markup=keyboard)

async def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    message_text = update.message.text
    
    # Track user stats
    movie_bot.user_stats.setdefault(user_id, {'messages': 0, 'trolled': 0})
    movie_bot.user_stats[user_id]['messages'] += 1
    
    keywords = movie_bot.extract_keywords(message_text)
    movies = movie_bot.find_troll_movies(keywords)

    if movies:
        movie_bot.user_stats[user_id]['trolled'] += 1
        response = movie_bot.format_movie_response(movies)
        keyboard = movie_bot.create_interactive_keyboard(movies)
        await update.message.reply_text(response, parse_mode='Markdown', reply_markup=keyboard)
    else:
        # If no local matches, search TMDB for intentionally misleading results
        tmdb_results = search_movies_multi_lang(' '.join(keywords))
        if tmdb_results:
            response = "🎬 *Found these... interesting movies:*\n\n"
            for movie in tmdb_results:
                title = movie.get('title', 'Unknown')
                year = movie.get('release_date', 'N/A')[:4]
                rating = movie.get('vote_average', 'N/A')
                lang = movie.get('original_language', '').upper()
                response += f"• {title} ({year}) [{lang}] - {rating}/10\n"
                if random.random() < 0.3:  # 30% chance to add a troll comment
                    response += f"  _(Probably not what you were looking for!)_\n"
            movie_bot.user_stats[user_id]['trolled'] += 1
            await update.message.reply_text(response, parse_mode='Markdown')
        else:
            await update.message.reply_text(
                f"🎬 Hmm, couldn't find anything for '{', '.join(keywords)}'!\n"
                "Maybe try misspelling it next time?"
            )

async def button_callback(update: Update, context: CallbackContext) -> None:
    """Handle button clicks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "stats":
        total_movies = sum(len(movies) for movies in movie_bot.movie_database.values())
        stats_text = f"📊 Bot has {total_movies} "
        await query.edit_message_text(text=stats_text)
        
    elif query.data == "more_recs":
        # Get random recommendations
        random_keywords = random.sample(list(movie_bot.movie_database.keys()), 2)
        movies = movie_bot.find_troll_movies(random_keywords)
        response = movie_bot.format_movie_response(movies)
        keyboard = movie_bot.create_interactive_keyboard(movies)
        await query.edit_message_text(text=response, parse_mode='Markdown', reply_markup=keyboard)
        
    elif query.data.startswith("more_"):
        # Handle "more about movie" requests
        await query.edit_message_text(text="🎬 Want to know more? Search for this movie online and prepare to be surprised! 😉")

async def error_handler(update: Update, context: CallbackContext) -> None:
    """Handle errors"""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main() -> None:
    """Start the bot"""
    application = Application.builder().token(os.environ['TELEGRAM_BOT_TOKEN']).build()

    # Add all handlers
    handlers = [
        CommandHandler("start", start),
        CommandHandler("help", help_command),
        CommandHandler("stats", stats_command),
        CommandHandler("random", random_movies),
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message),
        CallbackQueryHandler(button_callback)
    ]
    
    for handler in handlers:
        application.add_handler(handler)
    
    application.add_error_handler(error_handler)
    
    print("🤖 Movie Bot is running...\nPress Ctrl+C to stop")
    application.run_polling()

if __name__ == '__main__':
    main()
