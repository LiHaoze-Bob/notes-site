"""Parse Tabsdown 1.5 fenced blocks and prepare accessible site markup."""
from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import html
import re
from typing import Callable


class TabsdownError(ValueError):
    def __init__(self, message: str, line: int = 1):
        super().__init__(message)
        self.line = line


@dataclass
class Tab:
    label: str
    body: str
    icon: str | None = None


@dataclass
class Tabs:
    tabs: list[Tab]
    config_tokens: list[str] = field(default_factory=list)
    options: dict[str, str] = field(default_factory=dict)


@dataclass
class FencedTabs:
    source: str
    prefix: str
    fence: str
    start_line: int


CONFIG_VALUES = {
    'position': {'top', 'left', 'right', 'bottom'},
    'layout': {'one', 'multi'},
    'density': {'default', 'compact'},
    'personality': {'button', 'underline', 'separator', 'rail'},
    'palette': {'primary', 'secondary'},
    'alignment': {'start', 'center', 'equal-width'},
}
BARE_CONFIG = {'top': 'position', 'left': 'position', 'right': 'position',
               'bottom': 'position', 'one': 'layout', 'multi': 'layout'}
DEFAULT_OPTIONS = {
    'position': 'top',
    'layout': 'one',
    'density': 'default',
    'personality': 'button',
    'palette': 'primary',
    'alignment': 'start',
}
FENCE_RE = re.compile(r'^ {0,3}(`{3,}|~{3,})(.*)$')
OUTER_FENCE_RE = re.compile(r'^((?:(?:[ \t]*>[ \t]?)+)?[ \t]*)(`{3,}|~{3,})(.*)$')


def fence_line(line: str):
    match = FENCE_RE.match(line)
    return (match[1], match[2]) if match else (None, None)


def is_tabsdown(info: str | None) -> bool:
    return bool(info is not None and re.match(r'^[ \t]*tabsdown(?:[ \t]|$)', info))


def strip_prefix(line: str, prefix: str) -> str:
    """Strip a quote/fence prefix even when a blank quote omits its last space."""
    if not prefix:
        return line
    marker = prefix.rstrip(' \t')
    if not marker:
        if line.startswith(prefix):
            return line[len(prefix):]
        return '' if not line.strip() else line
    if not line.startswith(marker):
        return line
    value = line[len(marker):]
    return value[1:] if value.startswith((' ', '\t')) else value


def parse(source: str) -> Tabs:
    """Match Tabsdown 1.5 marker/configuration semantics."""
    tabs: list[Tab] = []
    tokens: list[str] = []
    options: dict[str, str] = {}
    keyed: set[str] = set()
    labels: set[str] = set()
    current: Tab | None = None
    open_fence: str | None = None
    nested = False
    nested_line = 0
    lines = source.splitlines(keepends=True)

    for number, raw in enumerate(lines, 1):
        ending = '\r\n' if raw.endswith('\r\n') else '\n' if raw.endswith('\n') else ''
        line = raw.removesuffix(ending)
        run, info = fence_line(line)
        if open_fence:
            if run and run.startswith(open_fence) and not (info or '').strip():
                open_fence = None
                nested = False
        elif run:
            open_fence = run
            nested = is_tabsdown(info)
            nested_line = number

        if not nested and current is None and line.startswith('config:'):
            values = [value.strip() for value in line.removeprefix('config:').split(',')]
            if values == ['']:
                raise TabsdownError('config: 后至少需要一个配置值', number)
            for value in values:
                key = BARE_CONFIG.get(value)
                if key:
                    options[key] = value
                    tokens.append(value)
                    continue
                match = re.fullmatch(r'([a-z-]+)=([^=]+)', value)
                if not match or match[1] not in CONFIG_VALUES or match[2] not in CONFIG_VALUES[match[1]]:
                    raise TabsdownError(f'未知配置值 {value!r}', number)
                key, option = match.groups()
                if key in keyed:
                    raise TabsdownError(f'配置项 {key!r} 重复', number)
                keyed.add(key)
                options[key] = option
                tokens.append(value)
            continue

        if not nested and line.startswith('tab:'):
            marker = line.removeprefix('tab:').strip()
            icon_match = re.match(r'^icon:(\S+)\s*', marker)
            icon = icon_match[1] if icon_match else None
            label = marker[icon_match.end():] if icon_match else marker
            if not icon_match and label.startswith(r'\icon:'):
                label = label[1:]
            if not label:
                raise TabsdownError('标签名称不能为空', number)
            if label in labels:
                raise TabsdownError(f'标签名称 {label!r} 重复', number)
            current = Tab(label=label, body='', icon=icon)
            tabs.append(current)
            labels.add(label)
            open_fence = None
            continue

        if current is None:
            if not line.strip():
                continue
            raise TabsdownError('第一个 tab: 标记之前不能有正文', number)

        value = line[1:] if not nested and line.startswith(r'\tab:') else line
        current.body += value + ending

    if nested:
        raise TabsdownError('嵌套的 Tabsdown 围栏没有闭合', nested_line)
    if len(tabs) < 2:
        raise TabsdownError('Tabsdown 块至少需要两个标签页')
    return Tabs(tabs=tabs, config_tokens=tokens, options=options)


