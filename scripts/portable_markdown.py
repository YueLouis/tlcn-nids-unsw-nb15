"""Make repository Markdown links usable in downloaded standalone copies."""
from pathlib import Path
import re
from urllib.parse import quote, unquote, urlsplit


REPOSITORY = 'https://github.com/YueLouis/tlcn-nids-unsw-nb15'
LINK = re.compile(
    r'(?P<prefix>(?<!!)\[[^\]\n]*\]\()'
    r'(?P<target><[^>\n]+>|[^\s)\n]+)'
    r'(?P<suffix>(?:\s+(?:"[^"\n]*"|\'[^\'\n]*\'))?\))'
)


def render_portable_markdown(text: str, source: Path, root: Path) -> str:
    """Rewrite local links only; source files and external URLs stay unchanged."""
    root = root.resolve()
    source = source.resolve()
    source.relative_to(root)

    def replace(match: re.Match) -> str:
        original = match['target']
        bracketed = original.startswith('<')
        href = original[1:-1] if bracketed else original
        parsed = urlsplit(href)
        if parsed.scheme or parsed.netloc:
            return match[0]
        target = (source.parent / unquote(parsed.path)).resolve() if parsed.path else source
        try:
            relative = target.relative_to(root)
        except ValueError as exc:
            raise ValueError(f'Markdown link leaves repository: {href}') from exc
        if not target.exists():
            raise ValueError(f'Markdown link does not exist: {href}')
        kind = 'tree' if target.is_dir() else 'blob'
        url = f'{REPOSITORY}/{kind}/main/{quote(relative.as_posix(), safe="/-._~")}'
        if parsed.query:
            url += '?' + parsed.query
        if parsed.fragment:
            url += '#' + quote(unquote(parsed.fragment), safe='-._~')
        if bracketed:
            url = '<' + url + '>'
        return match['prefix'] + url + match['suffix']

    return LINK.sub(replace, text)
