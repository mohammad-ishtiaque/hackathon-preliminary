from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json
import sqlite_utils
from pathlib import Path
import os
from dotenv import load_dotenv

import google.generativeai as genai

from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from database import db

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# GOOGLE_API_KEY=AIzaSyDf7NCUVVAXleSqbQgc_T5vgKJBH7gBo7s
genai.configure(api_key=GOOGLE_API_KEY)

app = FastAPI()


# Define the list of allowed origins
origins = [ "http://localhost:9000",
           "http://127.0.0.1:9000"
        ]
# Add the CORS middleware to your application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# API Response/Request Models
class Ingredient(BaseModel):
    id: int | None = None #Optional id
    name: str
    quantity: float
    unit: str
    date_added: str | None = None

class Recipe(BaseModel):
    id: int | None = None
    name: str
    cuisine_type: str
    taste: str
    reviews: str
    preparation_time: str
    ingredients: str

class ChatRequest(BaseModel):
    query: str

# Ingredient Endpoints
@app.get("/ingredients", response_model=List[Ingredient])
async def get_ingredients():
    return list(db["ingredients"].rows)

@app.post("/ingredients", response_model=Ingredient, status_code=201)
async def add_ingredient(ingredient: Ingredient):
    db["ingredients"].insert(ingredient.model_dump(), ignore=True) #ignoring id provided by the user
    return ingredient

@app.put("/ingredients/{item_id}", response_model=Ingredient)
async def update_ingredient(item_id: int, ingredient: Ingredient):
    if db["ingredients"].get(item_id) is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    db["ingredients"].update(item_id, ingredient.model_dump())
    return ingredient

@app.delete("/ingredients/{item_id}", status_code=204)
async def delete_ingredient(item_id: int):
    if db["ingredients"].get(item_id) is None:
         raise HTTPException(status_code=404, detail="Ingredient not found")
    db["ingredients"].delete(item_id)

# Recipe Endpoints
@app.get("/recipes", response_model=List[Recipe])
async def get_recipes():
  return list(db["recipes"].rows)

@app.post("/recipes", response_model=Recipe, status_code=201)
async def add_recipe(recipe: Recipe):
  db["recipes"].insert(recipe.model_dump(), ignore=True)
  return recipe

# Chatbot Endpoint
@app.post("/chatbot")
async def chatbot_endpoint(chat_request : ChatRequest):
    model = genai.GenerativeModel('gemini-pro')

    # Fetch available ingredients
    available_ingredients = list(db["ingredients"].rows)
    ingredients_string = ", ".join([f"{item['quantity']} {item['unit']} of {item['name']}" for item in available_ingredients])
    # Fetch available recipes
    available_recipes = list(db["recipes"].rows)
    recipes_string = json.dumps(available_recipes)

    prompt = f"""
        You are a recipe recommendation system that takes in a user query, available recipes and available ingredients
        and responds to the user based on the information.
        
        Here are the list of recipes available: {recipes_string}

        Here are the list of ingredients available: {ingredients_string}
        
        User query: {chat_request.query}

        Instructions:
        1. Recommend recipes that are possible to make with the provided ingredients and taking into account the user query.
        2. If there are no recipes possible with given ingredients respond with a message indicating that.
        3. If the user query does not indicate which recipe to look for, provide a recommendation based on the available ingredients.
         
        """

    response = model.generate_content(prompt)
    return {"response": response.text}

def populate_database():
    recipe_file = Path(__file__).parent / "my_fav_recipes.txt" #this will search for the `my_fav_recipes.txt` file in the same folder as `main.py`
    recipes_list = []
    with open(recipe_file, 'r') as f:
        current_recipe = {}
        for line in f:
            line = line.strip()
            if line.startswith("Recipe Name:"):
                current_recipe["name"] = line.split(": ", 1)[1]
            elif line.startswith("Cuisine type:"):
                current_recipe["cuisine_type"] = line.split(": ", 1)[1]
            elif line.startswith("Taste:"):
                current_recipe["taste"] = line.split(": ", 1)[1]
            elif line.startswith("Reviews:"):
                current_recipe["reviews"] = line.split(": ", 1)[1]
            elif line.startswith("Preparation time:"):
                current_recipe["preparation_time"] = line.split(": ", 1)[1]
            elif line.startswith("Ingredients:"):
                current_recipe["ingredients"] = line.split(": ", 1)[1]

                recipes_list.append(Recipe(**current_recipe).model_dump())
    db["recipes"].insert_all(recipes_list, ignore=True)
if not db["recipes"].exists():
    populate_database()
