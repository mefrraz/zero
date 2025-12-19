---
title: "Tmux: O Terminal Dentro do Terminal"
date: 2025-12-19
category: tools
tags: [terminal, produtividade, linux]
excerpt: "Porque é que um terminal não chega. Guia completo do tmux: desde os fundamentos até configurações avançadas."
featured: false
---

Tens o terminal aberto. Um processo a correr. Precisas de fazer outra coisa. Abres outro terminal. E outro. E outro. Tabs a multiplicar-se como coelhos. A cada reinício, perdes tudo. Liga-te a um servidor por SSH, a conexão cai, e o processo que estava a correr morre com ela.

Há uma forma melhor. E chama-se **tmux**.

## O Problema Real

O terminal tradicional tem uma limitação fundamental: uma janela, um contexto. Fecha-a e o processo morre. Desliga-te de um servidor remoto e perdes a sessão. É efémero por natureza.

Isto não era um problema quando usavas o terminal para comandos rápidos. Mas quando o terminal se torna o teu ambiente de trabalho principal, quando tens um editor, um servidor de desenvolvimento, logs, e uma shell de comandos todos a correr simultaneamente, a limitação torna-se insuportável.

O **tmux** (terminal multiplexer) resolve isto de forma elegante. Cria uma camada de abstração entre ti e o terminal. As tuas sessões vivem independentemente da janela que as mostra. São processos do sistema, não da aplicação de terminal.

Pensa nisto assim: o tmux é um gestor de janelas para o terminal. Tal como o i3 ou o Sway gerem as tuas janelas gráficas, o tmux gere as tuas sessões de terminal.

## Conceitos Fundamentais

Antes de meter as mãos na massa, precisas de entender três conceitos que formam a hierarquia do tmux:

| Conceito | Descrição | Analogia |
| :--- | :--- | :--- |
| Session | Um workspace completo. Pode ter múltiplas janelas. Persiste mesmo que te desligues. | Um desktop virtual |
| Window | Uma tab dentro da sessão. Ocupa o ecrã inteiro. | Uma janela maximizada |
| Pane | Uma divisão dentro de uma janela. Dois ou mais terminais lado a lado. | Split screen |

A hierarquia é: **Session > Window > Pane**

Uma sessão pode ter muitas janelas. Cada janela pode ter muitos panes. Todas as sessões persistem enquanto o servidor tmux estiver a correr, independentemente de teres alguma janela de terminal aberta ou não.

Este último ponto é crucial. Quando "sais" do tmux, não estás a fechar nada. Estás a desconectar-te de uma sessão que continua a existir. O servidor de desenvolvimento continua a correr. O ficheiro continua aberto no vim. Tudo à tua espera.

## Instalação

```bash
# Arch Linux
sudo pacman -S tmux

# Debian/Ubuntu
sudo apt install tmux

# Fedora
sudo dnf install tmux

# macOS (com Homebrew)
brew install tmux
```

Verifica a instalação:

```bash
tmux -V
# tmux 3.4
```

## Os Primeiros Passos

### Criar uma Sessão

O comando mais básico:

```bash
tmux
```

Isto cria uma sessão anónima. Funciona, mas não é ideal. Prefere sempre criar sessões com nome:

```bash
tmux new-session -s trabalho
```

Ou a forma abreviada:

```bash
tmux new -s trabalho
```

O `-s` define o nome da sessão. Nomes são importantes. Quando tens várias sessões (e vais ter), precisas de as distinguir.

### O Prefixo

Agora estás dentro do tmux. Parece um terminal normal. Quase é. A diferença está nos atalhos.

<div class="callout">
    <div class="callout-icon">&gt;</div>
    <div class="callout-content">
        <strong>Conceito Fundamental:</strong> Todos os comandos dentro do tmux começam com um <strong>prefixo</strong>. Por defeito é <code>Ctrl+b</code>. Carregas no prefixo, <em>largas</em>, e depois carregas na tecla do comando. Não é uma combinação simultânea.
    </div>
</div>

Por exemplo, para criar uma nova janela: `Ctrl+b` (larga) `c`.

Este prefixo pode parecer estranho. E é. Mais à frente vamos mudá-lo para algo mais ergonómico. Mas por agora, vamos usá-lo para aprendermos os comandos.

### Comandos Essenciais de Janelas

| Atalho | Ação |
| :--- | :--- |
| `Ctrl+b c` | Criar nova janela |
| `Ctrl+b ,` | Renomear janela atual |
| `Ctrl+b n` | Próxima janela |
| `Ctrl+b p` | Janela anterior |
| `Ctrl+b 0-9` | Ir para janela pelo número |
| `Ctrl+b w` | Lista interativa de janelas |
| `Ctrl+b &` | Fechar janela atual (com confirmação) |

