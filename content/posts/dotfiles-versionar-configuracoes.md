---
title: "Dotfiles: A Arte de Versionar o Teu Sistema"
date: 2025-12-19
category: linux
tags: [git, config, terminal, dotfiles]
excerpt: "As tuas configurações são código. Trata-as como tal. Um guia completo para gerir dotfiles com Git."
featured: false
---

Instalaste o sistema. Configuraste o Zsh. Personalizaste o Neovim. Ajustaste o i3. Passaste horas a afinar cada detalhe até ficar perfeito. E depois o disco morre. Ou mudas de máquina. E perdes tudo.

Os **dotfiles** existem para resolver isto.

## O Que São Dotfiles

No Unix, ficheiros de configuração começam tradicionalmente com um ponto: `.bashrc`, `.zshrc`, `.gitconfig`. Isso torna-os "ocultos" por defeito. Daí o nome: *dot*files.

Mas "dotfiles" como prática vai além disto. É a filosofia de tratar as tuas configurações como código fonte. Versiona-las. Documentá-las. Poder replicar o teu setup em qualquer máquina com um único comando.

## Porque é Que Isto Importa

### Portabilidade

Tens um laptop pessoal e um desktop de trabalho. Queres as mesmas configurações em ambos. Sem dotfiles, manténs duas versões separadas que divergem com o tempo. Com dotfiles, fazes `git pull` e tens tudo sincronizado.

### Backup Automático

Os teus dotfiles vivem num repositório Git, provavelmente no GitHub. São, por natureza, um backup distribuído. Mesmo que percas todas as tuas máquinas, as configs sobrevivem.

### Histórico de Alterações

Fizeste uma alteração no `.zshrc` que partiu qualquer coisa? Com Git, fazes `git log` para ver o que mudou e `git revert` para desfazer.

### Onboarding Rápido

Máquina nova? Clone, script de setup, e em minutos tens o teu ambiente completo.

## A Estrutura Fundamental

A abordagem mais simples: um repositório Git com os ficheiros de configuração.

```
~/dotfiles/
├── .bashrc
├── .zshrc
├── .gitconfig
├── .tmux.conf
├── nvim/
│   └── init.lua
└── README.md
```

O problema: estes ficheiros precisam de estar em sítios específicos. O `.zshrc` tem de estar em `~/.zshrc`. O Neovim espera a config em `~/.config/nvim/`.

A solução: **symlinks**.

## Symlinks: O Elo de Ligação

Um symlink é uma referência. Aponta de um local para outro. Para o sistema, é transparente.

```bash
# Cria symlink do repositório para o local esperado
ln -sf ~/dotfiles/.zshrc ~/.zshrc
ln -sf ~/dotfiles/nvim ~/.config/nvim
```

O `-s` cria um link simbólico. O `-f` força, substituindo se já existir.

Agora editas `~/dotfiles/.zshrc`, e as alterações refletem-se em `~/.zshrc`. Podes fazer commit, push, e ter a mesma config em qualquer máquina.

## GNU Stow: Automatização Elegante

Criar symlinks manualmente não escala. O **GNU Stow** automatiza isto.

```bash
sudo pacman -S stow  # Arch
sudo apt install stow  # Debian/Ubuntu
```

O Stow trata directórios como "pacotes". Cada subdirectório representa um programa. A estrutura interna espelha onde os ficheiros devem ir relativamente ao home.

```
~/dotfiles/
├── zsh/
│   └── .zshrc
├── git/
│   └── .gitconfig
├── tmux/
│   └── .tmux.conf
└── nvim/
    └── .config/
        └── nvim/
            └── init.lua
```

Repara: `nvim/.config/nvim/init.lua`. O Stow vai criar o symlink em `~/.config/nvim/init.lua`.

### Instalação de Pacotes

```bash
cd ~/dotfiles

# Instala um pacote específico
stow zsh

# Instala vários
stow zsh git tmux nvim

# Instala todos
stow */
```

### Remoção

```bash
stow -D zsh  # Remove os symlinks do pacote zsh
```

<div class="callout">
    <div class="callout-icon">&gt;</div>
    <div class="callout-content">
        <strong>Dica:</strong> Se já existir um ficheiro onde o Stow quer criar o symlink, ele avisa-te. Usa <code>--adopt</code> para absorver o ficheiro existente para o repositório.
    </div>
</div>

