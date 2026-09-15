from pathlib import Path

from bs4 import BeautifulSoup
import pytest
import yaml

from scripts.exporter import Exporter, ExportError, frontmatter
from scripts.jekyll import custom_callout_styles, render, stage, post_date

ROOT = Path(__file__).resolve().parents[1]


def test_render_preserves_code_math_and_chinese_links():
    body = '''# 标题 {#标题}

[下一篇](%E4%B8%8B%E4%B8%80%E7%AF%87.md#小节)
![图片](../../assets/notes/image.png){ width="240" }

!!! warning "注意"
    中文$x^2$，**保留强调**。

???+ tip "展开"
    $$x=1$$

```python
print("{{ site.title }}")
```
'''
    output = render(body, 'courses/课程/示例.md', '/notes-site', '标题')
    soup = BeautifulSoup(output, 'html.parser')
    assert not soup.h1 and soup.find(id='标题')
    assert soup.a['href'] == '/notes-site/courses/%E8%AF%BE%E7%A8%8B/%E4%B8%8B%E4%B8%80%E7%AF%87/#小节'
    assert soup.img['src'] == '/assets/notes/image.png' and soup.img['width'] == '240'
    assert 'width="240" />' in output
    assert soup.select_one('blockquote.prompt-warning')
    assert soup.select_one('details.obsidian-callout[data-callout="tip"][open] > summary').get_text() == '展开'
    assert len(soup.select('.arithmatex')) == 2
    assert soup.select_one('.language-python .rouge-code').get_text().strip() == 'print("{{ site.title }}")'
    assert soup.select_one('.language-python .nb').get_text() == 'print'


def test_a_different_body_heading_is_not_deleted():
    output = render('# 正文小节', 'reading/一.md', '', '文章标题')
    assert '<h1' in output and '正文小节' in output


def test_custom_callout_keeps_its_obsidian_identifier_and_title():
    output = render('!!! intro\n    导言', 'reading/一.md', '', '文章标题')
    soup = BeautifulSoup(output, 'html.parser')
    callout = soup.select_one('blockquote.obsidian-callout[data-callout="intro"].prompt-info')
    assert callout and callout.strong.get_text() == 'Intro'


def test_callout_manager_colors_and_icons_become_safe_css():
    css = custom_callout_styles({
        'intro': {'icon': 'lucide-anchor', 'dark_color': '83, 223, 221'},
        'bad"]': {'light_color': '999, 0, 0'},
    })
    assert 'data-callout="intro"' in css and 'rgb(83 223 221 / 14%)' in css
    assert 'content: "\\f13d"' in css
    assert 'bad' not in css


def test_code_html_stays_literal():
    output = render('```html\n<img src="secret"> & {{ site.title }}\n```', 'courses/例.md', '')
    soup = BeautifulSoup(output, 'html.parser')
    assert not soup.img
    assert soup.select_one('.rouge-code').get_text().strip() == '<img src="secret"> & {{ site.title }}'


def test_staging_uses_only_public_notes_and_keeps_paths_and_dates(tmp_path):
    vault = tmp_path / 'vault'
    (vault / '课程').mkdir(parents=True)
    (vault / '课程/文 档.md').write_text('---\npublish: true\ntags: [CNN]\n---\n# 公开\n正文\n`{{ site.title }}`\n[[秘密|普通文字]]')
    (vault / '课程/秘密.md').write_text('---\npublish: false\n---\nPRIVATE_SENTINEL')
    (vault / '课程/index.md').write_text('---\npublish: true\n---\n# 课程索引\n自己整理的索引。')
    cfg = {'site': {'name': 'test'}, 'sources': [{'path': '课程', 'destination': 'courses'}]}
    docs = tmp_path / 'docs'
    manifest = Exporter(vault, cfg, ROOT / 'site-template').export(docs, {'courses/文 档.md': '2026-09-14T12:30:00+08:00'})
    assert manifest['notes'][1]['published_at'] == '2026-09-14T12:30:00+08:00'
    output = tmp_path / 'jekyll'
    settings = yaml.safe_load((ROOT / '_config.yml').read_text())
    stage(docs, output, ROOT / 'site-template', settings, {})
    posts = list((output / '_posts').glob('*.html'))
    assert len(posts) == 1  # A published section index becomes the tab itself.
    metadata, body = frontmatter(posts[0].read_text())
    assert metadata['permalink'] == '/courses/文 档/'
    assert metadata['date'] == '2026-09-14T12:30:00+08:00'
    assert metadata['tags'] == ['CNN'] and metadata['render_with_liquid'] is False
    assert 'description' not in metadata
    assert '{{ site.title }}' in body
    assert '自己整理的索引' in (output / '_tabs/course.html').read_text()
    assert 'PRIVATE_SENTINEL' not in ''.join(p.read_text() for p in output.rglob('*.html'))
    assert sorted(frontmatter(p.read_text())[0]['order'] for p in (output / '_tabs').iterdir()) == [1, 2, 3, 4]


