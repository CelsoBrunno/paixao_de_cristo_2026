/**
 * Paixão de Cristo de Maracanaú - JavaScript Principal
 * Funcionalidades de interatividade e acessibilidade
 */

document.addEventListener('DOMContentLoaded', function() {
    'use strict';
    
    // Inicializar todas as funcionalidades
    initSmoothScrolling();
    initNavbarBehavior();
    initFormValidation();
    initImageLazyLoading();
    initAccessibilityFeatures();
    initAnimations();
    initCounters();
});

/**
 * Scroll suave para âncoras
 */
function initSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                e.preventDefault();
                
                const offsetTop = targetElement.offsetTop - 80; // Altura do navbar
                
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
                
                // Atualizar URL sem recarregar a página
                history.pushState(null, null, targetId);
                
                // Focar no elemento para acessibilidade
                targetElement.focus();
            }
        });
    });
}

/**
 * Comportamento da navbar
 */
function initNavbarBehavior() {
    const navbar = document.querySelector('.navbar');
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    // Forçar posicionamento do botão à esquerda sempre
    function forceTogglerPosition() {
        if (navbarToggler) {
            navbarToggler.style.setProperty('position', 'relative', 'important');
            navbarToggler.style.setProperty('margin-left', '0', 'important');
            navbarToggler.style.setProperty('margin-right', 'auto', 'important');
            navbarToggler.style.setProperty('left', '0', 'important');
            navbarToggler.style.setProperty('right', 'auto', 'important');
            navbarToggler.style.setProperty('order', '1', 'important');
            navbarToggler.style.setProperty('float', 'none', 'important');
            navbarToggler.style.setProperty('flex-shrink', '0', 'important');
        }
        
        // Forçar container a usar flex-start
        const container = navbar ? navbar.querySelector('.container') : null;
        if (container) {
            container.style.setProperty('justify-content', 'flex-start', 'important');
        }
    }
    
    // Aplicar posicionamento inicial
    setTimeout(forceTogglerPosition, 0);
    setTimeout(forceTogglerPosition, 100);
    setTimeout(forceTogglerPosition, 300);
    
    // Observar mudanças no atributo aria-expanded
    if (navbarToggler) {
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'attributes' && mutation.attributeName === 'aria-expanded') {
                    setTimeout(forceTogglerPosition, 0);
                    setTimeout(forceTogglerPosition, 50);
                }
            });
        });
        
        observer.observe(navbarToggler, {
            attributes: true,
            attributeFilter: ['aria-expanded']
        });
    }
    
    // Forçar posicionamento quando o menu abre/fecha
    if (navbarCollapse) {
        navbarCollapse.addEventListener('show.bs.collapse', function() {
            setTimeout(forceTogglerPosition, 0);
            setTimeout(forceTogglerPosition, 50);
        });
        navbarCollapse.addEventListener('hide.bs.collapse', function() {
            setTimeout(forceTogglerPosition, 0);
            setTimeout(forceTogglerPosition, 50);
        });
        navbarCollapse.addEventListener('shown.bs.collapse', function() {
            setTimeout(forceTogglerPosition, 0);
            setTimeout(forceTogglerPosition, 50);
        });
        navbarCollapse.addEventListener('hidden.bs.collapse', function() {
            setTimeout(forceTogglerPosition, 0);
            setTimeout(forceTogglerPosition, 50);
        });
    }
    
    // Observar cliques no botão
    if (navbarToggler) {
        navbarToggler.addEventListener('click', function() {
            setTimeout(forceTogglerPosition, 0);
            setTimeout(forceTogglerPosition, 50);
            setTimeout(forceTogglerPosition, 100);
        });
    }
    
    // Mudar aparência da navbar no scroll
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
        }
    });
    
    // Fechar menu mobile ao clicar em um link (exceto dropdowns)
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link:not(.dropdown-toggle)');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (navbarCollapse.classList.contains('show')) {
                navbarToggler.click();
            }
        });
    });
    
    // Melhorar comportamento do dropdown no mobile
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            // No mobile, permitir que o dropdown funcione normalmente
            if (window.innerWidth <= 991) {
                e.stopPropagation();
            }
        });
    });
    
    // Fechar menu mobile ao clicar fora dele
    document.addEventListener('click', function(e) {
        const isClickInsideNav = navbar.contains(e.target);
        
        if (!isClickInsideNav && navbarCollapse.classList.contains('show')) {
            navbarToggler.click();
        }
    });
}

