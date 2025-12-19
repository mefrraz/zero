# zero() Blog - Instruções para Continuar o Projeto

## 🎯 Contexto

Este é um blog pessoal minimalista chamado **zero()**. A **Fase 1 (Interface)** está **COMPLETA**. Todas as páginas HTML e estilos CSS estão prontos. Agora precisamos da **Fase 2: Automação**.

---

## ✅ O Que Já Existe

```
zero()/
├── index.html              # Homepage (funcional)
├── blog.html               # Lista de posts com pesquisa
├── projetos.html           # Projetos GitHub com accordion
├── sobre.html              # Página sobre
├── 404.html                # Erro 404
├── style.css               # Estilos globais
├── components.js           # Header/Footer dinâmico + tema
├── posts/
│   └── linux-pela-quinta-vez.html  # ⭐ TEMPLATE DE POST
├── categories/
│   └── *.html              # Páginas de categoria
└── assets/
    └── *.png               # Blobs decorativos
```

**IMPORTANTE:** O ficheiro `posts/linux-pela-quinta-vez.html` serve como **template** para novos posts.

---

## 🚀 Fase 2: O Que Criar

### 1. Estrutura de Conteúdo

Criar as seguintes pastas:

```bash
mkdir -p content/posts
mkdir -p assets/posts
```

### 2. Build Script (`build.py`)

Criar um script Python que:

#### Entrada:
- Ficheiros `.md` em `content/posts/` com frontmatter YAML:

```markdown
---
title: "Título do Post"
date: 2025-12-17
category: linux
tags: [arch, wayland]
excerpt: "Resumo para listagem"
---

Conteúdo em Markdown aqui...
```

#### Saída:
1. **Posts HTML** em `posts/` usando o template existente
2. **`blog.html`** atualizado com lista de todos os posts
3. **Navegação automática** (anterior/próximo) baseada na data
4. **Cálculo automático** do tempo de leitura (palavras ÷ 200)
5. **Páginas de categoria** atualizadas (`categories/category-*.html`)
6. **Homepage** atualizada com os 3 posts mais recentes
7. **`feed.xml`** RSS feed
8. **`sitemap.xml`** para SEO

#### Lógica do Script:

```python
# Pseudocódigo
1. Ler todos os .md de content/posts/
2. Parsear frontmatter YAML
3. Converter Markdown para HTML
4. Ordenar posts por data (mais recente primeiro)
5. Para cada post:
   - Calcular tempo de leitura
   - Identificar post anterior e próximo
   - Substituir placeholders no template
   - Guardar em posts/
6. Gerar blog.html com cards de todos os posts
7. Agrupar posts por categoria
8. Para cada categoria:
   - Gerar/atualizar categories/category-{nome}.html
9. Atualizar index.html com os 3 posts mais recentes
10. Gerar feed.xml e sitemap.xml
```

### Frontmatter Opcional: Destaque

O frontmatter pode incluir `featured: true` para marcar como destaque:

```markdown
---
title: "Post em Destaque"
date: 2025-12-17
category: linux
featured: true
excerpt: "Este post aparece em destaque na homepage"
---
```

Se `featured: true`, o post aparece como card grande na homepage. Caso contrário, usa o post mais recente.

### 3. Template de Post (já existe)

O template em `posts/linux-pela-quinta-vez.html` tem estas secções que o script deve preencher:

| Classe/ID | O Que Inserir |
|-----------|---------------|
| `<title>` | Título do post |
| `<meta description>` | Excerpt |
| `.post-category` | Categoria (link) |
| `.post-date` | Data formatada |
| `.reading-time` | "X min de leitura" |
| `.post-hero-title` | Título principal |
| `.post-hero-excerpt` | Excerpt/subtítulo |
| `.article-body` | Conteúdo HTML convertido do Markdown |
| `.post-navigation` | Links anterior/próximo |

### 4. Navegação Anterior/Próximo

**IMPORTANTE:** A navegação NÃO é por data. É pela **ordem de criação dos ficheiros** (ordem alfabética dos nomes de ficheiro ou ordem em que aparecem na pasta).

- **Anterior** = post criado antes (ficheiro anterior na lista)
- **Próximo** = post criado depois (ficheiro seguinte na lista)

Se não houver anterior ou próximo, **esconder** o link respetivo (não mostrar a `<nav>` vazia).

O template já tem esta estrutura:

```html
<nav class="post-navigation">
    <a href="POST_ANTERIOR.html" class="post-nav-link prev">
        <span class="nav-label">← Anterior</span>
        <span class="nav-title">TÍTULO_ANTERIOR</span>
    </a>
    <a href="POST_PROXIMO.html" class="post-nav-link next">
        <span class="nav-label">Próximo →</span>
        <span class="nav-title">TÍTULO_PRÓXIMO</span>
    </a>
</nav>
```

