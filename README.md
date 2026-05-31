# Paixão de Cristo de Maracanaú - Website Institucional

Website institucional para o projeto "Paixão de Cristo de Maracanaú" (PRONAC 262433), desenvolvido com Python Flask seguindo as melhores práticas de desenvolvimento web, acessibilidade e conformidade com a Lei de Incentivo à Cultura.

## 📋 Sobre o Projeto

Este website foi desenvolvido para apresentar o projeto cultural "Paixão de Cristo de Maracanaú", um evento de 47 anos de tradição que atrai mais de 30.000 pessoas anualmente. O site serve como canal oficial de comunicação e divulgação, além de ser uma ferramenta para captação de patrocinadores através da Lei de Incentivo à Cultura.

### Características Principais

- ✅ **Responsivo**: Adaptável para dispositivos móveis e desktop
- ✅ **Acessível**: Conforme WCAG 2.1 (Nível AA)
- ✅ **SEO Otimizado**: Meta tags, Open Graph, Schema.org, sitemap e RSS
- ✅ **Blog e Galeria**: Conteúdo dinâmico com painel administrativo
- ✅ **Conforme Lei Rouanet**: Logomarcas oficiais e informações obrigatórias
- ✅ **Seguro**: CSRF, rate limiting e validação de formulários
- ✅ **Profissional**: Design moderno e interface intuitiva

## 🚀 Tecnologias Utilizadas

- **Backend**: Python 3.9+ / Flask 2.3.3
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Framework CSS**: Bootstrap 5
- **Ícones**: Font Awesome 6
- **Fontes**: Google Fonts (Playfair Display + Open Sans)
- **Templates**: Jinja2

## 📁 Estrutura do Projeto

```
site/
├── app/
│   ├── __init__.py              # Factory Flask + CSRF + blueprints
│   ├── routes.py                # Rotas públicas
│   ├── admin_routes.py          # Painel administrativo
│   ├── blog_*.py                # Blog (MySQL)
│   ├── db_config.py             # Configuração do banco
│   ├── image_manager.py         # Galeria de imagens
│   ├── pdf_generator.py         # PDF de patrocínio
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── templates/
│       ├── base.html
│       ├── index.html, blog.html, faq.html, galeria.html, ...
│       ├── components/          # Navbar, breadcrumbs, etc.
│       └── admin/               # Telas do painel
├── deploy/
│   └── pythonanywhere/          # WSGI, SQL e scripts de deploy
├── docs/                        # Documentação do projeto
├── run.py                       # Entrada local (dev)
├── requirements.txt
├── env.example
└── README.md
```

## 🛠️ Instalação e Configuração

### Pré-requisitos

- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)
- Git (para clonar o repositório)

### Passo a Passo

1. **Clone o repositório**
   ```bash
   git clone <url-do-repositorio>
   cd paixao_de_cristo_site
   ```

2. **Crie um ambiente virtual**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**
   ```bash
   # Crie um arquivo .env na raiz do projeto
   echo "FLASK_APP=run.py" > .env
   echo "FLASK_ENV=development" >> .env
   echo "SECRET_KEY=sua-chave-secreta-aqui" >> .env
   ```

5. **Execute a aplicação**
   ```bash
   python run.py
   ```

6. **Acesse o site**
   - Abra seu navegador e acesse: `http://localhost:5000`

## 📱 Páginas do Site

### 1. **Página Inicial** (`/`)
- Hero section com destaque principal
- Informações rápidas (46 anos, 30.000 pessoas, PRONAC)
- Preview do evento 2026
- Call-to-action para patrocínio

### 2. **Sobre o Projeto** (`/sobre`)
- História do projeto (desde 1987)
- Reconhecimento público (Lei Municipal)
- Crescimento do público (gráficos)

### 3. **Evento 2026** (`/evento-2026`)
- Detalhes do evento (2 e 3 de abril)
- Planta 3D do evento
- Programação completa

### 4. **Atividades**
- **Espetáculo Cênico** (`/espetaculo-cenico`)
- **Festival de Música** (`/festival-musica`)
- **Formação Artística** (`/formacao-artistica`)
- **Feira Livre** (`/feira-livre`)

### 5. **Na Mídia** (`/na-midia`)
- Galeria de matérias
- Logos dos veículos parceiros
- Estatísticas de cobertura

### 6. **Seja um Patrocinador** (`/seja-patrocinador`)
- Benefícios da Lei de Incentivo à Cultura
- Oportunidades de ativação de marca
- Níveis de patrocínio

### 7. **Contato** (`/contato`)
- Formulário de contato
- Informações do diretor
- Áreas de atuação

## 🎨 Personalização

### Imagens
Substitua as imagens placeholder na pasta `app/static/images/`:

- `hero-background.jpg` - Imagem de fundo da página inicial
- `evento-2026-preview.jpg` - Preview do evento
- `planta-3d-evento.jpg` - Planta 3D do evento
- E outras imagens conforme necessário

### Cores
As cores principais estão definidas nas variáveis CSS no arquivo `style.css`:

```css
:root {
    --primary-color: #007bff;
    --secondary-color: #6c757d;
    --success-color: #28a745;
    --warning-color: #ffc107;
    /* ... */
}
```

### Conteúdo
Edite os templates HTML para personalizar textos, informações de contato e dados do projeto.

## 🔒 Conformidade Legal (Lei Rouanet)

O site inclui todos os elementos obrigatórios:

- ✅ Logomarcas oficiais no rodapé
- ✅ Informação do PRONAC (255599)
- ✅ Texto da Lei de Incentivo à Cultura
- ✅ Conformidade com Instrução Normativa MINC nº 23/2025

## ♿ Acessibilidade

O site foi desenvolvido seguindo as diretrizes WCAG 2.1:

- ✅ Navegação por teclado
- ✅ Textos alternativos em imagens
- ✅ Contraste adequado de cores
- ✅ Estrutura semântica HTML5
- ✅ Skip links para navegação
- ✅ ARIA labels apropriados

## 🚀 Deploy em Produção

### Opção 1: Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

### Opção 2: Waitress (Windows)
```bash
waitress-serve --host=0.0.0.0 --port=8000 run:app
```

### Configurações de Produção
- Configure `FLASK_ENV=production`
- Use uma chave secreta forte
- Configure proxy reverso (Nginx/Apache)
- Use HTTPS com certificado SSL

## 📊 Monitoramento e Analytics

Para adicionar Google Analytics ou outras ferramentas:

1. Adicione o código de tracking no `base.html`
2. Configure eventos personalizados no `main.js`
3. Monitore métricas de acessibilidade

## 🐛 Troubleshooting

### Problemas Comuns

**Erro de importação:**
```bash
# Certifique-se de que o ambiente virtual está ativado
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

**Porta já em uso:**
```bash
# Use uma porta diferente
python run.py --port 5001
```

**Imagens não carregam:**
- Verifique se as imagens estão na pasta `app/static/images/`
- Confirme os caminhos nos templates

## 📞 Suporte

Para dúvidas sobre o projeto:

- **Diretor Geral**: Celso Brunno
- **Telefone**: (85) 99999-9999
- **E-mail**: contato@paixaodecristomaracana.com.br

## 📄 Licença

Este projeto foi desenvolvido para o projeto cultural "Paixão de Cristo de Maracanaú" (PRONAC 255599) e está em conformidade com a Lei de Incentivo à Cultura.

---

**Desenvolvido com ❤️ para promover a cultura e arte de Maracanaú**


