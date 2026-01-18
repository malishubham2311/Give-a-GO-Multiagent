import os
from typing import Dict, List, Optional

from google.adk.agents.llm_agent import Agent


# -------------------------------------------------
# TOOL 1: Suggest dishes based on ingredients
# -------------------------------------------------
def suggest_dishes(
    ingredients: str,
    cuisine: Optional[str] = None,
    meal_type: Optional[str] = None,
) -> Dict:
    """
    Suggest dish ideas based on ingredients, cuisine and meal type.
    """
    print(f"[TOOL CALL] suggest_dishes")
    print(f"ingredients={ingredients}, cuisine={cuisine}, meal_type={meal_type}")

    ing = ingredients.lower()
    cui = cuisine.lower() if isinstance(cuisine, str) else None
    meal = meal_type.lower() if isinstance(meal_type, str) else None

    suggestions: List[Dict] = []

    # 1. Paneer-based Indian dishes
    if "paneer" in ing and (cui is None or cui == "indian"):
        suggestions.append({
            "name": "Paneer Butter Masala",
            "reason": "Rich North Indian curry using paneer and spices."
        })
        suggestions.append({
            "name": "Mixed Veg Paneer Curry",
            "reason": "Uses paneer plus mixed vegetables in one curry."
        })
        suggestions.append({
            "name": "Paneer Bhurji",
            "reason": "Quick scrambled paneer dish, great with roti or bread."
        })

    # 2. Chicken + rice based dishes
    if "chicken" in ing and "rice" in ing:
        if "butter" in ing and (cui is None or cui == "indian"):
            suggestions.append({
                "name": "Butter Chicken with Steamed Rice",
                "reason": "Butter + chicken fits perfectly for butter chicken with rice."
            })

        if cui is None or cui == "indian":
            suggestions.append({
                "name": "Chicken Pulao",
                "reason": "Mildly spiced one-pot chicken and rice."
            })

        suggestions.append({
            "name": "One-Pot Chicken Rice",
            "reason": "Simple one-pot chicken and rice using basic spices."
        })

    # 3. Simple generic dishes
    if "pasta" in ing:
        suggestions.append({
            "name": "Garlic Tomato Pasta",
            "reason": "Tomato and pasta make a quick meal."
        })

    if "potato" in ing and not any("potato" in s["name"].lower() for s in suggestions):
        suggestions.append({
            "name": "Crispy Masala Potatoes",
            "reason": "Pan-fried potatoes with spices as an easy side."
        })

    # 4. Fallback
    if not suggestions:
        suggestions.append({
            "name": "Mixed Veg Stir-Fry",
            "reason": "Generic stir-fry that works with most vegetables."
        })

    return {
        "status": "success",
        "ingredients": ingredients,
        "cuisine": cuisine,
        "meal_type": meal,
        "suggestions": suggestions,
    }