/**
 * Validação de formulários
 */
function initFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                return false;
            }
        });
        
        // Validação em tempo real
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                clearFieldError(this);
            });
        });
    });
    
    // Máscara para telefone
    const telefoneInputs = document.querySelectorAll('input[type="tel"]');
    telefoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            formatPhoneNumber(e.target);
        });
    });
}

/**
 * Validar formulário completo
 */
function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!validateField(field)) {
            isValid = false;
        }
    });
    
    // Validar email se presente
    const emailField = form.querySelector('input[type="email"]');
    if (emailField && !isValidEmail(emailField.value)) {
        showFieldError(emailField, 'Por favor, insira um e-mail válido.');
        isValid = false;
    }
    
    return isValid;
}

/**
 * Validar campo individual
 */
function validateField(field) {
    const value = field.value.trim();
    
    // Campo obrigatório vazio
    if (field.hasAttribute('required') && !value) {
        showFieldError(field, 'Este campo é obrigatório.');
        return false;
    }
    
    // Validação específica por tipo
    switch (field.type) {
        case 'email':
            if (value && !isValidEmail(value)) {
                showFieldError(field, 'Por favor, insira um e-mail válido.');
                return false;
            }
            break;
            
        case 'tel':
            if (value && !isValidPhone(value)) {
                showFieldError(field, 'Por favor, insira um telefone válido.');
                return false;
            }
            break;
    }
    
    clearFieldError(field);
    return true;
}

/**
 * Mostrar erro no campo
 */
function showFieldError(field, message) {
    clearFieldError(field);
    
    field.classList.add('is-invalid');
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    
    field.parentNode.appendChild(errorDiv);
}

/**
 * Limpar erro do campo
 */
