#!/bin/bash

# setup.sh - Reinicia o repo e envia tudo para o GitHub

echo "🗑️  A limpar configuração git antiga..."
rm -rf .git

echo "📦 A inicializar novo repositório..."
git init
git branch -M main

echo "🔗 A adicionar remote..."
git remote add origin https://github.com/mefrraz/zero.git

echo "📝 A adicionar ficheiros..."
git add .

echo "💾 A fazer commit..."
git commit -m "feat: initial commit for zero blog"

echo "🚀 A fazer push (force)..."
git push -f -u origin main

echo "✅ Feito! Verifica o GitHub Actions."
