from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# Lista para armazenar os usuários
usuarios = []

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Obter dados do usuário do formulário
        nome = request.form['nome']
        email = request.form['email']
        novo_usuario = {"nome": nome, "email": email}
        # Adicionar o novo usuário à lista
        usuarios.append(novo_usuario)
        return jsonify({"mensagem": "Usuario cadastrado com sucesso!"}), 201
    return render_template_string('''
        <h1>Cadastro de Usuários</h1>
        <form method="post">
            Nome: <input type="text" name="nome">
            Email: <input type="text" name="email">
            <input type="submit" value="Cadastrar">
        </form>
    ''')

@app.route('/status')
def status():
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
