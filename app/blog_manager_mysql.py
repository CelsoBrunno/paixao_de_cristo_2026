"""
Sistema de Blog usando MySQL
Armazena imagens como BLOB e metadados em tabelas
"""

import mysql.connector
from mysql.connector import Error
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import base64
from io import BytesIO
from PIL import Image

class BlogManagerMySQL:
    def __init__(self, db_config=None):
        """Inicializa conexão com MySQL"""
        if db_config is None:
            from app.db_config import get_db_config
            db_config = get_db_config()
        
        self.db_config = db_config
        self.connection = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Conecta ao banco MySQL"""
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            if self.connection.is_connected():
                print("Conectado ao MySQL com sucesso")
        except Error as e:
            print(f"Erro ao conectar MySQL: {e}")
            self.connection = None
    
    def create_tables(self):
        """Cria tabelas necessárias"""
        if not self.connection:
            return
        
        cursor = self.connection.cursor()
        
        # Tabela de notícias
        create_news_table = """
        CREATE TABLE IF NOT EXISTS blog_news (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            author VARCHAR(100) NOT NULL,
            category VARCHAR(50) NOT NULL,
            date DATE NOT NULL,
            views INT DEFAULT 0,
            likes INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        
        # Tabela de imagens
        create_images_table = """
        CREATE TABLE IF NOT EXISTS blog_images (
            id INT AUTO_INCREMENT PRIMARY KEY,
            news_id INT NOT NULL,
            filename VARCHAR(255) NOT NULL,
            image_data LONGBLOB NOT NULL,
            image_type VARCHAR(50) NOT NULL,
            file_size INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (news_id) REFERENCES blog_news(id) ON DELETE CASCADE
        )
        """
        
        try:
            cursor.execute(create_news_table)
            cursor.execute(create_images_table)
            self.connection.commit()
            print("✅ Tabelas criadas com sucesso")
        except Error as e:
            print(f"❌ Erro ao criar tabelas: {e}")
        finally:
            cursor.close()
    
    def add_news(self, title, content, author, category, date, image_files=None):
        """Adiciona uma nova notícia"""
        if not self.connection:
            return False
        
        cursor = self.connection.cursor()
        
        try:
            # Inserir notícia
            insert_news = """
            INSERT INTO blog_news (title, content, author, category, date)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_news, (title, content, author, category, date))
            news_id = cursor.lastrowid
            
            # Inserir imagens se fornecidas
            if image_files:
                for file_data in image_files:
                    if file_data and isinstance(file_data, dict):
                        # Dados já estão preparados como dicionário
                        filename = file_data.get('filename', '')
                        image_data = file_data.get('image_data', b'')
                        image_type = file_data.get('image_type', 'image/jpeg')
                        file_size = file_data.get('file_size', 0)
                        
                        if filename and image_data:
                            # Inserir imagem
                            insert_image = """
                            INSERT INTO blog_images (news_id, filename, image_data, image_type, file_size)
                            VALUES (%s, %s, %s, %s, %s)
                            """
                            cursor.execute(insert_image, (news_id, filename, image_data, image_type, file_size))
                            print(f"Imagem salva: {filename} ({file_size} bytes)")
                    elif file_data and hasattr(file_data, 'filename'):
                        # Objeto file tradicional (compatibilidade)
                        if file_data.filename:
                            # Ler dados da imagem
                            image_data = file_data.read()
                            file_data.seek(0)  # Resetar posição do arquivo
                            
                            # Obter informações da imagem
                            filename = secure_filename(file_data.filename)
                            image_type = file_data.content_type or 'image/jpeg'
                            file_size = len(image_data)
                            
                            # Inserir imagem
                            insert_image = """
                            INSERT INTO blog_images (news_id, filename, image_data, image_type, file_size)
                            VALUES (%s, %s, %s, %s, %s)
                            """
                            cursor.execute(insert_image, (news_id, filename, image_data, image_type, file_size))
                            print(f"Imagem salva: {filename} ({file_size} bytes)")
            
            self.connection.commit()
            return True
            
        except Error as e:
            print(f"❌ Erro ao adicionar notícia: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
    
    def get_all_news(self):
        """Obtém todas as notícias com suas imagens"""
        if not self.connection:
            return {}
        
        cursor = self.connection.cursor(dictionary=True)
        
        try:
            # Buscar notícias
            query = """
            SELECT n.*, i.id as image_id, i.filename, i.image_type, i.file_size
            FROM blog_news n
            LEFT JOIN blog_images i ON n.id = i.news_id
            ORDER BY n.created_at DESC
            """
            
            cursor.execute(query)
            results = cursor.fetchall()
            
            # Organizar dados
            news_dict = {}
            for row in results:
                news_id = row['id']
                
                if news_id not in news_dict:
                    news_dict[news_id] = {
                        'id': news_id,
                        'title': row['title'],
                        'content': row['content'],
                        'author': row['author'],
                        'category': row['category'],
                        'date': row['date'].strftime('%Y-%m-%d'),
                        'views': row['views'],
                        'likes': row['likes'],
                        'created_at': row['created_at'].isoformat(),
                        'images': []
                    }
                
                # Adicionar imagem se existir
                if row['image_id']:
                    news_dict[news_id]['images'].append({
                        'id': row['image_id'],
                        'filename': row['filename'],
                        'type': row['image_type'],
                        'size': row['file_size']
                    })
            
            return news_dict
            
        except Error as e:
            print(f"❌ Erro ao buscar notícias: {e}")
            return {}
        finally:
            cursor.close()
    
    def get_news_by_id(self, news_id):
        """Obtém uma notícia específica"""
        if not self.connection:
            return None
        
        cursor = self.connection.cursor(dictionary=True)
        
        try:
            query = """
            SELECT n.*, i.id as image_id, i.filename, i.image_data, i.image_type, i.file_size
            FROM blog_news n
            LEFT JOIN blog_images i ON n.id = i.news_id
            WHERE n.id = %s
            """
            
            cursor.execute(query, (news_id,))
            results = cursor.fetchall()
            
            if not results:
                return None
            
            # Organizar dados
            news_data = None
            for row in results:
                if not news_data:
                    news_data = {
                        'id': row['id'],
                        'title': row['title'],
                        'content': row['content'],
                        'author': row['author'],
                        'category': row['category'],
                        'date': row['date'].strftime('%Y-%m-%d'),
                        'views': row['views'],
                        'likes': row['likes'],
                        'created_at': row['created_at'].isoformat(),
                        'images': []
                    }
                
                # Adicionar imagem se existir
                if row['image_id']:
                    news_data['images'].append({
                        'id': row['image_id'],
                        'filename': row['filename'],
                        'data': row['image_data'],
                        'type': row['image_type'],
                        'size': row['file_size']
                    })
            
            return news_data
            
        except Error as e:
            print(f"❌ Erro ao buscar notícia: {e}")
            return None
        finally:
            cursor.close()
    
    def get_image_data(self, image_id):
        """Obtém dados de uma imagem específica"""
        if not self.connection:
            return None
        
        cursor = self.connection.cursor()
        
        try:
            query = "SELECT image_data, image_type FROM blog_images WHERE id = %s"
            cursor.execute(query, (image_id,))
            result = cursor.fetchone()
            
            if result:
                return {
                    'data': result[0],
                    'type': result[1]
                }
            return None
            
        except Error as e:
            print(f"❌ Erro ao buscar imagem: {e}")
            return None
        finally:
            cursor.close()
    
    def update_news(self, news_id, **kwargs):
        """Atualiza uma notícia"""
        if not self.connection:
            return False
        
        cursor = self.connection.cursor()
        
        try:
            # Construir query de atualização
            fields = []
            values = []
            
            for key, value in kwargs.items():
                if key in ['title', 'content', 'author', 'category', 'date']:
                    fields.append(f"{key} = %s")
                    values.append(value)
            
            if not fields:
                return False
            
            values.append(news_id)
            query = f"UPDATE blog_news SET {', '.join(fields)} WHERE id = %s"
            
            cursor.execute(query, values)
            self.connection.commit()
            
            return cursor.rowcount > 0
            
        except Error as e:
            print(f"❌ Erro ao atualizar notícia: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
    
    def delete_news(self, news_id):
        """Remove uma notícia e suas imagens"""
        if not self.connection:
            return False
        
        cursor = self.connection.cursor()
        
        try:
            # Deletar notícia (imagens serão deletadas automaticamente por CASCADE)
            query = "DELETE FROM blog_news WHERE id = %s"
            cursor.execute(query, (news_id,))
            self.connection.commit()
            
            return cursor.rowcount > 0
            
        except Error as e:
            print(f"❌ Erro ao deletar notícia: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
    
    def get_statistics(self):
        """Obtém estatísticas do blog"""
        if not self.connection:
            return {'total_news': 0, 'categories': [], 'total_views': 0, 'total_likes': 0}
        
        cursor = self.connection.cursor()
        
        try:
            # Total de notícias
            cursor.execute("SELECT COUNT(*) FROM blog_news")
            total_news = cursor.fetchone()[0]
            
            # Categorias únicas
            cursor.execute("SELECT DISTINCT category FROM blog_news")
            categories = [row[0] for row in cursor.fetchall()]
            
            # Total de visualizações
            cursor.execute("SELECT SUM(views) FROM blog_news")
            total_views = cursor.fetchone()[0] or 0
            
            # Total de curtidas
            cursor.execute("SELECT SUM(likes) FROM blog_news")
            total_likes = cursor.fetchone()[0] or 0
            
            return {
                'total_news': total_news,
                'categories': categories,
                'total_views': total_views,
                'total_likes': total_likes
            }
            
        except Error as e:
            print(f"❌ Erro ao obter estatísticas: {e}")
            return {'total_news': 0, 'categories': [], 'total_views': 0, 'total_likes': 0}
        finally:
            cursor.close()
    
    def increment_views(self, news_id):
        """Incrementa contador de visualizações"""
        if not self.connection:
            return False
        
        cursor = self.connection.cursor()
        
        try:
            query = "UPDATE blog_news SET views = views + 1 WHERE id = %s"
            cursor.execute(query, (news_id,))
            self.connection.commit()
            return True
        except Error as e:
            print(f"❌ Erro ao incrementar visualizações: {e}")
            return False
        finally:
            cursor.close()
    
    def close(self):
        """Fecha conexão com banco"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✅ Conexão MySQL fechada")
