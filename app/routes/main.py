from flask import Blueprint, jsonify, request, current_app
from app.models.user import LoginPayLoad
from pydantic import ValidationError
from app import db
from bson import ObjectId
from app.models.products import *
from app.decorators import token_required
from datetime import datetime, timedelta, timezone
import jwt

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def index():
    return jsonify({"message": "Bem vindo"})

# GET PRODUTOS
@main_bp.route('/products')
def get_products():
    products_cursor = db.products.find({})
    products_list = [ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True) for product in products_cursor]
    return jsonify(products_list)

# POST PRODUTOS
@main_bp.route('/products', methods=['POST'])
@token_required
def create_product(token):
    try:
        product = Product(**request.get_json())
    except ValidationError as e:
        return jsonify({"message": f"Error na rota {e.errors()}"})

    result = db.products.insert_one(product.model_dump())
    return jsonify({"message": "Criado com sucesso",
                    'id': str(result.inserted_id)}), 201

# GET UM PRODUTO
@main_bp.route('/products/<string:product_id>')
def get_product_by_id(product_id):
    try:
        oid = ObjectId(product_id)
    except Exception as e:
        return jsonify({"message": f"Erro ao buscar {product_id}: {e}"})

    product = db.products.find_one({'_id':oid})
    if product:
        product_model = ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True)
        return jsonify(product_model)
    else:
        return jsonify({"message": f"Produto nao encontrado"})

# ATUALIZA UM PRODUTO
@main_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    return jsonify({"message": f"Atualiza {product_id}"})

# DELETE UM PRODUTO
@main_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    return jsonify({"message": f"Delete {product_id}"})

# IMPORTA PARA UM ARQUIVO
@main_bp.route('/sales/upload', methods=['POST'])
def upload_dales():
    return jsonify({"message": "Upload arquivos"})

@main_bp.route('/login', methods=['POST'])
def login():
    try:
        raw_data = request.get_json()
        user_data = LoginPayLoad(**raw_data)
    except ValidationError as e:
        return jsonify({"message": f"error:{e.errors}"}), 400
    except Exception as e:
        return jsonify({"message": {e}}), 500

    if user_data.username == 'admin' and user_data.password == '123':
        token = jwt.encode(
            {
                "user_id": user_data.username,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        return jsonify({'access token': token}), 200
    return jsonify({"message": "Credenciais invalidas"}), 401

