"""Telegram HTML style helper functions"""

from html import escape as __escape

def escape(txt):
    """`txt` is automatically turned to `str`"""
    return __escape(str(txt))

def bold(txt: str) -> str:
    """`txt` is **not** escaped automatically"""
    return f"<b>{txt}</b>"

def italic(txt: str) -> str:
    """`txt` is **not** escaped automatically"""
    return f"<i>{txt}</i>"

def underline(txt: str) -> str:
    """`txt` is **not** escaped automatically"""
    return f"<u>{txt}</u>"

def strikethrough(txt: str) -> str:
    """`txt` is **not** escaped automatically"""
    return f"<s>{txt}</s>"

def link(txt: str, href: str) -> str:
    """`txt` is **not** escaped automatically"""
    return f"<a href=\"{href}\">{txt}</a>"

def spoiler(txt: str) -> str:
    """`txt` is **not** escaped automatically"""
    return f"<tg-spoiler>{txt}</tg-spoiler>"

def code(txt: str) -> str:
    """`txt` is **not** escaped automatically"""
    return f"<code>{txt}</code>"

def pre(txt: str) -> str:
    """`txt` is **not** escaped automatically"""
    return f"<pre>{txt}</pre>"

def codeblock(code: str, lang: str):
    """`code` is **not** escaped automatically  
    
    If you don't need a language, use `pre` instead.
    """
    return f"<pre><code class=\"{lang}\">{code}</code></pre>"

def blockquote(txt: str, expandable: bool = False) -> str:
    """`txt` is **not** escaped automatically"""
    return f"<blockquote{" expandable" if expandable else ""}>{txt}</blockquote>"

def python(code: str) -> str:
    """`code` is escaped automatically"""
    return codeblock(escape(code), "python")

def bash(code: str) -> str:
    """`code` is escaped automatically"""
    return codeblock(escape(code), "bash")


