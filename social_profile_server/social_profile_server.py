import json
import logging
import os

from flask import Flask, Response, request
from typing import Any, List, Optional
from query_executor import execute_query, execute_update

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


def create_table() -> None:
    execute_update(
        """
        CREATE TABLE IF NOT EXISTS "profiles" (
            "username" VARCHAR(64) NOT NULL,
            "first_name" VARCHAR(64) NOT NULL,
            "last_name" VARCHAR(64) NOT NULL,
            "email" VARCHAR(64) NOT NULL,
            "profile_image" VARCHAR(64) NOT NULL,
            PRIMARY KEY ("username")
        )
        """
    )


def get_profile_from_username_or_none(username: str) -> Optional[List[Any]]:
    results: Optional[List[Any]] = execute_query(
        f"SELECT * "
        f"FROM profiles "
        f"WHERE username = '{username}'; "
    )

    if results is None or not results:
        return None

    return results


@app.route("/create/", methods=["POST"])
def create_profile() -> Response:
    """
    parameters: -
    body: {
        "username": str,
        "first_name": str,
        "last_name": str,
        "email": str,
        "profile_image": str
    }
    responses:
        201 - successful operation
        400 - bad request
    """
    try:
        form_body = request.form
        username = form_body["username"].lower()
        first_name = form_body["first_name"]
        last_name = form_body["last_name"]
        email = form_body["email"]
        profile_image = form_body["profile_image"]

        # The username already exists
        if get_profile_from_username_or_none(username) is not None:
            logger.info(f"Failed to register user, the specified username is already registered")
            return Response("User already exists, try to login", status=400)

    except (KeyError, TypeError, AttributeError) as e:
        logger.warning(f"Failed to parse user registration request, error: {e}")
        return Response("Invalid request body", status=400)

    execute_update(
        f"INSERT INTO profiles (username, first_name, last_name, email, profile_image) " 
        f"VALUES ('{username}', '{first_name}', '{last_name}', '{email}', '{profile_image}');"
    )
    return Response("", status=201)


@app.route("/update/", methods=["PUT"])
def update_profile() -> Response:
    """
    parameters: -
    body: {
        "username": str,
        "first_name": str,
        "last_name": str,
        "email": str,
        "profile_image": str
    }
    responses:
        200 - successful operation
        400 - bad request
    """
    try:
        form_body = request.form
        username = form_body["username"].lower()
        first_name = form_body["first_name"]
        last_name = form_body["last_name"]
        email = form_body["email"]
        profile_image = form_body["profile_image"]

        # The username does not exist
        if get_profile_from_username_or_none(username) is None:
            logger.info(
                f"Failed to update user, the specified username is not found")
            return Response("User not found, try again", status=400)

    except (KeyError, TypeError, AttributeError) as e:
        logger.warning(
            f"Failed to parse user registration request, error: {e}")
        return Response("Invalid request body", status=400)

    execute_update(
        f"UPDATE profiles "
        f"SET first_name = '{first_name}', last_name = '{last_name}', email = '{email}', profile_image = '{profile_image}' "
        f"WHERE username = '{username}'; "
    )

    return Response("", status=200)


@app.route("/get/", methods=["GET"])
def get_profile() -> Response:
    """
    parameters: -
    body: {
        "username": str
    }
    responses:
        200 - successful operation
        400 - bad request
    """
    try:
        form_body = request.form
        username = form_body["username"].lower()

        # The username does not exist
        results = get_profile_from_username_or_none(username)
        if results is None:
            logger.info(
                f"Failed to update user, the specified username is not found")
            return Response("User not found, try again", status=400)

        if not os.path.exists(results[0]["profile_image"]):
            logger.info(
                f"Failed to find profile image, the specified path does not exist")
            return Response("Profile image not found", status=400)

    except (KeyError, TypeError, AttributeError) as e:
        logger.warning(
            f"Failed to parse user registration request, error: {e}")
        return Response("Invalid request body", status=400)

    return Response(json.dumps(dict(results[0]), indent=4), status=200)


@app.route("/delete/", methods=["PUT"])
def delete_profile() -> Response:
    """
    parameters: -
    body: {
        "username": str
    }
    responses:
        200 - successful operation
        400 - bad request
    """
    try:
        form_body = request.form
        username = form_body["username"].lower()

        # The username does not exist
        if get_profile_from_username_or_none(username) is None:
            logger.info(
                f"Failed to update user, the specified username is not found")
            return Response("User not found, try again", status=400)

    except (KeyError, TypeError, AttributeError) as e:
        logger.warning(
            f"Failed to parse user registration request, error: {e}")
        return Response("Invalid request body", status=400)

    execute_update(
        f"DELETE "
        f"FROM profiles "
        f"WHERE username = '{username}'; "
    )

    return Response("", status=200)


if __name__ == '__main__':
    create_table()
    app.run(host="0.0.0.0", port=5000)

