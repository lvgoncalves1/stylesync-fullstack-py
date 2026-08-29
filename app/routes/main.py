from flask import Blueprint, jsonify

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def index():
    return jsonify({"message": "Bem vindo"})

# GET PRODUTOS
@main_bp.route('/products')
def get_products():
    return jsonify({"message": "Todos os Produtos"})

# POST PRODUTOS
@main_bp.route('/products', methods=['POST'])
def create_product():
    return jsonify({"message": "Postar Produtos"})

# GET UM PRODUTO
@main_bp.route('/products/<int:product_id>')
def get_product_by_id(product_id):
    return jsonify({"message": f"Um unico produto {product_id}"})

# ATUALIZA UM PRODUTO
@main_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    return jsonify({"message": f"Atualiza {product_id}"})

# DELETE UM PRODUTO
@main_bp.route('/products/<int:product_id>', methods=['PUT'])
def delete_product(product_id):
    return jsonify({"message": f"Delete {product_id}"})

# IMPORTA PARA UM ARQUIVO
@main_bp.route('/sales/upload', methods=['POST'])
def upload_dales():
    return jsonify({"message": "Upload arquivos"})

@main_bp.route('/login', methods=['POST'])
def login():
    return jsonify({"message": "Realizar Login"})

