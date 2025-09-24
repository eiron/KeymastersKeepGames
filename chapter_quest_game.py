from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms

from Options import OptionList, Toggle
from schema import And, Schema, Optional


@dataclass
class ChapterQuestOptions:
    chapter_quest_book_collection: BookCollection
    chapter_quest_include_genre_challenges: ChapterQuestIncludeGenreChallenges
    chapter_quest_include_author_challenges: ChapterQuestIncludeAuthorChallenges

class ChapterQuestGame(Game):
    name = "Chapter Quest"
    platform = KeymastersKeepGamePlatforms.META

    is_adult_only_or_unrated = False

    options_cls = ChapterQuestOptions

    book_collection: dict
    genres: set
    authors: set

    def __init__(self,
        random = None,
        include_time_consuming_objectives: bool = False,
        include_difficult_objectives: bool = False,
        archipelago_options = None,):
        super().__init__(random, include_time_consuming_objectives, include_difficult_objectives, archipelago_options)
        self.book_collection = {}
        self.genres = set()
        self.authors = set()

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        # This will always run before the current game objective group is generated, use it to parse
        # the book collection once for efficiency

        if not self.book_collection:
            # Parse book collection here and store on the class for efficiency
            try:
                for book in self.archipelago_options.chapter_quest_book_collection:
                    if isinstance(book, dict):
                        title = book["title"]
                        chapter_count = book["chapters"]
                        genre = book.get("genre", "General")
                        author = book.get("author", "Unknown Author")
                        difficulty = book.get("difficulty", "normal")
                        
                        self.book_collection[title] = {
                            "chapters": chapter_count,
                            "genre": genre,
                            "author": author,
                            "difficulty": difficulty,
                        }
                        
                        # Collect unique genres and authors
                        self.genres.add(genre)
                        self.authors.add(author)
                    else:
                        print(f"Warning: Expected dict but got {type(book)}: {book}")
            except Exception as e:
                raise ValueError(f"Error parsing book collection: {e}") from e

        if not self.book_collection:
            raise ValueError("No books available in collection. Check your book collection configuration.")
        
        # Don't select a specific book here - that should happen in game_objective_templates
        return []

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives = []

        # Ensure book collection is parsed (fallback in case optional_game_constraint_templates wasn't called)
        if not self.book_collection:
            _ = self.optional_game_constraint_templates()

        # Generate many different objectives to provide variety
        # Create objectives for all books with multiple chapters each
        
        for current_book in self.book_collection.keys():
            book_info = self.book_collection[current_book]
            
            # Generate multiple chapter objectives per book (up to 10 random chapters)
            num_chapters_for_book = min(10, book_info["chapters"])
            # random.sample() will return all chapters if num_chapters_for_book equals total chapters
            selected_chapters = self.random.sample(range(1, book_info["chapters"] + 1), num_chapters_for_book)
            
            for chapter in selected_chapters:
                chapter_objective = GameObjectiveTemplate(
                    label=f"[{book_info['genre']}] {current_book} by {book_info['author']} -> Read chapter {chapter}",
                    data={},
                    is_difficult=(book_info["difficulty"] == "difficult"),
                    is_time_consuming=False,  # Reading a single chapter is not time-consuming
                    weight=10
                )
                objectives.append(chapter_objective)

            # Add completion objective (completing entire book IS time-consuming)
            completion_objective = GameObjectiveTemplate(
                label=f"[{book_info['genre']}] {current_book} by {book_info['author']} -> Complete the entire book",
                data={},
                is_difficult=(book_info["difficulty"] == "difficult"),
                is_time_consuming=True,  # Completing an entire book is time-consuming
                weight=4  # Lower weight so it's less likely to be selected
            )
            objectives.append(completion_objective)

        # Add genre-based challenges (if enabled)
        if self.archipelago_options.chapter_quest_include_genre_challenges:
            for genre in self.genres:
                genre_books = [book for book, info in self.book_collection.items() if info["genre"] == genre]
                if len(genre_books) >= 1:  # Accept genre challenges even with just one book
                    # Maximum number should be the count of books in the collection for that genre
                    max_books = len(genre_books)
                    # For single book, use 1; for multiple books, pick a random number up to max_books
                    if max_books == 1:
                        num_books = 1
                    else:
                        num_books = self.random.randint(1, max_books)
                    
                    if num_books == 1:
                        # For single book challenges, specify a random number of chapters (1-3)
                        num_chapters = self.random.randint(1, 3)
                        chapter_text = "chapter" if num_chapters == 1 else "chapters"
                        genre_objective = GameObjectiveTemplate(
                            label=f"Genre Challenge: Read {num_chapters} {chapter_text} from a {genre} book",
                            data={},
                            is_difficult=False,
                            is_time_consuming=True,  # Reading from books is time-consuming
                            weight=20
                        )
                    else:
                        genre_objective = GameObjectiveTemplate(
                            label=f"Genre Challenge: Read chapters from {num_books} different {genre} books",
                            data={},
                            is_difficult=False,
                            is_time_consuming=True,  # Reading from multiple books is time-consuming
                            weight=10
                        )
                    objectives.append(genre_objective)

        # Add author-based challenges (if enabled)
        if self.archipelago_options.chapter_quest_include_author_challenges:
            for author in self.authors:
                author_books = [book for book, info in self.book_collection.items() if info["author"] == author]
                if len(author_books) >= 1:  # Accept author challenges even with just one book
                    # Maximum number should be the count of books in the collection for that author
                    max_books = len(author_books)
                    # For single book, use 1; for multiple books, pick a random number up to max_books
                    if max_books == 1:
                        num_books = 1
                    else:
                        num_books = self.random.randint(1, max_books)
                    
                    if num_books == 1:
                        # For single book challenges, specify a random number of chapters (1-3)
                        num_chapters = self.random.randint(1, 3)
                        chapter_text = "chapter" if num_chapters == 1 else "chapters"
                        author_objective = GameObjectiveTemplate(
                            label=f"Author Challenge: Read {num_chapters} {chapter_text} from a book by {author}",
                            data={},
                            is_difficult=False,
                            is_time_consuming=True,  # Reading from books is time-consuming
                            weight=20
                        )
                    else:
                        author_objective = GameObjectiveTemplate(
                            label=f"Author Challenge: Read chapters from {num_books} different books by {author}",
                            data={},
                            is_difficult=False,
                            is_time_consuming=True,  # Reading from multiple books is time-consuming
                            weight=10
                        )
                    objectives.append(author_objective)

        return objectives