function clearFieldError(field) {
    field.classList.remove('is-invalid');
    
    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

/**
 * Validar email
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Validar telefone
 */
function isValidPhone(phone) {
    const phoneRegex = /^\(\d{2}\)\s\d{4,5}-\d{4}$/;
    return phoneRegex.test(phone);
}

/**
 * Formatar número de telefone
 */
function formatPhoneNumber(input) {
    let value = input.value.replace(/\D/g, '');
    
    if (value.length >= 11) {
        value = value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
    } else if (value.length >= 7) {
        value = value.replace(/(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3');
    } else if (value.length >= 3) {
        value = value.replace(/(\d{2})(\d{0,5})/, '($1) $2');
    }
    
    input.value = value;
}

/**
 * Lazy loading de imagens
 */
function initImageLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback para navegadores sem suporte
        images.forEach(img => {
            img.src = img.dataset.src;
            img.classList.remove('lazy');
        });
    }
}

/**
 * Funcionalidades de acessibilidade
 */
function initAccessibilityFeatures() {
    // Adicionar skip link
    addSkipLink();
    
    // Melhorar navegação por teclado
    improveKeyboardNavigation();
    
    // Adicionar ARIA labels onde necessário
    addAriaLabels();
    
    // Gerenciar foco em modais
    manageFocus();
}

/**
 * Adicionar skip link
 */
function addSkipLink() {
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.textContent = 'Pular para o conteúdo principal';
    skipLink.className = 'sr-only';
    skipLink.style.position = 'absolute';
    skipLink.style.left = '-10000px';
    skipLink.style.top = 'auto';
    skipLink.style.width = '1px';
    skipLink.style.height = '1px';
    skipLink.style.overflow = 'hidden';
    
    skipLink.addEventListener('focus', function() {
        this.style.position = 'absolute';
        this.style.left = '6px';
        this.style.top = '6px';
        this.style.width = 'auto';
        this.style.height = 'auto';
        this.style.overflow = 'visible';
        this.style.backgroundColor = '#007bff';
        this.style.color = 'white';
        this.style.padding = '8px 16px';
        this.style.textDecoration = 'none';
        this.style.borderRadius = '4px';
        this.style.zIndex = '9999';
    });
    
    skipLink.addEventListener('blur', function() {
        this.style.position = 'absolute';
        this.style.left = '-10000px';
        this.style.top = 'auto';
        this.style.width = '1px';
        this.style.height = '1px';
        this.style.overflow = 'hidden';
        this.style.backgroundColor = '';
        this.style.color = '';
        this.style.padding = '';
        this.style.textDecoration = '';
        this.style.borderRadius = '';
        this.style.zIndex = '';
    });
    
    document.body.insertBefore(skipLink, document.body.firstChild);
}

/**
 * Melhorar navegação por teclado
 */
function improveKeyboardNavigation() {
    // Adicionar suporte para ESC em dropdowns
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const openDropdown = document.querySelector('.dropdown-menu.show');
            if (openDropdown) {
                const dropdownToggle = openDropdown.previousElementSibling;
                dropdownToggle.click();
            }
        }
    });
    
    // Melhorar navegação em cards
    const cards = document.querySelectorAll('.card, .highlight-card, .detalhe-card');
    cards.forEach(card => {
        card.setAttribute('tabindex', '0');
        card.setAttribute('role', 'button');
        
        card.addEventListener('keydown', function(e) {
            // Não interceptar se o foco estiver em um campo de formulário
            const activeElement = document.activeElement;
            const isFormField = activeElement && (
                activeElement.tagName === 'INPUT' || 
                activeElement.tagName === 'TEXTAREA' || 
                activeElement.tagName === 'SELECT' ||
                activeElement.isContentEditable
            );
            
            if (!isFormField && (e.key === 'Enter' || e.key === ' ')) {
                e.preventDefault();
                const link = this.querySelector('a');
                if (link) {
                    link.click();
                }
            }
        });
    });
}

/**
 * Adicionar ARIA labels
 */
function addAriaLabels() {
    // Botões sem texto
    const iconButtons = document.querySelectorAll('button:not([aria-label])');
    iconButtons.forEach(button => {
        const icon = button.querySelector('i');
        if (icon && !button.textContent.trim()) {
            const iconClass = icon.className;
            let label = 'Botão';
            
            if (iconClass.includes('bars')) label = 'Menu';
            else if (iconClass.includes('times')) label = 'Fechar';
            else if (iconClass.includes('search')) label = 'Buscar';
            else if (iconClass.includes('phone')) label = 'Telefone';
            else if (iconClass.includes('envelope')) label = 'E-mail';
            
            button.setAttribute('aria-label', label);
        }
    });
    
    // Links de redes sociais
    const socialLinks = document.querySelectorAll('.social-link');
    socialLinks.forEach(link => {
        const icon = link.querySelector('i');
        if (icon) {
            const iconClass = icon.className;
            let label = 'Rede social';
            
            if (iconClass.includes('facebook')) label = 'Facebook';
            else if (iconClass.includes('instagram')) label = 'Instagram';
            else if (iconClass.includes('youtube')) label = 'YouTube';
            else if (iconClass.includes('twitter') || iconClass.includes('x-twitter')) label = 'X';
            
            link.setAttribute('aria-label', label);
        }
    });
}

/**
 * Gerenciar foco em modais e dropdowns
 */