A barra de estado no fundo mostra as janelas activas. Um asterisco marca a janela actual.

### Comandos Essenciais de Panes

| Atalho | Ação |
| :--- | :--- |
| `Ctrl+b %` | Dividir verticalmente (lado a lado) |
| `Ctrl+b "` | Dividir horizontalmente (um em cima do outro) |
| `Ctrl+b setas` | Navegar entre panes |
| `Ctrl+b o` | Próximo pane (rotação) |
| `Ctrl+b z` | Zoom no pane actual (toggle) |
| `Ctrl+b x` | Fechar pane atual (com confirmação) |
| `Ctrl+b {` | Mover pane para a esquerda |
| `Ctrl+b }` | Mover pane para a direita |
| `Ctrl+b Ctrl+setas` | Redimensionar pane |

O zoom (`Ctrl+b z`) é particularmente útil. Amplia o pane actual para ocupar toda a janela. Carrega outra vez para voltar ao layout anterior.

### Detach e Attach

O poder real do tmux está na capacidade de desanexar e reanexar sessões.

```bash
# Dentro do tmux: desanexar
Ctrl+b d

# Fora do tmux: ver sessões activas
tmux ls

# Reanexar a uma sessão específica
tmux attach -t trabalho

# Ou a forma abreviada
tmux a -t trabalho
```

Quando fazes `detach`, sais do tmux mas tudo continua a correr. Podes fechar o terminal. Podes desligar o computador (se for um servidor remoto). A sessão persiste.

Isto é transformador para trabalho remoto. Ligas-te por SSH, fazes attach à sessão, trabalhas. A conexão cai? Liga-te outra vez e faz attach. Está tudo exactamente como deixaste.

## O Workflow Real

Vamos ver como isto se traduz num dia de trabalho real.

### Sessão de Desenvolvimento

Estás a trabalhar num projecto. Crias uma sessão dedicada:

```bash
tmux new -s meu-projeto
```

**Janela 1 - Editor:** Abres o neovim com o projecto.

```bash
nvim .
```

**Janela 2 - Servidor:** `Ctrl+b c` para nova janela. Arranques o servidor de desenvolvimento.

```bash
npm run dev
```

**Janela 3 - Testes:** `Ctrl+b c`. Corres os testes em modo watch.

```bash
npm run test:watch
```

**Janela 4 - Shell:** `Ctrl+b c`. Uma shell livre para git, comandos diversos.

Agora navegas entre elas com `Ctrl+b n` ou `Ctrl+b p`. Ou directamente com `Ctrl+b 1`, `Ctrl+b 2`, etc.

### Sessões Múltiplas

Estás a meio deste projecto quando surge algo urgente noutro. Não precisas de fechar nada.

```bash
# Detach (ou usa Ctrl+b d)
Ctrl+b d

# Cria nova sessão para o urgente
tmux new -s emergencia

# Trabalhas no urgente...

# Quando acabares, volta ao projecto original
Ctrl+b d
tmux a -t meu-projeto
```

Tudo está como deixaste. O servidor ainda a correr. Os testes ainda em watch. O ficheiro aberto no editor exactamente na mesma linha.

### Panes para Contexto

Dentro de uma janela, às vezes precisas de ver várias coisas simultaneamente. É aqui que os panes brilham.

Exemplo: debugging. Divide a janela:
- Pane esquerdo: código (vim)
- Pane direito superior: logs do servidor
- Pane direito inferior: comandos curl para testar

```bash
# Começas com o editor
nvim app.py

# Divide verticalmente
Ctrl+b %

# No novo pane, segue os logs
tail -f /var/log/app.log

# Divide o pane direito horizontalmente
Ctrl+b "

# Agora tens 3 panes
```

O `Ctrl+b z` permite fazer zoom num pane quando precisas de mais espaço, e voltar ao layout com outro `Ctrl+b z`.

## Configuração

O tmux é altamente configurável. O ficheiro de configuração vive em `~/.tmux.conf`.

### Configuração Base Recomendada

