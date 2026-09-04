from functools import wraps
from flask import request, jsonify, current_app
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'message': 'Token Malformado'})
        if not token:
            return jsonify({'message': 'Token nao encontado'})

        try:
            data  = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'token expirado'})
        except jwt.InvalidTokenError:
            return jsonify({'error': 'token invalido'})
        return f(data,*args, **kwargs)
    return decorated