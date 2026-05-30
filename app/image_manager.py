"""
Sistema de gerenciamento de imagens para a galeria
"""

import os
import json
from datetime import datetime
from PIL import Image
import hashlib

class ImageManager:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder
        self.metadata_file = os.path.join(upload_folder, 'images_metadata.json')
        self.load_metadata()
    
    def load_metadata(self):
        """Carrega metadados das imagens"""
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {}
    
    def save_metadata(self):
        """Salva metadados das imagens"""
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)
    
    def find_image_file(self, filename):
        """Busca arquivo de imagem na pasta raiz e subpastas"""
        # Primeiro, tentar na pasta raiz
        filepath = os.path.join(self.upload_folder, filename)
        if os.path.exists(filepath):
            return filepath
        
        # Se não encontrou, buscar em subpastas
        for root, dirs, files in os.walk(self.upload_folder):
            if filename in files:
                return os.path.join(root, filename)
        
        return None
    
    def get_image_info(self, filename):
        """Obtém informações de uma imagem"""
        # Buscar arquivo na pasta raiz e subpastas
        filepath = self.find_image_file(filename)
        if not filepath:
            return None
        
        try:
            # Ler arquivo uma vez para hash e PIL
            with open(filepath, 'rb') as f:
                file_data = f.read()
                file_hash = hashlib.md5(file_data).hexdigest()
            
            # Processar imagem
            with Image.open(filepath) as img:
                width, height = img.size
                file_size = len(file_data)
                
                return {
                    'filename': filename,
                    'width': width,
                    'height': height,
                    'size': file_size,
                    'format': img.format,
                    'hash': file_hash,
                    'created': datetime.now().isoformat()
                }
        except Exception as e:
            print(f"Erro ao processar imagem {filename}: {e}")
            return None
    
    def add_image(self, filename, category, title, description=""):
        """Adiciona uma imagem ao sistema"""
        info = self.get_image_info(filename)
        if not info:
            return False
        
        # Verificar se já existe imagem com mesmo hash
        for existing_file, existing_info in self.metadata.items():
            if existing_info.get('hash') == info['hash'] and existing_file != filename:
                print(f"Imagem duplicada detectada: {filename} (mesmo hash que {existing_file})")
                return False
        
        # Adicionar metadados
        info.update({
            'category': category,
            'title': title,
            'description': description,
            'uploaded_at': datetime.now().isoformat(),
            'views': 0,
            'downloads': 0
        })
        
        self.metadata[filename] = info
        self.save_metadata()
        return True
    
    def get_images_by_category(self, category=None):
        """Obtém imagens por categoria"""
        if category:
            return {k: v for k, v in self.metadata.items() 
                   if v.get('category') == category}
        return self.metadata
    
    def get_all_images(self):
        """Obtém todas as imagens"""
        return self.metadata
    
    def delete_image(self, filename):
        """Remove uma imagem"""
        filepath = self.find_image_file(filename)
        
        # Remover arquivo físico
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
        
        # Remover dos metadados
        if filename in self.metadata:
            del self.metadata[filename]
            self.save_metadata()
            return True
        return False
    
    def update_image_info(self, filename, **kwargs):
        """Atualiza informações de uma imagem"""
        if filename in self.metadata:
            self.metadata[filename].update(kwargs)
            self.save_metadata()
            return True
        return False
    
    def increment_views(self, filename):
        """Incrementa contador de visualizações"""
        if filename in self.metadata:
            self.metadata[filename]['views'] = self.metadata[filename].get('views', 0) + 1
            self.save_metadata()
    
    def increment_downloads(self, filename):
        """Incrementa contador de downloads"""
        if filename in self.metadata:
            self.metadata[filename]['downloads'] = self.metadata[filename].get('downloads', 0) + 1
            self.save_metadata()
    
    def get_statistics(self):
        """Obtém estatísticas das imagens"""
        total_images = len(self.metadata)
        total_views = sum(img.get('views', 0) for img in self.metadata.values())
        total_downloads = sum(img.get('downloads', 0) for img in self.metadata.values())
        
        categories = {}
        for img in self.metadata.values():
            cat = img.get('category', 'uncategorized')
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            'total_images': total_images,
            'total_views': total_views,
            'total_downloads': total_downloads,
            'categories': categories
        }