```bash
# ~/.tmux.conf

# ========================================
# Prefixo
# ========================================
# Ctrl+b é difícil de alcançar. Ctrl+a é mais natural.
unbind C-b
set -g prefix C-a
bind C-a send-prefix

# ========================================
# Comportamento Geral
# ========================================
# Começar a contar janelas e panes de 1, não de 0
set -g base-index 1
setw -g pane-base-index 1

# Renumerar janelas quando uma é fechada
set -g renumber-windows on

# Histórico maior
set -g history-limit 50000

# Tempo de display de mensagens (ms)
set -g display-time 4000

# Refresh da barra de estado mais frequente
set -g status-interval 5

# Foco de eventos (útil para vim)
set -g focus-events on

# Modo vi para copy mode
setw -g mode-keys vi

# ========================================
# Divisões (Splits) Mais Intuitivas
# ========================================
# | para vertical, - para horizontal
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"
unbind '"'
unbind %

# O -c "#{pane_current_path}" abre o novo pane no mesmo directório

# ========================================
# Navegação Entre Panes
# ========================================
# Alt+setas sem prefixo (mais rápido)
bind -n M-Left select-pane -L
bind -n M-Right select-pane -R
bind -n M-Up select-pane -U
bind -n M-Down select-pane -D

# Ou estilo vim (com prefixo)
bind h select-pane -L
bind j select-pane -D
bind k select-pane -U
bind l select-pane -R

# ========================================
# Redimensionar Panes
# ========================================
bind -r H resize-pane -L 5
bind -r J resize-pane -D 5
bind -r K resize-pane -U 5
bind -r L resize-pane -R 5

# ========================================
# Recarregar Configuração
# ========================================
bind r source-file ~/.tmux.conf \; display "Config reloaded!"

# ========================================
# Visual
# ========================================
# Cores verdadeiras (truecolor)
set -g default-terminal "tmux-256color"
set -ag terminal-overrides ",xterm-256color:RGB"

# Barra de estado minimalista
set -g status-style 'bg=#1a1b26 fg=#a9b1d6'
set -g status-left '#[fg=#08F42A,bold] #S '
set -g status-right '#[fg=#a9b1d6] %H:%M '
set -g status-left-length 30

# Janela actual destacada
set -g window-status-current-style 'fg=#08F42A,bold'
set -g window-status-style 'fg=#565f89'

# Borda dos panes
set -g pane-border-style 'fg=#565f89'
set -g pane-active-border-style 'fg=#08F42A'
```

Depois de guardar, recarrega:

```bash
tmux source-file ~/.tmux.conf
```

Ou, se já adicionaste o bind: `Ctrl+a r` (assumindo que mudaste o prefixo para `Ctrl+a`).

### Copy Mode

O tmux tem um modo de cópia que permite navegar pelo histórico e copiar texto. Com a configuração acima (`mode-keys vi`), usas comandos vim.

| Atalho | Ação |
| :--- | :--- |
| `Ctrl+a [` | Entrar em copy mode |
| `q` | Sair de copy mode |
| `v` | Iniciar selecção |
| `y` | Copiar selecção |
| `/` | Pesquisar |
| `n` / `N` | Próxima/anterior ocorrência |

Para colar: `Ctrl+a ]`

Para integrar com o clipboard do sistema, adiciona à config:

```bash
# Linux (X11)
bind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "xclip -selection clipboard"

# Linux (Wayland)
bind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "wl-copy"

# macOS
bind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "pbcopy"
```

## Automação com Scripts

Para projectos recorrentes, criar a estrutura manualmente é repetitivo. Scripts de sessão resolvem isto.

### Script Básico

```bash
#!/bin/bash
# ~/scripts/tmux-projeto.sh

SESSION="projeto"
PROJECT_DIR="$HOME/dev/meu-projeto"

# Mata sessão existente se houver
tmux kill-session -t $SESSION 2>/dev/null

# Cria nova sessão em background
tmux new-session -d -s $SESSION -n editor -c $PROJECT_DIR

# Janela 1: Editor
tmux send-keys -t $SESSION:editor "nvim ." Enter

# Janela 2: Servidor
tmux new-window -t $SESSION -n server -c $PROJECT_DIR
tmux send-keys -t $SESSION:server "npm run dev" Enter

# Janela 3: Testes
tmux new-window -t $SESSION -n tests -c $PROJECT_DIR
tmux send-keys -t $SESSION:tests "npm run test:watch" Enter

# Janela 4: Git/Shell
tmux new-window -t $SESSION -n git -c $PROJECT_DIR

# Volta à primeira janela
tmux select-window -t $SESSION:editor

# Anexa à sessão
tmux attach -t $SESSION
```

Torna executável e corre:

```bash
chmod +x ~/scripts/tmux-projeto.sh
~/scripts/tmux-projeto.sh
```

Um comando e tens o ambiente completo.

### Sessões com Panes

