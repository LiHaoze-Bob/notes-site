"""Stage public Obsidian exports for the official Chirpy theme."""
from __future__ import annotations

from datetime import date, datetime
import hashlib
import html
import json
from pathlib import Path
import posixpath
import re
import shutil
from urllib.parse import quote, unquote, urlsplit, urlunsplit

from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter
from bs4.dammit import EntitySubstitution
import markdown
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.util import ClassNotFound
import yaml

from scripts.exporter import ExportError, frontmatter, natural_key, page_url


CALLOUT_STYLES = {
    'tip': {'tip', 'hint', 'important', 'success', 'check', 'done'},
    'warning': {'question', 'help', 'faq', 'warning', 'caution', 'attention'},
    'danger': {'failure', 'fail', 'missing', 'danger', 'error', 'bug'},
}


def callout_style(kind: str) -> str:
    return next((style for style, kinds in CALLOUT_STYLES.items() if kind in kinds), 'info')


def write_page(path: Path, metadata: dict, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('---\n' + yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False)
                    + '---\n' + content + '\n')


def render(body: str, source: str, baseurl: str, title: str | None = None) -> str:
    """Keep Obsidian syntax, then use Chirpy's native prompt/code markup."""
    result = markdown.markdown(body, extensions=[
        'admonition', 'attr_list', 'tables', 'footnotes', 'md_in_html',
        'pymdownx.details', 'pymdownx.highlight', 'pymdownx.superfences', 'pymdownx.arithmatex',
        'pymdownx.tasklist', 'toc',
    ], extension_configs={
        'pymdownx.arithmatex': {'generic': True, 'smart_dollar': False},
        'pymdownx.highlight': {'use_pygments': False},
    })
    soup = BeautifulSoup(result, 'html.parser')
    # The native layout supplies the title. Preserve the original H1 anchor.
    heading = soup.find('h1', recursive=False)
    if heading and (title is None or heading.get_text() == title):
        anchor = soup.new_tag('span', id=heading.get('id', 'page-title'))
        heading.replace_with(anchor)
    for prompt in soup.select('div.admonition, details[class]'):
        kind = next((c for c in prompt.get('class', []) if c != 'admonition'), 'note').lower()
        style = callout_style(kind)
        prompt['data-callout'] = kind
        if prompt.name == 'div':
            prompt.name = 'blockquote'
            prompt['class'] = ['prompt-' + style, 'obsidian-callout']
            title = prompt.find(class_='admonition-title', recursive=False)
            if title:
                title.attrs.pop('class', None)
                label = soup.new_tag('strong')
                label.string = title.get_text()
                title.clear()
                title.append(label)
        else:
            prompt['class'] = ['obsidian-callout', 'prompt-' + style]
            title = prompt.find('summary', recursive=False)
            if title:
                title['class'] = ['callout-title']
    for code in soup.select('pre > code'):
        language = next((c.removeprefix('language-') for c in code.get('class', [])
                         if c.startswith('language-')), 'plaintext')
        try:
            lexer = get_lexer_by_name(language)
        except ClassNotFound:
            lexer = TextLexer()
        text = code.get_text()
        colored = highlight(text, lexer, HtmlFormatter(nowrap=True))
        lines = '\n'.join(str(i) for i in range(1, len(text.splitlines()) + 1))
        # Same structure as Kramdown/Rouge, so Chirpy adds its own code toolbar.
        block = (f'<div class="language-{html.escape(language, quote=True)} highlighter-rouge">'
                 '<div class="highlight"><pre class="highlight"><code>'
                 '<table class="rouge-table"><tbody><tr><td class="rouge-gutter gl">'
                 f'<pre class="lineno">{lines}</pre></td><td class="rouge-code">'
                 f'<pre>{colored}</pre></td></tr></tbody></table></code></pre></div></div>')
        code.parent.replace_with(BeautifulSoup(block, 'html.parser'))
    for code in soup.select('code'):
        if not code.find_parent(class_='highlight'):
            code['class'] = [*code.get('class', []), 'highlighter-rouge']
    for element in soup.select('a[href], img[src]'):
        attribute = 'src' if element.name == 'img' else 'href'
        target = element[attribute]
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        path = unquote(parsed.path)
        if path.startswith('/'):
            path = path.removeprefix(baseurl + '/').lstrip('/')
        else:
            path = posixpath.normpath(posixpath.join(posixpath.dirname(source), path))
        if path.startswith('../'):
            raise ExportError('链接超出公开目录：' + target)
        url = page_url(path) if path.endswith('.md') else quote(path, safe='/.-_~')
        # Chirpy's native image renderer adds baseurl itself.
        prefix = '' if element.name == 'img' else baseurl
        element[attribute] = urlunsplit(('', '', prefix + '/' + url, parsed.query, parsed.fragment))
    # Chirpy parses the Kramdown-style space before a void element's closing slash.
    return soup.decode(formatter=HTMLFormatter(entity_substitution=EntitySubstitution.substitute_xml,
                                               void_element_close_prefix=' /'))


