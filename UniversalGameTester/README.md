# Universal Game Tester

A comprehensive testing framework for validating **any** Keymaster's Keep game implementation. The Universal Game Tester automatically discovers, loads, and tests game modules regardless of their structure, option types, or complexity.

## Key Features

- **Automatic Discovery**: Scans for game implementation files using pattern recognition
- **Universal Compatibility**: Works with any game module, including custom option types
- **Authentic Simulation**: Reproduces the Keep's weighted objective selection system
- **Comprehensive Analysis**: Provides detailed metrics on objectives, weights, and features
- **Robust Error Handling**: Gracefully handles missing dependencies and import failures

## Installation

This is a standard Archipelago world file (.apworld). To install:

1. Copy `keymasters_keep_game_tester.apworld` to your Archipelago `custom_worlds` directory
2. The Universal Game Tester will appear in your Archipelago launcher as a tool
3. Launch it from the Archipelago launcher's Tools menu

## Usage

Once installed, you can access the Universal Game Tester through:

**From Archipelago Launcher:**
- Open Archipelago Launcher
- Go to the Tools menu
- Select "Keymaster's Keep Game Tester"

**Features Available:**
- Interactive GUI for testing game implementations
- Automatic scanning and discovery of game files
- Detailed analysis reports with metrics
- Dynamic objective generation testing

## System Requirements

- Archipelago (latest version recommended)
- Python 3.7+ (included with Archipelago)
- Kivy (for GUI - automatically handled by Archipelago)

## What It Tests

### Objective Generation
- **Dynamic Selection**: Simulates the Keep's weighted objective selection process
- **Template Population**: Tests objective template data population with real values
- **Weight Distribution**: Analyzes how objectives are distributed across weight tiers
- **Variety Systems**: Validates duplicate prevention and objective cycling

### Option Compatibility
- **Standard Types**: Toggle, Choice, Range, OptionSet, DefaultOnToggle, PercentageRange
- **Custom Types**: Any OptionSet-based class with class-level defaults
- **Dynamic Creation**: Automatically handles undefined option types
- **Import Resolution**: Fixes relative imports and missing dependencies

### Implementation Analysis
- **Complexity Scoring**: Calculates implementation complexity based on multiple factors
- **Feature Detection**: Identifies relationship systems, difficulty scaling, cursed modes
- **Category Analysis**: Maps available option categories and their usage
- **Data Source Mapping**: Analyzes template complexity and data sources

## Sample Output

```
TESTING: Date Everything Game
IMPLEMENTATION ANALYSIS:
   • Total Objectives: 29
   • Complexity Score: 86
   • Weight Distribution:
     - Weight 10: 9 objectives
     - Weight 8: 2 objectives
   • Features: Relationship System
   • Categories: 10 options available

DYNAMIC OBJECTIVE SELECTION:
   1. Achieve LOVE with Rebel (Rubber Duck)
      Weight: 10 | Happy | Time x2 Weight 10
   2. Get 5 structural elements to FRIENDS status
      Weight: 8 | Challenge | Time x2 Weight 8
```

## Technical Architecture

### Core Components

1. **Mock Environment System**: Creates universal mock classes for all possible option types
2. **Dynamic Class Loading**: Loads game modules with automatic import fixing
3. **Smart Option Creation**: Intelligently instantiates option classes with sensible defaults
4. **Weighted Selection Engine**: Simulates authentic Keep objective selection behavior

### Advanced Features

- **String Type Resolution**: Handles dataclass fields stored as strings rather than class references
- **Fallback Creation**: Provides robust defaults for unknown or custom option types
- **Cross-Platform Support**: Works on Windows, Mac, and Linux
- **Error Recovery**: Continues testing even when individual components fail

## Troubleshooting

### Common Issues

**Tool doesn't appear in Archipelago launcher**
- Ensure the .apworld file is in the correct directory (`worlds` or `custom_worlds`)
- Restart Archipelago launcher after adding the file
- Check that the file isn't corrupted or blocked by antivirus

**No games found during scanning**
- The tool automatically scans for Keymaster's Keep games in your setup
- Verify your game files are accessible and follow naming conventions
- Ensure you have files available in your keymasters_keep folder

**GUI display issues**
- All Unicode characters have been replaced with ASCII equivalents for Kivy compatibility
- If text appears garbled, ensure your system supports the character encoding

### Results Interpretation

**Weight Distribution Analysis:**
- High Weights (8-10): Major objectives, relationship milestones
- Medium Weights (3-7): Standard objectives, skill challenges  
- Low Weights (1-2): Minor objectives, daily tasks

**Complexity Scoring:**
- Low (0-30): Simple implementations
- Medium (31-100): Standard game modules
- High (101+): Complex, feature-rich implementations

**Feature Detection:**
- Relationship System: Detected from relationship-focused methods/attributes
- Difficulty Scaling: Found through difficulty or preference patterns
- Cursed/Challenge Mode: Identified by specialized naming patterns

## Use Cases

- **Development**: Validate new game implementations before deployment
- **Quality Assurance**: Ensure existing games work correctly with updates
- **Analysis**: Understand objective distribution and complexity metrics
- **Debugging**: Identify issues with option systems or template population
- **Integration**: Verify games will work within the Keymaster's Keep ecosystem

This tool is essential for maintaining the quality and compatibility of Keymaster's Keep game implementations across the entire ecosystem.
