"""
Rotas da aplicação Flask para o projeto Paixão de Cristo de Maracanaú
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
import os

# Cria o blueprint
bp = Blueprint('main', __name__)

# Inicializa o Flask-Mail (opcional)
mail = Mail()

def init_mail(app):
    """Inicializa o Flask-Mail"""
    mail.init_app(app)

@bp.route('/')
def index():
    """Página inicial"""
    return render_template('index.html')

@bp.route('/sobre')
def sobre():
    """Página sobre o projeto"""
    return render_template('sobre.html')

@bp.route('/evento-2026')
def evento():
    """Página do evento 2026"""
    return render_template('evento.html')

@bp.route('/espetaculo-cenico')
def espetaculo():
    """Página do espetáculo cênico"""
    return render_template('espetaculo.html')

@bp.route('/festival-musica')
def festival():
    """Página do festival de música"""
    return render_template('festival.html')

@bp.route('/formacao-artistica')
def formacao():
    """Página da formação artística"""
    return render_template('formacao.html')

@bp.route('/feira-livre')
def feira():
    """Página da feira livre"""
    return render_template('feira.html')

@bp.route('/na-midia')
def midia():
    """Página na mídia"""
    return render_template('midia.html')

@bp.route('/seja-patrocinador')
def patrocinadores():
    """Página para patrocinadores"""
    return render_template('patrocinadores.html')

@bp.route('/contato', methods=['GET', 'POST'])
def contato():
    """Página de contato com formulário"""
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        mensagem = request.form.get('mensagem')
        
        # Validação básica
        if not nome or not email or not mensagem:
            flash('Por favor, preencha todos os campos obrigatórios.', 'error')
            return render_template('contato.html')
        
        # Aqui você pode adicionar lógica para enviar e-mail
        # Por enquanto, apenas simula o envio
        flash('Mensagem enviada com sucesso! Entraremos em contato em breve.', 'success')
        return redirect(url_for('main.contato'))
    
    return render_template('contato.html')

# Função para inicializar o blueprint
def init_app(app):
    """Inicializa o blueprint na aplicação"""
    app.register_blueprint(bp)
    init_mail(app)