CALLOUT_ICONS = {
    'lucide-anchor': '\\f13d',
    'lucide-blend': '\\f5fd',
    'lucide-book-open-check': '\\f518',
    'lucide-aperture': '\\f140',
    'lucide-book': '\\f02d',
    'lucide-book-open': '\\f518',
    'lucide-apple': '\\f0cb',
    'lucide-airplay': '\\e163',
}


def custom_callout_styles(callouts: dict) -> str:
    """Translate Callout Manager colors/icons into safe local CSS."""
    rules = []
    for kind, definition in sorted(callouts.items()):
        if not re.fullmatch(r'[\w-]+', kind) or not isinstance(definition, dict):
            continue
        selector = f'.obsidian-callout[data-callout="{kind}"]'
        for scheme in ('light', 'dark'):
            color = definition.get(scheme + '_color')
            if isinstance(color, str) and re.fullmatch(r'\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*', color):
                values = ' '.join(part.strip() for part in color.split(','))
                rules.append(
                    f':root[data-bs-theme="{scheme}"] {selector} '
                    f'{{ background-color: rgb({values} / 14%) !important; }}'
                )
                rules.append(
                    f':root[data-bs-theme="{scheme}"] blockquote{selector}::before, '
                    f':root[data-bs-theme="{scheme}"] details{selector} > summary::before '
                    f'{{ color: rgb({values}) !important; }}'
                )
        icon = CALLOUT_ICONS.get(definition.get('icon'))
        if icon:
            rules.append(
                f'blockquote{selector}::before, details{selector} > summary::before '
                f'{{ content: "{icon}"; transform: none; }}'
            )
    return '\n'.join(rules) + ('\n' if rules else '')


def post_date(value) -> str:
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    try:
        return datetime.fromisoformat(str(value)).isoformat()
    except ValueError as exc:
        raise ExportError('笔记 date 必须为 ISO 日期或日期时间：' + str(value)) from exc


def course_tree(notes: dict, baseurl: str, labels: dict) -> str:
    """Render public course folders in manifest order (including nav_order)."""
    courses = {path: note for path, note in notes.items()
               if path.startswith('courses/') and path != 'courses/index.md'}

    def link(path: str, title: str) -> str:
        url = baseurl + '/' + page_url(path)
        return f'<a href="{html.escape(url, quote=True)}">{html.escape(title)}</a>'

    def children(folder: str, top: bool = False) -> str:
        prefix = folder + '/'
        below = {path: note for path, note in courses.items() if path.startswith(prefix)}
        directories = sorted({path[len(prefix):].split('/')[0] for path in below
                              if '/' in path[len(prefix):]}, key=natural_key)
        folders = []
        for directory in directories:
            path = prefix + directory
            index = path + '/index.md'
            title = labels.get(path, courses.get(index, {}).get('title', directory))
            descendants = [name[len(path) + 1:] for name in below if name.startswith(path + '/')]
            subfolders = len({name.split('/')[0] for name in descendants if '/' in name})
            count = (f'{subfolders} 个子目录，' if subfolders else '') + f'{len(descendants)} 篇笔记'
            items = children(path)
            row = (
                '<span class="course-label">'
                '<i class="far fa-folder-open fa-fw course-folder-open" aria-hidden="true"></i>'
                '<i class="far fa-folder fa-fw course-folder-closed" aria-hidden="true"></i>'
                f'{link(index, title)}<span class="text-muted small">{count}</span></span>'
            )
            if items:
                header = 'card-header' if top else 'course-subfolder'
                branch = (
                    f'<details open><summary class="{header}">{row}'
                    '<span class="category-trigger" aria-hidden="true">'
                    '<i class="fas fa-fw fa-angle-down"></i></span></summary>'
                    f'<ul class="list-group">{items}</ul></details>'
                )
            else:
                # An index-only folder is a real public note, with no empty toggle.
                branch = f'<div class="course-index-only {"card-header" if top else "course-subfolder"}">{row}</div>'
            folders.append(f'<div class="card categories">{branch}</div>' if top else
                           f'<li class="list-group-item course-branch">{branch}</li>')
        leaves = [
            '<li class="list-group-item course-note">'
            '<i class="far fa-file-lines fa-fw" aria-hidden="true"></i>'
            f'{link(path, note["title"])}</li>'
            for path, note in below.items()
            if posixpath.dirname(path) == folder and path != prefix + 'index.md'
        ]
        if top and leaves:
            folders.append('<div class="card categories"><ul class="list-group">' + ''.join(leaves) + '</ul></div>')
            leaves = []
        return ''.join(folders + leaves)

    content = children('courses', top=True) or '<p class="text-muted">暂无公开笔记。</p>'
    stylesheet = html.escape(baseurl + '/assets/css/course-tree.css', quote=True)
    return f'<link rel="stylesheet" href="{stylesheet}"><div class="course-tree">{content}</div>'