def test_invalid_date_blocks_build():
    with pytest.raises(ExportError, match='ISO 日期'):
        post_date('yesterday')


def test_course_tree_keeps_hierarchy_order_and_public_links(tmp_path):
    vault = tmp_path / 'vault'
    files = {
        '课程/课程10/第一篇.md': '---\npublish: true\n---\n第一篇',
        '课程/课程2/index.md': '---\npublish: true\n---\n# 课程介绍',
        '课程/课程2/Lecture10.md': '---\npublish: true\n---\n第十讲',
        '课程/课程2/Lecture2.md': '---\npublish: true\n---\n第二讲',
        '课程/课程2/置顶.md': '---\npublish: true\nnav_order: 1\n---\n置顶',
        '课程/课程2/实验/示例.md': '---\npublish: true\ntitle: "<示例> & {{ literal }}"\n---\n正文',
        '课程/课程2/秘密/未公开.md': '---\npublish: false\n---\nPRIVATE_SENTINEL',
        '课程/导读.md': '---\npublish: true\n---\n导读',
        '阅读/书.md': '---\npublish: true\n---\n阅读',
    }
    for name, body in files.items():
        source = vault / name
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(body)
    labels = {'courses/课程2': '课程 & 二'}
    cfg = {'site': {'name': 'test'}, 'labels': labels, 'sources': [
        {'path': '课程', 'destination': 'courses'},
        {'path': '阅读', 'destination': 'reading'},
    ]}
    docs = tmp_path / 'docs'
    manifest = Exporter(vault, cfg, ROOT / 'site-template').export(docs)
    output = tmp_path / 'jekyll'
    stage(docs, output, ROOT / 'site-template', {'baseurl': '/notes-site'}, labels)
    _, body = frontmatter((output / '_tabs/course.html').read_text())
    soup = BeautifulSoup(body, 'html.parser')
    cards = soup.select('.course-tree > .categories')
    assert [card.select_one('a').get_text() for card in cards] == ['课程 & 二', '课程10', '导读']
    first = cards[0]
    assert first.select_one('summary .small').get_text() == '1 个子目录，5 篇笔记'
    assert [a.get_text() for a in first.select('details > ul > .course-note > a')] == [
        '<示例> & {{ literal }}', '置顶', 'Lecture2', 'Lecture10']
    assert first.select_one('.course-branch details summary a').get_text() == '实验'
    assert not soup.find('示例') and 'PRIVATE_SENTINEL' not in body and '秘密' not in body
    from scripts.exporter import page_url
    links = [a['href'] for a in soup.select('.course-tree a')]
    for note in manifest['notes']:
        url = '/notes-site/' + page_url(note['path'])
        assert links.count(url) == (1 if note['path'].startswith('courses/') else 0)


def test_empty_course_tree_has_no_disclosure(tmp_path):
    from scripts.jekyll import course_tree
    soup = BeautifulSoup(course_tree({}, '', {}), 'html.parser')
    assert '暂无公开笔记' in soup.get_text()
    assert not soup.find('details') and not soup.find('a')


