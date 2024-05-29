import httpx
from httpx import Response
from fastapi import Request
from functools import wraps
from jose import jwt
import fastapi

class AuthError(Exception):
    def __init__(self, error_msg:str, status_code:int):
        super().__init__(error_msg)

        self.error_msg = error_msg
        self.status_code = status_code

def initialize_auth(
    tenant_id_, 
    client_id_):
    global tenant_id, client_id
    tenant_id = tenant_id_
    client_id = client_id_

def get_token_auth_header(request: Request):
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError("Authentication error: Authorization header is missing", 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError("Authentication error: Authorization header must start with ' Bearer'", 401)
    elif len(parts) == 1:
        raise AuthError("Authentication error: Token not found", 401)
    elif len(parts) > 2:
        raise AuthError("Authentication error: Authorization header must be 'Bearer <token>'", 401)

    token = parts[1]
    return token

def requires_auth(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        try:
            token = get_token_auth_header(kwargs["request"])
            url = f'https://login.microsoftonline.com/{tenant_id}/discovery/v2.0/keys'
            
            async with httpx.AsyncClient() as client:
                resp: Response = await client.get(url)
                if resp.status_code != 200:
                    raise AuthError("Problem with Azure AD discovery URL", status_code=404)

                jwks = resp.json()
                unverified_header = jwt.get_unverified_header(token)
                rsa_key = {}
                for key in jwks["keys"]:
                    if key["kid"] == unverified_header["kid"]:
                        rsa_key = {
                            "kty": key["kty"],
                            "kid": key["kid"],
                            "use": key["use"],
                            "n": key["n"],
                            "e": key["e"]
                        }
        except Exception:
            return fastapi.Response(content="Invalid_header: Unable to parse authentication", status_code= 401)
        if rsa_key:
            try :
                token_version = __get_token_version(token)
                __decode_JWT(token_version, token, rsa_key)
                return await f(*args, **kwargs)
            except AuthError as auth_err:
                fastapi.Response(content=auth_err.error_msg, status_code=auth_err.status_code)
        return fastapi.Response(content="Invalid header error: Unable to find appropriate key", status_code=401)
    return decorated

def __decode_JWT(token_version, token, rsa_key):
    if token_version == "1.0":
        _issuer = f'https://sts.windows.net/{tenant_id}/'
        _audience=f'api://{client_id}'
    else:
        _issuer = f'https://login.microsoftonline.com/{tenant_id}/v2.0'
        _audience=f'{client_id}'
    try:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=_audience,
            issuer=_issuer
        )
    except jwt.ExpiredSignatureError:
        raise AuthError("Token error: The token has expired", 401)
    except jwt.JWTClaimsError:
        raise AuthError("Token error: Please check the audience and issuer", 401)
    except Exception:
        raise AuthError("Token error: Unable to parse authentication", 401)


def __get_token_version(token):
    unverified_claims = jwt.get_unverified_claims(token)
    if unverified_claims.get("ver"):
        return unverified_claims["ver"]   
    else:
        raise AuthError("Missing version claim from token. Unable to validate", 403)