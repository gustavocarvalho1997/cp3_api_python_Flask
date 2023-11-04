from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///produtos.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

produtos = {
    1: {"nome": "Produto 1", "preco": 100.00},
    2: {"nome": "Produto 2", "preco": 200.00},
    3: {"nome": "Produto 3", "preco": 300.00},
    4: {"nome": "Produto 4", "preco": 400.00},
}

# EXERCICIO 1
class HelloWorld(Resource):
    def get(self):
        return "Hello, World!"

# EXERCICIO 2
class About(Resource):
    def get(self):
        return "Feita por Gustavo Carvalho, RM552466 para o cp3 do segundo semestre de Computational Thinking Using Python."

class Contact(Resource):
    def get(self):
        return "Cel.: (11) 91234-5678 | Email: exemplo@fiap.com.br"
    
class Products(Resource):
    def get(self):
        return jsonify(produtos)

# Exercicio 3
class Data(Resource):
    def post(self):
        data = request.get_json()
        if "id" in data and "nome" in data and "preco" in data:
            return f'O produto recebido foi o de nome {data["nome"]}, cujo o preço é de R$ {data["preco"]} e seu id é : {data["id"]}'
        else:
            return "Dados incompletos"

# Exercicio 4
class User(Resource):
    def get(self, username):
        print(username)
        return f"Olá {username}, seja bem vindo(a)!"
    
# Exercicio 5
class MetodoAcessado(Resource):
    def get(self):
        return "O método acessado foi o: GET"
    def post(self):
        return "O método acessado foi o: POST"
    def put(self):
        return "O método acessado foi o: PUT"
    def delete(self):
        return "O método acessado foi o: DELETE"

# EXERCICIO 6
@app.errorhandler(404)
def not_found(error):
    return jsonify({"message": "A pagina ou recurso nao foi encontrado!"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"message": "Oooops! Erro Interno!"}), 500

# EXERCICIO 7
class Produto(db.Model):
    __tablename__ = "produtos"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nome = db.Column(db.Text, nullable=False)
    preco = db.Column(db.Float, nullable=False)

    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco

app.app_context().push()
db.create_all()

class DbProduto(Resource):
    def get(self):
        produtos = Produto.query.all()
        lista = []
        for produto in produtos:
            lista.append({"id": produto.id, "nome": produto.nome, "preco": produto.preco})
        return jsonify(lista)
    def post(self):
        data = request.get_json()
        if "nome" in data and "preco" in data:
            novo_produto = Produto(nome=data["nome"], preco=data["preco"])
            db.session.add(novo_produto)
            db.session.commit()
            return {"message": "Produto cadastrado com sucesso!"}, 201
        else:
            return {"message": "Dados incompletos"}, 400


api.add_resource(HelloWorld, "/hello")
api.add_resource(About, "/about")
api.add_resource(Contact, "/contact")
api.add_resource(Products, "/products")
api.add_resource(Data, "/data")
api.add_resource(User, "/user/<username>")
api.add_resource(MetodoAcessado, "/metodoacessado")
api.add_resource(DbProduto, "/dbprodutos")
if __name__ == "__main__":   
    app.run(port=8080, debug=True)