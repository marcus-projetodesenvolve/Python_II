from flask import render_template, redirect, url_for, request, flash
from app import app, alquimias
from flask_login import current_user, login_user, logout_user, login_required

@app.route('/')
@login_required
def index():
    posts = alquimias.get_timeline()
    return render_template('index.html', title='Página Inicial', user=current_user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username'].lower()
        password = request.form['password']
        user = alquimias.validate_user_password(username, password)
        if user:
            remember_me = True if request.form.get('remember') == 'on' else False
            login_user(user, remember=remember_me)
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha incorretos.')
            return redirect(url_for('login'))
    return render_template('login.html', title='Entrar')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username'].lower()
        password = request.form['password']
        avatar_url = request.form.get('avatar_url')
        bio = request.form.get('bio')
        if alquimias.user_exists(username):
            flash('Este nome de usuário já está cadastrado.')
            return redirect(url_for('login'))
        else:
            user = alquimias.create_user(username=username, password=password, avatar_url=avatar_url, bio=bio)
            login_user(user, remember=True)
            return redirect(url_for('index'))
    return render_template('cadastro.html', title='Cadastrar-se')

@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    if request.method == 'POST':
        body = request.form.get('body')
        if body:
            alquimias.create_post(body=body, author_user=current_user)
            return redirect(url_for('index'))
    return render_template('post.html', title='Escrever Post')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))