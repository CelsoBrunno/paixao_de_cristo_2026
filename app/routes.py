"""
Rotas da aplicação Flask para o projeto Paixão de Cristo de Maracanaú
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response, current_app
import os
import re
from datetime import datetime, timedelta
import json
from xml.etree.ElementTree import Element, SubElement, tostring

# Tentar importar Flask-Mail (opcional)
try:
    from flask_mail import Mail, Message
    MAIL_AVAILABLE = True
except ImportError:
    MAIL_AVAILABLE = False
    print("Flask-Mail não disponível - funcionalidade de email desabilitada")

# Cria o blueprint
bp = Blueprint('main', __name__)

# Inicializa o Flask-Mail (opcional)
if MAIL_AVAILABLE:
    mail = Mail()
else:
    mail = None

# Rate limiting simples
RATE_LIMIT_FILE = 'rate_limit.json'
MAX_REQUESTS_PER_HOUR = 5

def init_mail(app):
    """Inicializa o Flask-Mail"""
    if MAIL_AVAILABLE and mail:
        mail.init_app(app)

def check_rate_limit(ip_address):
    """Verifica se o IP não excedeu o limite de requisições"""
    try:
        if os.path.exists(RATE_LIMIT_FILE):
            with open(RATE_LIMIT_FILE, 'r') as f:
                rate_data = json.load(f)
        else:
            rate_data = {}
        
        now = datetime.now()
        hour_key = now.strftime('%Y-%m-%d-%H')
        
        # Limpar dados antigos (mais de 24 horas)
        for key in list(rate_data.keys()):
            if key < (now - timedelta(hours=24)).strftime('%Y-%m-%d-%H'):
                del rate_data[key]
        
        # Verificar limite para este IP nesta hora
        ip_hour_key = f"{ip_address}_{hour_key}"
        if ip_hour_key in rate_data:
            if rate_data[ip_hour_key] >= MAX_REQUESTS_PER_HOUR:
                return False
            rate_data[ip_hour_key] += 1
        else:
            rate_data[ip_hour_key] = 1
        
        # Salvar dados atualizados
        with open(RATE_LIMIT_FILE, 'w') as f:
            json.dump(rate_data, f)
        
        return True
        
    except Exception as e:
        print(f"Erro no rate limiting: {e}")
        return True  # Em caso de erro, permitir a requisição

@bp.route('/')
def index():
    """Página inicial"""
    return render_template('index.html')

@bp.route('/sobre')
def sobre():
    """Página sobre o projeto"""
    return render_template('sobre.html')

@bp.route('/edicao-2026')
def edicao_2026():
    """Página retrospectiva da edição 2026"""
    from app.edicao_2026_data import PATROCINADORES_EDICAO_2026
    return render_template(
        'edicao_2026.html',
        patrocinadores=PATROCINADORES_EDICAO_2026,
    )

@bp.route('/evento-2026')
def evento_2026_redirect():
    """Redireciona URL antiga para a página da edição 2026"""
    return redirect(url_for('main.edicao_2026'), code=301)

@bp.route('/evento-2027')
def evento():
    """Página do evento 2027"""
    return render_template('evento.html')

@bp.route('/espetaculo-cenico')
def espetaculo():
    """Página do espetáculo cênico"""
    return render_template('espetaculo.html')

@bp.route('/festival-musica')
def festival():
    """Página do festival de música"""
    return render_template('festival.html')

@bp.route('/formacao-artistica')
def formacao():
    """Página da formação artística"""
    return render_template('formacao.html')

@bp.route('/feira-livre')
def feira():
    """Página da feira livre"""
    return render_template('feira.html')

@bp.route('/na-midia')
def midia():
    """Página na mídia"""
    return render_template('midia.html')

@bp.route('/seja-patrocinador')
def patrocinadores():
    """Página para patrocinadores"""
    return render_template('patrocinadores.html')

@bp.route('/seja-patrocinador/folheto')
def patrocinadores_folheto():
    """Página de folheto em formato impressão para patrocinadores"""
    return render_template('patrocinadores_folheto.html')

@bp.route('/faq')
def faq():
    """Página de perguntas frequentes"""
    return render_template('faq.html')

@bp.route('/newsletter/subscribe', methods=['POST'])
def newsletter_subscribe():
    """Processa inscrição na newsletter"""
    nome = request.form.get('nome', '').strip()
    email = request.form.get('email', '').strip()
    
    if not nome or not email:
        flash('Por favor, preencha todos os campos.', 'error')
        return redirect(request.referrer or url_for('main.index'))
    
    # Validar email
    import re
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        flash('Por favor, insira um e-mail válido.', 'error')
        return redirect(request.referrer or url_for('main.index'))
    
    # Salvar inscrição (aqui você pode adicionar lógica para salvar no banco de dados)
    try:
        # Log da inscrição
        import os
        log_file = 'newsletter_subscriptions.log'
        with open(log_file, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"{timestamp}: Nome={nome}, Email={email}\n")
        
        flash('Inscrição realizada com sucesso! Obrigado por se cadastrar.', 'success')
    except Exception as e:
        flash('Ocorreu um erro ao processar sua inscrição. Tente novamente.', 'error')
    
    return redirect(request.referrer or url_for('main.index'))

@bp.route('/seja-patrocinador/folheto.pdf')
def patrocinadores_folheto_pdf():
    """Gera PDF do folheto de patrocinadores"""
    try:
        from app.pdf_generator import generate_folheto_pdf
    except ImportError:
        flash('Dependência para geração de PDF não instalada. Por favor, contate o administrador.', 'danger')
        return redirect(url_for('main.patrocinadores_folheto'))

    try:
        pdf_bytes = generate_folheto_pdf()

        response = make_response(pdf_bytes)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=folheto-patrocinadores.pdf'
        return response

    except Exception as exc:
        current_app.logger.exception('Erro ao gerar PDF do folheto: %s', exc)
        flash('Não foi possível gerar o PDF no momento. Por favor, tente novamente em instantes.', 'danger')
        return redirect(url_for('main.patrocinadores_folheto'))

@bp.route('/galeria')
def galeria():
    """Página da galeria de imagens"""
    from app.image_manager import ImageManager
    from app.upload_config import IMAGE_CATEGORIES
    
    # Inicializar gerenciador de imagens
    upload_folder = os.path.join(os.path.dirname(__file__), 'static', 'images', 'galeria')
    image_manager = ImageManager(upload_folder)
    
    # Obter todas as imagens
    all_images = image_manager.get_all_images()
    stats = image_manager.get_statistics()
    
    # Função helper para gerar URL da imagem
    def get_image_url(filename):
        # Mapear categoria para pasta
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
        
        # Buscar categoria da imagem
        if filename in all_images:
            category = all_images[filename].get('category', '')
            folder = category_folders.get(category, '')
            if folder:
                return f"images/galeria/{folder}/{filename}"
        
        return f"images/galeria/{filename}"
    
    return render_template('galeria.html', images=all_images, stats=stats, categories=IMAGE_CATEGORIES, get_image_url=get_image_url)

@bp.route('/blog')
def blog():
    """Página do blog/notícias"""
    try:
        from app.blog_manager_mysql import BlogManagerMySQL
        from app.blog_config import BLOG_CATEGORIES
        
        # Inicializar gerenciador de blog MySQL
        blog_manager = BlogManagerMySQL()
        
        # Obter todas as notícias
        all_news = blog_manager.get_all_news()
        stats = blog_manager.get_statistics()
        
        # Função helper para gerar URL da imagem
        def get_news_image_url(news_id, image_index=0):
            if news_id in all_news and all_news[news_id]['images']:
                image_id = all_news[news_id]['images'][image_index]['id']
                return f"/blog/images/{image_id}"
            return None
        
        blog_manager.close()
        
        return render_template('blog.html', news=all_news, stats=stats, categories=BLOG_CATEGORIES, get_news_image_url=get_news_image_url)
    
    except Exception as e:
        print(f"Erro na página do blog: {e}")
        # Em caso de erro, renderizar página sem dados
        return render_template('blog.html', news={}, stats={'total_news': 0, 'categories': [], 'total_views': 0, 'total_likes': 0}, categories={}, get_news_image_url=lambda x, y=0: None)

@bp.route('/rss.xml')
def rss_feed():
    """Gera RSS feed das notícias"""
    # Dados das notícias (em um sistema real, isso viria de um banco de dados)
    news_data = [
        {
            'title': 'Ensaios da Paixão de Cristo 2027 Iniciam em Março',
            'description': 'Os ensaios para o maior espetáculo a céu aberto da região começam em março.',
            'content': 'Mais de 200 artistas participarão dos ensaios que acontecerão aos fins de semana...',
            'date': '2026-01-15',
            'category': 'evento',
            'url': url_for('main.blog', _external=True) + '#noticia-1'
        },
        {
            'title': 'Bastidores: Confecção dos Costumes Históricos',
            'description': 'Conheça o trabalho minucioso da equipe de figurinistas.',
            'content': 'Mais de 300 costumes históricos estão sendo criados para o espetáculo...',
            'date': '2026-01-12',
            'category': 'bastidores',
            'url': url_for('main.blog', _external=True) + '#noticia-2'
        },
        {
            'title': 'Novos Patrocinadores Confirmados para 2027',
            'description': 'Três novas empresas confirmaram patrocínio para a edição 2027.',
            'content': 'Os benefícios fiscais da Lei Rouanet continuam atraindo investidores...',
            'date': '2026-01-10',
            'category': 'patrocinio',
            'url': url_for('main.blog', _external=True) + '#noticia-3'
        }
    ]
    
    # Criar RSS XML
    rss_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
    <channel>
        <title>Paixão de Cristo de Maracanaú - Notícias</title>
        <description>Notícias e atualizações sobre a Paixão de Cristo de Maracanaú</description>
        <link>{url_for('main.blog', _external=True)}</link>
        <language>pt-BR</language>
        <lastBuildDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')}</lastBuildDate>
        <atom:link href="{url_for('main.rss_feed', _external=True)}" rel="self" type="application/rss+xml"/>
        
"""
    
    for news in news_data:
        rss_content += f"""        <item>
            <title>{news['title']}</title>
            <description>{news['description']}</description>
            <link>{news['url']}</link>
            <guid isPermaLink="true">{news['url']}</guid>
            <pubDate>{datetime.strptime(news['date'], '%Y-%m-%d').strftime('%a, %d %b %Y %H:%M:%S GMT')}</pubDate>
            <category>{news['category']}</category>
        </item>
"""
    
    rss_content += """    </channel>
</rss>"""
    
    response = make_response(rss_content)
    response.headers['Content-Type'] = 'application/rss+xml; charset=utf-8'
    return response


