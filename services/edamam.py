import requests
from django.conf import settings

def search_recipes(
    query=None,
    calories=None,
    ingredients=None,
    diet_labels=None,
    health_labels=None,
    cuisine_type=None,
    meal_type=None,
    dish_type=None
):
    url = 'https://api.edamam.com/api/recipes/v2'
    params = {
        'type': 'public',
        'app_id': settings.EDAMAM_APP_ID,
        'app_key': settings.EDAMAM_APP_KEY,
    }

    headers = {
        'Edamam-Account-User': settings.EDAMAM_APP_ID,
    }

    if query:
        params['q'] = query
    if calories:
        params['calories'] = calories
    if ingredients:
        params['ingr'] = ingredients
    if diet_labels:
        params['diet'] = diet_labels
    if health_labels:
        params['health'] = health_labels
    if cuisine_type:
        params['cuisineType'] = cuisine_type
    if meal_type:
        params['mealType'] = meal_type
    if dish_type:
        params['dishType'] = dish_type

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        filtered_results = [data.get('count', 0), data.get('from', 0), data.get('to', 0), data.get('_links', {})]

        for hit in data.get('hits', []):
            recipe = hit.get('recipe', {})
            filtered_results.append({
                'label': recipe.get('label'),
                'image': recipe.get('image'),
                'url': recipe.get('url'),
                'uri': recipe.get('uri'),
                'ingredientLines': recipe.get('ingredientLines', []),
                'ingredients': recipe.get('ingredients', []),
                'cuisineType': recipe.get('cuisineType', []),
                'dishType': recipe.get('dishType', []),
                'mealType': recipe.get('mealType', []),
            })

        return filtered_results                 
    else:
        return {'error': f'API Error {response.status_code}', 'details': response.text}

def get_recipe_by_uri(uri):
    url = 'https://api.edamam.com/api/recipes/v2/by-uri'
    params = {
        'type': 'public',
        'app_id': settings.EDAMAM_APP_ID,
        'app_key': settings.EDAMAM_APP_KEY,
        'uri': uri
    }
    headers = {
        'Edamam-Account-User': settings.EDAMAM_APP_ID,
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f'API Error {response.status_code}', 'details': response.text}
