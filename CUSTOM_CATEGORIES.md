# Custom Categories Sample Configuration

This file demonstrates how to use the Custom Categories game implementation.

## Basic Structure

```yaml
custom_categories_collection:
  - category: "Category Name"
    weight: 50  # Optional: How often objectives from this category appear (default: 50)
    tasks:
      - task: "Task description"
        difficulty: "normal"  # Optional: "normal" or "difficult" (default: "normal")
        time_consuming: false  # Optional: true or false (default: false)
        weight: 50  # Optional: How often this specific task appears (default: 50)
      - "Simple task without extra options"  # Simplified format
```

## Full Example

```yaml
custom_categories_collection:
  # High priority category with many tasks
  - category: "Fitness Goals"
    weight: 80  # High weight = appears more often
    tasks:
      - task: "Complete a 30-minute workout"
        difficulty: "normal"
        time_consuming: false
        weight: 70
      - task: "Run 5 kilometers"
        difficulty: "difficult"
        time_consuming: true
        weight: 40
      - task: "Do 50 pushups"
        difficulty: "normal"
        time_consuming: false
        weight: 60
      - task: "Attend a yoga class"
        difficulty: "normal"
        time_consuming: true
        weight: 50
      - "Stretch for 15 minutes"  # Simple format

  # Medium priority category
  - category: "Learning & Skills"
    weight: 60
    tasks:
      - task: "Complete an online course module"
        difficulty: "normal"
        time_consuming: true
        weight: 50
      - task: "Practice a new language for 20 minutes"
        difficulty: "normal"
        time_consuming: false
        weight: 70
      - task: "Read a technical article"
        difficulty: "normal"
        time_consuming: false
        weight: 80
      - task: "Build a small coding project"
        difficulty: "difficult"
        time_consuming: true
        weight: 30

  # Low priority category with fewer tasks
  - category: "Household Chores"
    weight: 30  # Low weight = appears less often
    tasks:
      - "Vacuum the living room"
      - "Do the laundry"
      - "Clean the kitchen"
      - task: "Deep clean the bathroom"
        difficulty: "normal"
        time_consuming: true
        weight: 40

  # Specialized category
  - category: "Creative Writing"
    weight: 50
    tasks:
      - task: "Write 500 words"
        difficulty: "normal"
        time_consuming: false
        weight: 70
      - task: "Write a complete short story"
        difficulty: "difficult"
        time_consuming: true
        weight: 20
      - task: "Edit a previous draft"
        difficulty: "normal"
        time_consuming: true
        weight: 50
      - task: "Write poetry"
        difficulty: "normal"
        time_consuming: false
        weight: 60
      - "Freewrite for 10 minutes"

  # Professional development
  - category: "Career Development"
    weight: 55
    tasks:
      - task: "Update your resume"
        difficulty: "normal"
        time_consuming: true
        weight: 40
      - task: "Network with a professional contact"
        difficulty: "normal"
        time_consuming: false
        weight: 50
      - task: "Apply to a job posting"
        difficulty: "normal"
        time_consuming: true
        weight: 45
      - task: "Learn a new professional skill"
        difficulty: "difficult"
        time_consuming: true
        weight: 35
      - "Polish your LinkedIn profile"

# Toggle which types of objectives to generate
custom_categories_include_specific_tasks: true  # e.g., "[Fitness Goals] Complete a 30-minute workout"
custom_categories_include_bulk_tasks: true  # e.g., "[Fitness Goals] Complete 3 tasks"
custom_categories_include_category_completion: true  # e.g., "[Fitness Goals] Complete all tasks in this category"
```

## Weight Guidelines

### Category Weight
- **80-100**: Very high priority - objectives from this category will appear very frequently
- **60-79**: High priority - objectives appear often
- **40-59**: Medium priority - balanced appearance
- **20-39**: Low priority - objectives appear occasionally
- **1-19**: Very low priority - objectives appear rarely

### Task Weight
- **70-100**: This task appears very frequently when this category is selected
- **50-69**: This task appears regularly
- **30-49**: This task appears moderately
- **10-29**: This task appears occasionally
- **1-9**: This task appears rarely

## Objective Types Generated

1. **Specific Task Objectives**: Individual tasks from categories
   - Example: `[Fitness Goals] Complete a 30-minute workout`

2. **Bulk Task Objectives**: Complete multiple tasks from a category
   - Example: `[Fitness Goals] Complete 3 tasks`
   - Automatically weighted toward smaller numbers (1-3 tasks more common than 7-10)

3. **Category Completion Objectives**: Complete all tasks in a category
   - Example: `[Fitness Goals] Complete all tasks in this category`
   - Always marked as time-consuming if category has multiple tasks

## Tips

1. **Use simplified task format** for simple tasks without special requirements:
   ```yaml
   tasks:
     - "Simple task"
     - "Another simple task"
   ```

2. **Use detailed task format** when you need granular control:
   ```yaml
   tasks:
     - task: "Complex task"
       difficulty: "difficult"
       time_consuming: true
       weight: 25
   ```

3. **Mix formats** within the same category:
   ```yaml
   tasks:
     - task: "Important detailed task"
       difficulty: "difficult"
       weight: 30
     - "Simple quick task"
     - "Another simple task"
   ```

4. **Balance weights** across categories to ensure variety in your objectives

5. **Mark time-consuming tasks appropriately** to help with filtering based on available time