@bp.route('/patrocinio')
def patrocinio():
    """Página de patrocínio"""
    return render_template('patrocinio.html')

@bp.route('/sitemap.xml')
def sitemap():
    """Gera sitemap.xml dinâmico"""
    # Criar elemento raiz
    urlset = Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    # URLs estáticas do site
    urls = [
        {'loc': '/', 'changefreq': 'weekly', 'priority': '1.0'},
        {'loc': '/sobre', 'changefreq': 'monthly', 'priority': '0.8'},
        {'loc': '/evento-2027', 'changefreq': 'weekly', 'priority': '0.9'},
        {'loc': '/edicao-2026', 'changefreq': 'monthly', 'priority': '0.7'},
        {'loc': '/espetaculo-cenico', 'changefreq': 'monthly', 'priority': '0.7'},
        {'loc': '/festival-musica', 'changefreq': 'monthly', 'priority': '0.7'},
        {'loc': '/formacao-artistica', 'changefreq': 'monthly', 'priority': '0.7'},
        {'loc': '/feira-livre', 'changefreq': 'monthly', 'priority': '0.7'},
        {'loc': '/na-midia', 'changefreq': 'weekly', 'priority': '0.6'},
               {'loc': '/galeria', 'changefreq': 'weekly', 'priority': '0.7'},
               {'loc': '/blog', 'changefreq': 'daily', 'priority': '0.8'},
               {'loc': '/patrocinio', 'changefreq': 'monthly', 'priority': '0.8'},
               {'loc': '/seja-patrocinador', 'changefreq': 'monthly', 'priority': '0.8'},
               {'loc': '/contato', 'changefreq': 'monthly', 'priority': '0.6'},
               {'loc': '/faq', 'changefreq': 'monthly', 'priority': '0.7'}
    ]
    
    # Adicionar cada URL ao sitemap
    for url_data in urls:
        url_elem = SubElement(urlset, 'url')
        
        loc = SubElement(url_elem, 'loc')
        loc.text = request.url_root.rstrip('/') + url_data['loc']
        
        lastmod = SubElement(url_elem, 'lastmod')
        lastmod.text = datetime.now().strftime('%Y-%m-%d')
        
        changefreq = SubElement(url_elem, 'changefreq')
        changefreq.text = url_data['changefreq']
        
        priority = SubElement(url_elem, 'priority')
        priority.text = url_data['priority']
    
    # Converter para string XML
    xml_str = tostring(urlset, encoding='unicode')
    xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_str
    
    # Criar resposta
    response = make_response(xml_str)
    response.headers['Content-Type'] = 'application/xml'
    return response