def test_official_jekyll_build_keeps_literal_code_and_navigation(tmp_path):
    from scripts.site import build_snapshot
    vault = tmp_path / 'vault'
    (vault / '课程').mkdir(parents=True)
    (vault / '课程/示例.md').write_text('''---
publish: true
tags: [test]
---
# 示例

正文[^1]。中文$x^2$。

```html
<img src="literal"> & {{ site.title }} {% include missing.html %}
```

[^1]: 脚注正文。
''')
    cfg = {'site': {'name': 'test'}, 'sources': [{'path': '课程', 'destination': 'courses'}]}
    docs = tmp_path / 'docs'
    Exporter(vault, cfg, ROOT / 'site-template').export(docs, {'courses/示例.md': '2026-09-14T12:30:00+08:00'})
    pages = build_snapshot(docs, tmp_path / 'build')
    assert pages >= 10
    site = tmp_path / 'build/site'
    soup = BeautifulSoup((site / 'courses/示例/index.html').read_text(), 'html.parser')
    assert [link.get_text(strip=True) for link in soup.select('#sidebar a.nav-link')] == ['HOME', 'COURSE', 'READING', 'TECH', 'ABOUT']
    assert soup.select_one('.rouge-code').get_text().strip() == '<img src="literal"> & {{ site.title }} {% include missing.html %}'
    assert soup.select_one('.code-header button') and soup.find(id='fn:1')
    assert not soup.select_one('img[src="literal"]')
    assert not soup.select_one('.post-desc')


def test_built_post_navigation_uses_only_same_folder_in_filename_order(tmp_path):
    from scripts.exporter import page_url
    from scripts.site import build_snapshot

    vault = tmp_path / 'vault'
    files = {
        '课程/index.md': {'publish': True},
        '课程/课程2/Lecture10.md': {'publish': True, 'date': '2020-01-01', 'nav_order': 1},
        '课程/课程2/Lecture2 中文.md': {
            'publish': True, 'date': '2020-01-02', 'title': '<第二讲> & {{ literal }}'},
        '课程/课程2/Lecture1.md': {'publish': True, 'date': '2020-01-03', 'title': 'Z first'},
        '课程/课程2/Lecture3.md': {'publish': False},
        '课程/课程2/实验/Lecture3.md': {'publish': True},
        '课程/课程20/Lecture3.md': {'publish': True},
    }
    for name, metadata in files.items():
        source = vault / name
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text('---\n' + yaml.safe_dump(metadata, allow_unicode=True) + '---\n正文。')
    cfg = {'site': {'name': 'test'}, 'sources': [{'path': '课程', 'destination': 'courses'}]}
    docs = tmp_path / 'docs'
    Exporter(vault, cfg, ROOT / 'site-template').export(docs)
    build_snapshot(docs, tmp_path / 'build')
    site = tmp_path / 'build/site'

    def navigation(path):
        soup = BeautifulSoup((site / path / 'index.html').read_text(), 'html.parser')
        buttons = soup.select('.post-navigation > *')
        assert [button['aria-label'] for button in buttons] == ['Older', 'Newer']
        for button in buttons:
            if not button.get('href'):
                assert 'disabled' in button['class'] and button.get_text(strip=True) == '-'
        return buttons

    siblings = ['Lecture1', 'Lecture2 中文', 'Lecture10']
    titles = ['Z first', '<第二讲> & {{ literal }}', 'Lecture10']
    for i, name in enumerate(siblings):
        buttons = navigation('courses/课程2/' + name)
        for button, offset in zip(buttons, [-1, 1]):
            j = i + offset
            if 0 <= j < len(siblings):
                assert button['href'] == '/notes-site/' + page_url('courses/课程2/' + siblings[j] + '.md')
                assert button.get_text(strip=True) == titles[j]
            else:
                assert not button.get('href')
    for path in ['courses/课程2/实验/Lecture3', 'courses/课程20/Lecture3']:
        assert all(not button.get('href') for button in navigation(path))
