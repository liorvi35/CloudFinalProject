import requests
import uuid
import logging

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
        raise Exception("Deleted nonexistent user")
    
    logger.info("delete_nonexistent_user() success")


def create_empty_user():
    user_uuid = str(uuid.uuid4())
    response = requests.post(EP + "/prod/db", json={
        "accountID": user_uuid,
        "firstName": "Test",
        "hashedPassword": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b",
        "email": "test@test.test",
        "birthDate": "1111-11-11",
        "gender": "male"
    })
    if int(response.json()["statusCode"]) != 400:
        logger.error("create_empty_user()/POST failed")
        raise Exception("Created Bad User")
    
    response = requests.post(EP + "/prod/db", json={})
    if int(response.json()["statusCode"]) != 400:
        logger.error("create_empty_user()/POST failed")
        raise Exception("Created Bad User")
    
    response = requests.post(EP + "/prod/db", json={
        "accountID": user_uuid,
        "lastName": "Test",
        "birthDate": "1111-11-11",
        "gender": "male"
    })
    if int(response.json()["statusCode"]) != 400:
        logger.error("create_empty_user()/POST failed")
        raise Exception("Created Bad User")
    
    response = requests.post(EP + "/prod/db", json={
        "accountID": user_uuid,
        "firstName": "Test",
        "lastName": "Test",
        "hashedPassword": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b",
        "email": "test@test.test"
    })
    if int(response.json()["statusCode"]) != 400:
        logger.error("create_empty_user()/POST failed")
        raise Exception("Created Bad User")
    
    response = requests.post(EP + "/prod/db", json={
        "accountID": user_uuid,
        "firstName": "Test",
        "lastName": "Test",
        "email": "test@test.test",
        "birthDate": "1111-11-11",
        "gender": "male"
    })
    if int(response.json()["statusCode"]) != 400:
        logger.error("create_empty_user()/POST failed")
        raise Exception("Created Bad User")
    
    logger.info("create_empty_user() success")


def create_user_empty_params():
    user_uuid = str(uuid.uuid4())
    response = requests.post(EP + "/prod/db", json={
        "accountID": user_uuid,
        "firstName": "",
        "lastName": "",
        "hashedPassword": "",
        "email": "",
        "birthDate": "",
        "gender": ""
    })
    if int(response.json()["statusCode"]) != 400:
        logger.error("create_user_empty_params()/POST failed")
        raise Exception("Created user with empty parameters")
    
    response = requests.post(EP + "/prod/db", json={
        "accountID": user_uuid,
        "firstName": "",
        "lastName": "",
        "hashedPassword": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b",
        "email": "test@test.test",
        "birthDate": "1111-11-11",
        "gender": "male"
    })
    if int(response.json()["statusCode"]) != 400:
        logger.error("create_user_empty_params()/POST failed")
        raise Exception("Created user with empty parameters")
    
    response = requests.post(EP + "/prod/db", json={
        "accountID": user_uuid,
        "firstName": "Test",
        "lastName": "Test",
        "hashedPassword": "",
        "email": "",
        "birthDate": "1111-11-11",
        "gender": "male"
    })
    if int(response.json()["statusCode"]) != 400:
        logger.error("create_user_empty_params()/POST failed")
        raise Exception("Created user with empty parameters")
    
    response = requests.post(EP + "/prod/db", json={
        "accountID": user_uuid,
        "firstName": "Test",
        "lastName": "Test",
        "hashedPassword": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b",
        "email": "test@test.test",
        "birthDate": "1111-11-11",
        "gender": ""
    })
    if int(response.json()["statusCode"]) != 400:
        logger.error("create_user_empty_params()/POST failed")
        raise Exception("Created user with empty parameters")
    
    logger.info("create_user_empty_params() success")


def create_user_existing_uuid():
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
        logger.error("create_user_existing_uuid()/POST failed")
        raise Exception("Cannot create new user")
    
    response = requests.post(EP + "/prod/db", json={
        "accountID": user_uuid,
        "firstName": "Test",
        "lastName": "Test",
        "hashedPassword": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b",
        "email": "test2@test.test",
        "birthDate": "1111-11-11",
        "gender": "male"
    })
    if int(response.json()["statusCode"]) != 400:
        logger.error("create_user_existing_uuid()/POST failed")
        raise Exception("Created new user with already existing uuid")
    
    response = requests.delete(EP + "/prod/db", json={
        "accountID": user_uuid
    })
    if int(response.json()["statusCode"]) != 200:
            logger.error("create_user_existing_uuid()/DELETE failed")
            raise Exception("Cannot Delete existing user")

    logger.info("create_user_existing_uuid() success")


def create_user_exisitng_email():
    user_uuid_1 = str(uuid.uuid4())
    response = requests.post(EP + "/prod/db", json={
        "accountID": user_uuid_1,
        "firstName": "Test",
        "lastName": "Test",
        "hashedPassword": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b",
        "email": "test@test.test",
        "birthDate": "1111-11-11",
        "gender": "male"
    })
    if int(response.json()["statusCode"]) != 200:
        logger.error("create_user_exisitng_email()/POST failed")
        raise Exception("Cannot create new user")
    
    user_uuid_2 = str(uuid.uuid4())
    response = requests.post(EP + "/prod/db", json={
        "accountID": user_uuid_2,
        "firstName": "Test",
        "lastName": "Test",
        "hashedPassword": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b",
        "email": "test@test.test",
        "birthDate": "1111-11-11",
        "gender": "male"
    })
    if int(response.json()["statusCode"]) != 400:
        logger.error("create_user_exisitng_email()/POST failed")
        raise Exception("Created user with existing email (GSI)")
    
    response = requests.delete(EP + "/prod/db", json={
        "accountID": user_uuid_1
    })
    if int(response.json()["statusCode"]) != 200:
            logger.error("create_user_exisitng_email()/DELETE failed")
            raise Exception("Cannot Delete existing user")

    logger.info("create_user_exisitng_email() success")



if __name__ == "__main__":
    try:
        create_read_delete()
        delete_nonexistent_user()
        create_empty_user()
        create_user_empty_params()
        create_user_existing_uuid()
        create_user_exisitng_email()
        logger.info("Passed all test!")
    except Exception as e:
        print(str(e))