@bp.route('/robots.txt')
def robots():
    """Gera robots.txt"""
    robots_content = """User-agent: *
Allow: /

# Sitemap
Sitemap: {}/sitemap.xml

# Disallow admin areas
Disallow: /admin/
Disallow: /private/

# Allow static content
Allow: /static/
Allow: /images/

# Crawl-delay (opcional, ajuda a não sobrecarregar o servidor)
Crawl-delay: 1
""".format(request.url_root.rstrip('/'))
    
    response = make_response(robots_content)
    response.headers['Content-Type'] = 'text/plain'
    return response

@bp.route('/contato', methods=['GET', 'POST'])
def contato():
    """Página de contato com formulário"""
    if request.method == 'POST':
        # Verificar rate limiting
        client_ip = request.remote_addr
        if not check_rate_limit(client_ip):
            flash('Muitas tentativas de envio. Tente novamente em uma hora.', 'error')
            return render_template('contato.html')
        
        # Coleta dados do formulário
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        telefone = request.form.get('telefone', '').strip()
        empresa = request.form.get('empresa', '').strip()
        assunto = request.form.get('assunto', '').strip()
        mensagem = request.form.get('mensagem', '').strip()
        aceito = request.form.get('aceito')
        
        # Campos específicos do formulário de patrocínio
        cnpj = request.form.get('cnpj', '').strip()
        ramo = request.form.get('ramo', '').strip()
        porte = request.form.get('porte', '').strip()
        cargo = request.form.get('cargo', '').strip()
        valor_interesse = request.form.get('valor_interesse', '').strip()
        tipo_patrocinio = request.form.get('tipo_patrocinio', '').strip()
        
        # Verificar se é formulário de patrocínio
        is_patrocinio_form = bool(cnpj or ramo or porte or cargo or valor_interesse or tipo_patrocinio or 'Patrocínio' in assunto)
        
        # Validação robusta
        errors = []
        
        if not nome or len(nome) < 2:
            errors.append('Nome deve ter pelo menos 2 caracteres.')
        
        if not email or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors.append('E-mail inválido.')
        
        if not assunto:
            errors.append('Assunto é obrigatório.')
        
        # Para formulário de patrocínio, mensagem é opcional
        if not is_patrocinio_form:
            if not mensagem or len(mensagem) < 10:
                errors.append('Mensagem deve ter pelo menos 10 caracteres.')
        
        # Aceito é obrigatório apenas para formulário de contato normal
        if not is_patrocinio_form and not aceito:
            errors.append('Você deve aceitar receber informações sobre o projeto.')
        
        # Validação adicional de segurança
        if mensagem and len(mensagem) > 2000:
            errors.append('Mensagem muito longa (máximo 2000 caracteres).')
        
        # Verificar se contém spam básico (apenas se houver mensagem)
        if mensagem:
            spam_keywords = ['viagra', 'casino', 'lottery', 'winner', 'congratulations']
            if any(keyword in mensagem.lower() for keyword in spam_keywords):
                errors.append('Mensagem contém conteúdo suspeito.')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            # Redirecionar para página correta conforme tipo de formulário
            if is_patrocinio_form:
                return render_template('patrocinio.html')
            else:
                return render_template('contato.html')
        
        try:
            # Preparar dados para envio
            form_data = {
                'nome': nome,
                'email': email,
                'telefone': telefone,
                'empresa': empresa,
                'assunto': assunto,
                'mensagem': mensagem,
                'data': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                'ip': request.remote_addr
            }
            
            # Adicionar campos específicos do formulário de patrocínio
            if is_patrocinio_form:
                form_data.update({
                    'cnpj': cnpj,
                    'ramo': ramo,
                    'porte': porte,
                    'cargo': cargo,
                    'valor_interesse': valor_interesse,
                    'tipo_patrocinio': tipo_patrocinio
                })
            
            # Aqui você pode implementar o envio real de e-mail
            # Por enquanto, apenas simula o envio
            print(f"E-mail recebido: {form_data}")  # Para debug
            
            # Tentar enviar e-mail real se configurado
            try:
                if current_app.config.get('MAIL_USERNAME') and current_app.config.get('MAIL_PASSWORD'):
                    # E-mail para administradores
                    # Montar corpo do e-mail com campos específicos do patrocínio
                    email_body = f"""
                        Novo contato recebido do site Paixão de Cristo de Maracanaú:
                        
                        Nome: {nome}
                        E-mail: {email}
                        Telefone: {telefone}
                        Empresa: {empresa}
                        Assunto: {assunto}
                        Mensagem: {mensagem}
                        """
                    
                    if is_patrocinio_form:
                        email_body += f"""
                        
                        === INFORMAÇÕES DE PATROCÍNIO ===
                        CNPJ: {cnpj or 'Não informado'}
                        Ramo de Atividade: {ramo or 'Não informado'}
                        Porte da Empresa: {porte or 'Não informado'}
                        Cargo/Função: {cargo or 'Não informado'}
                        Valor de Interesse: {valor_interesse or 'Não informado'}
                        Tipo de Patrocínio: {tipo_patrocinio or 'Não informado'}
                        """
                    
                    email_body += f"""
                        
                        Data: {form_data['data']}
                        IP: {form_data['ip']}
                        """
                    
                    admin_msg = Message(
                        subject=f"Novo contato: {assunto}",
                        recipients=[current_app.config['MAIL_DEFAULT_SENDER']],
                        body=email_body,
                        sender=current_app.config['MAIL_DEFAULT_SENDER']
                    )
                    if MAIL_AVAILABLE and mail:
                        mail.send(admin_msg)
                    else:
                        print("Email não enviado - Flask-Mail não disponível")
                    
                    # E-mail de confirmação para o usuário
                    user_msg = Message(
                        subject="Confirmação de contato - Paixão de Cristo de Maracanaú",
                        recipients=[email],
                        body=f"""
                        Olá {nome},
                        
                        Recebemos sua mensagem com sucesso!
                        
                        Assunto: {assunto}
                        Sua mensagem: {mensagem or 'N/A'}
                        
                        Entraremos em contato em breve.
                        
                        Atenciosamente,
                        Equipe Paixão de Cristo de Maracanaú
                        
                        ---
                        Projeto realizado com o apoio da Lei de Incentivo à Cultura
                        PRONAC 262433
                        """,
                        sender=current_app.config['MAIL_DEFAULT_SENDER']
                    )
                    if MAIL_AVAILABLE and mail:
                        mail.send(user_msg)
                        flash('Mensagem enviada com sucesso! Você receberá uma confirmação por e-mail.', 'success')
                    else:
                        print("Email não enviado - Flask-Mail não disponível")
                        flash('Mensagem recebida! Entraremos em contato em breve.', 'success')
                else:
                    # Fallback para quando e-mail não está configurado
                    flash('Mensagem recebida! Entraremos em contato em breve.', 'success')
                    
            except Exception as email_error:
                print(f"Erro no envio de e-mail: {email_error}")
                # Mesmo com erro de e-mail, salvar o contato
                flash('Mensagem recebida! Entraremos em contato em breve.', 'success')
            
            # Log da mensagem (para debug)
            with open('contatos.log', 'a', encoding='utf-8') as f:
                # Usar formato completo de data/hora para facilitar parsing
                timestamp_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"{timestamp_str}: {form_data}\n")
            
            # Redirecionar para página apropriada
            if is_patrocinio_form:
                return redirect(url_for('main.patrocinio'))
            else:
                return redirect(url_for('main.contato'))
            
        except Exception as e:
            flash('Erro ao enviar mensagem. Tente novamente mais tarde.', 'error')
            print(f"Erro no envio: {e}")
            return render_template('contato.html')
    
    return render_template('contato.html')

# Função para inicializar o blueprint
def init_app(app):
    """Inicializa o blueprint na aplicação"""
    app.register_blueprint(bp)
    init_mail(app)
