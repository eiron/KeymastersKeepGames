# Ranch of Rivershine - Keymaster's Keep Implementation

A cozy horse ranch simulation game where you care for horses, train them in various skills, compete in events, breed new foals, and explore the beautiful world of Rivershine.

## Game Overview

**Ranch of Rivershine** (by Cozy Bee Games) is a relaxing horse ranch management and training simulator. Players care for horses, train them in four core skills, compete in events, breed horses, farm crops, and explore various locations.

**Release Date:** May 23, 2025  
**Platform:** PC (Steam)  
**Genre:** Simulation, Horse Ranch Management

## Core Categories

This implementation provides objectives across 11 main gameplay categories:

### 1. **Horse Training** 🏇
Train your horses in four essential skills:
- **Speed**: How fast your horse can move (trained by cantering)
- **Endurance**: How long your horse can gallop (trained by galloping)
- **Jump**: How high your horse can jump (trained by jumping obstacles)
- **Flexibility**: How maneuverable your horse is (trained by turning and circling)

Each skill can be trained from 0% to 100%, with competition requirements at 25%, 50%, 75%, and 100%.

**Accelerated Training:**
- Feed specific grains before training for 2x speed
- Train at specific locations for 2x speed
- Combine both for 3x training speed!

| Skill | Grain | Location |
|-------|-------|----------|
| Speed | Corn | Lupine Meadow |
| Endurance | Barley | Pine Forest |
| Jump | Wheat | Crystal Lake |
| Flexibility | Milo | Rocky Mountain |

### 2. **Horse Care** 💚
Keep your horses happy and healthy:
- Groom horses regularly
- Feed all your horses daily
- Maintain high affection levels (75%+)
- Use medicine when needed
- Equip horse tack and equipment
- Purchase new gear

### 3. **Competitions** 🏆
Enter your horses in events and earn ribbons:
- **Beginner** level competitions (easiest)
- **Intermediate** level competitions (requires 25% skills)
- **Advanced** level competitions (requires 50% skills)
- **Expert** level competitions (requires 75% skills)
- **Trail Racing** events for additional challenges

### 4. **Breeding** 🐴
Expand your ranch through breeding:
- Breed horses together
- Raise foals from birth
- Breed for high skill potential (inherited from parents)
- Breed for specific coat patterns
- Create multi-generational bloodlines
- Purchase horses from the auction house (Common to Legendary rarity)

**Note:** Foals start with 100% Potential. Parent skills at breeding time influence foal base skills.

### 5. **Exploration** 🗺️
Discover the world of Rivershine:
- **Rivershine Ranch**: Your home base
- **Rivershine Town**: Meet NPCs and shop
- **Lupine Meadow**: Speed training bonus
- **Pine Forest**: Endurance training bonus
- **Crystal Lake**: Jump training bonus
- **Rocky Mountain**: Flexibility training bonus
- **Azure Coast**: Scenic coastal area

While exploring:
- Find chests with rewards
- Discover Horse Statues that boost skills
- Forage for items and grain

### 6. **Farming** 🌾
Grow crops to support your ranch:
- **Training Grains**: Corn, Barley, Wheat, Milo (boost skill training)
- **Horse Feed**: Timothy Hay, Oats
- Purchase seeds from Aisha Jamil
- Forage for wild grain on trails
- Harvest crops for your horses
- Collect Yellow Flowers while foraging

### 7. **Wild Horses** 🦄
Encounter and tame wild horses:
- Find Wild Horses in the world
- Tame them to bring to your ranch
- Wild horses start with 100% Potential
- Train them for competitions
- Add unique horses to your collection

### 8. **Social/NPCs** 👥
Meet the residents of Rivershine Town:
- **Aisha Jamil**: Seed Shop owner
- **George Robinson**: Local resident
- **Shin Dae**: Community member
- **Jai Maji**: Town NPC
- **Liam Flinn**: Ranch Upgrades vendor (farm plots, fruit trees, animals)
- **Madelaine Beauchamp**: Rivershine resident
- **River**: Riding Arena Course vendor (Cavaletti, Flower Fence, Country Barrel)
- **Orion Gallio**: Dye recipes vendor
- **Daphne Woolsey**: Local resident
- **Amelia Trotter**: Town Veterinarian (sells medicine)

### 9. **Crafting** ⚗️
Create useful items for your horses and farm:
- **Medicine**: Craft remedies to heal your horses
  - Common Cold Remedy, Rain Rot Poultice, Fertility Boost
  - Hair Growth Potion, Dapple Dust, Appetite Stimulant
  - Coat Conditioner, Hoof Strengthener, Energy Tonic
  - Calming Balm, Anti-Inflammatory Salve
- **Dyes**: Create vibrant colors for horse customization
  - 15 different dye colors available
  - Recipes purchased from Orion Gallio
  - Location-specific ingredients required
- **Fertilizers**: Boost your crop yields
  - Swift Fertilizer (faster growth)
  - Rich Fertilizer (better quality)
  - Shield Fertilizer (crop protection)
  - Lucky Fertilizer (bonus rewards)
- **Animal Feed**: Create feed for farm animals

### 10. **Riding Arena** 🏇
Practice jumping courses to train your horses:
- **Cavaletti Courses**: Ground poles for basic jump training
  - Beginner, Intermediate, Advanced difficulty levels
- **Flower Fence Courses**: Decorative jump obstacles
  - Beginner, Intermediate, Advanced difficulty levels
- **Country Barrel Courses**: Barrel jump challenges
  - Beginner, Intermediate, Advanced difficulty levels
- Purchase courses from River in Rivershine Town
- Available in every exploration area
- Best method for training Jump skill efficiently