# -------------------------------------------------
# TOOL 2: Generate recipe for selected dish
# -------------------------------------------------
def get_recipe(dish_name: str, servings: int = 2) -> Dict:
    """
    Return a simple recipe for the given dish name.
    """
    print(f"[TOOL CALL] get_recipe: {dish_name}, servings={servings}")

    dish = dish_name.lower().strip()

    # Paneer recipes
    if "paneer butter masala" in dish:
        ingredients = [
            f"Paneer – {100 * servings} g (cubed)",
            "Butter – 1–2 tbsp",
            "Onion – 1, finely chopped",
            "Tomatoes or tomato puree – 1 cup",
            "Ginger-garlic paste – 1 tsp",
            "Cream (optional) – 2–3 tbsp",
            "Spices: chili powder, turmeric, garam masala, salt",
            "Kasuri methi (optional)",
            "Oil or ghee as needed",
        ]
        steps = [
            "Heat oil and a little butter in a pan, sauté onion until golden.",
            "Add ginger-garlic paste and cook for a minute.",
            "Add tomato/puree and cook until the raw smell goes.",
            "Add spices and cook a few minutes.",
            "Blend gravy smooth (optional) and return to pan.",
            "Add paneer cubes, more butter and cream; simmer 3–5 minutes.",
            "Finish with crushed kasuri methi and serve with roti or rice.",
        ]

    elif "mixed veg paneer curry" in dish or ("paneer" in dish and "curry" in dish):
        ingredients = [
            f"Paneer – {80 * servings} g (cubed)",
            "Mixed vegetables – 1–2 cups",
            "Onion – 1, chopped",
            "Tomatoes – 1 cup, chopped or pureed",
            "Ginger-garlic paste – 1 tsp",
            "Oil or ghee",
            "Spices: cumin seeds, turmeric, chili powder, coriander powder, garam masala, salt",
        ]
        steps = [
            "Heat oil, add cumin seeds and let them splutter.",
            "Sauté onion until light golden, then add ginger-garlic paste.",
            "Add tomatoes and cook until soft.",
            "Add dry spices and cook 1–2 minutes.",
            "Add mixed vegetables with a little water, cover and cook.",
            "Add paneer cubes and simmer 3–5 minutes.",
            "Adjust seasoning and serve with rice or roti.",
        ]

    elif "paneer bhurji" in dish:
        ingredients = [
            f"Paneer – {100 * servings} g, crumbled",
            "Onion – 1, chopped",
            "Tomato – 1, chopped",
            "Green chili – 1 (optional), chopped",
            "Ginger-garlic paste – 1 tsp",
            "Oil or ghee",
            "Spices: turmeric, chili powder, garam masala, salt",
            "Coriander leaves for garnish",
        ]
        steps = [
            "Heat oil and sauté onion and green chili until soft.",
            "Add ginger-garlic paste and cook briefly.",
            "Add tomato and cook until mushy.",
            "Add spices and cook 1–2 minutes.",
            "Add crumbled paneer, mix well and cook a few minutes.",
            "Garnish with coriander leaves and serve with roti or bread.",
        ]

    # Chicken + rice recipes
    elif "butter chicken" in dish:
        ingredients = [
            f"Chicken – {150 * servings} g (boneless preferred)",
            "Butter – 2–3 tbsp",
            "Onion – 1, chopped",
            "Tomato puree – 1 cup",
            "Ginger-garlic paste – 1–2 tsp",
            "Cream or milk – 1/4 cup (optional)",
            "Spices: chili powder, turmeric, garam masala, salt",
            "Kasuri methi (optional)",
        ]
        steps = [
            "Marinate chicken with salt, chili and a little yogurt (optional).",
            "Pan-fry or grill chicken pieces until mostly cooked; set aside.",
            "In another pan, heat butter and sauté onion until golden.",
            "Add ginger-garlic paste and cook briefly, then add tomato puree.",
            "Cook until raw smell goes, then add spices and simmer.",
            "Add cooked chicken pieces into gravy and simmer 5–10 minutes.",
            "Finish with cream and kasuri methi; serve with rice or naan.",
        ]

    elif "chicken pulao" in dish:
        ingredients = [
            f"Chicken – {150 * servings} g",
            f"Basmati rice – {0.5 * servings} cup (uncooked)",
            "Onion – 1, sliced",
            "Ginger-garlic paste – 1 tsp",
            "Whole spices (bay leaf, cloves, cardamom, cinnamon) – optional",
            "Oil or ghee",
            "Salt and pulao masala / garam masala",
            "Water – about 2× the rice volume",
        ]
        steps = [
            "Wash and soak rice 15–20 minutes.",
            "Heat oil/ghee, add whole spices and let them splutter.",
            "Add sliced onion and sauté until golden.",
            "Add ginger-garlic paste and chicken pieces; sauté a few minutes.",
            "Add spices and salt, then drained rice; sauté gently.",
            "Add water, bring to a boil, then cover and cook on low until rice is done.",
            "Rest a few minutes, fluff and serve.",
        ]

    elif "one-pot chicken rice" in dish or ("chicken" in dish and "rice" in dish):
        ingredients = [
            f"Chicken – {150 * servings} g",
            f"Rice – {0.5 * servings} cup (uncooked)",
            "Onion – 1, chopped",
            "Garlic & ginger – 1 tsp each, chopped",
            "Mixed vegetables – 1 cup (optional)",
            "Spices: salt, pepper, chili powder, cumin/coriander powder",
            "Oil or butter",
            "Water or stock – about 2× rice volume",
        ]
        steps = [
            "Heat oil or butter and sauté onion, garlic and ginger.",
            "Add chicken and cook until lightly browned.",
            "Add vegetables and spices; cook 2–3 minutes.",
            "Add washed rice and water/stock, bring to a boil.",
            "Cover and cook on low until rice is done (15–20 minutes).",
            "Fluff and serve warm.",
        ]

    # Generic fallback recipes
    elif "pasta" in dish:
        ingredients = [
            f"Pasta – {80 * servings} g",
            "Garlic – 3 cloves",
            "Tomatoes – 1 cup",
            "Olive oil – 2 tbsp",
            "Salt & pepper",
        ]
        steps = [
            "Boil salted water and cook pasta until soft.",
            "Heat oil and lightly fry garlic.",
            "Add tomatoes and cook 5 minutes.",
            "Season and mix pasta into sauce.",
            "Serve hot.",
        ]

    elif "fried rice" in dish:
        ingredients = [
            "Cooked rice",
            "Eggs",
            "Vegetables",
            "Soy sauce",
            "Oil",
            "Salt",
        ]
        steps = [
            "Scramble eggs and remove from pan.",
            "Fry vegetables in oil.",
            "Add rice and soy sauce, stir-fry well.",
            "Mix eggs back in and serve.",
        ]

    elif "potato" in dish:
        ingredients = [
            "Potatoes",
            "Oil",
            "Salt",
            "Chili powder",
            "Turmeric",
        ]
        steps = [
            "Boil or parboil potatoes.",
            "Fry in oil until crispy.",
            "Add spices and salt.",
            "Serve hot.",
        ]

    else:
        return {
            "status": "error",
            "error_message": "Dish not found in predefined list. Try another dish name."
        }

    return {
        "status": "success",
        "dish_name": dish_name,
        "servings": servings,
        "ingredients": ingredients,
        "steps": steps,
        "notes": [
            "Adjust spices and oil to taste.",
            "Serve with roti, naan, or rice as appropriate.",
        ],
    }


