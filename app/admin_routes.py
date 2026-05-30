"""
Rotas administrativas para gerenciamento de imagens
"""

import os
import zipfile
import json
import ast
import re
from datetime import datetime
from functools import wraps
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, send_file, session, current_app
from werkzeug.utils import secure_filename
from app.upload_config import IMAGE_CATEGORIES, configure_upload_system, allowed_file, save_uploaded_file
from app.image_manager import ImageManager

# Criar blueprint para admin
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Inicializar gerenciador de imagens
image_manager = None

def init_admin(app):
    """Inicializa o sistema administrativo"""
    global image_manager
    upload_folder = configure_upload_system(app)
    image_manager = ImageManager(upload_folder)
    app.register_blueprint(admin_bp)

# Decorador para proteger rotas administrativas
def login_required(f):
    """Decorador para exigir autenticação em rotas administrativas"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Você precisa fazer login para acessar esta página.', 'warning')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login administrativo"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        # Credenciais padrão (podem ser sobrescritas via .env)
        admin_username = current_app.config.get('ADMIN_USERNAME', 'admin')
        admin_password = current_app.config.get('ADMIN_PASSWORD', 'admin123')
        
        if username == admin_username and password == admin_password:
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash('Credenciais inválidas. Tente novamente.', 'error')
            return render_template('admin/login.html')
    
    # Se já estiver logado, redirecionar para dashboard
    if session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_dashboard'))
    
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    """Fazer logout do sistema administrativo"""
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('admin.login'))

@admin_bp.route('/')
@login_required
def admin_dashboard():
    """Dashboard administrativo"""
    stats = image_manager.get_statistics()
    return render_template('admin/dashboard.html', stats=stats, categories=IMAGE_CATEGORIES)

@admin_bp.route('/upload')
@login_required
def upload_page():
    """Página de upload de imagens"""
    return render_template('admin/upload.html', categories=IMAGE_CATEGORIES)

@admin_bp.route('/upload', methods=['POST'])
@login_required
def upload_images():
    """Processa upload de imagens"""
    try:
        if 'images' not in request.files:
            flash('Nenhuma imagem selecionada.', 'error')
            return redirect(url_for('admin.upload_page'))
        
        files = request.files.getlist('images')
        category = request.form.get('category', 'uncategorized')
        
        uploaded_count = 0
        errors = []
        
        for file in files:
            if file and file.filename and allowed_file(file.filename):
                try:
                    # Salvar arquivo na pasta da categoria
                    filename = save_uploaded_file(file, category)
                    
                    if filename:
                        # Gerar título automaticamente a partir do nome do arquivo
                        name_without_ext = os.path.splitext(filename)[0]
                        title = name_without_ext.replace('_', ' ').replace('-', ' ').title()
                        description = request.form.get('description', '')
                        
                        # Adicionar ao gerenciador
                        if image_manager.add_image(filename, category, title, description):
                            uploaded_count += 1
                        else:
                            errors.append(f"Erro ao processar {filename}")
                    else:
                        errors.append(f"Arquivo inválido: {file.filename}")
                        
                except Exception as e:
                    errors.append(f"Erro ao fazer upload de {file.filename}: {str(e)}")
            elif file and file.filename:
                errors.append(f"Tipo de arquivo não permitido: {file.filename}")
        
        if uploaded_count > 0:
            flash(f'{uploaded_count} imagem(ns) enviada(s) com sucesso!', 'success')
        
        if errors:
            for error in errors:
                flash(error, 'error')
        
        return redirect(url_for('admin.upload_page'))
        
    except Exception as e:
        flash(f'Erro no upload: {str(e)}', 'error')
        return redirect(url_for('admin.upload_page'))

@admin_bp.route('/upload-zip', methods=['POST'])
@login_required
def upload_zip():
    """Processa upload de arquivo ZIP com múltiplas imagens"""
    try:
        if 'zip_file' not in request.files:
            flash('Nenhum arquivo ZIP selecionado.', 'error')
            return redirect(url_for('admin.upload_page'))
        
        zip_file = request.files['zip_file']
        if not zip_file.filename:
            flash('Nenhum arquivo selecionado.', 'error')
            return redirect(url_for('admin.upload_page'))
        
        if not zip_file.filename.lower().endswith('.zip'):
            flash('Arquivo deve ser um ZIP.', 'error')
            return redirect(url_for('admin.upload_page'))
        
        # Salvar arquivo ZIP temporariamente
        zip_filename = secure_filename(zip_file.filename)
        zip_path = os.path.join(image_manager.upload_folder, f"temp_{zip_filename}")
        zip_file.save(zip_path)
        
        # Extrair imagens
        uploaded_count = 0
        errors = []
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                if not file_info.is_dir():
                    filename = secure_filename(file_info.filename)
                    
                    # Verificar se é uma imagem
                    if any(filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
                        try:
                            # Determinar pasta de destino baseada na categoria
                            category_folders = {
                                'espetaculo': 'espetaculo',
                                'musical': 'musical', 
                                'feira': 'feira-livre',
                                'midia': 'na-midia',
                                'patrocinio': 'patrocinio',
                                'formacao': 'formacao',
                                'evento': 'evento',
                                'bastidores': 'bastidores',
                                'publico': 'publico'
                            }
                            
                            category = request.form.get('category', 'uncategorized')
                            folder_name = category_folders.get(category, '')
                            
                            if folder_name:
                                # Criar pasta da categoria se não existir
                                category_path = os.path.join(image_manager.upload_folder, folder_name)
                                os.makedirs(category_path, exist_ok=True)
                                # Extrair diretamente na pasta da categoria
                                zip_ref.extract(file_info, category_path)
                                old_path = os.path.join(category_path, file_info.filename)
                                new_path = os.path.join(category_path, filename)
                            else:
                                # Extrair na pasta raiz se categoria não mapeada
                                zip_ref.extract(file_info, image_manager.upload_folder)
                                old_path = os.path.join(image_manager.upload_folder, file_info.filename)
                                new_path = os.path.join(image_manager.upload_folder, filename)
                            
                            if old_path != new_path:
                                os.rename(old_path, new_path)
                            
                            # Verificar se é uma imagem válida
                            if allowed_file(filename):
                                # Gerar título automaticamente
                                name_without_ext = os.path.splitext(filename)[0]
                                title = name_without_ext.replace('_', ' ').replace('-', ' ').title()
                                
                                # Adicionar ao gerenciador
                                category = request.form.get('category', 'uncategorized')
                                
                                if image_manager.add_image(filename, category, title, ''):
                                    uploaded_count += 1
                                else:
                                    errors.append(f"Erro ao processar {filename}")
                            else:
                                # Remover arquivo se não for imagem válida
                                os.remove(new_path)
                                errors.append(f"Arquivo não é uma imagem válida: {filename}")
                                
                        except Exception as e:
                            errors.append(f"Erro ao extrair {file_info.filename}: {str(e)}")
        
        # Remover arquivo ZIP temporário
        os.remove(zip_path)
        
        if uploaded_count > 0:
            flash(f'{uploaded_count} imagem(ns) extraída(s) do ZIP com sucesso!', 'success')
        
        if errors:
            for error in errors:
                flash(error, 'error')
        
        return redirect(url_for('admin.upload_page'))
        
    except Exception as e:
        flash(f'Erro no upload ZIP: {str(e)}', 'error')
        return redirect(url_for('admin.upload_page'))

@admin_bp.route('/gallery')
@login_required
def manage_gallery():
    """Página de gerenciamento da galeria"""
    all_images = image_manager.get_all_images()
    stats = image_manager.get_statistics()
    
    # Função helper para gerar URL da imagem
    def get_image_url(filename):
        # Mapear categoria para pasta
        category_folders = {
            'espetaculo': 'espetaculo',
            'musical': 'musical', 
            'feira': 'feira-livre',
            'midia': 'na-midia',
            'patrocinio': 'patrocinio',
            'formacao': 'formacao',
            'evento': 'evento',
            'bastidores': 'bastidores',
            'publico': 'publico'
        }
        
        # Buscar categoria da imagem
        if filename in all_images:
            category = all_images[filename].get('category', '')
            folder = category_folders.get(category, '')
            if folder:
                return f"images/galeria/{folder}/{filename}"
        
        return f"images/galeria/{filename}"
    
    return render_template('admin/gallery.html', 
                         images=all_images, 
                         stats=stats, 
                         categories=IMAGE_CATEGORIES,
                         get_image_url=get_image_url)

@admin_bp.route('/delete-image/<filename>', methods=['POST'])
@login_required
def delete_image(filename):
    """Remove uma imagem"""
    try:
        if image_manager.delete_image(filename):
            flash(f'Imagem {filename} removida com sucesso!', 'success')
        else:
            flash(f'Erro ao remover imagem {filename}', 'error')
    except Exception as e:
        flash(f'Erro ao remover imagem: {str(e)}', 'error')
    
    return redirect(url_for('admin.manage_gallery'))

@admin_bp.route('/update-image/<filename>', methods=['POST'])
@login_required
def update_image(filename):
    """Atualiza informações de uma imagem"""
    try:
        title = request.form.get('title', '')
        description = request.form.get('description', '')
        category = request.form.get('category', '')
        
        updates = {}
        if title:
            updates['title'] = title
        if description:
            updates['description'] = description
        if category:
            updates['category'] = category
        
        if image_manager.update_image_info(filename, **updates):
            flash(f'Informações da imagem {filename} atualizadas!', 'success')
        else:
            flash(f'Erro ao atualizar imagem {filename}', 'error')
            
    except Exception as e:
        flash(f'Erro ao atualizar imagem: {str(e)}', 'error')
    
    return redirect(url_for('admin.manage_gallery'))

@admin_bp.route('/api/images')
@login_required
def api_images():
    """API para obter imagens"""
    category = request.args.get('category')
    images_data = image_manager.get_images_by_category(category)
    return jsonify(images_data)

@admin_bp.route('/api/stats')
@login_required
def api_stats():
    """API para obter estatísticas"""
    return jsonify(image_manager.get_statistics())

@admin_bp.route('/contatos')
@login_required
def listar_contatos():
    """Lista todos os contatos recebidos"""
    contatos = []
    log_file = 'contatos.log'
    
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Separar data/hora do dicionário Python
                    try:
                        # Formato esperado: "2025-10-31 14:00:00: {'nome': 'João', ...}"
                        # Encontrar o primeiro ':' que separa data/hora dos dados
                        # Padrão para data/hora: YYYY-MM-DD HH:MM:SS ou YYYY-MM-DD HH:MM ou YYYY-MM-DD HH
                        # O padrão deve capturar até o último ':' antes do dicionário
                        date_pattern = r'(\d{4}-\d{2}-\d{2}\s+\d{1,2}(?::\d{2}){0,2})\s*:'
                        match = re.match(date_pattern, line)
                        
                        if match:
                            timestamp = match.group(1)
                            # Pegar tudo após a data/hora e os dois pontos
                            data_str = line[match.end():].strip()
                            
                            # Tentar parsear como dicionário Python
                            try:
                                data = ast.literal_eval(data_str)
                            except:
                                # Tentar parsear como JSON
                                try:
                                    data = json.loads(data_str)
                                except:
                                    # Se falhar, tentar extrair informações básicas
                                    data = {'raw': data_str}
                            
                            # Garantir que data é um dicionário
                            if not isinstance(data, dict):
                                data = {'raw': str(data)}
                            
                            contato = {
                                'timestamp': timestamp,
                                'data': data
                            }
                            contatos.append(contato)
                        else:
                            # Tentar método alternativo: split no primeiro ':' após a data
                            # Formato aproximado: "YYYY-MM-DD HH:MM:SS: {...}"
                            parts = line.split(':', 2)  # Dividir em no máximo 3 partes
                            if len(parts) >= 3:
                                timestamp = f"{parts[0]}:{parts[1]}".strip()
                                data_str = parts[2].strip()
                                
                                try:
                                    data = ast.literal_eval(data_str)
                                    if not isinstance(data, dict):
                                        data = {'raw': str(data)}
                                except:
                                    try:
                                        data = json.loads(data_str)
                                        if not isinstance(data, dict):
                                            data = {'raw': str(data)}
                                    except:
                                        data = {'raw': data_str}
                                
                                contato = {
                                    'timestamp': timestamp,
                                    'data': data
                                }
                                contatos.append(contato)
                    except Exception as e:
                        # Se não conseguir parsear, adicionar linha raw
                        contatos.append({
                            'timestamp': 'Erro no parsing',
                            'data': {'raw': line, 'erro': str(e)}
                        })
        except Exception as e:
            flash(f'Erro ao ler arquivo de contatos: {str(e)}', 'error')
    
    # Ordenar por timestamp (mais recentes primeiro)
    contatos.reverse()
    
    return render_template('admin/contatos.html', contatos=contatos)

@admin_bp.route('/contatos/<int:index>')
@login_required
def ver_contato(index):
    """Visualiza detalhes de um contato específico"""
    contatos = []
    log_file = 'contatos.log'
    
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        # Padrão para data/hora
                        date_pattern = r'(\d{4}-\d{2}-\d{2}\s+\d{1,2}(?::\d{2}){0,2})\s*:'
                        match = re.match(date_pattern, line)
                        
                        if match:
                            timestamp = match.group(1)
                            data_str = line[match.end():].strip()
                            
                            try:
                                data = ast.literal_eval(data_str)
                            except:
                                try:
                                    data = json.loads(data_str)
                                except:
                                    data = {'raw': data_str}
                            
                            if not isinstance(data, dict):
                                data = {'raw': str(data)}
                            
                            contatos.append({
                                'timestamp': timestamp,
                                'data': data
                            })
                        else:
                            # Método alternativo
                            parts = line.split(':', 2)
                            if len(parts) >= 3:
                                timestamp = f"{parts[0]}:{parts[1]}".strip()
                                data_str = parts[2].strip()
                                
                                try:
                                    data = ast.literal_eval(data_str)
                                    if not isinstance(data, dict):
                                        data = {'raw': str(data)}
                                except:
                                    try:
                                        data = json.loads(data_str)
                                        if not isinstance(data, dict):
                                            data = {'raw': str(data)}
                                    except:
                                        data = {'raw': data_str}
                                
                                contatos.append({
                                    'timestamp': timestamp,
                                    'data': data
                                })
                    except Exception as e:
                        # Log do erro para debug
                        print(f"Erro ao processar linha: {line[:50]}... Erro: {e}")
                        pass
        except Exception as e:
            print(f"Erro ao ler arquivo: {e}")
            flash(f'Erro ao ler arquivo de contatos: {str(e)}', 'error')
    
    # Ordenar por timestamp (mais recentes primeiro)
    contatos.reverse()
    
    if 0 <= index < len(contatos):
        return render_template('admin/contato_detalhes.html', contato=contatos[index], index=index, total=len(contatos))
    else:
        flash('Contato não encontrado.', 'error')
        return redirect(url_for('admin.listar_contatos'))