## Bare Git Repository (Alternativa)

Se preferes uma abordagem sem dependências externas, podes usar um repositório Git "bare".

### Setup Inicial

```bash
# Cria o repositório bare
git init --bare $HOME/.dotfiles

# Alias para interagir com ele
alias config='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'

# Não mostrar ficheiros untracked
config config --local status.showUntrackedFiles no
```

Adiciona o alias ao `.zshrc`:

```bash
alias config='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
```

### Uso Diário

```bash
config add .zshrc
config commit -m "Add zsh config"
config push
```

Os ficheiros ficam nos locais correctos directamente, sem symlinks.

## O Repositório

Inicializa e faz push:

```bash
cd ~/dotfiles
git init
git add .
git commit -m "Initial dotfiles setup"
git remote add origin git@github.com:username/dotfiles.git
git push -u origin main
```

### O README

Um bom README documenta:
- O que está incluído
- Dependências do sistema
- Instruções de instalação

```markdown
# Dotfiles

Configurações para Arch Linux + Zsh + Neovim.

## Instalação

\`\`\`bash
git clone git@github.com:username/dotfiles.git ~/dotfiles
cd ~/dotfiles
stow */
\`\`\`

## Dependências

- zsh
- neovim >= 0.9
- tmux
- ripgrep
```

## Configurações Sensíveis

**Nunca faças commit de passwords, tokens, ou chaves privadas.**

Para valores sensíveis, usa ficheiros separados:

```bash
# .zshrc
source ~/.secrets  # Este ficheiro NÃO está no dotfiles
```

Adiciona ao `.gitignore`:

```
.secrets
*.key
*.pem
```

## Script de Bootstrap

Para máquinas novas, um script que automatiza tudo:

```bash
#!/bin/bash
# install.sh
set -e

echo "=== Dotfiles Installation ==="

# Detecta distro
if command -v pacman &> /dev/null; then
    PKG="sudo pacman -S --needed --noconfirm"
elif command -v apt &> /dev/null; then
    PKG="sudo apt install -y"
else
    echo "Package manager not supported"
    exit 1
fi

# Dependências
echo "Installing dependencies..."
$PKG git stow zsh neovim tmux

# Clone
if [ ! -d "$HOME/dotfiles" ]; then
    git clone git@github.com:username/dotfiles.git ~/dotfiles
fi

cd ~/dotfiles

# Backup de conflitos
mkdir -p ~/dotfiles-backup
for item in ~/.zshrc ~/.gitconfig ~/.tmux.conf; do
    if [ -e "$item" ] && [ ! -L "$item" ]; then
        mv "$item" ~/dotfiles-backup/
    fi
done

# Stow
for dir in */; do
    stow "${dir%/}"
done

# Muda shell
chsh -s $(which zsh)

echo "=== Done! Restart your terminal. ==="
```

## Configurações por Máquina

Se tens máquinas diferentes, usa condicionais:

```bash
# .zshrc
case $(hostname) in
    work-laptop)
        source ~/.work-aliases
        export HTTP_PROXY="http://proxy.company.com:8080"
        ;;
    home-desktop)
        alias sync-music='rsync -av ~/Music nas:/media/music'
        ;;
esac

# Por SO
if [[ "$OSTYPE" == "darwin"* ]]; then
    export PATH="/opt/homebrew/bin:$PATH"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    alias open='xdg-open'
fi
```

## Estrutura Madura

Depois de alguns anos:

```
~/dotfiles/
├── alacritty/
├── git/
├── nvim/
├── scripts/
├── tmux/
├── zsh/
├── .gitignore
├── install.sh
├── Makefile
└── README.md
```

O `Makefile`:

```makefile
.PHONY: install uninstall update

install:
	@./install.sh

uninstall:
	@for dir in */; do stow -D "$${dir%/}"; done

update:
	@git pull
	@for dir in */; do stow -R "$${dir%/}"; done
```

## O Investimento

Configurar dotfiles demora tempo. Mas é tempo investido, não gasto.

Na próxima vez que reinstalares o sistema, serão 10 minutos em vez de um dia. Na próxima vez que mudares de máquina, não terás que lembrar-te de como tinhas aquele alias configurado.

Os teus dotfiles são a tua assinatura digital. O reflexo de anos de ajustes e preferências. Merecem ser tratados com o mesmo rigor que o código que escreves.
