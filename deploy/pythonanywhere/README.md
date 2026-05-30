# Deploy no PythonAnywhere

## Estrutura no servidor

```
/home/SEU_USUARIO/mysite/
├── app/
├── run.py
├── requirements.txt
└── ...
```

## Passos

1. Enviar o código para `/home/SEU_USUARIO/mysite/` (git pull ou upload).
2. Instalar dependências: `pip install -r requirements.txt`
3. Configurar variáveis de ambiente no painel **Web**:
   - `SECRET_KEY`
   - `DB_PASSWORD`
   - `PYTHONANYWHERE_DOMAIN`
4. Copiar `wsgi.example.py` para o arquivo WSGI do painel Web.
5. Executar `database_setup.sql` no banco MySQL (se ainda não existir).
6. Clicar em **Reload** no painel Web.

## Arquivos auxiliares

- `database_setup.sql` — script de criação das tabelas
- `limpar_pythonanywhere.sh` — limpeza de arquivos temporários no servidor
- `verificar_armazenamento.py` — verificação de uso de disco