def folder_navigation(notes: dict) -> dict:
    """Link direct siblings by filename, independently of dates and nav_order."""
    folders = {}
    for path in notes:
        folders.setdefault(posixpath.dirname(path), []).append(path)
    navigation = {}
    for paths in folders.values():
        paths.sort(key=lambda path: (natural_key(posixpath.basename(path)), path))
        for i, path in enumerate(paths):
            neighbors = {}
            for direction, offset in [('previous', -1), ('next', 1)]:
                neighbor = paths[i + offset] if 0 <= i + offset < len(paths) else None
                neighbors['folder_' + direction] = (
                    {'url': '/' + page_url(neighbor), 'title': notes[neighbor]['title']}
                    if neighbor else None
                )
            navigation[path] = neighbors
    return navigation


def stage(docs: Path, destination: Path, template: Path, settings: dict, labels: dict):
    """Build only from the exported snapshot; never needs the private Vault."""
    shutil.copytree(template, destination, dirs_exist_ok=True)
    if (docs / 'assets').exists():
        shutil.copytree(docs / 'assets', destination / 'assets', dirs_exist_ok=True)
    shutil.copy2(docs / 'publication.json', destination / 'publication.json')
    (destination / '_config.yml').write_text(yaml.safe_dump(settings, allow_unicode=True, sort_keys=False))
    manifest = json.loads((docs / 'publication.json').read_text())
    callout_css = destination / 'assets/css/obsidian-callouts.css'
    callout_css.write_text(callout_css.read_text() + '\n' + custom_callout_styles(manifest.get('callouts', {})))
    notes = {note['path']: note for note in manifest['notes']}
    tabs = {}
    for path in (destination / '_tabs').glob('*.html'):
        metadata, _ = frontmatter(path.read_text())
        source = metadata.pop('source_index')
        tabs[source] = (path, metadata)
    navigation = folder_navigation({path: note for path, note in notes.items()
                                    if path not in tabs and path != 'index.md'
                                    and not path.startswith('assets/')})
    for source in sorted(docs.rglob('*.md')):
        relative = source.relative_to(docs).as_posix()
        if relative == 'index.md' or relative.startswith('assets/'):
            continue
        metadata, body = frontmatter(source.read_text())
        content = render(body, relative, settings.get('baseurl', ''), metadata.get('title'))
        metadata.update(render_with_liquid=False, permalink='/' + unquote(page_url(relative)))
        if relative in tabs:
            path, tab_metadata = tabs[relative]
            metadata.update(tab_metadata)
            if metadata.pop('navigation', None) == 'course-tree':
                # Keep an authored section introduction, replace generated lists.
                introduction = content if relative in notes else ''
                content = introduction + course_tree(notes, settings.get('baseurl', ''), labels)
        elif relative in notes:
            note = notes[relative]
            timestamp = post_date(metadata.get('date') or note['published_at'])
            identifier = hashlib.sha256(relative.encode()).hexdigest()[:12]
            path = destination / '_posts' / f'{timestamp[:10]}-{identifier}.html'
            folder = posixpath.dirname(relative)
            section = relative.split('/')[0]
            category = labels.get(folder, {'courses': 'Course', 'reading': 'Reading', 'knowledge': 'Tech'}.get(section, section))
            metadata.update(layout='post', date=timestamp, categories=[category], math=True)
            metadata.update(navigation[relative])
        else:
            path = destination / Path(relative).with_suffix('.html')
            heading = BeautifulSoup(markdown.markdown(body), 'html.parser').find('h1')
            metadata.update(layout='page', title=heading.get_text() if heading else source.parent.name)
        write_page(path, metadata, content)