def transform_blocks(text: str, transform: Callable[[FencedTabs], str]) -> str:
    """Replace actual outer Tabsdown fences without touching literal examples."""
    lines = text.splitlines()
    output: list[str] = []
    index = 0
    while index < len(lines):
        match = OUTER_FENCE_RE.match(lines[index])
        if not match:
            output.append(lines[index])
            index += 1
            continue
        prefix, opening = match[1], match[2]
        body: list[str] = []
        cursor = index + 1
        while cursor < len(lines):
            line = lines[cursor]
            unprefixed = strip_prefix(line, prefix)
            closing, info = fence_line(unprefixed)
            if (closing and closing[0] == opening[0] and len(closing) >= len(opening)
                    and not (info or '').strip()):
                break
            body.append(unprefixed)
            cursor += 1
        if cursor >= len(lines) and is_tabsdown(match[3]):
            raise TabsdownError('Tabsdown 围栏没有闭合', index + 1)
        if cursor >= len(lines):
            output.extend(lines[index:])
            break
        if not is_tabsdown(match[3]):
            output.extend(lines[index:cursor + 1])
            index = cursor + 1
            continue
        replacement = transform(FencedTabs('\n'.join(body), prefix, opening, index + 1))
        output.extend(replacement.splitlines())
        index = cursor + 1
    result = '\n'.join(output)
    return result + ('\n' if text.endswith('\n') else '')


def fence_for(text: str) -> str:
    longest = max((len(match[0]) for match in re.finditer(r'(?m)^~{3,}', text)), default=2)
    return '~' * max(3, longest + 1)


def serialize(tabs: Tabs) -> str:
    rows: list[str] = []
    if tabs.config_tokens:
        rows.extend(['config: ' + ', '.join(tabs.config_tokens), ''])
    for index, tab in enumerate(tabs.tabs):
        label = (f'icon:{tab.icon} ' if tab.icon else '') + tab.label
        rows.append('tab: ' + label)
        if tab.body:
            rows.extend(tab.body.rstrip('\r\n').splitlines())
        if index < len(tabs.tabs) - 1:
            rows.append('')
    body = '\n'.join(rows)
    fence = fence_for(body)
    return f'{fence}tabsdown\n{body}\n{fence}'


INLINE_DELIMITERS = [('**', 'strong'), ('~~', 'del'), ('`', 'code'), ('*', 'em')]


def _is_escaped(source: str, index: int) -> bool:
    slashes = 0
    index -= 1
    while index >= 0 and source[index] == '\\':
        slashes += 1
        index -= 1
    return slashes % 2 == 1


def _overlaps(source: str, delimiter: str, index: int) -> bool:
    marker = delimiter[0]
    return ((index > 0 and source[index - 1] == marker)
            or (index + len(delimiter) < len(source)
                and source[index + len(delimiter)] == marker))


def _find_close(source: str, delimiter: str, start: int) -> int:
    for index in range(start, len(source) - len(delimiter) + 1):
        if (source.startswith(delimiter, index) and not _is_escaped(source, index)
                and not _overlaps(source, delimiter, index)):
            return index
    return -1


def _contains_delimiter(source: str) -> bool:
    return any(source.startswith(delimiter, index) and not _is_escaped(source, index)
               for index in range(len(source)) for delimiter, _ in INLINE_DELIMITERS)


def render_label(value: str) -> str:
    """Render only Tabsdown's documented inline label formatting."""
    result: list[str] = []
    cursor = 0
    while cursor < len(value):
        if value[cursor] == '\\' and cursor + 1 < len(value) and value[cursor + 1] in '*~`\\':
            result.append(html.escape(value[cursor + 1]))
            cursor += 2
            continue
        found: tuple[str, str, int, str] | None = None
        for delimiter, tag in INLINE_DELIMITERS:
            if not value.startswith(delimiter, cursor) or _overlaps(value, delimiter, cursor):
                continue
            end = _find_close(value, delimiter, cursor + len(delimiter))
            if end >= 0:
                raw = value[cursor + len(delimiter):end]
                if raw.strip() and (delimiter == '`' or not _contains_delimiter(raw)):
                    found = (delimiter, tag, end, raw)
                    break
        if found:
            delimiter, tag, end, raw = found
            if delimiter != '`':
                raw = re.sub(r'\\([*~`\\])', r'\1', raw)
            result.append(f'<{tag}>{html.escape(raw)}</{tag}>')
            cursor = end + len(delimiter)
        else:
            result.append(html.escape(value[cursor]))
            cursor += 1
    return ''.join(result)


def site_markup(tabs: Tabs, body_transform: Callable[[str], str], key: str) -> str:
    options = {**DEFAULT_OPTIONS, **tabs.options}
    classes = ['tabsdown-site'] + [f'tabsdown-site--{options[name]}' for name in DEFAULT_OPTIONS]
    digest = hashlib.sha256(key.encode()).hexdigest()[:12]
    buttons = []
    panels = []
    for index, tab in enumerate(tabs.tabs):
        tab_id = f'tabsdown-{digest}-tab-{index}'
        panel_id = f'tabsdown-{digest}-panel-{index}'
        label = render_label(tab.label)
        buttons.append(
            f'<button type="button" id="{tab_id}" class="tabsdown-site__tab" '
            f'aria-controls="{panel_id}" aria-selected="{str(index == 0).lower()}" '
            f'tabindex="{0 if index == 0 else -1}">{label}</button>'
        )
        content = body_transform(tab.body).strip()
        panels.append(
            f'<section id="{panel_id}" class="tabsdown-site__panel" '
            f'aria-labelledby="{tab_id}" markdown="block">\n\n'
            f'<div class="tabsdown-site__fallback-label">{label}</div>\n\n'
            f'{content}\n\n</section>'
        )
    return (
        f'<div class="{" ".join(classes)}" data-tabsdown-site markdown="block">\n\n'
        '<div class="tabsdown-site__tablist">\n'
        + '\n'.join(buttons)
        + '\n</div>\n\n<div class="tabsdown-site__panels" markdown="block">\n\n'
        + '\n\n'.join(panels)
        + '\n\n</div>\n\n</div>'
    )
