# Chapter Quest Game

A meta-game module that transforms your personal reading list into gaming objectives, creating targeted reading challenges based on your book collection.

## Overview

The Chapter Quest game allows you to:
- Import your book collection with chapter counts
- Generate reading objectives for specific chapters
- Track progress through individual books
- Organize books by genre and difficulty
- Get completion objectives for shorter books

## Sample Objectives

- `"[Fantasy Fiction] The Hobbit by J.R.R. Tolkien -> Read chapter 7"`
- `"[Science Fiction] Dune by Frank Herbert -> Read chapter 23"`
- `"[Classic Literature] The Great Gatsby by F. Scott Fitzgerald -> Complete the entire book"`
- `"Genre Challenge: Read 2 chapters from a Science Fiction book"`
- `"Author Challenge: Read 1 chapter from a book by J.R.R. Tolkien"`

## Configuration

### Book Collection Format

```yaml
Chapter Quest:
  chapter_quest_book_collection:
    - title: "Book Title"
      chapters: 25
      author: "Author Name"   # Optional
      genre: "Fiction"        # Optional
      difficulty: "normal"    # Optional: "normal" or "difficult"
  chapter_quest_include_genre_challenges: true   # Optional
  chapter_quest_include_author_challenges: true  # Optional
```

### Required Fields
- **title**: The exact title of the book
- **chapters**: Total number of chapters in the book (positive integer)

### Optional Fields
- **author**: Author's name (enables author-based challenges)
- **genre**: Book category (Fiction, Non-fiction, Science, etc.)
- **difficulty**: "normal" (default) or "difficult"

### Optional Settings
- **chapter_quest_include_genre_challenges**: Enable genre-based meta-challenges (default: true)
- **chapter_quest_include_author_challenges**: Enable author-based meta-challenges (default: true)

## Features

### Chapter-Based Objectives
- Generates specific chapter reading goals
- Randomly selects chapters from your books
- Creates achievable, bite-sized reading targets

### Completion Goals
- Automatically suggests completion objectives for shorter books (≤20 chapters)
- 30% chance to generate "complete the entire book" objectives
- Helps balance chapter reading with full book completion

### Difficulty System
- **Normal books**: Standard objectives
- **Difficult books**: Marked as difficult objectives (filtered based on settings)
- **Long books** (>30 chapters): Marked as time-consuming

### Genre Organization
- Tracks book genres for variety
- Supports any genre classification you prefer
- Helps ensure diverse reading across different categories

## Objective Types

### Chapter Reading (Primary)
- Format: `"[Genre] Book Title by Author -> Read chapter [X]"`
- Weight: 10
- Generated for every book (up to 10 chapters per book)
- Individual chapters are not time-consuming

### Book Completion (Secondary)  
- Format: `"[Genre] Book Title by Author -> Complete the entire book"`
- Weight: 4
- Generated for all books
- Marked as time-consuming

### Genre Challenges (Meta-objectives)
- Format: `"Genre Challenge: Read [X] chapters from [Y] [Genre] book(s)"`
- Weight: 10-20
- Requires `chapter_quest_include_genre_challenges: true`
- Single book: 1-3 chapters specified
- Multiple books: Random count up to available books

### Author Challenges (Meta-objectives)
- Format: `"Author Challenge: Read [X] chapters from [Y] book(s) by [Author]"`
- Weight: 10-20
- Requires `chapter_quest_include_author_challenges: true`
- Single book: 1-3 chapters specified
- Multiple books: Random count up to available books

## Usage Tips

### Book Selection
- Include books you actually want to read
- Mix short and long books for variety
- Add accurate chapter counts for proper pacing

### Genre Classification
- Use consistent genre naming
- Consider your reading preferences
- Popular genres: Fiction, Non-fiction, Science Fiction, Fantasy, Biography, Self-Help

### Difficulty Settings
- Mark dense academic books as "difficult"
- Mark books with complex language as "difficult"
- Leave entertaining reads as "normal"

## Integration with Keymaster's Keep

The Chapter Quest integrates seamlessly with Keymaster's Keep settings:

- **Difficult Objectives**: Can be filtered out if you prefer easier reading goals
- **Time-Consuming Objectives**: Long books (>30 chapters) respect this filter
- **META Platform**: Works alongside other meta-games in your selection

## Sample Configuration

See `chapter_quest_sample_config.yaml` for a complete example with 16 popular books across various genres and authors, plus optional meta-challenge settings.

This module transforms your personal reading goals into structured, gamified objectives that integrate perfectly with the Keymaster's Keep experience!