"""
Rotas para servir imagens do blog armazenadas no MySQL
"""

from flask import Blueprint, Response, request
from app.blog_manager_mysql import BlogManagerMySQL
from app.db_config import get_db_config
import os

# Blueprint para imagens do blog
blog_images_bp = Blueprint('blog_images', __name__, url_prefix='/blog/images')

# Instância global do gerenciador
blog_manager = None

def init_blog_images(app):
    """Inicializa o sistema de imagens do blog"""
    global blog_manager
    blog_manager = BlogManagerMySQL()
    app.register_blueprint(blog_images_bp)

@blog_images_bp.route('/<int:image_id>')
def serve_image(image_id):
    """Serve uma imagem específica do banco"""
    if not blog_manager:
        return "Sistema não inicializado", 500
    
    # Obter dados da imagem
    image_data = blog_manager.get_image_data(image_id)
    
    if not image_data:
        return "Imagem não encontrada", 404
    
    # Criar resposta com dados da imagem
    response = Response(
        image_data['data'],
        mimetype=image_data['type'],
        headers={
            'Cache-Control': 'public, max-age=31536000',  # Cache por 1 ano
            'Content-Disposition': 'inline'
        }
    )
    
    return response

@blog_images_bp.route('/news/<int:news_id>')
def serve_news_images(news_id):
    """Serve todas as imagens de uma notícia"""
    if not blog_manager:
        return "Sistema não inicializado", 500
    
    # Obter dados da notícia
    news_data = blog_manager.get_news_by_id(news_id)
    
    if not news_data or not news_data['images']:
        return "Nenhuma imagem encontrada", 404
    
    # Retornar primeira imagem (pode ser expandido para múltiplas)
    image = news_data['images'][0]
    
    response = Response(
        image['data'],
        mimetype=image['type'],
        headers={
            'Cache-Control': 'public, max-age=31536000',
            'Content-Disposition': 'inline'
        }
    )
    
    return response
