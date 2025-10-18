"""
Factory da aplicação Flask para o projeto Paixão de Cristo de Maracanaú
"""

import os
from flask import Flask
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

def create_app():
    """Factory function para criar a aplicação Flask"""
    app = Flask(__name__)
    
    # Configurações básicas
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['FLASK_ENV'] = os.environ.get('FLASK_ENV', 'development')
    
    # Configurações de e-mail (opcional)
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() in ['true', 'on', '1']
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
    
    # Configurações do projeto
    app.config['PROJECT_NAME'] = os.environ.get('PROJECT_NAME', 'Paixão de Cristo de Maracanaú')
    app.config['PROJECT_PRONAC'] = os.environ.get('PROJECT_PRONAC', '255599')
    app.config['PROJECT_YEAR'] = os.environ.get('PROJECT_YEAR', '2026')
    app.config['PROJECT_DIRECTOR'] = os.environ.get('PROJECT_DIRECTOR', 'Celso Brunno')
    app.config['PROJECT_PHONE'] = os.environ.get('PROJECT_PHONE', '(85) 99999-9999')
    app.config['PROJECT_EMAIL'] = os.environ.get('PROJECT_EMAIL', 'contato@paixaodecristomaracana.com.br')
    
    # Registra as rotas
    from app import routes
    app.register_blueprint(routes.bp)
    
    return app

# Cria a instância da aplicação para compatibilidade com WSGI
app = create_app()