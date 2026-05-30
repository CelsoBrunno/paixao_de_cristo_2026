"""
Rotas administrativas para gerenciamento do blog
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os
import zipfile
from app.blog_manager_mysql import BlogManagerMySQL
from app.blog_config import BLOG_CATEGORIES, allowed_file, save_uploaded_file

# Blueprint para rotas administrativas do blog
blog_admin_bp = Blueprint('blog_admin', __name__, url_prefix='/admin/blog')

# Gerenciador de blog será inicializado quando necessário
blog_manager = None

def get_blog_manager():
    """Obtém instância do gerenciador de blog"""
    global blog_manager
    if blog_manager is None:
        blog_manager = BlogManagerMySQL()
    return blog_manager

def init_blog_admin():
    """Inicializa o sistema administrativo do blog"""
    pass

@blog_admin_bp.route('/')
def dashboard():
    """Dashboard do blog"""
    try:
        manager = get_blog_manager()
        stats = manager.get_statistics()
        return render_template('admin/blog_dashboard.html', stats=stats)
    except Exception as e:
        print(f"Erro no dashboard: {e}")
        return render_template('admin/blog_dashboard.html', stats={'total_news': 0, 'categories': [], 'total_views': 0, 'total_likes': 0})

@blog_admin_bp.route('/upload')
def upload_page():
    """Página de upload de notícias"""
    return render_template('admin/blog_upload.html', categories=BLOG_CATEGORIES)

@blog_admin_bp.route('/upload', methods=['POST'])
def upload_news():
    """Upload de notícias"""
    try:
        # Obter dados do formulário
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        author = request.form.get('author', '').strip()
        category = request.form.get('category', 'geral')
        date = request.form.get('date', '')
        
        # Validar dados obrigatórios
        if not title or not content or not author:
            flash('Título, conteúdo e autor são obrigatórios!', 'error')
            return redirect(url_for('blog_admin.upload_page'))
        
        # Processar upload de imagem para MySQL
        uploaded_files = []
        if 'images' in request.files:
            files = request.files.getlist('images')
            
            for file in files:
                if file and file.filename and allowed_file(file.filename):
                    # Para MySQL, ler os dados da imagem diretamente
                    file_data = file.read()
                    filename = secure_filename(file.filename)
                    image_type = file.mimetype
                    file_size = len(file_data)
                    
                    # Criar dicionário com dados da imagem para MySQL
                    image_data = {
                        'filename': filename,
                        'image_data': file_data,
                        'image_type': image_type,
                        'file_size': file_size
                    }
                    uploaded_files.append(image_data)
        
        # Se não há imagem, usar imagem padrão (apenas para desenvolvimento local)
        if not uploaded_files:
            try:
                # Criar uma imagem padrão simples em memória
                from PIL import Image
                import io
                
                # Criar uma imagem padrão 300x200 com texto
                img = Image.new('RGB', (300, 200), color='lightgray')
                
                # Converter para bytes
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='JPEG')
                img_byte_arr = img_byte_arr.getvalue()
                
                # Criar dados da imagem padrão
                default_image = {
                    'filename': 'default-news.jpg',
                    'image_data': img_byte_arr,
                    'image_type': 'image/jpeg',
                    'file_size': len(img_byte_arr)
                }
                uploaded_files.append(default_image)
                
            except Exception as e:
                print(f"Erro ao criar imagem padrão: {e}")
                # Fallback: criar dados mínimos
                uploaded_files.append({
                    'filename': 'default-news.jpg',
                    'image_data': b'',
                    'image_type': 'image/jpeg',
                    'file_size': 0
                })
        
        # Adicionar notícia ao gerenciador
        try:
            manager = get_blog_manager()
            if manager.add_news(title, content, author, category, date, uploaded_files):
                flash('Notícia adicionada com sucesso!', 'success')
            else:
                flash('Erro ao adicionar notícia!', 'error')
        except Exception as e:
            print(f"Erro ao adicionar notícia: {e}")
            flash('Erro ao adicionar notícia!', 'error')
            
    except Exception as e:
        flash(f'Erro no upload: {str(e)}', 'error')
    
    return redirect(url_for('blog_admin.upload_page'))

@blog_admin_bp.route('/manage')
def manage_news():
    """Página de gerenciamento de notícias"""
    try:
        manager = get_blog_manager()
        all_news = manager.get_all_news()
        stats = manager.get_statistics()
        
        # Função helper para gerar URL da imagem
        def get_image_url(filename):
            # Mapear categoria para pasta
            category_folders = {
                'evento': 'evento',
                'bastidores': 'bastidores',
                'patrocinio': 'patrocinio',
                'midia': 'midia',
                'formacao': 'formacao',
                'publico': 'publico',
                'geral': 'geral'
            }
            
            # Buscar categoria da notícia
            if filename in all_news:
                category = all_news[filename].get('category', '')
                folder = category_folders.get(category, '')
                if folder:
                    return f"images/blog/{folder}/{filename}"
            
            return f"images/blog/{filename}"
    
        return render_template('admin/blog_manage.html', 
                             news=all_news, 
                             stats=stats, 
                             categories=BLOG_CATEGORIES,
                             get_image_url=get_image_url)
    except Exception as e:
        print(f"Erro ao gerenciar notícias: {e}")
        return render_template('admin/blog_manage.html', news={}, stats={'total_news': 0, 'categories': [], 'total_views': 0, 'total_likes': 0}, categories=BLOG_CATEGORIES, get_image_url=lambda x, y=0: None)

@blog_admin_bp.route('/delete/<filename>', methods=['POST'])
def delete_news(filename):
    """Remove uma notícia"""
    try:
        if blog_manager.delete_news(filename):
            flash('Notícia removida com sucesso!', 'success')
        else:
            flash('Erro ao remover notícia!', 'error')
    except Exception as e:
        flash(f'Erro: {str(e)}', 'error')
    
    return redirect(url_for('blog_admin.manage_news'))

@blog_admin_bp.route('/edit/<filename>')
def edit_news(filename):
    """Página de edição de notícia"""
    all_news = blog_manager.get_all_news()
    if filename not in all_news:
        flash('Notícia não encontrada!', 'error')
        return redirect(url_for('blog_admin.manage_news'))
    
    news_data = all_news[filename]
    return render_template('admin/blog_edit.html', 
                         filename=filename, 
                         news=news_data, 
                         categories=BLOG_CATEGORIES)

@blog_admin_bp.route('/update/<filename>', methods=['POST'])
def update_news(filename):
    """Atualiza uma notícia"""
    try:
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        author = request.form.get('author', '').strip()
        category = request.form.get('category', 'geral')
        date = request.form.get('date', '')
        
        if not title or not content or not author:
            flash('Título, conteúdo e autor são obrigatórios!', 'error')
            return redirect(url_for('blog_admin.edit_news', filename=filename))
        
        if blog_manager.update_news(filename, 
                                  title=title, 
                                  content=content, 
                                  author=author, 
                                  category=category, 
                                  date=date):
            flash('Notícia atualizada com sucesso!', 'success')
        else:
            flash('Erro ao atualizar notícia!', 'error')
            
    except Exception as e:
        flash(f'Erro: {str(e)}', 'error')
    
    return redirect(url_for('blog_admin.manage_news'))

@blog_admin_bp.route('/api/news')
def api_news():
    """API para obter dados das notícias"""
    filename = request.args.get('filename')
    if filename:
        all_news = blog_manager.get_all_news()
        if filename in all_news:
            return jsonify({filename: all_news[filename]})
        return jsonify({}), 404
    
    return jsonify(blog_manager.get_all_news())
