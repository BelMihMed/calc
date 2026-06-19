#!/usr/bin/env python3
# Генерирует ASCII-safe фрагмент для вставки в HTML-блок Битрикс24.
import re, sys

src = open("index.html", encoding="utf-8").read()

css    = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
js     = re.search(r"<script>(.*?)</script>", src, re.S).group(1)
markup = re.search(r"<body>(.*?)<script>", src, re.S).group(1)

# --- убрать CSS-комментарии ---
css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)

# --- скоупинг CSS под .bgpt ---
def scope_selector(p):
    p = p.strip()
    if not p:
        return p
    if p in (":root", "body"):
        return ".bgpt"
    if p == "*":
        return ".bgpt *,.bgpt *::before,.bgpt *::after"
    return ".bgpt " + p

def scope_block(s):
    out, i, n = "", 0, len(s)
    while i < n:
        brace = s.find("{", i)
        if brace == -1:
            out += s[i:]
            break
        selector = s[i:brace].strip()
        depth, j = 1, brace + 1
        while j < n and depth > 0:
            if s[j] == "{": depth += 1
            elif s[j] == "}": depth -= 1
            j += 1
        body = s[brace + 1:j - 1]
        if selector.startswith("@media"):
            out += selector + "{" + scope_block(body) + "}"
        elif selector.startswith("@"):
            out += selector + "{" + body + "}"
        else:
            out += ",".join(scope_selector(p) for p in selector.split(",")) + "{" + body + "}"
        i = j
    return out

css = scope_block(css)

# --- ASCII-escape по контекстам ---
def esc_html(s): return "".join(c if ord(c) < 128 else f"&#{ord(c)};" for c in s)
def esc_css(s):  return "".join(c if ord(c) < 128 else f"\\{ord(c):X} " for c in s)
def esc_js(s):   return "".join(c if ord(c) < 128 else f"\\u{ord(c):04x}" for c in s)

# JS храним в <textarea> (санитайзеры его не трогают и не парсят теги внутри),
# а запускаем «бутстрапом» через <img onload> -> создаём настоящий <script>.
# Это нужно потому, что блоки Битрикс вставляют HTML через innerHTML,
# а <script>, вставленный так, браузером НЕ выполняется.
js_ascii = esc_js(js).strip()
js_ta = js_ascii.replace("&", "&amp;").replace("<", "&lt;")  # .value вернёт исходный JS

GIF = "R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"  # валидный 1x1 gif
boot = ("(function(){if(window.__bgptInit)return;window.__bgptInit=1;"
        "var t=document.getElementById('bgpt-src');if(!t)return;"
        "var s=document.createElement('script');s.text=t.value;document.body.appendChild(s);})()")

fragment = (
    "<style>\n" + esc_css(css).strip() + "\n</style>\n"
    + '<div class="bgpt">' + esc_html(markup).strip() + "</div>\n"
    + '<textarea id="bgpt-src" style="display:none" aria-hidden="true">\n' + js_ta + "\n</textarea>\n"
    + '<img src="data:image/gif;base64,' + GIF + '" alt="" '
      'style="display:none;width:0;height:0;position:absolute" '
      'onload="' + boot + '">\n'
)

open("embed_bitrix24.html", "w", encoding="ascii").write(fragment)

# тест: вставка фрагмента ИМЕННО через innerHTML (имитация блока Битрикс)
import base64
b64 = base64.b64encode(fragment.encode("ascii")).decode("ascii")
test = (
    "<!DOCTYPE html><html lang='ru'><head><meta charset='UTF-8'>"
    "<title>Тест innerHTML</title></head><body style='font-family:sans-serif;padding:20px'>"
    "<h3>Симуляция вставки в блок Битрикс24 (через innerHTML)</h3>"
    "<p>Текст страницы сверху — для проверки, что стили не утекают.</p><hr>"
    "<div id='host'></div>"
    "<scr" + "ipt>document.getElementById('host').innerHTML=atob('" + b64 + "');</scr" + "ipt>"
    "</body></html>"
)
open("test_innerhtml.html", "w", encoding="utf-8").write(test)

# проверка: чистый ASCII?
non_ascii = [c for c in fragment if ord(c) > 127]
print("Готово: embed_bitrix24.html")
print("Размер:", len(fragment), "символов")
print("Не-ASCII символов:", len(non_ascii), "(должно быть 0)")
