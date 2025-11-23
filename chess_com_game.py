from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class ChessComArchipelagoOptions:
    pass


class ChessComGame(Game):
    name = "Chess.com"
    platform = KeymastersKeepGamePlatforms.WEB

    platforms_other = [
        KeymastersKeepGamePlatforms.AND,
        KeymastersKeepGamePlatforms.IOS,
        KeymastersKeepGamePlatforms.PC
    ]

    is_adult_only_or_unrated = False

    options_cls = ChessComArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Disable premoves (no premoving)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Do not use the opening explorer or book",  # persistent self-imposed rule
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Do not run engine or post-game analysis until objectives complete",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Never castle (keep king uncastled all game)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Always play a flank pawn (a or h) on your first move as White",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Avoid queen promotions (attempt underpromotion when legal)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="No piece retreats (pieces may not move to a square closer to starting rank/file)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="No captures before move 10 (first capture must be at move 10 or later)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Play only one time control for the entire session",  # player chooses outside system
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Win without moving your queen (queen must stay on starting square)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Sacrifice a rook before move 15 in every game (if possible)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="First move must be a4 if White or a5 if Black in every game",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Follow only chat-suggested moves while playing on stream",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Reach RATING rating in MODE mode",
                data={
                    "RATING": (self.ratings_normal, 1),
                    "MODE": (self.modes, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Reach RATING rating in MODE mode",
                data={
                    "RATING": (self.ratings_hard, 1),
                    "MODE": (self.modes, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win GAME_COUNT games in MODE mode as COLOR",
                data={
                    "GAME_COUNT": (self.game_counts, 1),
                    "MODE": (self.modes, 1),
                    "COLOR": (self.colors, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a VARIANT variant game",
                data={
                    "VARIANT": (self.variants, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win GAME_COUNT games in VARIANT variant",
                data={
                    "GAME_COUNT": (self.game_counts, 1),
                    "VARIANT": (self.variants, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win DIFFERENT different variant types",
                data={
                    "DIFFERENT": (self.variant_diversity_counts, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Deliver checkmate pattern PATTERN",
                data={
                    "PATTERN": (self.checkmate_patterns, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Deliver checkmate with PIECE",
                data={
                    "PIECE": (self.pieces, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Underpromote a pawn to UNDERPROMOTION",
                data={
                    "UNDERPROMOTION": (self.underpromotions, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Solve PUZZLE_COUNT puzzles with at least ACCURACY% accuracy",
                data={
                    "PUZZLE_COUNT": (self.puzzle_counts, 1),
                    "ACCURACY": (self.puzzle_accuracy_levels, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Achieve Puzzle Rush score SCORE",
                data={
                    "SCORE": (self.puzzle_rush_scores, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Reach a puzzle streak of STREAK",
                data={
                    "STREAK": (self.puzzle_streaks, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win a MODE game with time control TIME_CONTROL",
                data={
                    "MODE": (self.modes, 1),
                    "TIME_CONTROL": (self.time_controls, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a game after sacrificing MATERIAL",
                data={
                    "MATERIAL": (self.material_sacrifices, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Defeat BOT",
                data={
                    "BOT": (self.bots, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Defeat BOT after sacrificing MATERIAL for initiative",
                data={
                    "BOT": (self.bots, 1),
                    "MATERIAL": (self.material_sacrifices, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Defeat BOT after promoting a pawn",
                data={
                    "BOT": (self.bots, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Checkmate BOT after sacrificing MINOR_PIECE earlier",
                data={
                    "BOT": (self.bots, 1),
                    "MINOR_PIECE": (self.minor_pieces, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Defeat BOT after being materially behind (down PIECE at some point)",
                data={
                    "BOT": (self.bots, 1),
                    "PIECE": (self.pieces, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Checkmate BOT with PIECE",
                data={
                    "BOT": (self.bots, 1),
                    "PIECE": (self.pieces, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Execute MOTIF tactic against BOT",
                data={
                    "MOTIF": (self.tactical_motifs, 1),
                    "BOT": (self.bots, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Deliver checkmate using a MOTIF motif against BOT",
                data={
                    "MOTIF": (self.tactical_motifs, 1),
                    "BOT": (self.bots, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Achieve a BOT win streak of STREAK wins",
                data={
                    "BOT": (self.bots, 1),  # any bots, player chooses mix
                    "STREAK": (self.streak_lengths, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Defeat DIFFERENT different bots",
                data={
                    "DIFFERENT": (self.different_bot_counts, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win as White using opening SEQUENCE",
                data={
                    "SEQUENCE": (self.opening_sequences_white, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win as Black using opening SEQUENCE",
                data={
                    "SEQUENCE": (self.opening_sequences_black, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win as Black without losing both rooks",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win as Black after promoting a pawn to a Knight",
                data=dict(),
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win as Black opening with the Bongcloud (play Ke7 on first move)",
                data=dict(),
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win as White opening with c6 then d5 (inverted Caro structure)",
                data=dict(),
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win a game after performing an en passant capture",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win as White after fianchettoing both bishops (Bg2 & Bb2)",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win as Black after fianchettoing both bishops (Bg7 & Bb7)",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win a game where you castle queenside",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win a game after a successful deflection tactic gaining material",
                data=dict(),
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

    @staticmethod
    def modes() -> List[str]:
        return [
            "Bullet",
            "Blitz",
            "Rapid",
            "Classical",
            "Daily",
            "Puzzle",
        ]

    @staticmethod
    def variants() -> List[str]:
        return [
            "Standard",
            "Chess960",
            "King of the Hill",
            "Three-Check",
            "Crazyhouse",
            "Horde",
            "Atomic",
        ]

    @staticmethod
    def pieces() -> List[str]:
        return [
            "Queen",
            "Rook",
            "Bishop",
            "Knight",
            "Pawn",
            "King",
        ]

    @staticmethod
    def checkmate_patterns() -> List[str]:
        return [
            "Back Rank Mate",
            "Smothered Mate",
            "Boden's Mate",
            "Arabian Mate",
            "Anastasia's Mate",
            "Scholar's Mate",
            "Fool's Mate",
            "Ladder Mate",
            "Opera Mate",
            "Epaulette Mate",
        ]

    @staticmethod
    def underpromotions() -> List[str]:
        return [
            "Knight",
            "Bishop",
            "Rook",
        ]

    @staticmethod
    def time_controls() -> List[str]:
        return [
            "1+0",
            "3+0",
            "3+2",
            "5+0",
            "10+0",
            "15+10",
            "30+0",
        ]

    @staticmethod
    def ratings_normal() -> List[int]:
        return [800, 1000, 1200]

    @staticmethod
    def ratings_hard() -> List[int]:
        return [1400, 1600, 1800]

    @staticmethod
    def puzzle_counts() -> List[int]:
        return [5, 10, 20]

    @staticmethod
    def puzzle_accuracy_levels() -> List[int]:
        return [70, 80, 90, 95]

    @staticmethod
    def puzzle_rush_scores() -> List[int]:
        return [20, 25, 30, 35]

    @staticmethod
    def puzzle_streaks() -> List[int]:
        return [10, 15, 20]

    @staticmethod
    def game_counts() -> List[int]:
        return [3, 5, 10]

    @staticmethod
    def colors() -> List[str]:
        return ["White", "Black"]

    @staticmethod
    def material_sacrifices() -> List[str]:
        return [
            "Queen",
            "Rook",
            "Bishop",
            "Knight",
            "Exchange",  # Rook for minor piece
        ]

    @staticmethod
    def minor_pieces() -> List[str]:
        return ["Bishop", "Knight"]

    @staticmethod
    def bots() -> List[str]:
        return [
            # Influencer / personality bots requested plus assorted higher-quality training bots
            "Nisha",
            "Janjay",
            "Aron",
            "Zara",
            "Santiago",
            "Karim",
            "Pokimane",
            "QTCinderella",
            "Tectone",
            "xQc",
            # Additional common Chess.com bots (optional expansion)
            "Nelson",
            "Martin",
            "Li",
            "Tiffany",
            "Anna",
            "Lina",
            "Noam",
            "Maia 1100",
            "Maia 1400",
            "Maia 1700",
        ]

    @staticmethod
    def tactical_motifs() -> List[str]:
        return [
            "Fork",
            "Pin",
            "Skewer",
            "Discovered Attack",
            "Discovered Check",
            "Double Check",
            "Clearance Sacrifice",
            "Deflection",
            "Interference",
            "Zwischenzug",
            "Underpromotion Tactic",
            "Smothered Mate Setup",
        ]

    @staticmethod
    def streak_lengths() -> List[int]:
        return [2, 3, 5]

    @staticmethod
    def different_bot_counts() -> List[int]:
        return [3, 5, 8]

    @staticmethod
    def variant_diversity_counts() -> List[int]:
        return [2, 3, 5]

    @staticmethod
    def opening_sequences_white() -> List[str]:
        return [
            "d4 Nf3 Bf4",      # London System
            "d4 c4 g3",        # Catalan
            "e4 Nf3 Bb5",      # Ruy Lopez
            "e4 d4 Nf3",       # Scotch Game
            "e4 Nc3 Nf3",      # Vienna Game
            "d4 Nf3 c4",       # Indian System setup
            "d4 Bf4 e3",       # London with e3
            "Nf3 g3 Bg2",      # King's Indian Attack
            "c4 Nf3 g3",       # English with fianchetto
            "c6 d5",           # Inverted Caro
            "f4",              # Bird's Opening
            "b3",              # Larsen's Opening
            "Nc3 e4",          # Nimzowitsch-Larsen Attack
            "g4",              # Grob's Attack
            "a3",              # Anderssen's Opening
            "Na3",             # Sodium Attack
            "h4",              # Desprez Opening
            "e4 Qh5",          # Parham Attack / Napoleon Opening
            "Nh3",             # Amar Opening
            "f3 Kf2",          # Barnes Opening / Fool's Mate setup
        ]

    @staticmethod
    def opening_sequences_black() -> List[str]:
        return [
            "e5",              # Open Game (vs 1.e4)
            "c5",              # Sicilian Defense
            "e6",              # French Defense
            "c6",              # Caro-Kann Defense
            "d5",              # Scandinavian or vs 1.d4
            "Nf6",             # Indian Defenses (vs 1.d4)
            "g6",              # Modern Defense / King's Indian
            "d6 Nf6 g6",       # Pirc Defense
            "Nc6 e5",          # vs 1.e4 (Italian/Scotch lines)
            "e5 Nf6",          # Petroff Defense
            "d6 e5",           # Philidor Defense
            "Nf6 g6 Bg7",      # King's Indian Defense
            "Nf6 c5",          # Benoni Defense
            "f5",              # Dutch Defense
            "Nc6 e5 Nf6",      # Nimzowitsch Defense
            "b6",              # Owen's Defense
            "a6",              # St. George Defense
            "Na6",             # Lemming Defense
            "h6",              # Carr Defense
            "g5",              # Borg Defense / Grob Gambit Declined
            "f6",              # Barnes Defense
            "Nh6",             # Adams Defense
        ]


# Archipelago Options
# ...