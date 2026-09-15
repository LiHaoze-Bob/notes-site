from pathlib import Path
import json
import pytest
from scripts.exporter import Exporter, ExportError


@pytest.fixture
def setup(tmp_path):
    vault=tmp_path/'vault'; source=vault/'课程'; source.mkdir(parents=True)
    template=tmp_path/'template'; template.mkdir(); (template/'base.yml').write_text('site_name: test\n')
    cfg={'site':{'name':'test','url':'https://example.com/notes-site/'},'sources':[{'path':'课程','destination':'courses'}]}
    def note(name,body,published=True,extra=''):
        p=source/name; p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text('---\npublish: '+str(published).lower()+'\n'+extra+'---\n'+body)
        return p
    def export():
        destination=tmp_path/('output-'+str(len(list(tmp_path.glob('output-*')))))
        exporter=Exporter(vault,cfg,template)
        manifest=exporter.export(destination)
        return destination,manifest,exporter
    return source,note,export


def test_only_explicit_true_and_removal(setup):
    source,note,export=setup
    selected=note('公开.md','# 公开\n公开正文')
    note('私人.md','# 秘密\nPRIVATE_SENTINEL',False)
    (source/'旧标记.md').write_text('---\npublished: true\n---\nLEGACY_PRIVATE')
    output,manifest,_=export()
    assert len(manifest['notes'])==1
    assert 'PRIVATE_SENTINEL' not in ''.join(p.read_text() for p in output.rglob('*.md'))
    selected.write_text(selected.read_text().replace('publish: true','publish: false'))
    output,manifest,_=export()
    assert not manifest['notes']
    assert not (output/'courses/公开.md').exists()


def test_unicode_paths_images_and_same_names(setup):
    source,note,export=setup
    for folder,data in [('一',b'one'),('二',b'two')]:
        note(folder+'/文 档.md','# 标题\n![](图 片(1).png )')
        (source/folder/'图 片(1).png').write_bytes(data)
    output,manifest,_=export()
    assert len(manifest['images'])==2
    assert {p.read_bytes() for p in (output/'assets/notes').glob('*')}=={b'one',b'two'}


def test_wikilink_alias_heading_and_private_target(setup):
    _,note,export=setup
    note('公开.md','# 公开\n[[目标#中文标题|跳转]]\n[[私人|保留文字]]')
    note('目标.md','# 目标\n## 中文标题\n正文')
    note('私人.md','# 私人\nSECRET',False)
    output,_,exporter=export()
    page=(output/'courses/公开.md').read_text()
    assert '[跳转](%E7%9B%AE%E6%A0%87.md#%E4%B8%AD%E6%96%87%E6%A0%87%E9%A2%98)' in page
    assert '保留文字' in page and '[保留文字]' not in page
    assert '{#中文标题}' in (output/'courses/目标.md').read_text()
    assert len(exporter.warnings)==1


def test_protect_code_inline_math_and_nested_callout(setup):
    _,note,export=setup
    literal='```md\n[[不会转换]]\n![](missing.png)\n> [!tip] 原样\n```'
    note('示例.md','# 示例\n'+literal+'\n`[[不会转换]]`\n$$a_i = \\sum x_i$$\n> [!tip]+ 标题\n> 内容\n> > [!warning] 内层\n> > 文字\n> ```python\n> print("[[literal]]")\n> ```')
    output,_,_=export(); text=(output/'courses/示例.md').read_text()
    assert literal in text
    assert '`[[不会转换]]`' in text
    assert '$$a_i = \\sum x_i$$' in text
    assert '???+ tip "标题"' in text and '    !!! warning "内层"' in text
    assert '    print("[[literal]]")' in text


