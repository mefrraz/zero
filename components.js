function loadHeader() {
    // Detect if we're in a subfolder
    const path = window.location.pathname;
    const inSubfolder = path.includes('/posts/') || path.includes('/categories/');
    const base = inSubfolder ? '../' : '';

    const headerHTML = `
    <header class="site-header">
        <a href="${base}index.html" class="logo">zero<span>()</span></a>
        <nav class="nav-links">
            <a href="${base}index.html">Início</a>
            <a href="${base}blog.html">Blog</a>
            <a href="${base}projetos.html">Projetos</a>
            <a href="${base}sobre.html">Sobre</a>
        </nav>
        <div class="header-actions">
            <button class="theme-toggle" aria-label="Toggle theme" title="Alternar tema">
                <svg class="theme-icon sun-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="5"></circle>
                    <line x1="12" y1="1" x2="12" y2="3"></line>
                    <line x1="12" y1="21" x2="12" y2="23"></line>
                    <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                    <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                    <line x1="1" y1="12" x2="3" y2="12"></line>
                    <line x1="21" y1="12" x2="23" y2="12"></line>
                    <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                    <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
                </svg>
                <svg class="theme-icon moon-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
                </svg>
            </button>
            <button class="mobile-menu-toggle" aria-label="Toggle menu">
                <span class="hamburger-line"></span>
                <span class="hamburger-line"></span>
                <span class="hamburger-line"></span>
            </button>
        </div>
    </header>
    <nav class="mobile-nav">
        <a href="${base}index.html">Início</a>
        <a href="${base}blog.html">Blog</a>
        <a href="${base}projetos.html">Projetos</a>
        <a href="${base}sobre.html">Sobre</a>
    </nav>
    `;

    const placeholder = document.getElementById('header-placeholder');
    if (placeholder) {
        placeholder.innerHTML = headerHTML;
        highlightActiveLink();
        setupMobileMenu();
        setupThemeToggle();
    }
}

function setupThemeToggle() {
    const toggle = document.querySelector('.theme-toggle');

    // Load saved theme
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);

    toggle?.addEventListener('click', () => {
        const current = document.documentElement.getAttribute('data-theme');
        const next = current === 'light' ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('theme', next);
    });
}

function highlightActiveLink() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-links a, .mobile-nav a');

    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');

        let isActive = false;

        // Check exact match or trailing match
        if (currentPath.endsWith(linkPath)) {
            isActive = true;
        }
        // Handle root path aliasing to index.html
        else if ((currentPath === '/' || currentPath.endsWith('/')) && linkPath === 'index.html') {
            isActive = true;
        }

        if (isActive) {
            link.style.color = 'var(--c-text-main)';
        } else {
            link.style.color = '';
        }
    });
}

function setupMobileMenu() {
    const toggle = document.querySelector('.mobile-menu-toggle');
    const mobileNav = document.querySelector('.mobile-nav');

    if (toggle && mobileNav) {
        toggle.addEventListener('click', () => {
            mobileNav.classList.toggle('active');
            toggle.classList.toggle('active');
        });
    }
}

function loadFooter() {
    const currentYear = new Date().getFullYear();
    const footerHTML = `
    <footer class="site-footer">
        <p>&copy; ${currentYear} zero(). Feito com <span style="color: var(--c-accent)">♥</span> e HTML estático.</p>
    </footer>
    `;

    const placeholder = document.getElementById('footer-placeholder');
    if (placeholder) {
        placeholder.innerHTML = footerHTML;
    }
}
