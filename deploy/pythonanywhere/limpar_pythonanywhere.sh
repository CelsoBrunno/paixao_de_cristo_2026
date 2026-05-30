#!/bin/bash
"""
Script de limpeza do PythonAnywhere
Remove arquivos desnecessários para liberar espaço
"""

echo "=========================================="
echo "🧹 LIMPEZA DO PYTHONANYWHERE"
echo "   Projeto: Paixão de Cristo de Maracanaú"
echo "   PRONAC: 255599"
echo "=========================================="

# Função para mostrar espaço antes e depois
show_space() {
    echo "📊 Espaço atual:"
    du -hs /home/paixaodecristomaracanau/.cache /home/paixaodecristomaracanau/.local /tmp 2>/dev/null || echo "Erro ao verificar espaço"
    echo ""
}

# Mostrar espaço inicial
echo "🔍 Verificando espaço inicial..."
show_space

# 1. Limpar cache do pip
echo "🧹 Limpando cache do pip..."
pip cache purge 2>/dev/null && echo "✅ Cache do pip limpo" || echo "⚠️  Pip não encontrado"

# 2. Limpar cache geral
echo "🧹 Limpando cache geral..."
rm -rf ~/.cache/* 2>/dev/null && echo "✅ Cache geral limpo" || echo "⚠️  Erro ao limpar cache"

# 3. Limpar arquivos temporários antigos
echo "🧹 Limpando arquivos temporários antigos..."
find /tmp -type f -mtime +1 -delete 2>/dev/null && echo "✅ Arquivos temporários antigos removidos" || echo "⚠️  Erro ao limpar /tmp"

# 4. Limpar logs antigos
echo "🧹 Limpando logs antigos..."
find ~/.local -name "*.log" -mtime +7 -delete 2>/dev/null && echo "✅ Logs antigos removidos" || echo "⚠️  Nenhum log antigo encontrado"

# 5. Limpar arquivos Python compilados desnecessários
echo "🧹 Limpando arquivos Python compilados..."
find ~ -name "*.pyc" -delete 2>/dev/null && echo "✅ Arquivos .pyc removidos" || echo "⚠️  Nenhum arquivo .pyc encontrado"
find ~ -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null && echo "✅ Diretórios __pycache__ removidos" || echo "⚠️  Nenhum __pycache__ encontrado"

# Mostrar espaço final
echo ""
echo "🔍 Verificando espaço após limpeza..."
show_space

# Calcular economia
echo "=========================================="
echo "📋 RESUMO DA LIMPEZA"
echo "=========================================="
echo "✅ Cache do pip: Limpo"
echo "✅ Cache geral: Limpo"
echo "✅ Arquivos temporários: Limpos"
echo "✅ Logs antigos: Removidos"
echo "✅ Arquivos Python compilados: Removidos"
echo ""
echo "💡 RECOMENDAÇÕES:"
echo "   - Execute este script semanalmente"
echo "   - Monitore o espaço regularmente"
echo "   - Considere upgrade para conta paga se necessário"
echo ""
echo "🎉 Limpeza concluída!"