### 11. **Ranch Upgrades** 🏡
Expand and improve your ranch facilities:
- **Farm Plots**: Purchase additional farm plots to grow more crops
  - 2nd Farm Plot, 3rd Farm Plot, 4th Farm Plot, 5th Farm Plot
- **Fruit Trees**: Add apple and pear trees to your farm
  - Seasonal fruit production
  - Requires 2nd Ranch Festival completion
- **Farm Animals**: Raise chickens, sheep, and goats
  - 12 Chickens for egg production
  - 8 Sheep for wool
  - 8 Goats for milk
  - Available after 2nd Ranch Festival
- All upgrades purchased from Liam Flinn in Rivershine Town


## Sample Objectives

### Training Examples
- `Train a horse's Speed skill to 50%`
- `Train a horse's Jump skill to Expert level (75%)`
- `Feed a horse Corn before training Speed`
- `Train two skills simultaneously on a single horse`
- `Fully train a horse in all four skills to 100%` (difficult, time-consuming)

### Care Examples
- `Groom a horse`
- `Keep a horse's affection above 75%`
- `Maintain perfect care for a horse for 7 in-game days` (time-consuming)
- `Equip horse tack on a horse`

### Competition Examples
- `Win a Beginner level competition`
- `Enter a horse into an Advanced level competition` (time-consuming)
- `Win an Expert level competition` (difficult, time-consuming)
- `Earn 5 competition ribbons` (time-consuming)

### Breeding Examples
- `Breed two horses together` (time-consuming)
- `Raise a foal from birth` (time-consuming)
- `Purchase a Legendary horse from the auction house` (time-consuming)
- `Breed three generations of horses in one bloodline` (difficult, time-consuming)

### Exploration Examples
- `Explore Crystal Lake`
- `Find a chest while exploring`
- `Use a Horse Statue to boost a skill`
- `Visit all exploration locations in one day` (time-consuming)

### Farming Examples
- `Plant Corn seeds`
- `Harvest crops from your farm`
- `Grow all twelve crop types` (time-consuming)
- `Use Swift Fertilizer on crops for faster growth`
- `Harvest from Apple and Pear fruit trees` (time-consuming)

### Wild Horse Examples
- `Encounter a Wild Horse`
- `Tame a Wild Horse` (time-consuming)
- `Train a Wild Horse to competition level` (difficult, time-consuming)

### Social Examples
- `Talk to Aisha Jamil (Seed Shop)`
- `Meet all NPCs in Rivershine Town` (time-consuming)

### Crafting Examples
- `Craft a Common Cold Remedy`
- `Create a Red Dye from foraged ingredients`
- `Craft Swift Fertilizer to speed up crop growth`
- `Make Animal Feed for your farm animals`
- `Craft all 11 medicine types` (difficult, time-consuming)

### Riding Arena Examples
- `Complete a Beginner Cavaletti Course`
- `Master an Intermediate Flower Fence Course` (time-consuming)
- `Complete all three Advanced difficulty courses` (difficult, time-consuming)

### Ranch Upgrades Examples
- `Purchase a 2nd Farm Plot from Liam`
- `Raise 12 chickens for egg production` (time-consuming)
- `Collect wool from 8 sheep` (time-consuming)
- `Harvest fruit from both Apple and Pear trees` (time-consuming)


## Configuration Options

All objective categories can be toggled on/off:

- **`ranch_of_rivershine_include_horse_training`**: Enable/disable horse skill training objectives (Speed, Endurance, Jump, Flexibility)
- **`ranch_of_rivershine_include_horse_care`**: Enable/disable horse care and maintenance objectives
- **`ranch_of_rivershine_include_competitions`**: Enable/disable competition and racing objectives
- **`ranch_of_rivershine_include_breeding`**: Enable/disable breeding and auction house objectives
- **`ranch_of_rivershine_include_exploration`**: Enable/disable exploration and discovery objectives
- **`ranch_of_rivershine_include_farming`**: Enable/disable farming and foraging objectives
- **`ranch_of_rivershine_include_wild_horses`**: Enable/disable wild horse encounter objectives
- **`ranch_of_rivershine_include_social`**: Enable/disable NPC interaction objectives
- **`ranch_of_rivershine_include_crafting`**: Enable/disable crafting objectives (medicine, dyes, fertilizers, feed)
- **`ranch_of_rivershine_include_riding_arena`**: Enable/disable Riding Arena course objectives
- **`ranch_of_rivershine_include_ranch_upgrades`**: Enable/disable ranch upgrade objectives (plots, animals, trees)

All options default to **enabled** (true).

## Gameplay Tips

1. **Potential Management**: Horses lose 1 Potential per skill point gained AND 1 per night in pasture. Plan your training carefully!

2. **Accelerated Training**: Maximize efficiency by:
   - Feeding the right grain before training (+2x)
   - Training at the matching location (+2x)
   - Both combined = +3x training speed!
   - Using Skill Arenas for even faster training

3. **Multi-Skill Training**: You can train multiple skills at once! For example, jumping while cantering trains both Jump and Speed.

4. **Competition Prep**: Check skill requirements before entering competitions:
   - Beginner: Any skill level
   - Intermediate: 25% minimum
   - Advanced: 50% minimum
   - Expert: 75% minimum

5. **Breeding Strategy**: Parent skills at breeding time affect foal base skills. Train parents before breeding for better foals!

6. **Seasons**: The game features a seasonal system that affects various gameplay elements.

## Official Resources

- **Steam Page**: https://store.steampowered.com/app/1559600/The_Ranch_of_Rivershine/
- **Developer Website**: https://www.cozybeegames.com/
- **Community Wiki**: https://rivershine.miraheze.org/wiki/Main_Page

## Credits

Implementation based on game information from the Ranch of Rivershine Wiki and Steam page.  
Game developed by **Cozy Bee Games**.