---

## 📝 Exemplo Completo de Post Markdown

Criar `content/posts/exemplo-completo.md`:

```markdown
---
title: "Guia Completo: Configurar Neovim do Zero"
date: 2025-12-17
category: linux
tags: [neovim, dotfiles, terminal, produtividade]
excerpt: "Um tutorial passo-a-passo para transformar o Neovim num IDE completo, sem plugins pesados."
featured: false
---

Depois de anos a saltar entre IDEs, finalmente encontrei paz no Neovim. Neste guia, vou mostrar exactamente como configurei tudo.

## Porquê Neovim?

O Neovim é **rápido**, **leve** e **infinitamente personalizável**. Ao contrário do VS Code, não precisa de um browser inteiro a correr em segundo plano.

> **Nota:** Este guia assume que já tens Neovim instalado. Se não, corre `sudo pacman -S neovim` no Arch.

## Estrutura de Configuração

A minha configuração vive em `~/.config/nvim/`:

```bash
nvim/
├── init.lua          # Ponto de entrada
├── lua/
│   ├── plugins.lua   # Gestão de plugins
│   ├── keymaps.lua   # Atalhos de teclado
│   └── options.lua   # Configurações gerais
```

## Configuração Base

Primeiro, criamos o ficheiro de opções:

```lua
-- lua/options.lua
local opt = vim.opt

opt.number = true           -- Números de linha
opt.relativenumber = true  -- Números relativos
opt.tabstop = 4            -- Tabs de 4 espaços
opt.shiftwidth = 4
opt.expandtab = true       -- Espaços em vez de tabs
opt.smartindent = true
opt.termguicolors = true   -- Cores de 24-bit
opt.clipboard = "unnamedplus"  -- Clipboard do sistema
```

## Plugins Essenciais

Uso o **lazy.nvim** como gestor de plugins:

```lua
-- lua/plugins.lua
return {
    { "folke/tokyonight.nvim" },      -- Tema
    { "nvim-treesitter/nvim-treesitter" },  -- Syntax highlighting
    { "neovim/nvim-lspconfig" },      -- LSP
}
```

## Atalhos Personalizados

Alguns atalhos que uso diariamente:

| Atalho | Acção |
|--------|-------|
| `<leader>w` | Guardar ficheiro |
| `<leader>q` | Sair |
| `<leader>ff` | Procurar ficheiros |
| `<leader>fg` | Grep no projecto |

```lua
-- lua/keymaps.lua
vim.g.mapleader = " "
local keymap = vim.keymap.set

keymap("n", "<leader>w", ":w<CR>")
keymap("n", "<leader>q", ":q<CR>")
```

## Resultado Final

![Screenshot do Neovim configurado](screenshot-neovim.png)

Após seguir este guia, terás um editor que:

- ✅ Abre instantaneamente
- ✅ Tem syntax highlighting avançado
- ✅ Suporta LSP para autocomplete
- ✅ Usa atalhos personalizados

## Próximos Passos

No próximo post, vou cobrir como configurar o **LSP** para diferentes linguagens e adicionar **debugging** integrado.

---

*Se tiveres dúvidas, encontra-me no [GitHub](https://github.com/mefrraz) ou [Reddit](https://reddit.com/u/frraz_me).*
```

Este exemplo demonstra:
- ✅ Frontmatter completo
- ✅ Parágrafos e formatação
- ✅ Citação/callout (`>`)
- ✅ Blocos de código com linguagem
- ✅ Tabela
- ✅ Lista de verificação
- ✅ Imagem com alt text
- ✅ Links

---

## 🎨 Cores (Referência)

### Modo Escuro
- Fundo: `#000D17`
- Cards: `#172940`
- Accent: `#08F42A` (verde neon)

### Modo Claro
- Fundo: `#FFFFFF`
- Cards: `#f0eee9`
- Accent: `#C33399` (rosa)

---

## ✅ Checklist de Implementação

- [ ] Criar `content/posts/` e `assets/posts/`
- [ ] Criar `build.py` com:
  - [ ] Parser de Markdown com frontmatter
  - [ ] Conversão MD → HTML
  - [ ] Cálculo de tempo de leitura
  - [ ] Navegação anterior/próximo automática
  - [ ] Geração de `blog.html`
  - [ ] Geração de `feed.xml`
  - [ ] Geração de `sitemap.xml`
- [ ] Testar com 2-3 posts de exemplo
- [ ] Documentar uso do script

---

## 💡 Dependências Python Sugeridas

```bash
pip install markdown pyyaml python-frontmatter
```

---

**NOTA:** Não modificar os ficheiros HTML/CSS existentes a não ser que seja estritamente necessário. A interface está completa.
