---
title: "Título do Post (Claro e Essencialista)"
date: 2025-12-19
category: linux
tags: [tutorial, config, exemplo]
excerpt: "Uma frase curta que resume o post para o card do blog. Máximo 2 linhas."
featured: false
---

Introdução direta ao ponto. O texto deve ser técnico mas acessível.

## Estrutura e Títulos

Usa `##` para tópicos principais. O texto deve fluir logicamente.

### Subtópicos

Usa `###` para detalhar pontos específicos dentro de um tópico.

## Formatação de Texto

- **Negrito** para ênfase (não abuses).
- *Itálico* para termos estrangeiros ou subtis.
- `Código inline` para comandos, caminhos de ficheiros ou atalhos.

## Blocos de Código

Sempre especifica a linguagem para o highlight funcionar (Prism.js).

```bash
# Comentários explicativos
sudo pacman -S neovim
```

```python
def exemplo():
    return "Simples e limpo"
```

## Listas

### Não Ordenada
- Ponto 1
- Ponto 2
  - Subponto

### Ordenada
1. Primeiro passo
2. Segundo passo

## Tabelas (Estilo Terminal)

Usa tabelas para comparar dados. Elas serão renderizadas com estilo minimalista/terminal.

| Ferramenta | Função | Categoria |
| :--- | :--- | :--- |
| Neovim | Editor | CLI |
| Docker | Containers | DevOps |
| Zsh | Shell | Sistema |

## Callouts

Como o Markdown padrão não tem "admonitions", usamos HTML simples com um ícone de texto `>`.

<div class="callout">
    <div class="callout-icon">&gt;</div>
    <div class="callout-content">
        <strong>Nota:</strong>
        Isto é um callout padrão. O ícone é apenas um caracter.
    </div>
</div>

## Imagens

Usa caminhos relativos ou URLs externos. Adiciona sempre texto alternativo.

![Configuração final do terminal](../assets/placeholder.png)
*Legenda opcional em itálico por baixo da imagem.*

## Conclusão

Termina com uma reflexão ou resumo.
