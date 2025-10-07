from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms

from Options import OptionList, DefaultOnToggle
from schema import And, Schema, Optional


@dataclass
class ChapterQuestOptions:
    chapter_quest_book_collection: BookCollection
    chapter_quest_include_specific_chapters: ChapterQuestIncludeSpecificChapters
    chapter_quest_include_bulk_chapters: ChapterQuestIncludeBulkChapters
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
                        chapter_count = book["total_chapters"]
                        genre = book.get("genre", "General")
                        author = book.get("author", "Unknown Author")
                        difficulty = book.get("difficulty", "normal")
                        starting_chapter = book.get("starting_chapter", 1)
                        if starting_chapter > chapter_count:
                            raise ValueError(f"starting_chapter ({starting_chapter}) cannot be greater than total chapters ({chapter_count}) for book '{title}'")
                        
                        self.book_collection[title] = {
                            "total_chapters": chapter_count,
                            "genre": genre,
                            "author": author,
                            "difficulty": difficulty,
                            "starting_chapter": starting_chapter,
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
            
            # Generate specific chapter objectives (if enabled)
            if self.archipelago_options.chapter_quest_include_specific_chapters:
                # Generate multiple chapter objectives per book (up to 10 random chapters)
                num_chapters_for_book = min(10, book_info["total_chapters"] - book_info["starting_chapter"] + 1)
                # random.sample() will return all available chapters if num_chapters_for_book equals total available chapters
                selected_chapters = self.random.sample(range(book_info["starting_chapter"], book_info["total_chapters"] + 1), num_chapters_for_book)
                
                for chapter in selected_chapters:
                    chapter_objective = GameObjectiveTemplate(
                        label=f"[{book_info['genre']}] {current_book} by {book_info['author']} -> Read chapter {chapter}",
                        data={},
                        is_difficult=(book_info["difficulty"] == "difficult"),
                        is_time_consuming=False,  # Reading a single chapter is not time-consuming
                        weight=2
                    )
                    objectives.append(chapter_objective)

            # Generate bulk chapter objectives (if enabled)
            if self.archipelago_options.chapter_quest_include_bulk_chapters:
                # Calculate remaining chapters after starting_chapter
                remaining_chapters = book_info["total_chapters"] - book_info["starting_chapter"] + 1
                # Generate "Read X chapters from Y book" objectives that favor lower numbers
                max_bulk_chapters = min(remaining_chapters, 10)  # Cap at 10 chapters max
                # Use weighted random to favor lower numbers (1-3 are more likely than 7-10)
                weights = [max_bulk_chapters - i for i in range(max_bulk_chapters)]  # Higher weight for lower numbers
                num_bulk_chapters = self.random.choices(range(1, max_bulk_chapters + 1), weights=weights)[0]
                
                chapter_text = "chapter" if num_bulk_chapters == 1 else "chapters"
                bulk_objective = GameObjectiveTemplate(
                    label=f"[{book_info['genre']}] {current_book} by {book_info['author']} -> Read {num_bulk_chapters} {chapter_text}",
                    data={},
                    is_difficult=(book_info["difficulty"] == "difficult"),
                    is_time_consuming=(num_bulk_chapters > 3),  # More than 3 chapters is time-consuming
                    weight=20
                )
                objectives.append(bulk_objective)

            # Add completion objective (completing entire book IS time-consuming)
            completion_objective = GameObjectiveTemplate(
                label=f"[{book_info['genre']}] {current_book} by {book_info['author']} -> Complete the entire book",
                data={},
                is_difficult=(book_info["difficulty"] == "difficult"),
                is_time_consuming=True,  # Completing an entire book is time-consuming
                weight=5
            )
            objectives.append(completion_objective)

        # Add genre-based challenges (if enabled)
        if self.archipelago_options.chapter_quest_include_genre_challenges:
            for genre in self.genres:
                genre_books = [book for book, info in self.book_collection.items() if info["genre"] == genre]
                # Maximum number should be the count of books in the collection for that genre
                max_books = min(3, len(genre_books)) # Cap at 3 books max to avoid overly long challenges
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
                            is_time_consuming=False,  # Reading one chapter is not time-consuming
                            weight=60
                        )
                    else:
                        genre_objective = GameObjectiveTemplate(
                            label=f"Genre Challenge: Read chapters from {num_books} different {genre} books",
                            data={},
                            is_difficult=False,
                            is_time_consuming=True,  # Reading from multiple books is time-consuming
                            weight=40
                        )
                    objectives.append(genre_objective)

        # Add author-based challenges (if enabled)
        if self.archipelago_options.chapter_quest_include_author_challenges:
            for author in self.authors:
                author_books = [book for book, info in self.book_collection.items() if info["author"] == author]
                # Maximum number should be the count of books in the collection for that author
                max_books = min(3,len(author_books)) # Cap at 3 books max to avoid overly long challenges
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
                            is_time_consuming=False,  # Reading one chapter is not time-consuming
                            weight=40
                        )
                    else:
                        author_objective = GameObjectiveTemplate(
                            label=f"Author Challenge: Read chapters from {num_books} different books by {author}",
                            data={},
                            is_difficult=False,
                            is_time_consuming=True,  # Reading from multiple books is time-consuming
                            weight=25
                        )
                    objectives.append(author_objective)

        return objectives


