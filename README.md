# zero()

> O cursor piscando no terminal vazio. O ponto de partida.

Blog minimalista sobre tecnologia, Linux e programação. Escrito por alguém que prefere configurar o `.bashrc` a scrollar feeds infinitos.

**Live:** [mefrraz.github.io/zero](https://mefrraz.github.io/zero)

---

## O que é isto

Um blog estático. Sem frameworks pesados, sem analytics invasivos, sem cookies desnecessários. Apenas HTML, CSS e um script Python que converte Markdown em páginas.

A estética segue a filosofia "The Void": fundo escuro, verde neon como destaque, blobs difusos como ambientação. O design respira.

## Estrutura

```
zero/
├── content/posts/     # Posts em Markdown
├── posts/             # HTML gerado
├── categories/        # Páginas de categoria
├── build.py           # Converte tudo
├── style.css          # Estilos globais
└── setup.sh           # Setup e push inicial
```

## Como funciona

### Criar um post

```bash
python new_post.py "Título do Post" categoria
```

Edita o ficheiro em `content/posts/`. O frontmatter define os metadados:

```yaml
---
title: "Título do Post"
date: 2025-12-19
category: linux
tags: [arch, terminal]
excerpt: "Resumo curto."
featured: false
---
```

### Build

```bash
python build.py
```

O script:
- Converte Markdown para HTML
- Atualiza listagem do blog
- Gera páginas de categoria
- Cria RSS feed e sitemap

### Deploy

```bash
./deploy.sh
```

Faz commit de tudo e push para o GitHub Pages.

## Categorias

| Slug | Tema |
| :--- | :--- |
| `linux` | Distribuições, configs, terminal |
| `devops` | CI/CD, automação, infra |
| `git` | Controlo de versões |
| `python` | Scripts, frameworks |
| `web` | Frontend, CSS, HTML |
| `ia` | Machine Learning, LLMs |
| `vida` | Reflexões, minimalismo digital |
| `geral` | O resto |

## Dependências

```bash
pip install python-frontmatter markdown
```

Ou com ambiente virtual:

```bash
python -m venv .venv
.venv/bin/pip install python-frontmatter markdown
```

## Stack

- **Geração:** Python + Markdown
- **Estilo:** CSS vanilla, sem Tailwind
- **Hosting:** GitHub Pages
- **Tipografia:** Outfit + JetBrains Mono
- **Filosofia:** Menos é mais

---

*"O zero é a origem."*
