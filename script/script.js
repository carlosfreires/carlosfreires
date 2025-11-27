// Elementos DOM
const elements = {
    langSelect: document.getElementById('languageSelect'),
    themeToggle: document.getElementById('themeToggle'),
    navLinks: document.querySelector('.nav-links'),
    mobileBtn: document.querySelector('.mobile-menu-btn'),
    skillsContainer: document.getElementById('skillsContainer'),
    projectsContainer: document.getElementById('projectsContainer'),
    docsContainer: document.getElementById('docsContainer'),
    contactContainer: document.getElementById('contactContainer')
};

let currentLang = 'pt';
let translations = {};
let skillsData = [];
let projectsData = [];
let docsData = [];
let contactsData = [];

// Inicialização
async function init() {
    await loadData();
    renderSkills();
    renderProjects();
    renderDocs();
    renderContacts();
    updateLanguage(currentLang);
    setupEventListeners();
}

// Carregar dados dos arquivos JSON
async function loadData() {
    try {
        // Carregar traduções
        const langResponse = await fetch(`data/languages/${currentLang}.json`);
        translations = await langResponse.json();
        
        // Carregar outros dados
        const [skillsResponse, projectsResponse, docsResponse, contactsResponse] = await Promise.all([
            fetch('data/skills.json'),
            fetch('data/projects/projects.json'),
            fetch('data/documents/documents.json'),
            fetch('data/external/external.json')
        ]);
        
        skillsData = await skillsResponse.json();
        projectsData = await projectsResponse.json();
        docsData = await docsResponse.json();
        contactsData = await contactsResponse.json();
    } catch (error) {
        console.error('Erro ao carregar dados:', error);
    }
}

// Event Listeners
function setupEventListeners() {
    // Troca de Idioma
    elements.langSelect.addEventListener('change', async (e) => {
        currentLang = e.target.value;
        await loadData();
        updateLanguage(currentLang);
        renderProjects(); // Re-renderizar projetos pois as descrições mudam
    });

    // Troca de Tema
    elements.themeToggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTheme);
        
        const icon = elements.themeToggle.querySelector('i');
        icon.className = newTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
        
        // Salvar preferência no localStorage
        localStorage.setItem('theme', newTheme);
    });

    // Menu Mobile
    elements.mobileBtn.addEventListener('click', () => {
        elements.navLinks.classList.toggle('active');
    });

    // Fechar menu mobile ao clicar em um link
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            elements.navLinks.classList.remove('active');
        });
    });
}

// Função i18n
function updateLanguage(lang) {
    const t = translations;
    
    // Busca todos elementos com data-i18n
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        // Navega no objeto de tradução (ex: nav.home)
        const value = key.split('.').reduce((obj, k) => obj && obj[k], t);
        if (value) el.textContent = value;
    });

    // Atualiza select
    elements.langSelect.value = lang;
    document.documentElement.lang = lang === 'zh' ? 'zh-CN' : lang;
}

// Renderizadores Dinâmicos
function renderSkills() {
    elements.skillsContainer.innerHTML = skillsData.map(group => `
        <div class="skill-category">
            <h3>${group.category}</h3>
            <div class="skill-list">
                ${group.items.map(item => `<span class="skill-tag">${item}</span>`).join('')}
            </div>
        </div>
    `).join('');
}

function renderProjects() {
    const btnText = translations.buttons;
    
    elements.projectsContainer.innerHTML = projectsData.map(proj => `
        <article class="project-card">
            <div class="project-content">
                <span class="project-category">${proj.category}</span>
                <h3 class="project-title">${proj.name}</h3>
                <p class="project-desc">${proj.desc[currentLang] || proj.desc.pt}</p>
                <div class="skill-list" style="margin-bottom: 1rem;">
                    ${proj.tech.map(t => `<span class="skill-tag" style="font-size: 0.75rem; padding: 0.2rem 0.6rem;">${t}</span>`).join('')}
                </div>
                <div class="project-links">
                    <a href="${proj.links.github}" class="icon-link" aria-label="GitHub Repo" target="_blank"><i class="fab fa-github"></i></a>
                    <a href="${proj.links.live}" class="icon-link" aria-label="Live Demo" target="_blank"><i class="fas fa-external-link-alt"></i></a>
                </div>
            </div>
        </article>
    `).join('');
}

function renderDocs() {
    const btnText = translations.buttons;
    elements.docsContainer.innerHTML = docsData.map(doc => `
        <div class="doc-item">
            <div>
                <strong>${doc.name}</strong>
                <span style="font-size: 0.8rem; color: var(--text-secondary); margin-left: 0.5rem;">(${doc.size})</span>
            </div>
            <a href="${doc.url}" class="btn" style="padding: 0.4rem 1rem; font-size: 0.9rem;" download>
                <i class="fas fa-download"></i> ${btnText.download}
            </a>
        </div>
    `).join('');
}

function renderContacts() {
    elements.contactContainer.innerHTML = contactsData.map(contact => `
        <a href="${contact.link}" class="contact-btn" target="_blank" rel="noopener noreferrer">
            <i class="${contact.icon}"></i>
            <span>${contact.name}</span>
        </a>
    `).join('');
}

// Aplicar tema salvo ao carregar
function applySavedTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
        const icon = elements.themeToggle.querySelector('i');
        icon.className = savedTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
}

// Iniciar App
document.addEventListener('DOMContentLoaded', () => {
    applySavedTheme();
    init();
});