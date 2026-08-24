"""
Chart Attack game for Keymaster's Keep.

Lets the user specify charts they follow (music, books, films, games, restaurants,
etc.) and generates objectives that pick a specific chart and a chart position.
Users can also set the verb that accompanies the objective label (e.g., "Follow",
"Watch", "Read", "Play", "Visit").

Features:
- Single per-chart entry including name, verb, position range, optional chart weight,
  and an opt-in flag for whether the list is an actual ranked chart
- Optional weighting that prefers smaller chart numbers (e.g., #1 more likely)
- Weight strength control (linear boost 1..10)
- Per-chart weighting to make some charts appear more frequently than others
- Per-entry opt-in/opt-out of the top-position weighting, so unranked lists (award
  nominee ballots, personal library categories, catalog/spine numbers, etc.) aren't
  skewed toward small numbers

Configure via entries like:
- "Billboard Hot 100 | Follow | 1-50 | 3 | yes" (real chart, appears 3x as often, weighted toward #1)
- "UK Top 40 | Listen to | 1-20 | 1 | yes" (default weight, opted into top-position weighting)
- "Goodreads Fantasy | Read | 1-100" (weight and chart-flag omitted = 1 and not weighted)

Range supports either a single number (e.g., 10) or a span (e.g., 1-50). If omitted, defaults to 1-100.
Chart weight is optional; if omitted, defaults to 1.
The 5th field (yes/no) marks whether this is an actual ranked chart; only entries marked "yes"
participate in the top-position weighting boost (when chart_attack_weight_top_positions is enabled).
Omitted or "no" = not weighted toward the top, regardless of the global toggle.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

# Project-specific imports (provide stubs for standalone WIP testing)
from Options import NamedRange, FreeText, OptionSet, Toggle, Range  # type: ignore
from ..game import Game  # type: ignore
from ..game_objective_template import GameObjectiveTemplate  # type: ignore
from ..enums import KeymastersKeepGamePlatforms  # type: ignore


# === Options Dataclass ===
@dataclass
class ChartAttackArchipelagoOptions:
    chart_attack_entries: "ChartAttackEntries"
    chart_attack_weight_top_positions: "ChartAttackWeightTopPositions"
    chart_attack_weight_strength: "ChartAttackWeightStrength"


class ChartAttackGame(Game):
    name = "Chart Attack"
    platform = KeymastersKeepGamePlatforms.META
    is_adult_only_or_unrated = False
    options_cls = ChartAttackArchipelagoOptions

    # ---- Helpers to read options ----
    def _get_opts(self) -> ChartAttackArchipelagoOptions | None:
        return getattr(self, "archipelago_options", None)

    def charts(self) -> List[str]:
        # Expose distinct chart names from parsed entries
        return sorted({e[0] for e in self._entries()})

    def _defaults(self) -> Tuple[int, int]:
        # Default when an entry omits a range
        return (1, 100)

    def _entries(self) -> List[Tuple[str, str, int, int, int, bool]]:
        """Parse entries from a single OptionSet where each item is:
        "Chart Name | Verb | Range | Weight | IsChart". Range may be "N" or "A-B". Weight is optional.
        Missing range -> defaults. Missing weight -> 1. IsChart (yes/no) is optional and defaults to
        "no" (not weighted toward the top) since not every list is an actual ranked chart.
        Returns list of tuples: (chart, verb, lo, hi, weight, is_chart).
        """
        opts = self._get_opts()
        items: List[str] = []
        if opts is not None:
            try:
                raw_set = getattr(opts.chart_attack_entries, "value", set())
                if isinstance(raw_set, (list, set, tuple)):
                    items = [str(x) for x in raw_set]
            except Exception:
                items = []
        out: List[Tuple[str, str, int, int, int, bool]] = []
        for item in items:
            chart, verb, lo, hi, weight, is_chart = self._parse_entry(item)
            if chart:
                out.append((chart, verb, lo, hi, weight, is_chart))
        return out

    def _parse_entry(self, s: str) -> Tuple[str, str, int, int, int, bool]:
        parts = [p.strip() for p in s.split("|")]
        chart = parts[0] if parts else ""
        verb = "Follow"
        lo, hi = self._defaults()
        weight = 1
        is_chart = False
        if len(parts) >= 2 and parts[1]:
            verb = parts[1]
        if len(parts) >= 3 and parts[2]:
            rng = self._parse_range_string(parts[2])
            if rng:
                lo, hi = rng
        if len(parts) >= 4 and parts[3]:
            try:
                weight = max(1, int(parts[3]))
            except (ValueError, TypeError):
                weight = 1
        if len(parts) >= 5 and parts[4]:
            is_chart = self._parse_bool_string(parts[4])
        return chart, verb or "Follow", lo, hi, weight, is_chart

    def _parse_bool_string(self, s: str) -> bool:
        return s.strip().lower() in ("1", "true", "yes", "y")

    def _parse_range_string(self, s: str) -> Tuple[int, int] | None:
        s = s.strip()
        if not s:
            return None
        if "-" in s:
            a, b = s.split("-", 1)
            try:
                lo = max(1, int(a.strip()))
                hi = max(1, int(b.strip()))
                if hi < lo:
                    hi = lo
                return (lo, hi)
            except Exception:
                return None
        try:
            v = max(1, int(s))
            return (v, v)
        except Exception:
            return None

    def _positions_for_chart(self, lo: int, hi: int) -> List[int]:
        return list(range(lo, hi + 1))

    def _weighting(self) -> Tuple[bool, int]:
        opts = self._get_opts()
        if not opts:
            return (False, 1)
        try:
            enabled = bool(getattr(opts.chart_attack_weight_top_positions, "value", False))
        except Exception:
            enabled = False
        try:
            strength = int(getattr(opts.chart_attack_weight_strength, "value", 3))
        except Exception:
            strength = 3
        if strength < 1:
            strength = 1
        if strength > 10:
            strength = 10
        return (enabled, strength)

    def chart_and_position_pairs(self) -> List[str]:
        """Build combined choices like "Billboard Hot 100 #7".
        If position weighting is enabled AND the entry is opted in as an actual chart,
        duplicate entries so smaller positions appear more often.
        Uses a simple linear boost: position 1 gets `strength` copies, last position gets 1 copy.
        Chart weight multiplies all positions for that chart (e.g., weight=3 means 3× as many entries).
        """
        entries = self._entries()
        if not entries:
            return []
        weighted, strength = self._weighting()
        pairs: List[str] = []
        for chart, verb, lo, hi, chart_weight, is_chart in entries:
            positions = self._positions_for_chart(lo, hi)
            if not positions:
                continue
            lo, hi = positions[0], positions[-1]
            span = max(1, hi - lo)
            use_top_weighting = weighted and is_chart
            for pos in positions:
                if not use_top_weighting:
                    pairs.extend([f"{verb} {chart} #{pos}"] * chart_weight)
                else:
                    # Linear scaling: top rank gets `strength`, bottom gets 1
                    extra = 1
                    if span > 0:
                        extra = 1 + int((strength - 1) * (hi - pos) / span)
                    count = max(1, extra) * chart_weight
                    pairs.extend([f"{verb} {chart} #{pos}"] * count)
        # Ensure non-empty and reasonable size
        return pairs

    # ---- Game templates ----
    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        # No pre-computation required
        return []

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        # If no entries configured, do not emit objectives
        if not self._entries():
            return []

        choices = lambda: list(self.chart_and_position_pairs())
        return [
            GameObjectiveTemplate(
                label="CHART_AND_POSITION",
                data={"CHART_AND_POSITION": (choices, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            )
        ]


# === Options ===
class ChartAttackEntries(OptionSet):
    """
    Per-chart entries combining chart name, verb, range, optional weight, and an
    opt-in flag for whether the list is an actual ranked chart.

    One entry per item, formatted as:
    - Chart Name | Verb | Range | Weight | IsChart

    Examples:
    - Billboard Hot 100 | Follow | 1-50 | 3 | yes  (real chart, appears 3x as often, weighted toward #1)
    - UK Top 40 | Listen to | 1-20 | 1 | yes  (default weight, opted into top-position weighting)
    - Goodreads Fantasy | Read | 1-100  (weight and chart-flag omitted = 1 and not weighted)

    Range may be a single number (e.g., 10) or a span (e.g., 1-50). If omitted, defaults to 1-100.
    Weight is optional; if omitted, defaults to 1. Higher weights make that chart appear more frequently.
    IsChart (yes/no) is optional and defaults to "no". Only entries marked "yes" participate in the
    top-position weighting boost controlled by Chart Attack Weight Smaller Numbers Higher/Strength —
    mark a list "yes" only when a smaller number genuinely means "more popular/better" (e.g., sales
    charts, rating-based rankings). Award nominee ballots, personal library categories, and catalog/
    spine numbers are not ranked in that sense and should stay "no".
    """

    display_name = "Chart Attack Entries (Chart | Verb | Range | Weight | IsChart)"
    # Starter examples to make configuration easier; edit or remove as desired.
    default = {
        "Billboard Hot 100 | Follow | 1-50 | 2 | yes",
        "Goodreads Choice Awards | Read | 1-50 | 1 | no",
        "Sight & Sound Greatest Films | Watch | 1-100 | 1 | yes",
        "Steam Top Sellers | Play | 1-30 | 2 | yes",
        "BoardGameGeek Top 100 | Play | 1-50 | 1 | yes",
        "Guardian Best Podcasts | Listen to | 1-30 | 1 | no",
        "Michelin Guide Restaurants | Visit | 1-20 | 1 | no",
        "Netflix Top 10 | Watch | 1-10 | 2 | yes",
    }


class ChartAttackWeightTopPositions(Toggle):
    """
    If enabled, smaller chart numbers (e.g., #1) are more likely to be selected.
    Uses a linear boost so the top rank appears more often than the bottom rank.
    """

    display_name = "Chart Attack Weight Smaller Numbers Higher"


class ChartAttackWeightStrength(NamedRange):
    """
    Strength of the weighting when preferring smaller chart numbers. 1 = no extra boost,
    10 = strongest linear boost. The top rank will appear roughly `strength` times
    more often than the bottom rank.
    """

    display_name = "Chart Attack Weight Strength"
    default = 3
    range_start = 1
    range_end = 10
