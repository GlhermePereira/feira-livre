from flask import Flask, render_template, request, redirect, flash
import re
import os

app = Flask(__name__)
app.secret_key = 'chave_secreta_para_flash_messages'

@app.route('/')
def index():
    return render_template('formulario.html')  # HTML com o formulário

@app.route('/cadastro', methods=['POST'])
def cadastro():
    tipo = request.form.get('tipo')

    if tipo == 'feirante':
        return validar_feirante()
    elif tipo == 'usuario':
        return validar_usuario()
    else:
        flash('Tipo de cadastro inválido.')
        return redirect('/')

def validar_feirante():
    licenca = request.files.get('licenca')
    tipo_cadastro = request.form.get('tipoCadastro')
    numero = request.form.get('numeroTipo')

    if not licenca or licenca.filename == '':
        flash('Por favor, envie a foto da licença.')
        return redirect('/')

    if not tipo_cadastro or not numero.strip():
        flash('Selecione um tipo de cadastro e informe o número.')
        return redirect('/')

    # Aqui você poderia salvar os dados no banco ou processar como quiser
    flash('Cadastro de feirante realizado com sucesso!')
    return redirect('/')

def validar_usuario():
    email = request.form.get('emailUsuario')
    senha = request.form.get('senhaUsuario')

    email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'

    if not re.match(email_regex, email):
        flash('Informe um e-mail válido.')
        return redirect('/')

    if len(senha) < 6:
        flash('A senha deve conter no mínimo 6 caracteres.')
        return redirect('/')

    flash('Cadastro de usuário realizado com sucesso!')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