class BookCollection(OptionList):
    """
    Definition of book collection. Format is as follows:
    - title: "Book Title"
      starting_chapter: 1 (*optional, defaults to 1)
      total_chapters: 25
      author: "Author Name" (*optional)
      genre: "Fiction" (*optional)
      difficulty: "normal" (*optional, can be "normal" or "difficult")
    """

    display_name = "Chapter Quest Book Collection"
    default = [
        {
            "title": "1984",
            "starting_chapter": 5,
            "total_chapters": 24,
            "author": "George Orwell",
            "genre": "Dystopian Fiction",
            "difficulty": "normal"
        },
        {
            "title": "Pride and Prejudice",
            "starting_chapter": 10,
            "total_chapters": 61,
            "author": "Jane Austen",
            "genre": "Classic Romance",
            "difficulty": "normal"
        },
        {
            "title": "Ulysses",
            "starting_chapter": 3,
            "total_chapters": 18,
            "author": "James Joyce",
            "genre": "Modernist Literature",
            "difficulty": "difficult"
        },
        {
            "title": "Atomic Habits",
            "starting_chapter": 5,
            "total_chapters": 20,
            "author": "James Clear",
            "genre": "Self-Help",
            "difficulty": "normal"
        }
    ]
    schema = Schema([
        {
            "title": And(str, len),
            Optional("starting_chapter"): And(int, lambda x: x > 0),
            "total_chapters": And(int, lambda x: x > 0),
            Optional("author"): And(str, len),
            Optional("genre"): And(str, len),
            Optional("difficulty"): And(str, lambda x: x in ["normal", "difficult"]),
        }
    ])


class ChapterQuestIncludeGenreChallenges(DefaultOnToggle):
    """
    Whether to include genre-based challenges like 'Read chapters from X Science Fiction books'
    """
    display_name = "Chapter Quest Include Genre Challenges"


class ChapterQuestIncludeAuthorChallenges(DefaultOnToggle):
    """
    Whether to include author-based challenges like 'Read chapters from X books by Jane Austen'
    """
    display_name = "Chapter Quest Include Author Challenges"


class ChapterQuestIncludeSpecificChapters(DefaultOnToggle):
    """
    Whether to include specific chapter objectives like 'Read chapter 5'
    """
    display_name = "Chapter Quest Include Specific Chapter Objectives"


class ChapterQuestIncludeBulkChapters(DefaultOnToggle):
    """
    Whether to include bulk chapter objectives like 'Read 3 chapters from Book Title'
    """
    display_name = "Chapter Quest Include Bulk Chapter Objectives"