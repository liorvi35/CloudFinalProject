import requests
import uuid
import logging


# logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# !! update API endpoint (without stage/resource) !!
EP = "https://ohr4tu0ed3.execute-api.us-east-1.amazonaws.com"


def create_read_delete():
    user_uuid = str(uuid.uuid4())
    response = requests.post(EP + "/prod/db", json={
        "accountID": user_uuid,
        "firstName": "Test",
        "lastName": "Test",
        "hashedPassword": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b",
        "email": "test@test.test",
        "birthDate": "1111-11-11",
        "gender": "male"
    })
    if int(response.json()["statusCode"]) != 200:
        logger.error("create_read_delete()/POST failed")
        raise Exception("Cannot create new user")
    
    response = requests.get(EP + f"/prod/db?accountID={user_uuid}")
    try:
        response.json()["statusCode"]
        logger.error("create_read_delete()/GET failed")
        raise Exception("Cannot read existing user")
    except KeyError:
        pass

    response = requests.delete(EP + "/prod/db", json={
        "accountID": user_uuid
    })
    if int(response.json()["statusCode"]) != 200:
            logger.error("create_read_delete()/DELETE failed")
            raise Exception("Cannot Delete existing user")

    logger.info("create_read_delete() success")


def delete_nonexistent_user():
    user_uuid = str(uuid.uuid4())
    response = requests.delete(EP + "/prod/db", json={
        "accountID": user_uuid
    })
    if int(response.json()["statusCode"]) != 404:
        logger.error("delete_nonexistent_user()/DELETE failed")
        raise Exception("Somehow deleted nonexistent user")
    
    logger.info("delete_nonexistent_user() success")


if __name__ == "__main__":
    try:
        create_read_delete()
        delete_nonexistent_user()
    except Exception as e:
        print(str(e))
