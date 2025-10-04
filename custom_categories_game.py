from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms

from Options import OptionList, DefaultOnToggle
from schema import And, Schema, Optional


@dataclass
class CustomCategoriesOptions:
    custom_categories_collection: CustomCategoriesCollection
    custom_categories_include_specific_tasks: CustomCategoriesIncludeSpecificTasks
    custom_categories_include_bulk_tasks: CustomCategoriesIncludeBulkTasks
    custom_categories_include_category_completion: CustomCategoriesIncludeCategoryCompletion


class CustomCategoriesGame(Game):
    name = "Custom Categories"
    platform = KeymastersKeepGamePlatforms.META

    is_adult_only_or_unrated = False

    options_cls = CustomCategoriesOptions

    categories_collection: dict

    def __init__(self,
        random = None,
        include_time_consuming_objectives: bool = False,
        include_difficult_objectives: bool = False,
        archipelago_options = None,):
        super().__init__(random, include_time_consuming_objectives, include_difficult_objectives, archipelago_options)
        self.categories_collection = {}

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        # Parse the categories collection once for efficiency

        if not self.categories_collection:
            try:
                for category in self.archipelago_options.custom_categories_collection:
                    if isinstance(category, dict):
                        category_name = category["category"]
                        tasks = category["tasks"]
                        weight = category.get("weight", 50)
                        
                        # Validate tasks structure
                        parsed_tasks = []
                        for task in tasks:
                            if isinstance(task, dict):
                                task_name = task["task"]
                                task_difficulty = task.get("difficulty", "normal")
                                task_time_consuming = task.get("time_consuming", False)
                                task_weight = task.get("weight", 50)
                                
                                parsed_tasks.append({
                                    "task": task_name,
                                    "difficulty": task_difficulty,
                                    "time_consuming": task_time_consuming,
                                    "weight": task_weight,
                                })
                            else:
                                # Simple string format for tasks
                                parsed_tasks.append({
                                    "task": str(task),
                                    "difficulty": "normal",
                                    "time_consuming": False,
                                    "weight": 50,
                                })
                        
                        self.categories_collection[category_name] = {
                            "tasks": parsed_tasks,
                            "weight": weight,
                        }
                    else:
                        print(f"Warning: Expected dict but got {type(category)}: {category}")
            except Exception as e:
                raise ValueError(f"Error parsing custom categories collection: {e}") from e

        if not self.categories_collection:
            raise ValueError("No categories available in collection. Check your custom categories configuration.")
        
        return []

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives = []

        # Ensure categories collection is parsed
        if not self.categories_collection:
            _ = self.optional_game_constraint_templates()

        # Generate objectives for each category
        for category_name, category_info in self.categories_collection.items():
            category_weight = category_info["weight"]
            tasks = category_info["tasks"]
            
            # Generate specific task objectives (if enabled)
            if self.archipelago_options.custom_categories_include_specific_tasks:
                for task in tasks:
                    task_objective = GameObjectiveTemplate(
                        label=f"[{category_name}] {task['task']}",
                        data={},
                        is_difficult=(task["difficulty"] == "difficult"),
                        is_time_consuming=task["time_consuming"],
                        weight=task["weight"]
                    )
                    objectives.append(task_objective)

            # Generate bulk task objectives (if enabled)
            if self.archipelago_options.custom_categories_include_bulk_tasks and len(tasks) > 1:
                # Calculate how many tasks to include in bulk objectives
                max_bulk_tasks = min(len(tasks), 10)  # Cap at 10 tasks max
                
                # Generate a few different bulk options with weighted randomness
                # Favor lower numbers (1-3 tasks more likely than 7-10 tasks)
                for _ in range(min(3, max_bulk_tasks)):  # Generate up to 3 different bulk objectives per category
                    weights = [max_bulk_tasks - i for i in range(max_bulk_tasks)]
                    num_tasks = self.random.choices(range(1, max_bulk_tasks + 1), weights=weights)[0]
                    
                    task_text = "task" if num_tasks == 1 else "tasks"
                    
                    # Determine if this bulk objective is difficult or time-consuming
                    # Consider it difficult if ANY task in the category is difficult
                    is_difficult = any(task["difficulty"] == "difficult" for task in tasks)
                    # Consider it time-consuming if completing multiple tasks OR if any task is time-consuming
                    is_time_consuming = (num_tasks > 3) or any(task["time_consuming"] for task in tasks)
                    
                    bulk_objective = GameObjectiveTemplate(
                        label=f"[{category_name}] Complete {num_tasks} {task_text}",
                        data={},
                        is_difficult=is_difficult,
                        is_time_consuming=is_time_consuming,
                        weight=category_weight
                    )
                    objectives.append(bulk_objective)

            # Add category completion objective (if enabled)
            if self.archipelago_options.custom_categories_include_category_completion and len(tasks) > 1:
                # Determine difficulty based on any difficult task in category
                is_difficult = any(task["difficulty"] == "difficult" for task in tasks)
                # Completing entire category is always time-consuming if there are multiple tasks
                is_time_consuming = True
                
                completion_objective = GameObjectiveTemplate(
                    label=f"[{category_name}] Complete all tasks in this category",
                    data={},
                    is_difficult=is_difficult,
                    is_time_consuming=is_time_consuming,
                    weight=max(10, category_weight // 2)  # Lower weight for completion objectives
                )
                objectives.append(completion_objective)

        return objectives


class CustomCategoriesCollection(OptionList):
    """
    Definition of custom categories collection. Format is as follows:
    - category: "Category Name"
      weight: 50 (*optional, defaults to 50, controls how often this category's objectives appear)
      tasks:
        - task: "Task description"
          difficulty: "normal" (*optional, can be "normal" or "difficult")
          time_consuming: false (*optional, defaults to false)
          weight: 50 (*optional, defaults to 50, controls how often this specific task appears)
        - task: "Another task description"
          difficulty: "difficult"
          time_consuming: true
          weight: 25
        - "Simple task without options" (*simplified format)
    """

    display_name = "Custom Categories Collection"
    default = [
        {
            "category": "Fitness & Health",
            "weight": 75,
            "tasks": [
                {
                    "task": "Complete a 30-minute workout",
                    "difficulty": "normal",
                    "time_consuming": False,
                    "weight": 70
                },
                {
                    "task": "Go for a 5km run or walk",
                    "difficulty": "normal",
                    "time_consuming": True,
                    "weight": 60
                },
                {
                    "task": "Do 50 push-ups",
                    "difficulty": "normal",
                    "time_consuming": False,
                    "weight": 65
                },
                {
                    "task": "Attend a fitness class",
                    "difficulty": "normal",
                    "time_consuming": True,
                    "weight": 45
                },
                {
                    "task": "Complete a HIIT workout",
                    "difficulty": "difficult",
                    "time_consuming": False,
                    "weight": 40
                },
                "Stretch for 15 minutes",
                "Track your meals for the day",
                "Drink 8 glasses of water"
            ]
        },
        {
            "category": "Home Improvement",
            "weight": 50,
            "tasks": [
                {
                    "task": "Organize the garage or storage area",
                    "difficulty": "normal",
                    "time_consuming": True,
                    "weight": 35
                },
                {
                    "task": "Clean out the refrigerator",
                    "difficulty": "normal",
                    "time_consuming": False,
                    "weight": 60
                },
                {
                    "task": "Declutter one room",
                    "difficulty": "normal",
                    "time_consuming": True,
                    "weight": 45
                },
                {
                    "task": "Deep clean the bathroom",
                    "difficulty": "normal",
                    "time_consuming": True,
                    "weight": 40
                },
                "Vacuum the entire house",
                "Do the laundry",
                "Organize your desk or workspace",
                "Clean all windows",
                "Sort and recycle old items"
            ]
        },
        {
            "category": "Creative Projects",
            "weight": 55,
            "tasks": [
                {
                    "task": "Write a short story (500+ words)",
                    "difficulty": "difficult",
                    "time_consuming": True,
                    "weight": 30
                },
                {
                    "task": "Create a piece of digital art",
                    "difficulty": "normal",
                    "time_consuming": True,
                    "weight": 45
                },
                {
                    "task": "Write and record an original song",
                    "difficulty": "difficult",
                    "time_consuming": True,
                    "weight": 25
                },
                {
                    "task": "Complete a drawing or sketch",
                    "difficulty": "normal",
                    "time_consuming": False,
                    "weight": 60
                },
                "Learn a new creative technique",
                "Work on a creative hobby for 30 minutes",
                "Take and edit 10 photos",
                "Write poetry or lyrics"
            ]
        },
        {
            "category": "Learning & Skills",
            "weight": 65,
            "tasks": [
                {
                    "task": "Complete an online course module",
                    "difficulty": "normal",
                    "time_consuming": True,
                    "weight": 50
                },
                {
                    "task": "Practice a new language for 30 minutes",
                    "difficulty": "normal",
                    "time_consuming": False,
                    "weight": 70
                },
                {
                    "task": "Read a technical or educational article",
                    "difficulty": "normal",
                    "time_consuming": False,
                    "weight": 75
                },
                {
                    "task": "Build a small coding project",
                    "difficulty": "difficult",
                    "time_consuming": True,
                    "weight": 30
                },
                {
                    "task": "Watch an educational documentary",
                    "difficulty": "normal",
                    "time_consuming": True,
                    "weight": 55
                },
                "Practice a musical instrument for 20 minutes",
                "Learn 10 new vocabulary words",
                "Solve a challenging puzzle or brain teaser"
            ]
        },
        {
            "category": "Personal Development",
            "weight": 80,
            "tasks": [
                {
                    "task": "Practice meditation for 15 minutes",
                    "difficulty": "normal",
                    "time_consuming": False,
                    "weight": 75
                },
                {
                    "task": "Journal about your goals and progress",
                    "difficulty": "normal",
                    "time_consuming": False,
                    "weight": 70
                },
                {
                    "task": "Read a self-help or motivational book chapter",
                    "difficulty": "normal",
                    "time_consuming": True,
                    "weight": 60
                },
                {
                    "task": "Review and update your personal goals",
                    "difficulty": "normal",
                    "time_consuming": False,
                    "weight": 50
                },
                "Practice gratitude - list 5 things you're grateful for",
                "Do a self-reflection exercise",
                "Plan your week ahead",
                "Learn about a new personal development concept"
            ]
        },
        {
            "category": "Social & Connections",
            "weight": 60,
            "tasks": [
                {
                    "task": "Call or video chat with a friend or family member",
                    "difficulty": "normal",
                    "time_consuming": False,
                    "weight": 70
                },
                {
                    "task": "Write a thoughtful message to someone you care about",
                    "difficulty": "normal",
                    "time_consuming": False,
                    "weight": 75
                },
                {
                    "task": "Plan and host a social gathering",
                    "difficulty": "normal",
                    "time_consuming": True,
                    "weight": 30
                },
                {
                    "task": "Attend a community event or meetup",
                    "difficulty": "normal",
                    "time_consuming": True,
                    "weight": 40
                },
                "Send a thank you note to someone",
                "Reconnect with an old friend",
                "Perform a random act of kindness",
                "Join or participate in an online community"
            ]
        },
        {
            "category": "Career Development",
            "weight": 45,
            "tasks": [
                {
                    "task": "Update your resume or CV",
                    "difficulty": "normal",
                    "time_consuming": True,
                    "weight": 40
                },
                {
                    "task": "Network with a professional contact",
                    "difficulty": "normal",
                    "time_consuming": False,
                    "weight": 55
                },
                {
                    "task": "Apply to a job posting or opportunity",
                    "difficulty": "normal",
                    "time_consuming": True,
                    "weight": 45
                },
                {
                    "task": "Learn a new professional skill",
                    "difficulty": "difficult",
                    "time_consuming": True,
                    "weight": 35
                },
                {
                    "task": "Complete a professional certification module",
                    "difficulty": "difficult",
                    "time_consuming": True,
                    "weight": 30
                },
                "Polish your LinkedIn profile",
                "Research a company or industry you're interested in",
                "Practice interview skills",
                "Read industry news or articles"
            ]
        },
        {
            "category": "Financial Management",
            "weight": 40,
            "tasks": [
                {
                    "task": "Review and update your budget",
                    "difficulty": "normal",
                    "time_consuming": True,
                    "weight": 60
                },
                {
                    "task": "Track all expenses for a week",
                    "difficulty": "normal",
                    "time_consuming": False,
                    "weight": 70
                },
                {
                    "task": "Research and compare investment options",
                    "difficulty": "difficult",
                    "time_consuming": True,
                    "weight": 30
                },
                {
                    "task": "Pay all outstanding bills",
                    "difficulty": "normal",
                    "time_consuming": False,
                    "weight": 65
                },
                "Review your subscriptions and cancel unused ones",
                "Set up or contribute to savings",
                "Read about personal finance",
                "Organize your financial documents"
            ]
        }
    ]
    schema = Schema([
        {
            "category": And(str, len),
            Optional("weight"): And(int, lambda x: x >= 0),
            "tasks": [
                # Can be either a simple string or a detailed dict
                lambda task: (
                    isinstance(task, str) or
                    (isinstance(task, dict) and 
                     "task" in task and 
                     isinstance(task["task"], str) and
                     len(task["task"]) > 0 and
                     task.get("difficulty", "normal") in ["normal", "difficult"] and
                     isinstance(task.get("time_consuming", False), bool) and
                     (isinstance(task.get("weight", 50), int) and task.get("weight", 50) >= 0))
                )
            ],
        }
    ])


class CustomCategoriesIncludeSpecificTasks(DefaultOnToggle):
    """
    Whether to include specific task objectives like '[Category] Task Name'
    """
    display_name = "Include Specific Task Objectives"


class CustomCategoriesIncludeBulkTasks(DefaultOnToggle):
    """
    Whether to include bulk task objectives like '[Category] Complete 3 tasks'
    """
    display_name = "Include Bulk Task Objectives"


class CustomCategoriesIncludeCategoryCompletion(DefaultOnToggle):
    """
    Whether to include category completion objectives like '[Category] Complete all tasks in this category'
    """
    display_name = "Include Category Completion Objectives"
