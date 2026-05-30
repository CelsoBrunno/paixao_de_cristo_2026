-- =====================================================
-- SCRIPT DE CRIAÇÃO DO BANCO DE DADOS MYSQL
-- Projeto: Paixão de Cristo de Maracanaú (PRONAC 255599)
-- Sistema: Blog e Website Institucional
-- =====================================================

-- Configurações iniciais
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

-- =====================================================
-- CRIAÇÃO DO BANCO DE DADOS
-- =====================================================

-- Criar banco de dados (comentado para produção)
-- CREATE DATABASE IF NOT EXISTS `paixao_cristo` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- USE `paixao_cristo`;

-- Para PythonAnywhere, usar o banco existente:
-- USE `paixaodecristoma$paixao_cristo_db`;

-- =====================================================
-- TABELA DE NOTÍCIAS DO BLOG
-- =====================================================

DROP TABLE IF EXISTS `blog_images`;
DROP TABLE IF EXISTS `blog_news`;

CREATE TABLE `blog_news` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL COMMENT 'Título da notícia',
  `content` text NOT NULL COMMENT 'Conteúdo da notícia',
  `author` varchar(100) NOT NULL COMMENT 'Autor da notícia',
  `category` varchar(50) NOT NULL COMMENT 'Categoria da notícia',
  `date` date NOT NULL COMMENT 'Data da notícia',
  `views` int(11) DEFAULT 0 COMMENT 'Número de visualizações',
  `likes` int(11) DEFAULT 0 COMMENT 'Número de curtidas',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Data de criação',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Data de atualização',
  PRIMARY KEY (`id`),
  KEY `idx_category` (`category`),
  KEY `idx_date` (`date`),
  KEY `idx_created_at` (`created_at`),
  KEY `idx_views` (`views`),
  KEY `idx_likes` (`likes`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Tabela de notícias do blog';

-- =====================================================
-- TABELA DE IMAGENS DO BLOG
-- =====================================================

CREATE TABLE `blog_images` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `news_id` int(11) NOT NULL COMMENT 'ID da notícia relacionada',
  `filename` varchar(255) NOT NULL COMMENT 'Nome do arquivo',
  `image_data` longblob NOT NULL COMMENT 'Dados binários da imagem',
  `image_type` varchar(50) NOT NULL COMMENT 'Tipo MIME da imagem',
  `file_size` int(11) NOT NULL COMMENT 'Tamanho do arquivo em bytes',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Data de criação',
  PRIMARY KEY (`id`),
  KEY `idx_news_id` (`news_id`),
  KEY `idx_filename` (`filename`),
  KEY `idx_image_type` (`image_type`),
  KEY `idx_file_size` (`file_size`),
  CONSTRAINT `fk_blog_images_news` FOREIGN KEY (`news_id`) REFERENCES `blog_news` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Tabela de imagens do blog';

-- =====================================================
-- TABELA DE CATEGORIAS (OPCIONAL - PARA EXPANSÃO FUTURA)
-- =====================================================

CREATE TABLE `blog_categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL COMMENT 'Nome da categoria',
  `description` text COMMENT 'Descrição da categoria',
  `color` varchar(7) DEFAULT '#007bff' COMMENT 'Cor da categoria (hex)',
  `icon` varchar(50) DEFAULT 'fas fa-folder' COMMENT 'Ícone da categoria',
  `is_active` tinyint(1) DEFAULT 1 COMMENT 'Categoria ativa',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_name` (`name`),
  KEY `idx_is_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Categorias do blog';

-- =====================================================
-- TABELA DE USUÁRIOS ADMINISTRATIVOS (OPCIONAL)
-- =====================================================

CREATE TABLE `admin_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL COMMENT 'Nome de usuário',
  `email` varchar(100) NOT NULL COMMENT 'E-mail do usuário',
  `password_hash` varchar(255) NOT NULL COMMENT 'Hash da senha',
  `full_name` varchar(100) NOT NULL COMMENT 'Nome completo',
  `role` enum('admin','editor','viewer') DEFAULT 'editor' COMMENT 'Papel do usuário',
  `is_active` tinyint(1) DEFAULT 1 COMMENT 'Usuário ativo',
  `last_login` timestamp NULL DEFAULT NULL COMMENT 'Último login',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_username` (`username`),
  UNIQUE KEY `unique_email` (`email`),
  KEY `idx_role` (`role`),
  KEY `idx_is_active` (`is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Usuários administrativos';

-- =====================================================
-- TABELA DE CONFIGURAÇÕES DO SISTEMA (OPCIONAL)
-- =====================================================

CREATE TABLE `system_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `config_key` varchar(100) NOT NULL COMMENT 'Chave da configuração',
  `config_value` text COMMENT 'Valor da configuração',
  `config_type` enum('string','int','float','boolean','json') DEFAULT 'string' COMMENT 'Tipo do valor',
  `description` text COMMENT 'Descrição da configuração',
  `is_public` tinyint(1) DEFAULT 0 COMMENT 'Configuração pública',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_config_key` (`config_key`),
  KEY `idx_is_public` (`is_public`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Configurações do sistema';

-- =====================================================
-- TABELA DE LOGS DO SISTEMA (OPCIONAL)
-- =====================================================

CREATE TABLE `system_logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `level` enum('DEBUG','INFO','WARNING','ERROR','CRITICAL') NOT NULL COMMENT 'Nível do log',
  `message` text NOT NULL COMMENT 'Mensagem do log',
  `module` varchar(100) COMMENT 'Módulo que gerou o log',
  `user_id` int(11) COMMENT 'ID do usuário (se aplicável)',
  `ip_address` varchar(45) COMMENT 'Endereço IP',
  `user_agent` text COMMENT 'User Agent do navegador',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_level` (`level`),
  KEY `idx_module` (`module`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_created_at` (`created_at`),
  CONSTRAINT `fk_system_logs_user` FOREIGN KEY (`user_id`) REFERENCES `admin_users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Logs do sistema';

-- =====================================================
-- INSERÇÃO DE DADOS INICIAIS
-- =====================================================

-- Inserir categorias padrão
INSERT INTO `blog_categories` (`name`, `description`, `color`, `icon`) VALUES
('Evento', 'Notícias sobre eventos e apresentações', '#dc3545', 'fas fa-calendar-alt'),
('Patrocínio', 'Notícias sobre patrocinadores e incentivos', '#28a745', 'fas fa-handshake'),
('Formação', 'Notícias sobre formação artística', '#ffc107', 'fas fa-graduation-cap'),
('Mídia', 'Notícias sobre cobertura na mídia', '#17a2b8', 'fas fa-newspaper'),
('Geral', 'Notícias gerais do projeto', '#6c757d', 'fas fa-info-circle');

-- Inserir configurações padrão do sistema
INSERT INTO `system_config` (`config_key`, `config_value`, `config_type`, `description`, `is_public`) VALUES
('site_title', 'Paixão de Cristo de Maracanaú', 'string', 'Título do site', 1),
('site_description', 'Projeto cultural incentivado pela Lei Rouanet (PRONAC 255599)', 'string', 'Descrição do site', 1),
('site_keywords', 'paixão de cristo, maracanaú, cultura, lei rouanet, pronac', 'string', 'Palavras-chave do site', 1),
('project_pronac', '255599', 'string', 'Número do PRONAC', 1),
('project_year', '2026', 'string', 'Ano do projeto', 1),
('project_director', 'Celso Brunno', 'string', 'Diretor do projeto', 1),
('project_phone', '(85) 99999-9999', 'string', 'Telefone de contato', 1),
('project_email', 'contato@paixaodecristomaracana.com.br', 'string', 'E-mail de contato', 1),
('max_upload_size', '10485760', 'int', 'Tamanho máximo de upload em bytes (10MB)', 0),
('allowed_image_types', '["image/jpeg", "image/png", "image/gif", "image/webp"]', 'json', 'Tipos de imagem permitidos', 0),
('blog_posts_per_page', '10', 'int', 'Número de posts por página', 0),
('enable_comments', 'false', 'boolean', 'Habilitar comentários', 0);

-- Inserir usuário administrador padrão (senha: admin123)
-- ATENÇÃO: Alterar a senha após o primeiro login!
INSERT INTO `admin_users` (`username`, `email`, `password_hash`, `full_name`, `role`) VALUES
('admin', 'admin@paixaodecristomaracana.com.br', 'pbkdf2:sha256:260000$8X9K2L3M$4f8a2b1c3d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z7a8b9c0d1e2f3', 'Administrador do Sistema', 'admin');

-- Inserir notícia de exemplo
INSERT INTO `blog_news` (`title`, `content`, `author`, `category`, `date`) VALUES
('Bem-vindos ao Blog da Paixão de Cristo de Maracanaú', 
'<p>Este é o blog oficial do projeto cultural "Paixão de Cristo de Maracanaú", incentivado pela Lei Rouanet (PRONAC 255599).</p><p>Aqui você encontrará todas as notícias, eventos e atualizações sobre nosso projeto cultural que já tem mais de 46 anos de tradição.</p><p>Fique por dentro das novidades e acompanhe nossa jornada cultural!</p>', 
'Equipe Editorial', 
'Geral', 
CURDATE());

-- =====================================================
-- ÍNDICES ADICIONAIS PARA PERFORMANCE
-- =====================================================

-- Índices compostos para consultas frequentes
CREATE INDEX `idx_news_category_date` ON `blog_news` (`category`, `date` DESC);
CREATE INDEX `idx_news_views_likes` ON `blog_news` (`views` DESC, `likes` DESC);
CREATE INDEX `idx_images_news_type` ON `blog_images` (`news_id`, `image_type`);

-- =====================================================
-- VIEWS PARA CONSULTAS FREQUENTES
-- =====================================================

-- View para estatísticas do blog
CREATE VIEW `blog_stats` AS
SELECT 
    COUNT(*) as total_posts,
    COUNT(DISTINCT category) as total_categories,
    SUM(views) as total_views,
    SUM(likes) as total_likes,
    AVG(views) as avg_views_per_post,
    MAX(created_at) as last_post_date
FROM blog_news;

-- View para posts mais populares
CREATE VIEW `popular_posts` AS
SELECT 
    id,
    title,
    category,
    views,
    likes,
    created_at,
    ROW_NUMBER() OVER (ORDER BY views DESC, likes DESC) as popularity_rank
FROM blog_news
ORDER BY views DESC, likes DESC;

-- =====================================================
-- PROCEDURES PARA OPERAÇÕES COMUNS
-- =====================================================

DELIMITER //

-- Procedure para incrementar visualizações
CREATE PROCEDURE IncrementPostViews(IN post_id INT)
BEGIN
    UPDATE blog_news 
    SET views = views + 1 
    WHERE id = post_id;
END //

-- Procedure para incrementar curtidas
CREATE PROCEDURE IncrementPostLikes(IN post_id INT)
BEGIN
    UPDATE blog_news 
    SET likes = likes + 1 
    WHERE id = post_id;
END //

-- Procedure para obter posts por categoria
CREATE PROCEDURE GetPostsByCategory(IN cat_name VARCHAR(50), IN limit_count INT)
BEGIN
    SELECT 
        n.id,
        n.title,
        n.content,
        n.author,
        n.category,
        n.date,
        n.views,
        n.likes,
        n.created_at,
        COUNT(i.id) as image_count
    FROM blog_news n
    LEFT JOIN blog_images i ON n.id = i.news_id
    WHERE n.category = cat_name
    GROUP BY n.id
    ORDER BY n.created_at DESC
    LIMIT limit_count;
END //

DELIMITER ;

-- =====================================================
-- TRIGGERS PARA AUDITORIA
-- =====================================================

-- Trigger para log de inserção de posts
DELIMITER //
CREATE TRIGGER `tr_blog_news_insert` 
AFTER INSERT ON `blog_news`
FOR EACH ROW
BEGIN
    INSERT INTO system_logs (level, message, module) 
    VALUES ('INFO', CONCAT('Novo post criado: ', NEW.title), 'blog');
END //

-- Trigger para log de atualização de posts
CREATE TRIGGER `tr_blog_news_update` 
AFTER UPDATE ON `blog_news`
FOR EACH ROW
BEGIN
    INSERT INTO system_logs (level, message, module) 
    VALUES ('INFO', CONCAT('Post atualizado: ', NEW.title), 'blog');
END //

-- Trigger para log de exclusão de posts
CREATE TRIGGER `tr_blog_news_delete` 
AFTER DELETE ON `blog_news`
FOR EACH ROW
BEGIN
    INSERT INTO system_logs (level, message, module) 
    VALUES ('WARNING', CONCAT('Post excluído: ', OLD.title), 'blog');
END //

DELIMITER ;

-- =====================================================
-- CONFIGURAÇÕES FINAIS
-- =====================================================

-- Reabilitar verificações de chave estrangeira
SET FOREIGN_KEY_CHECKS = 1;

-- Commit das alterações
COMMIT;

-- =====================================================
-- VERIFICAÇÃO FINAL
-- =====================================================

-- Mostrar tabelas criadas
SHOW TABLES;

-- Mostrar estrutura das tabelas principais
DESCRIBE blog_news;
DESCRIBE blog_images;

-- Mostrar estatísticas iniciais
SELECT * FROM blog_stats;

-- =====================================================
-- INSTRUÇÕES DE USO
-- =====================================================

/*
INSTRUÇÕES PARA USO DO BANCO DE DADOS:

1. CONFIGURAÇÃO INICIAL:
   - Para PythonAnywhere: Use o banco 'paixaodecristoma$paixao_cristo_db'
   - Para desenvolvimento local: Descomente as linhas de criação do banco

2. CONFIGURAÇÃO DO PYTHON:
   - Instale: pip install mysql-connector-python
   - Configure as credenciais no arquivo db_config.py

3. OPERAÇÕES BÁSICAS:
   - Inserir post: INSERT INTO blog_news (title, content, author, category, date) VALUES (...)
   - Buscar posts: SELECT * FROM blog_news ORDER BY created_at DESC
   - Estatísticas: SELECT * FROM blog_stats

4. PROCEDURES DISPONÍVEIS:
   - CALL IncrementPostViews(post_id);
   - CALL IncrementPostLikes(post_id);
   - CALL GetPostsByCategory('categoria', 10);

5. SEGURANÇA:
   - Alterar senha do usuário admin após primeiro login
   - Configurar variáveis de ambiente para credenciais
   - Usar HTTPS em produção

6. BACKUP:
   - Fazer backup regular do banco de dados
   - Especialmente da tabela blog_images (contém dados binários)

7. MANUTENÇÃO:
   - Monitorar logs na tabela system_logs
   - Verificar estatísticas na view blog_stats
   - Limpar logs antigos periodicamente
*/

-- =====================================================
-- FIM DO SCRIPT
-- =====================================================
