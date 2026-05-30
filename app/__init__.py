"""
Factory da aplicação Flask para o projeto Paixão de Cristo de Maracanaú
"""

import os
from flask import Flask, request
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

def create_app():
    """Factory function para criar a aplicação Flask"""
    app = Flask(__name__)
    
    # Configurações básicas
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['FLASK_ENV'] = os.environ.get('FLASK_ENV', 'development')
    
    # Configurações de segurança
    app.config['WTF_CSRF_ENABLED'] = os.environ.get('WTF_CSRF_ENABLED', 'True').lower() in ['true', 'on', '1']
    app.config['WTF_CSRF_TIME_LIMIT'] = int(os.environ.get('WTF_CSRF_TIME_LIMIT', 3600))
    app.config['WTF_CSRF_SSL_STRICT'] = os.environ.get('WTF_CSRF_SSL_STRICT', 'False').lower() in ['true', 'on', '1']
    
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
    app.config['PROJECT_EMAIL'] = os.environ.get('PROJECT_EMAIL', 'contato@teatroalmirdutra.com.br')
    
    # Configurações de upload
    app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_CONTENT_LENGTH', 16777216))  # 16MB
    app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images', 'blog'))
    app.config['ALLOWED_EXTENSIONS'] = os.environ.get('ALLOWED_EXTENSIONS', 'jpg,jpeg,png,gif,webp').split(',')
    
    # Inicializar CSRF Protection
    csrf = CSRFProtect()
    csrf.init_app(app)
    
    # Registra as rotas
    from app import routes
    app.register_blueprint(routes.bp)
    
    # Registra rotas administrativas
    from app import admin_routes
    admin_routes.init_admin(app)
    
    # Registra rotas administrativas do blog
    from app import blog_admin_routes
    app.register_blueprint(blog_admin_routes.blog_admin_bp)
    
    # Registra rotas de imagens do blog
    from app import blog_images_routes
    blog_images_routes.init_blog_images(app)

    # Configurações de cache e performance
    @app.after_request
    def after_request(response):
        # Cache para assets estáticos
        if request.endpoint == 'static':
            response.headers['Cache-Control'] = 'public, max-age=31536000'  # 1 ano
            # Headers específicos para imagens
            if request.path.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
        else:
            response.headers['Cache-Control'] = 'public, max-age=3600'  # 1 hora
        
        # Headers de segurança
        response.headers['X-Content-Type-Options'] = 'nosniff'
        # X-Frame-Options removido - usando apenas CSP para controle de iframes (permite Google Maps)
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Headers de segurança adicionais
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        # Content-Security-Policy atualizado para permitir Google Maps
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://www.google-analytics.com https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; img-src 'self' data: https:; connect-src 'self' https://www.google-analytics.com https://cdn.jsdelivr.net; frame-src 'self' https://www.google.com https://maps.google.com https://*.google.com;"
        response.headers['Permissions-Policy'] = "geolocation=(), microphone=(), camera=()"
        
        return response

    return app

# Cria a instância da aplicação para compatibilidade com WSGI
app = create_app()