from fastapi import FastAPI, HTTPException, status, Depends
from keycloak import KeycloakOpenID


app = FastAPI()


# Configure client
keycloak_openid = KeycloakOpenID(
    server_url="http://localhost:8080/",
    client_id="myclient",
    realm_name="first-practice-realm",
    client_secret_key="fL6eyx0GfFIU9hWXnoPslTTqEEw9UH6H",
)

# Get WellKnow
config_well_known = keycloak_openid.well_known()

# Get Token
def get_current_user(token):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        userinfo = keycloak_openid.userinfo(token)
    except:
        raise credentials_exception
    return userinfo


@app.get("/hello")
def hello(token: str = Depends(get_current_user)):
    return "Hello User"
