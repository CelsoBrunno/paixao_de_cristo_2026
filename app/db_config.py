"""
Configuração do banco MySQL para PythonAnywhere
"""

import os

# Configuração do banco MySQL do PythonAnywhere
DB_CONFIG = {
    'host': 'paixaodecristomaracanau.mysql.pythonanywhere-services.com',
    'user': 'paixaodecristoma',
    'password': os.environ.get('DB_PASSWORD', ''),  # Definir no PythonAnywhere
    'database': 'paixaodecristoma$paixao_cristo_db',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'port': 3306,
    'autocommit': True
}

# Configuração para desenvolvimento local (opcional)
DB_CONFIG_LOCAL = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'paixao_cristo',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}

def get_db_config():
    """Retorna configuração do banco baseada no ambiente"""
    if os.environ.get('PYTHONANYWHERE_DOMAIN'):
        # Estamos no PythonAnywhere
        return DB_CONFIG
    else:
        # Desenvolvimento local
        return DB_CONFIG_LOCAL
