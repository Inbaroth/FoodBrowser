from json import load, dump
from typing import Dict, Optional
import os

from flask_login import UserMixin, current_user

# todo: make users json files name(s) configurable instead of hardcoded


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def read_favorites_json():
    user_favorites: Dict[str, "Favorites"] = {}
    if current_user.is_authenticated:
        username = current_user.username

        with open(f"{ROOT_DIR}/data_store/{username}.json") as json_file:
            data = load(json_file)
            if data:
                for key in data:
                    user_favorites[key] = Favorite(
                        food_name=key,
                        food_img_url=data[key]["food_img_url"]

                    )
    print(user_favorites)
    return user_favorites


def update_user_favorites_json(favorite):

    if current_user.is_authenticated:
        user_favorites_path = current_user.favorites

        with open(f"{ROOT_DIR}/{user_favorites_path}") as json_file:
            json_decoded = load(json_file)

        json_decoded[favorite.id] = {"food_img_url": favorite.food_img_url}

        with open(f"{ROOT_DIR}/{user_favorites_path}", 'w') as json_file:
            dump(json_decoded, json_file)

    return favorite


def create_favorite(food_name):
    new_favorite = Favorite(food_name)
    if not new_favorite.get(food_name):
        user_dict = update_user_favorites_json(new_favorite)
    return user_dict


class Favorite(UserMixin):
    def __init__(self, food_name: str, food_img_url: str):

        # note: I assume there's no duplications in food name

        self.id = food_name
        self.food_img_url = food_img_url

    @staticmethod
    def get(favorite_id: str) -> Optional["Favorite"]:
        return read_favorites_json().get(favorite_id)

    def __str__(self) -> str:
        return f"<food_name: {self.id}, food_img_url: {self.food_img_url}>"

    def __repr__(self) -> str:
        return self.__str__()