# -------------------------------------------------
# MULTI-AGENT SETUP
# -------------------------------------------------

ROOT_MODEL = os.getenv("ROOT_MODEL", "gemini-2.0-flash")
DISH_MODEL = os.getenv("DISH_MODEL", ROOT_MODEL)
RECIPE_MODEL = os.getenv("RECIPE_MODEL", ROOT_MODEL)

# Dish suggester agent
dish_agent = Agent(
    model=DISH_MODEL,
    name="dish_agent",
    description="Suggests dishes from ingredients, cuisine and meal type.",
    instruction=(
        "You are a dish suggestion specialist.\n"
        "Always call the 'suggest_dishes' tool using the user's ingredients, "
        "and cuisine/meal_type if they mention them.\n"
        "Return 1–3 dish options as a bullet list with a short reason.\n"
        "Do NOT give full recipes."
    ),
    tools=[suggest_dishes],
)

# Recipe agent
recipe_agent = Agent(
    model=RECIPE_MODEL,
    name="recipe_agent",
    description="Generates full recipes for a specific dish.",
    instruction=(
        "You are a recipe specialist.\n"
        "Always call the 'get_recipe' tool with the requested dish_name and "
        "servings (default 2 if user doesn't specify).\n"
        "Then respond with:\n"
        "- A title\n"
        "- Ingredients as a bullet list\n"
        "- Steps as a numbered list\n"
        "- Optional notes."
    ),
    tools=[get_recipe],
)

# Root orchestrator agent
root_agent = Agent(
    model=ROOT_MODEL,
    name="root_agent",
    description="Orchestrator that delegates to dish_agent or recipe_agent.",
    instruction=(
        "You are the main cooking assistant coordinating two sub-agents:\n"
        "- 'dish_agent' suggests dishes from ingredients.\n"
        "- 'recipe_agent' generates full recipes.\n\n"
        "If the user asks what they can cook with some ingredients, delegate "
        "to 'dish_agent'.\n"
        "If they ask for the recipe for a specific dish, delegate to 'recipe_agent'.\n"
        "If they choose a dish from a previous list, send that follow-up to 'recipe_agent'."
    ),
    sub_agents=[dish_agent, recipe_agent],
)
