"""
Configurações para upload de notícias/blog usando Flask nativo
"""

import os
from werkzeug.utils import secure_filename

# Configurações de upload
UPLOAD_FOLDER = 'app/static/images/blog'
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Categorias de notícias
BLOG_CATEGORIES = {
    'evento': 'Eventos',
    'bastidores': 'Bastidores',
    'patrocinio': 'Patrocínio',
    'midia': 'Mídia',
    'formacao': 'Formação Artística',
    'publico': 'Público',
    'geral': 'Geral'
}

def configure_blog_system(app):
    """Configura o sistema de blog"""
    # Criar diretório de upload se não existir
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # Criar subpastas por categoria
    for category in BLOG_CATEGORIES.keys():
        category_folder = os.path.join(UPLOAD_FOLDER, category)
        os.makedirs(category_folder, exist_ok=True)

def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, category=None):
    """Salva arquivo enviado na pasta da categoria"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        # Adicionar timestamp para evitar conflitos
        import time
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{int(time.time())}{ext}"
        
        # Mapear categoria para nome da pasta
        category_folders = {
            'evento': 'evento',
            'bastidores': 'bastidores',
            'patrocinio': 'patrocinio',
            'midia': 'midia',
            'formacao': 'formacao',
            'publico': 'publico',
            'geral': 'geral'
        }
        
        # Definir pasta de destino baseada na categoria
        if category and category in category_folders:
            folder_name = category_folders[category]
            upload_path = os.path.join(UPLOAD_FOLDER, folder_name)
            
            # Criar pasta se não existir
            os.makedirs(upload_path, exist_ok=True)
            
            # Caminho completo do arquivo
            filepath = os.path.join(upload_path, filename)
            
            # Salvar arquivo
            file.save(filepath)
            
            # Verificar se o arquivo foi salvo corretamente
            if os.path.exists(filepath):
                print(f"Arquivo salvo com sucesso: {filepath}")
                return filename
            else:
                print(f"Erro: Arquivo não foi salvo em {filepath}")
                return None
        else:
            # Se categoria não mapeada, salvar na pasta raiz
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            
            if os.path.exists(filepath):
                print(f"Arquivo salvo na pasta raiz: {filepath}")
                return filename
            else:
                print(f"Erro: Arquivo não foi salvo em {filepath}")
                return None
    return None
