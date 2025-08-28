from datetime import datetime, timedelta, timezone
from jose import jwt
import jose
from functools import wraps
from flask import request, jsonify

SECRET_KEY = "a super secret, secret key"


def encode_token(mechanic_id): # using unique pieces of info to make our token user specific
  payload = {
    'exp': datetime.now(timezone.utc) + timedelta(days=0,hours=1), #setting the expiration time to an hour past from now
    'iat': datetime.now(timezone.utc), #Issued at
    'sub': str(mechanic_id) # this needs to be a string or the token will be malformed and won't be able to be decoded.
  }
  token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
  return token


def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs): # the function that will  run before the function we are wrapping
    token = None#Look for token in the Authorization header
    if 'Authorization' in request.headers:
      token = request.headers['Authorization'].split()[1] # Accesses the headers , then the bearer token string ,  we then split into [,Bearer', token]

    if not token:
      return jsonify({"message": "Token is missing!"}), 401
    
    try:
      #decode the token
      data= jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
      print(data)
      request.mechanic_id = int(data['sub'])

    except jose.exceptions.ExpiredSignatureError:
      return jsonify({'message': 'Token has expired!'}), 403
    except jose.exceptions.JWTError: # misscopied , fradualy created
      return jsonify({'message': 'Invalid token!'}), 403
    
    return f(*args, **kwargs)
  
  return decorated