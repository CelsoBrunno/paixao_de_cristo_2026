#!/usr/bin/env python3
"""
Script para verificar espaço de armazenamento usado
Mostra informações sobre imagens armazenadas no banco de dados
"""

import os
import sys

# Configurar ambiente para PythonAnywhere
os.environ['PYTHONANYWHERE_DOMAIN'] = 'paixaodecristomaracanau.pythonanywhere.com'
os.environ['SECRET_KEY'] = 'hehahe11'
os.environ['DB_PASSWORD'] = 'hehahe11'

def format_bytes(bytes_size):
    """Converte bytes para formato legível"""
    if bytes_size == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while bytes_size >= 1024 and i < len(size_names) - 1:
        bytes_size /= 1024.0
        i += 1
    
    return f"{bytes_size:.2f} {size_names[i]}"

def check_database_storage():
    """Verifica espaço usado no banco de dados"""
    try:
        print("🔍 Verificando armazenamento no banco de dados...")
        
        from app.blog_manager_mysql import BlogManagerMySQL
        
        blog_manager = BlogManagerMySQL()
        
        if blog_manager.connection and blog_manager.connection.is_connected():
            cursor = blog_manager.connection.cursor()
            
            # Estatísticas gerais
            cursor.execute("SELECT COUNT(*) FROM blog_images")
            total_images = cursor.fetchone()[0]
            
            cursor.execute("SELECT SUM(file_size) FROM blog_images")
            total_size = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT AVG(file_size) FROM blog_images")
            avg_size = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT MAX(file_size) FROM blog_images")
            max_size = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT MIN(file_size) FROM blog_images")
            min_size = cursor.fetchone()[0] or 0
            
            print(f"📊 Estatísticas do Banco de Dados:")
            print(f"   - Total de imagens: {total_images}")
            print(f"   - Espaço total usado: {format_bytes(total_size)}")
            print(f"   - Tamanho médio: {format_bytes(avg_size)}")
            print(f"   - Maior arquivo: {format_bytes(max_size)}")
            print(f"   - Menor arquivo: {format_bytes(min_size)}")
            
            # Detalhes por tipo de imagem
            cursor.execute("""
                SELECT image_type, COUNT(*) as count, SUM(file_size) as total_size
                FROM blog_images 
                GROUP BY image_type
                ORDER BY total_size DESC
            """)
            
            print(f"\n📋 Detalhes por Tipo de Imagem:")
            for row in cursor.fetchall():
                image_type, count, size = row
                print(f"   - {image_type}: {count} arquivos, {format_bytes(size)}")
            
            # Top 10 maiores arquivos
            cursor.execute("""
                SELECT filename, file_size, image_type, created_at
                FROM blog_images 
                ORDER BY file_size DESC 
                LIMIT 10
            """)
            
            print(f"\n🔝 Top 10 Maiores Arquivos:")
            for i, row in enumerate(cursor.fetchall(), 1):
                filename, size, image_type, created_at = row
                print(f"   {i:2d}. {filename} - {format_bytes(size)} ({image_type})")
            
            blog_manager.close()
            return total_size, total_images
            
        else:
            print("❌ Não foi possível conectar ao banco de dados")
            return 0, 0
            
    except Exception as e:
        print(f"❌ Erro ao verificar banco de dados: {e}")
        return 0, 0

def check_file_storage():
    """Verifica espaço usado em arquivos locais"""
    try:
        print("\n🔍 Verificando armazenamento em arquivos locais...")
        
        # Verificar pasta de galeria
        gallery_path = "app/static/images/galeria"
        total_size = 0
        total_files = 0
        
        if os.path.exists(gallery_path):
            for root, dirs, files in os.walk(gallery_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.isfile(file_path):
                        file_size = os.path.getsize(file_path)
                        total_size += file_size
                        total_files += 1
            
            print(f"📁 Pasta de Galeria ({gallery_path}):")
            print(f"   - Total de arquivos: {total_files}")
            print(f"   - Espaço total usado: {format_bytes(total_size)}")
            
            # Verificar por categoria
            categories = ['espetaculo', 'musical', 'feira-livre', 'na-midia', 'patrocinio', 'formacao', 'evento', 'bastidores', 'publico']
            
            print(f"\n📂 Detalhes por Categoria:")
            for category in categories:
                category_path = os.path.join(gallery_path, category)
                if os.path.exists(category_path):
                    category_size = 0
                    category_files = 0
                    
                    for root, dirs, files in os.walk(category_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            if os.path.isfile(file_path):
                                category_size += os.path.getsize(file_path)
                                category_files += 1
                    
                    if category_files > 0:
                        print(f"   - {category}: {category_files} arquivos, {format_bytes(category_size)}")
        else:
            print(f"⚠️  Pasta de galeria não encontrada: {gallery_path}")
        
        return total_size, total_files
        
    except Exception as e:
        print(f"❌ Erro ao verificar arquivos locais: {e}")
        return 0, 0

def check_pythonanywhere_limits():
    """Verifica limites do PythonAnywhere"""
    print(f"\n📋 Limites do PythonAnywhere:")
    print(f"   - Conta gratuita: 512 MB de armazenamento")
    print(f"   - Conta paga: até 20 GB de armazenamento")
    print(f"   - Banco MySQL: até 1 GB (gratuito) ou mais (pago)")
    print(f"   - Arquivos estáticos: compartilhados com o limite da conta")

def main():
    """Função principal"""
    print("=" * 70)
    print("📊 VERIFICAÇÃO DE ESPAÇO DE ARMAZENAMENTO")
    print("   Projeto: Paixão de Cristo de Maracanaú")
    print("   PRONAC: 255599")
    print("=" * 70)
    
    # Verificar armazenamento no banco de dados
    db_size, db_files = check_database_storage()
    
    # Verificar armazenamento em arquivos
    file_size, file_files = check_file_storage()
    
    # Mostrar limites
    check_pythonanywhere_limits()
    
    # Resumo final
    total_size = db_size + file_size
    total_files = db_files + file_files
    
    print(f"\n" + "=" * 70)
    print(f"📋 RESUMO GERAL")
    print(f"=" * 70)
    print(f"🗄️  Banco de Dados: {db_files} arquivos, {format_bytes(db_size)}")
    print(f"📁 Arquivos Locais: {file_files} arquivos, {format_bytes(file_size)}")
    print(f"📊 TOTAL GERAL: {total_files} arquivos, {format_bytes(total_size)}")
    
    # Recomendações
    print(f"\n💡 RECOMENDAÇÕES:")
    
    if total_size > 100 * 1024 * 1024:  # Mais de 100MB
        print(f"   ⚠️  Você está usando mais de 100MB de armazenamento")
        print(f"   💰 Considere fazer upgrade para conta paga no PythonAnywhere")
    
    if db_size > 50 * 1024 * 1024:  # Mais de 50MB no banco
        print(f"   ⚠️  Banco de dados usando mais de 50MB")
        print(f"   🔧 Considere otimizar imagens antes do upload")
    
    if total_files > 100:
        print(f"   ⚠️  Muitos arquivos ({total_files})")
        print(f"   🗑️  Considere remover imagens antigas ou não utilizadas")
    
    print(f"\n✅ Verificação concluída!")

if __name__ == "__main__":
    main()
