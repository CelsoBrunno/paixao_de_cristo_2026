#!/usr/bin/env python3
"""
Exemplo de WSGI para PythonAnywhere.

No painel Web do PythonAnywhere, copie este conteúdo para:
  /var/www/SEU_USUARIO_pythonanywhere_com_wsgi.py

Configure SECRET_KEY e DB_PASSWORD nas variáveis de ambiente
do PythonAnywhere (Web > Environment variables), não no código.
"""

import os
import sys

path = '/home/SEU_USUARIO/mysite'
if path not in sys.path:
    sys.path.append(path)

os.chdir(path)

os.environ.setdefault('PYTHONANYWHERE_DOMAIN', 'SEU_DOMINIO.pythonanywhere.com')
os.environ.setdefault('FLASK_ENV', 'production')

from app import create_app

application = create_app()
