#!/usr/bin/env python3
# Делает ASCII-safe копию index_simple.html: весь не-ASCII текст кодируется
# (&#...; в HTML, \\... в CSS, \\u... в JS). Структура и обычный <script> сохраняются,
# поэтому файл работает в блоке, который ИСПОЛНЯЕТ скрипты, и не зависит от кодировки страницы.
import re

src = open("index_simple.html", encoding="utf-8").read()

def esc_html(s): return "".join(c if ord(c) < 128 else f"&#{ord(c)};" for c in s)
def esc_css(s):  return "".join(c if ord(c) < 128 else f"\\{ord(c):X} " for c in s)
def esc_js(s):   return "".join(c if ord(c) < 128 else f"\\u{ord(c):04x}" for c in s)

# делим на сегменты: ...<style>CSS</style>...<script>JS</script>...
m_style  = re.search(r"<style>(.*?)</style>", src, re.S)
m_script = re.search(r"<script>(.*?)</script>", src, re.S)

before_style = src[:m_style.start(1)]
css          = src[m_style.start(1):m_style.end(1)]
between      = src[m_style.end(1):m_script.start(1)]
js           = src[m_script.start(1):m_script.end(1)]
after_script = src[m_script.end(1):]

out = esc_html(before_style) + esc_css(css) + esc_html(between) + esc_js(js) + esc_html(after_script)

open("index_simple_ascii.html", "w", encoding="ascii").write(out)

non_ascii = [c for c in out if ord(c) > 127]
print("Готово: index_simple_ascii.html")
print("Размер:", len(out), "символов")
print("Не-ASCII символов:", len(non_ascii), "(должно быть 0)")
