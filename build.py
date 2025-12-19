#!/usr/bin/env python3
"""
zero() Blog Build System
Refactored to be robust, independent of existing posts, and maintainable.
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime
import frontmatter
import markdown
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import List, Dict, Optional, Tuple
from xml.dom import minidom
from typing import List, Dict, Optional, Tuple

# Configuration
BASE_DIR = Path(__file__).parent.absolute()
CONTENT_DIR = BASE_DIR / "content/posts"
POSTS_DIR = BASE_DIR / "posts"
CATEGORIES_DIR = BASE_DIR / "categories"
TEMPLATE_FILE = POSTS_DIR / "_template.html"
BLOG_FILE = BASE_DIR / "blog.html"
INDEX_FILE = BASE_DIR / "index.html"
FEED_FILE = BASE_DIR / "feed.xml"
SITEMAP_FILE = BASE_DIR / "sitemap.xml"

# Site configuration
SITE_URL = "https://mefrraz.github.io/zero"
SITE_TITLE = "zero()"
SITE_DESCRIPTION = "Blog pessoal sobre tecnologia, Linux e programação"

# Predefined category descriptions
CATEGORY_DESCRIPTIONS = {
    'linux': 'Tutoriais sobre Linux, distribuições, configs e tudo relacionado com o pinguim.',
    'devops': 'Containers, CI/CD, automação, infraestrutura e deployment.',
    'git': 'Controlo de versões, workflows, e boas práticas com Git.',
    'python': 'Python, frameworks, bibliotecas e scripting.',
    'javascript': 'JS, Node.js, React e o ecosistema web moderno.',
    'web': 'Desenvolvimento web, HTML, CSS e frontend em geral.',
    'backend': 'Servidores, APIs, bases de dados e arquitetura.',
    'tools': 'Ferramentas, editores, terminais e produtividade.',
    'ia': 'Inteligência Artificial, Machine Learning e LLMs.',
    'security': 'Segurança, privacidade e boas práticas.',
    'database': 'Bases de dados, SQL, NoSQL e modelagem de dados.',
    'tutorial': 'Guias passo-a-passo e tutoriais práticos.',
    'vida': 'Reflexões pessoais, minimalismo digital e filosofia.',
    'carreira': 'Desenvolvimento profissional, aprendizagem e experiências.',
    'geral': 'Posts que não se encaixam em categorias específicas.',
}

class Post:
    """Represents a blog post"""
    
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.slug = filepath.stem
        
        # Parse frontmatter and content
        with open(filepath, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
            
        self.title = post.get('title', 'Sem Título')
        self.date = post.get('date')
        if isinstance(self.date, str):
            try:
                self.date = datetime.strptime(self.date, '%Y-%m-%d').date()
            except ValueError:
                self.date = datetime.now().date() # Fallback
        elif isinstance(self.date, datetime):
            self.date = self.date.date()
                
        self.category = post.get('category', 'geral').lower()
        self.tags = post.get('tags', [])
        # Ensure tags is a list
        if isinstance(self.tags, str):
            self.tags = [t.strip() for t in self.tags.split(',')]
            
        self.excerpt = post.get('excerpt', '')
        self.featured = post.get('featured', False)
        self.content = post.content
        
        # Convert Markdown to HTML
        # Using extensions for nice code highlighting and tables
        md = markdown.Markdown(extensions=[
            'extra', 
            'codehilite', 
            'tables', 
            'fenced_code', 
            'toc'
        ])
        self.html_content = md.convert(self.content)
        
        # Calculate reading time
        word_count = len(self.content.split())
        self.reading_time = max(1, round(word_count / 200))
        
    def __repr__(self):
        return f"Post({self.slug}, {self.date})"


def format_date_pt(date_obj) -> str:
    """Format date in Portuguese (DD MMM YYYY)"""
    months_pt = {
        1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
        7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
    }
    return f"{date_obj.day} {months_pt[date_obj.month]} {date_obj.year}"


def load_template() -> str:
    """Load the HTML template"""
    if not TEMPLATE_FILE.exists():
        raise FileNotFoundError(f"Template not found: {TEMPLATE_FILE}")
    
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        return f.read()


def generate_single_post(post: Post, prev_post: Optional[Post], next_post: Optional[Post], template: str):
    """Generate HTML file for a single post"""
    
    # 1. Prepare Navigation HTML
    nav_html = ""
    if prev_post:
        nav_html += f'''                <a href="{prev_post.slug}.html" class="post-nav-link prev">
                    <span class="nav-label">← Anterior</span>
                    <span class="nav-title">{prev_post.title}</span>
                </a>'''
    
    if next_post:
        nav_html += f'''                <a href="{next_post.slug}.html" class="post-nav-link next">
                    <span class="nav-label">Próximo →</span>
                    <span class="nav-title">{next_post.title}</span>
                </a>'''
    
    if not prev_post and not next_post:
         # Empty nav if no links, but better to keep the structure empty or minimal
         pass

    # 2. Prepare Tags HTML
    tags_html = '\n'.join([f'<span class="tag">{tag}</span>' for tag in post.tags])

    # 3. Replace placeholders
    # We use a dictionary mapping for cleaner replacement
    replacements = {
        '{{ title }}': post.title,
        '{{ title_meta }}': f"{post.title} - zero()",
        '{{ description_meta }}': post.excerpt.replace('"', '&quot;'),
        '{{ category_name }}': post.category.capitalize(),
        '{{ category_slug }}': post.category,
        '{{ date }}': format_date_pt(post.date),
        '{{ reading_time }}': str(post.reading_time),
        '{{ excerpt }}': post.excerpt,
        '{{ content }}': post.html_content,
        '{{ tags_html }}': tags_html,
        '{{ nav_html }}': nav_html
    }
    
    html = template
    for key, value in replacements.items():
        html = html.replace(key, value)
        
    # Write to file
    output_path = POSTS_DIR / f"{post.slug}.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✓ Generated: {output_path.name}")


def update_blog_listing(posts: List[Post]):
    """Update the blog.html page with the list of posts"""
    if not BLOG_FILE.exists():
        print(f"⚠️  {BLOG_FILE} not found. Skipping update.")
        return

    # Sort by date (newest first)
    sorted_posts = sorted(posts, key=lambda p: p.date, reverse=True)
    
    posts_html = ""
    for post in sorted_posts:
        title_keywords = post.title.lower().replace(':', '').replace(',', '')
        category_keywords = f"{post.category} {' '.join(post.tags)}".lower()
        
        posts_html += f'''            <article class="post-card" data-title="{title_keywords}" data-category="{category_keywords}">
                <div class="post-meta">
                    <span>{format_date_pt(post.date)}</span>
                    <span>•</span>
                    <span>{post.category.capitalize()}</span>
                </div>
                <a href="posts/{post.slug}.html" class="post-title-link">
                    <h2 class="post-title">{post.title}</h2>
                </a>
                <p class="post-excerpt">{post.excerpt}</p>
                <a href="posts/{post.slug}.html" class="read-more">Ler mais →</a>
            </article>
'''

    # Read existing file
    with open(BLOG_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Robust regex replacement for the posts grid
    # Looking for <section class="posts-grid blog-grid" id="postsGrid"> ... </section>
    pattern = re.compile(
        r'(<section class="posts-grid blog-grid" id="postsGrid">)(.*?)(</section>)', 
        re.DOTALL
    )
    
    if pattern.search(content):
        new_content = pattern.sub(f'\\1\n{posts_html}        \\3', content)
        with open(BLOG_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✓ Updated: {BLOG_FILE.name}")
    else:
        print(f"⚠️  Could not find posts grid in {BLOG_FILE.name}")


def update_homepage(posts: List[Post]):
    """Update index.html with featured and recent posts"""
    if not INDEX_FILE.exists():
        print(f"⚠️  {INDEX_FILE} not found. Skipping update.")
        return

    sorted_posts = sorted(posts, key=lambda p: p.date, reverse=True)
    
    # 1. Determine Featured Post
    featured_post = next((p for p in posts if p.featured), None)
    if not featured_post and sorted_posts:
        featured_post = sorted_posts[0]
        
    if not featured_post:
        return

    # 2. Determine Recent Posts (excluding featured)
    recent_posts = [p for p in sorted_posts if p.slug != featured_post.slug][:6]

    # Read content
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- UPDATE FEATURED SECTION ---
    featured_html = f'''        <section class="featured-section" style="margin-bottom: 4rem; position: relative;">
            <img src="assets/2.png" alt="" class="featured-blob">
            <article class="post-card featured">
                <div class="post-content">
                    <div class="post-meta">
                        <span style="color: var(--c-accent)">★ Destaque</span>
                        <span>•</span>
                        <span>{format_date_pt(featured_post.date)}</span>
                    </div>
                    <a href="posts/{featured_post.slug}.html" class="post-title-link">
                        <h2 class="post-title">{featured_post.title}</h2>
                    </a>
                    <p class="post-excerpt" style="font-size: 1.1rem;">{featured_post.excerpt}</p>
                    <a href="posts/{featured_post.slug}.html" class="read-more">Ler artigo completo →</a>
                </div>
            </article>
        </section>'''

    # Regex for featured section
    # Matches <section class="featured-section" ... > ... </section>
    # Logic: look for class="featured-section" and end at first </section>
    # Note: Regex parsing HTML is fragile, but controlled here. 
    # We'll use a specific marker approach based on the known structure or just simple string replacement if unique.
    # The previous script used simple string find/slice. Let's try to be slightly more robust but simple.
    
    featured_pattern = re.compile(r'(<section class="featured-section".*?>).*?(</section>)', re.DOTALL)
    if featured_pattern.search(content):
        # We replace the whole block with our generated block
        # Since our generated block already has the opening and closing tags, we can just replace the match
        # BUT wait, the pattern includes capturing groups.
        # Actually, let's just replace the whole match.
        pass # Logic handled below
    
    # Actually, simpler: finding the start and end indices of the section is safer than regex for large blocks
    f_start = content.find('<section class="featured-section"')
    if f_start != -1:
        f_end = content.find('</section>', f_start) + len('</section>')
        content = content[:f_start] + featured_html + content[f_end:]

    # --- UPDATE RECENT POSTS SECTION ---
    recent_html = ""
    for post in recent_posts:
        recent_html += f'''            <article class="post-card">
                <div class="post-meta">
                    <span>{format_date_pt(post.date)}</span>
                    <span>•</span>
                    <span>{post.category.capitalize()}</span>
                </div>
                <a href="posts/{post.slug}.html" class="post-title-link">
                    <h2 class="post-title">{post.title}</h2>
                </a>
                <p class="post-excerpt">{post.excerpt}</p>
                <a href="posts/{post.slug}.html" class="read-more">Ler mais →</a>
            </article>
'''
    
    g_start = content.find('<section class="posts-grid">')
    if g_start != -1:
        g_end = content.find('        </section>', g_start)
        # We want to keep the closing tag this time in the slice logic
        prefix = '<section class="posts-grid">'
        content = (
            content[:g_start + len(prefix)] + 
            '\n' + recent_html + '        ' + 
            content[g_end:]
        )

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Updated: {INDEX_FILE.name}")


def generate_category_pages(posts: List[Post]):
    """Generate pages for each category"""
    
    # 1. Group by category
    categories = {}
    for post in posts:
        cat = post.category
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(post)
    
    # 2. Generate pages
    for cat, cat_posts in categories.items():
        cat_posts.sort(key=lambda p: p.date, reverse=True)
        
        description = CATEGORY_DESCRIPTIONS.get(cat, f'Posts sobre {cat}.')
        post_count = len(cat_posts)
        last_update = cat_posts[0].date
        
        posts_html = ""
        for post in cat_posts:
            posts_html += f'''            <article class="post-card">
                <div class="post-meta">
                    <span>{format_date_pt(post.date)}</span>
                    <span>•</span>
                    <span>{post.category.capitalize()}</span>
                </div>
                <a href="../posts/{post.slug}.html" class="post-title-link">
                    <h2 class="post-title">{post.title}</h2>
                </a>
                <p class="post-excerpt">{post.excerpt}</p>
                <a href="../posts/{post.slug}.html" class="read-more">Ler mais →</a>
            </article>
'''

        # We need a template for categories too. 
        # Since we don't have a separate file, we can inline it or minimal-replace.
        # But wait, the previous build used a huge inline string. 
        # Let's keep it inline for now to avoid creating too many files, but keep it clean.
        
        html = f'''<!DOCTYPE html>
<html lang="pt-PT">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{cat.capitalize()} - zero()</title>
    <meta name="description" content="{description}">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>0</text></svg>">
    <link rel="stylesheet" href="../style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
</head>
<body>
    <div class="bg-layer">
        <img src="../assets/1.png" alt="" class="bg-blob blob-1">
        <img src="../assets/2.png" alt="" class="bg-blob blob-2">
        <img src="../assets/3.png" alt="" class="bg-blob blob-3">
    </div>

    <div class="container">
        <div id="header-placeholder"></div>
        <script src="../components.js"></script>
        <script>loadHeader();</script>

        <!-- Category Hero -->
        <section class="category-hero">
            <h1>/{cat}</h1>
            <p>{description}</p>
            <div class="category-stats">
                <span class="stat"><strong>{post_count}</strong> post{"s" if post_count != 1 else ""}</span>
                <span class="stat-dot">•</span>
                <span class="stat">Última atualização: {format_date_pt(last_update)}</span>
            </div>
        </section>

        <!-- Posts Grid -->
        <section class="posts-grid">
{posts_html}        </section>

        <div id="footer-placeholder"></div>
        <script>loadFooter();</script>
    </div>

    <style>
        .category-hero {{
            padding: 4rem 0 3rem;
            text-align: center;
            max-width: 700px;
            margin: 0 auto;
        }}
        .category-hero h1 {{
            font-size: 4rem;
            font-weight: 800;
            line-height: 1.1;
            margin-bottom: 1.5rem;
            letter-spacing: -0.03em;
            background: linear-gradient(135deg, var(--c-text-main) 0%, var(--c-text-sub) 50%, var(--c-accent) 100%);
            background-size: 150% 150%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: gradient-shift 8s ease infinite;
        }}
        .category-hero p {{
            font-size: 1.15rem;
            color: var(--c-text-sub);
            line-height: 1.7;
            margin-bottom: 2rem;
        }}
        .category-stats {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 1rem;
            font-family: var(--font-mono);
            font-size: 0.85rem;
            color: var(--c-text-sub);
        }}
        .category-stats strong {{
            color: var(--c-accent);
        }}
        .stat-dot {{
            opacity: 0.3;
        }}
        @media (max-width: 768px) {{
            .category-hero h1 {{
                font-size: 2.5rem;
            }}
            .category-stats {{
                flex-direction: column;
                gap: 0.5rem;
            }}
            .stat-dot {{
                display: none;
            }}
        }}
    </style>
</body>
</html>'''

        cat_file = CATEGORIES_DIR / f"category-{cat}.html"
        with open(cat_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✓ Generated Category: {cat}")


def generate_rss(posts: List[Post]):
    """Generate RSS Feed"""
    sorted_posts = sorted(posts, key=lambda p: p.date, reverse=True)
    
    rss = ET.Element('rss', version='2.0')
    channel = ET.SubElement(rss, 'channel')
    
    ET.SubElement(channel, 'title').text = SITE_TITLE
    ET.SubElement(channel, 'link').text = SITE_URL
    ET.SubElement(channel, 'description').text = SITE_DESCRIPTION
    ET.SubElement(channel, 'language').text = 'pt-PT'
    
    for post in sorted_posts[:10]:
        item = ET.SubElement(channel, 'item')
        ET.SubElement(item, 'title').text = post.title
        ET.SubElement(item, 'link').text = f"{SITE_URL}/posts/{post.slug}.html"
        ET.SubElement(item, 'description').text = post.excerpt
        # RSS date format: Mon, 15 Dec 2025 00:00:00 GMT
        dt = datetime(post.date.year, post.date.month, post.date.day)
        ET.SubElement(item, 'pubDate').text = dt.strftime('%a, %d %b %Y 00:00:00 GMT')
        ET.SubElement(item, 'guid').text = f"{SITE_URL}/posts/{post.slug}.html"
        
    xml_str = minidom.parseString(ET.tostring(rss)).toprettyxml(indent="  ")
    with open(FEED_FILE, 'w', encoding='utf-8') as f:
        f.write(xml_str)
    print("✓ Generated: RSS Feed")


def generate_sitemap(posts: List[Post]):
    """Generate Sitemap"""
    urlset = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    
    # Static pages
    for page in ['/', '/blog.html', '/projetos.html', '/sobre.html']:
        url = ET.SubElement(urlset, 'url')
        ET.SubElement(url, 'loc').text = SITE_URL + page
        ET.SubElement(url, 'changefreq').text = 'weekly'
        ET.SubElement(url, 'priority').text = '0.8' if page == '/' else '0.6'
        
    # Posts
    for post in posts:
        url = ET.SubElement(urlset, 'url')
        ET.SubElement(url, 'loc').text = f"{SITE_URL}/posts/{post.slug}.html"
        ET.SubElement(url, 'lastmod').text = post.date.strftime('%Y-%m-%d')
        ET.SubElement(url, 'changefreq').text = 'monthly'
        ET.SubElement(url, 'priority').text = '0.7'
        
    xml_str = minidom.parseString(ET.tostring(urlset)).toprettyxml(indent="  ")
    with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
        f.write(xml_str)
    print("✓ Generated: Sitemap")


def main():
    print("🚀 zero() Build System v2.0")
    print("-" * 30)
    
    if not CONTENT_DIR.exists():
        print(f"❌ Content directory not found: {CONTENT_DIR}")
        return

    # 1. Load Posts
    posts = []
    print("📖 Loading markdown posts...")
    for md_file in CONTENT_DIR.glob("*.md"):
        try:
            posts.append(Post(md_file))
        except Exception as e:
            print(f"❌ Error loading {md_file.name}: {e}")
            
    if not posts:
        print("⚠️  No posts found.")
        return
        
    print(f"✓ Loaded {len(posts)} posts.")
    
    # 2. Sort for Navigation (Alphabetical to match file system ordering usually, or date?)
    # Usually blog navigation is by date, but previous script did by filename (slug).
    # Let's align with Date for better UX, but handle same-dates.
    # Actually, previous script: posts_sorted = sorted(posts, key=lambda p: p.slug)
    # Let's keep slug sorting for "Previous/Next" if that's the desired deterministic order,
    # OR sort by date. 
    # Let's stick to Date for logical reading order.
    posts_by_date = sorted(posts, key=lambda p: p.date, reverse=True)
    
    # However, Previous/Next usually means Chronological.
    # So "Previous" is older, "Next" is newer.
    # List is [Newest, ..., Oldest]
    # So for index i:
    # Next (Newer) is i-1
    # Prev (Older) is i+1
    
    template = load_template()
    
    print("\n🔨 Generating Post HTMLs...")
    for i, post in enumerate(posts_by_date):
        # Next (Newer)
        next_post = posts_by_date[i-1] if i > 0 else None
        # Prev (Older)
        prev_post = posts_by_date[i+1] if i < len(posts_by_date) - 1 else None
        
        generate_single_post(post, prev_post, next_post, template)
        
    print("\n📝 Updating Pages...")
    update_blog_listing(posts)
    update_homepage(posts)
    
    print("\n📂 Generating Categories...")
    generate_category_pages(posts)
    
    print("\n📡 Generating Feeds...")
    generate_rss(posts)
    generate_sitemap(posts)
    
    print("\n✅ Build Complete!")

if __name__ == "__main__":
    main()
