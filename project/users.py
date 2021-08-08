from json import load, dump
from typing import Dict, Optional
import os
from pathlib import Path

from flask_login import UserMixin


# note: I assumes there isn't a lot of users, therefore it's fine saving them all in same json file
# for scaling I would save the users in A-Z users json files for faster querying of user data

# todo: make users json files name(s) configurable instead of hardcoded


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def read_users_json():
    users: Dict[str, "User"] = {}
    with open(f"{ROOT_DIR}/data_store/users.json") as json_file:
        data = load(json_file)
        if data:
            for key in data:
                users[key] = User(
                    username=key
                )
    print(users)
    return users


def update_users_json(user):

    with open(f"{ROOT_DIR}/data_store/users.json") as json_file:
        json_decoded = load(json_file)

    json_decoded[user.id] = {"favorites": user.favorites}

    with open(f"{ROOT_DIR}/data_store/users.json", 'w') as json_file:
        dump(json_decoded, json_file)

    return user


def create_user(username):
    new_user = User(username)
    if not new_user.get(username):
        user_dict = update_users_json(new_user)
        create_user_favorites_json(new_user)
    return user_dict


def create_user_favorites_json(user):
    abs_favorites_path = f"{ROOT_DIR}/{user.favorites}"
    if not Path.is_file(Path(abs_favorites_path)):
        with open(abs_favorites_path, 'w+') as json_file:
            dump({}, json_file)


class User(UserMixin):
    def __init__(self, username: str):

        # note: I decided to "duplicate" the username to two attributes,
        # so that for later implementation the user will hold a real one-to-one id, and a username
        # while minimizing affection of rest of the code

        self.id = username
        self.username = username
        self.favorites = f"data_store/favorites/{username}.json"  # TODO: make path configurable instead of hard coded

    @staticmethod
    def get(user_id: str) -> Optional["User"]:
        return read_users_json().get(user_id)

    def __str__(self) -> str:
        return f"<Username: {self.id}, Favorites: {self.favorites}>"

    def __repr__(self) -> str:
        return self.__str__()