def test_custom_callout_types_and_manager_settings_are_preserved(setup):
    source,note,export=setup
    manager = source.parent / '.obsidian/plugins/callout-manager'
    manager.mkdir(parents=True)
    manager.joinpath('data.json').write_text(json.dumps({'callouts': {
        'custom': ['intro', 'theorem'],
        'settings': {
            'intro': [{'changes': {'icon': 'lucide-anchor'}},
                      {'condition': {'colorScheme': 'dark'}, 'changes': {'color': '83, 223, 221'}}],
        },
    }}))
    note('自定义.md', '# 自定义\n> [!intro]\n> 导言\n\n普通正文\n\n> [!word]\n> 单词')
    output,manifest,_=export()
    text=(output/'courses/自定义.md').read_text()
    assert '!!! intro' in text and '!!! word' in text
    assert '!!! note' not in text
    assert manifest['callouts']['intro'] == {'icon': 'lucide-anchor', 'dark_color': '83, 223, 221'}
    assert manifest['callouts']['theorem'] == {}


@pytest.mark.parametrize('body,error',[
    ('![](missing.png)','找不到图片'),
    ('[[不存在]]','找不到链接目标'),
    ('![[私人]]','暂不支持笔记'),
    ('```dataview\nLIST\n```','不支持动态内容'),
    ('[本机](file:///Users/user/private.md)','不支持本地资源'),
])
def test_errors_block_export(setup,body,error):
    _,note,export=setup; note('公开.md','# 公开\n'+body)
    with pytest.raises(ExportError,match=error): export()


def test_ambiguous_link_does_not_pick_first(setup):
    _,note,export=setup
    note('主.md','[[同名]]'); note('甲/同名.md','# A'); note('乙/同名.md','# B')
    with pytest.raises(ExportError,match='多个匹配'): export()


def test_outside_scope_and_symlink_attachment(setup,tmp_path):
    source,note,export=setup
    secret=tmp_path/'secret.png'; secret.write_bytes(b'SECRET')
    (source/'linked.png').symlink_to(secret)
    note('主.md','![](linked.png)')
    with pytest.raises(ExportError,match='超出配置目录'): export()


def test_image_embed_dimensions_and_markdown_reference(setup):
    source,note,export=setup
    note('主.md','![[a.png|240]]\n![说明][image]\n\n[image]: a.png')
    (source/'a.png').write_bytes(b'image')
    output,manifest,_=export()
    text=(output/'courses/主.md').read_text()
    assert '{ width="240" }' in text
    assert '![说明](../assets/notes/' in text
    assert len(manifest['images'])==1


def test_private_reference_links_and_unused_images(setup):
    _,note,export=setup
    note('公开.md','# 公开\n[保留文字][private]\n[私人][]\n[私人]\n`[保留文字][private]`\n\n[private]: 私人.md\n[私人]: 私人.md\n[unused]: missing.png')
    note('私人.md','SECRET',False)
    output,manifest,exporter=export()
    text=(output/'courses/公开.md').read_text()
    assert '保留文字\n私人\n私人' in text
    assert '`[保留文字][private]`' in text
    assert '私人.md' not in text and 'missing.png' not in text
    assert len(exporter.warnings)==3 and not manifest['images']


def test_bad_publish_and_empty_notes(setup):
    source,note,export=setup
    note('空.md','')
    with pytest.raises(ExportError,match='没有正文'): export()
    (source/'空.md').write_text('---\npublish: "true"\n---\n正文')
    with pytest.raises(ExportError,match='只能是'): export()


def test_multiline_inline_and_quoted_display_math_render(setup):
    import markdown
    _,note,export=setup
    note('公式.md','# 公式\n中文$x +\ny$中文\n\n> [!tip] 公式\n> $$\n> P=\\frac{K-1}{2}\n> $$\n> 结束')
    output,_,_=export()
    text=(output/'courses/公式.md').read_text()
    _,body=__import__('scripts.exporter',fromlist=['frontmatter']).frontmatter(text)
    html=markdown.markdown(body,extensions=['admonition','pymdownx.arithmatex'],extension_configs={'pymdownx.arithmatex':{'generic':True,'smart_dollar':False}})
    assert html.count('class="arithmatex"')==2
    assert '$$' not in html
    assert '\\frac{K-1}{2}' in html


def test_callout_with_leading_spaces_is_not_literal(setup):
    import markdown
    _,note,export=setup
    note('空格.md','# 空格\n > [! note]\n > 正文')
    output,_,_=export()
    text=(output/'courses/空格.md').read_text()
    rendered=markdown.markdown(text,extensions=['admonition'])
    assert 'class="admonition note"' in rendered
    assert '!!! note' not in rendered
