"""
Configurações para upload de imagens usando Flask nativo
"""

import os
from werkzeug.utils import secure_filename

# Configurações de upload
UPLOAD_FOLDER = 'app/static/images/galeria'
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Categorias de imagens
IMAGE_CATEGORIES = {
    'espetaculo': 'Espetáculo Cênico',
    'musical': 'Espetáculo Musical', 
    'feira': 'Feira Livre',
    'midia': 'Na Mídia',
    'patrocinio': 'Patrocínio',
    'formacao': 'Formação Artística',
    'evento': 'Eventos',
    'bastidores': 'Bastidores',
    'publico': 'Público'
}

def configure_upload_system(app):
    """Configura o sistema de upload"""
    # Criar diretório de upload se não existir
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # Configurar Flask
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
    
    return UPLOAD_FOLDER

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
        
        # Definir pasta de destino baseada na categoria
        if category and category in category_folders:
            folder_name = category_folders[category]
            upload_path = os.path.join(UPLOAD_FOLDER, folder_name)
            os.makedirs(upload_path, exist_ok=True)
            filepath = os.path.join(upload_path, filename)
        else:
            # Se categoria não mapeada, salvar na pasta raiz
            filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        file.save(filepath)
        return filename
    return None