function manageFocus() {
    // Fechar modais com ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const modal = document.querySelector('.modal.show');
            if (modal) {
                const closeButton = modal.querySelector('.btn-close');
                if (closeButton) {
                    closeButton.click();
                }
            }
        }
    });
}

/**
 * Inicializar animações
 */
function initAnimations() {
    // Animação de fade-in quando elementos entram na viewport
    const animatedElements = document.querySelectorAll('.fade-in-up, .fade-in, .slide-up, .animate-on-scroll');
    
    if ('IntersectionObserver' in window) {
        const animationObserver = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate', 'animated');
                    animationObserver.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });
        
        animatedElements.forEach(el => animationObserver.observe(el));
    } else {
        // Fallback: animar imediatamente
        animatedElements.forEach(el => el.classList.add('animate', 'animated'));
    }
    
    // Adicionar classes de animação automaticamente em elementos comuns
    // EXCETO para elementos dentro do .main-content (para evitar que desapareçam)
    const mainContent = document.querySelector('.main-content');
    
    const sections = document.querySelectorAll('section:not(.hero-section)');
    sections.forEach((section, index) => {
        // Não adicionar animação a seções dentro do main-content
        if (!section.classList.contains('no-animate') && 
            (!mainContent || !mainContent.contains(section))) {
            section.classList.add('fade-in-up');
        } else if (mainContent && mainContent.contains(section)) {
            // Garantir que seções dentro do main-content estejam visíveis
            section.style.opacity = '1';
            section.style.zIndex = '1';
        }
    });
    
    const cards = document.querySelectorAll('.card, .highlight-card, .testimonial-card');
    cards.forEach((card, index) => {
        // Não adicionar animação a cards dentro do main-content
        if (!card.classList.contains('no-animate') && 
            (!mainContent || !mainContent.contains(card))) {
            card.classList.add('fade-in-up');
            // Adicionar delay progressivo
            card.style.animationDelay = `${index * 0.1}s`;
        } else if (mainContent && mainContent.contains(card)) {
            // Garantir que cards dentro do main-content estejam visíveis
            card.style.opacity = '1';
            card.style.zIndex = '1';
        }
    });
    
    // Garantir que o conteúdo principal sempre esteja visível
    if (mainContent) {
        mainContent.style.opacity = '1';
        mainContent.style.zIndex = '1';
        // Remover classes de animação do conteúdo principal e seus filhos diretos
        mainContent.classList.remove('fade-in-up', 'fade-in', 'slide-up', 'animate-on-scroll');
        // Forçar visibilidade de todos os elementos dentro do main-content
        const allChildren = mainContent.querySelectorAll('*');
        allChildren.forEach(child => {
            child.style.opacity = '1';
        });
    }
}

/**
 * Inicializar contadores animados
 */
function initCounters() {
    const counters = document.querySelectorAll('.counter');
    
    if ('IntersectionObserver' in window) {
        const counterObserver = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    counterObserver.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.5
        });
        
        counters.forEach(counter => counterObserver.observe(counter));
    }
}

/**
 * Animar contador
 */
function animateCounter(element) {
    const target = parseInt(element.textContent.replace(/\D/g, ''));
    const duration = 2000; // 2 segundos
    const increment = target / (duration / 16); // 60 FPS
    let current = 0;
    
    const timer = setInterval(function() {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        
        element.textContent = Math.floor(current).toLocaleString('pt-BR');
    }, 16);
}

/**
 * Utilitários
 */

// Debounce function para otimizar eventos
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle function para scroll events
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Verificar se elemento está visível
function isElementVisible(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

// Scroll suave para elemento
function scrollToElement(element, offset = 80) {
    const elementPosition = element.offsetTop - offset;
    window.scrollTo({
        top: elementPosition,
        behavior: 'smooth'
    });
}

// Exportar funções para uso global se necessário
window.PaixaoCristo = {
    scrollToElement,
    isElementVisible,
    debounce,
    throttle
};