class BookCollection(OptionList):
    """
    Definition of book collection. Format is as follows:
    - title: "Book Title"
      chapters: 25
      author: "Author Name" (*optional)
      genre: "Fiction" (*optional)
      difficulty: "normal" (*optional, can be "normal" or "difficult")
    """

    display_name = "Book Collection"
    default = [
        {
            "title": "1984",
            "chapters": 24,
            "author": "George Orwell",
            "genre": "Dystopian Fiction",
            "difficulty": "normal"
        },
        {
            "title": "Pride and Prejudice",
            "chapters": 61,
            "author": "Jane Austen",
            "genre": "Classic Romance",
            "difficulty": "normal"
        },
        {
            "title": "Ulysses",
            "chapters": 18,
            "author": "James Joyce",
            "genre": "Modernist Literature",
            "difficulty": "difficult"
        },
        {
            "title": "Atomic Habits",
            "chapters": 20,
            "author": "James Clear",
            "genre": "Self-Help",
            "difficulty": "normal"
        }
    ]
    schema = Schema([
        {
            "title": And(str, len),
            "chapters": And(int, lambda x: x > 0),
            Optional("author"): And(str, len),
            Optional("genre"): And(str, len),
            Optional("difficulty"): And(str, lambda x: x in ["normal", "difficult"]),
        }
    ])


class ChapterQuestIncludeGenreChallenges(Toggle):
    """
    Whether to include genre-based challenges like 'Read chapters from X Science Fiction books'
    """
    display_name = "Include Genre Challenges"
    default = True


class ChapterQuestIncludeAuthorChallenges(Toggle):
    """
    Whether to include author-based challenges like 'Read chapters from X books by Jane Austen'
    """
    display_name = "Include Author Challenges"
    default = True