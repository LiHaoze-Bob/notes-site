import pytest

from scripts.tabsdown import TabsdownError, parse, render_label, serialize, transform_blocks


def test_parser_keeps_nested_tabsdown_inside_the_current_panel():
    source = '''config: position=left, layout=multi, density=compact

tab: 外层一
~~~~tabsdown
tab: 内层一
A
tab: 内层二
B
~~~~

tab: 外层二
C
'''
    tabs = parse(source)
    assert tabs.options == {'position': 'left', 'layout': 'multi', 'density': 'compact'}
    assert [tab.label for tab in tabs.tabs] == ['外层一', '外层二']
    assert 'tab: 内层二' in tabs.tabs[0].body
    assert parse(transform_blocks(serialize(tabs), lambda block: block.source)).tabs[1].body.strip() == 'C'


@pytest.mark.parametrize('source, message', [
    ('tab: 只有一个\n正文', '至少需要两个'),
    ('tab: A\n1\ntab: A\n2', '重复'),
    ('config: layout=bad\ntab: A\n1\ntab: B\n2', '未知配置'),
])
def test_parser_rejects_invalid_blocks(source, message):
    with pytest.raises(TabsdownError, match=message):
        parse(source)


def test_literal_example_is_not_transformed_and_label_markup_is_safe():
    source = '````md\n```tabsdown\ntab: A\n1\ntab: B\n2\n```\n````\n'
    assert transform_blocks(source, lambda block: 'CHANGED') == source
    assert render_label(r'\*plain\* **strong** <script>') == (
        '*plain* <strong>strong</strong> &lt;script&gt;')


def test_blockquoted_tabs_accept_blank_quote_lines_without_trailing_space():
    source = '> ```tabsdown\n> config: layout=one\n>\n> tab: A\n> 一\n>\n> tab: B\n> 二\n> ```\n'
    found = []
    transform_blocks(source, lambda block: found.append(parse(block.source)) or 'done')
    assert [tab.label for tab in found[0].tabs] == ['A', 'B']


def test_indented_tabs_inside_generated_admonitions_are_transformed():
    source = '!!! note\n    正文\n\n    ```tabsdown\n    tab: A\n    一\n    tab: B\n    二\n    ```\n'
    found = []
    transform_blocks(source, lambda block: found.append(parse(block.source)) or '    done')
    assert [tab.label for tab in found[0].tabs] == ['A', 'B']
