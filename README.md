# Калькулятор экономии от внедрения BitrixGPT

Интерактивный калькулятор экономического эффекта от внедрения ИИ **BitrixGPT** в Битрикс24.
Самодостаточный фронтенд (HTML + CSS + JS), **без бэкенда** — все расчёты выполняются в браузере.

## Возможности
- **10 сценариев**, сгруппированных: «Сценарии в CRM», «ИИ-агенты» (Агент для CRM, Агент общения с клиентами, Агент по базе знаний), «Другие сценарии» (Follow-up, BitrixGPT для всех), «VibeCode».
- Липкая **панель навигации** с быстрыми переходами по группам и живым итогом «Эффект: X ₽/мес».
- Мгновенный пересчёт, разделители разрядов в полях, валидация.
- Итоговый блок: экономия ФОТ, прирост выручки, общий эффект (месяц/год), строка стоимости подписки и вывод «выгоднее в N×».
- **Экспорт результата в PDF** (через печать) с диалогом выбора тарифа Битрикс24 и названием компании.

## Структура репозитория
```
index.html                      ← ПОЛНАЯ версия (это и есть сайт GitHub Pages)
.nojekyll                       ← отключает Jekyll (для статичного HTML)
README.md
docs/
  TZ.md                         ← техническое задание (формулы, сценарии, эталонные примеры)
variants/
  index_simple.html             ← без экспорта и диалога тарифов (UTF-8)
  index_simple_ascii.html       ← то же, но текст в ASCII-кодах (для вставки в CMS с чужой кодировкой)
  embed_bitrix24.html           ← фрагмент для вставки в HTML-блок (scoped CSS + ASCII + bootstrap-запуск)
build/
  build_embed.py                ← генератор embed_bitrix24.html из index_simple.html
  build_ascii.py                ← генератор index_simple_ascii.html из index_simple.html
```

> Какой файл использовать:
> - **Хостинг / GitHub Pages / iframe** → `index.html` (или `variants/index_simple.html`, если экспорт не нужен).
> - **Вставка кода в чужую CMS** → `variants/embed_bitrix24.html` или `variants/index_simple_ascii.html`.
> Примечание: конструктор «Битрикс24.Сайты» вырезает `<script>` из HTML-блока — туда калькулятор подключается только через **iframe**.

## Публикация на GitHub Pages
1. Создайте репозиторий на GitHub.
2. Загрузите содержимое этой папки (минимально нужны `index.html` и `.nojekyll`).
3. **Settings → Pages → Build and deployment**: Source = *Deploy from a branch*, Branch = **main**, папка = **/ (root)**. Сохраните.
4. Через 1–2 минуты сайт будет доступен: `https://<логин>.github.io/<репозиторий>/`

### Через git
```bash
git init
git add .
git commit -m "BitrixGPT calculator"
git branch -M main
git remote add origin https://github.com/<логин>/<репозиторий>.git
git push -u origin main
```

## Встраивание через iframe (в т.ч. в Битрикс24)
```html
<iframe src="https://<логин>.github.io/<репозиторий>/"
        style="width:100%;border:0;min-height:1600px"
        title="Калькулятор BitrixGPT"
        loading="lazy"></iframe>
```
`min-height` подбирается под высоту контента (при раскрытии всех сценариев страница выше).

## Пересборка вариантов (необязательно)
Скрипты рассчитаны на запуск из каталога с исходниками `index.html` / `index_simple.html`:
```bash
python3 build/build_embed.py    # -> embed_bitrix24.html
python3 build/build_ascii.py    # -> index_simple_ascii.html
```

## Методика расчёта
Все формулы, сценарии, константы (налоговая нагрузка ×1,4; 176 рабочих часов; и т.д.) и эталонные примеры
описаны в [docs/TZ.md](docs/TZ.md). Цены подписки BitrixGPT приведены при оплате за год.
Расчёт носит оценочный характер.