```bash
#!/bin/bash
# Sessão de monitorização

SESSION="monitor"

tmux new-session -d -s $SESSION -n main

# Divide em 4 panes
tmux split-window -h -t $SESSION:main
tmux split-window -v -t $SESSION:main.0
tmux split-window -v -t $SESSION:main.1

# Comandos em cada pane
tmux send-keys -t $SESSION:main.0 "htop" Enter
tmux send-keys -t $SESSION:main.1 "watch -n 1 'df -h'" Enter
tmux send-keys -t $SESSION:main.2 "journalctl -f" Enter
tmux send-keys -t $SESSION:main.3 "tail -f /var/log/syslog" Enter

tmux attach -t $SESSION
```

### Tmuxinator (Opcional)

Se quiseres gestão mais sofisticada, o tmuxinator permite definir sessões em YAML:

```bash
# Instala
gem install tmuxinator

# Cria projecto
tmuxinator new projeto
```

Isto cria `~/.config/tmuxinator/projeto.yml`:

```yaml
name: projeto
root: ~/dev/meu-projeto

windows:
  - editor:
      layout: main-vertical
      panes:
        - nvim .
        - # pane vazio para comandos
  - server: npm run dev
  - tests: npm run test:watch
  - git:
```

Arrancar: `tmuxinator start projeto`

## Plugins

O tmux tem um ecossistema de plugins. O gestor mais popular é o **TPM** (Tmux Plugin Manager).

### Instalar TPM

```bash
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
```

Adiciona ao fim do `~/.tmux.conf`:

```bash
# Lista de plugins
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'tmux-plugins/tmux-continuum'

# Inicializar TPM (manter no fim)
run '~/.tmux/plugins/tpm/tpm'
```

Recarrega e instala: `Ctrl+a I` (I maiúsculo).

### Plugins Recomendados

**tmux-resurrect**: Guarda e restaura sessões.

```bash
set -g @plugin 'tmux-plugins/tmux-resurrect'

# Ctrl+a Ctrl+s - guardar
# Ctrl+a Ctrl+r - restaurar
```

**tmux-continuum**: Guarda automaticamente a cada 15 minutos.

```bash
set -g @plugin 'tmux-plugins/tmux-continuum'
set -g @continuum-restore 'on'
```

**tmux-yank**: Copy/paste melhorado.

```bash
set -g @plugin 'tmux-plugins/tmux-yank'
```

## Dicas Avançadas

### Sessões Partilhadas

Múltiplos utilizadores podem anexar à mesma sessão:

```bash
# Utilizador 1 cria
tmux new -s partilhada

# Utilizador 2 anexa (mesmo sistema)
tmux attach -t partilhada
```

Ambos vêem e controlam a mesma sessão. Útil para pair programming.

### Nested Tmux (Tmux dentro de Tmux)

Quando fazes SSH para um servidor que também usa tmux, tens tmux dentro de tmux. Para enviar comandos ao tmux "interior":

```bash
Ctrl+a a <comando>  # O segundo 'a' envia Ctrl+a ao tmux interior
```

Ou muda o prefixo do tmux remoto para algo diferente.

### Capturar Output

Guardar o histórico de um pane para ficheiro:

```bash
# Dentro do tmux
Ctrl+a : capture-pane -S -3000
Ctrl+a : save-buffer ~/output.txt
```

Ou num comando:

```bash
tmux capture-pane -t sessao:janela.pane -p -S -3000 > output.txt
```

## A Curva de Aprendizagem

Vou ser honesto: a primeira semana é difícil. Vais esquecer-te dos atalhos. Vais confundir-te entre janelas e panes. Vais ter que consultar este guia vezes sem conta.

Mas depois de uma semana, os atalhos tornam-se memória muscular. Depois de um mês, não consegues imaginar trabalhar sem isto. O terminal deixa de ser uma ferramenta descartável e passa a ser um ambiente de trabalho persistente e organizado.

A chave é forçares-te a usar, mesmo quando seria mais fácil abrir outra tab do terminal. É no desconforto inicial que o hábito se forma.

## Conclusão

O tmux não é sobre ter mais terminais. É sobre organizar melhor o que já tens.

É sobre sessões que persistem. Sobre contextos que se mantêm. Sobre nunca mais perderes trabalho por uma conexão SSH que caiu ou um terminal que fechaste por engano.

O tmux transforma o terminal de uma ferramenta efémera numa extensão do teu sistema. Sempre disponível. Sempre no mesmo estado. Sempre à tua espera.

É uma daquelas ferramentas que, depois de a dominares, te faz perguntar como é que vivias sem ela.
