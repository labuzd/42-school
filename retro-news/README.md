# Ретро Авто Новости

Мини-программа, которая раз в час:

1. собирает новости о классических и ретро-автомобилях из RSS-лент (`config.toml`);
2. отсеивает дубли (по ссылке и заголовку), а с общих автосайтов берёт только ретро-тематику;
3. публикует свежие новости в Telegram-канал;
4. пересобирает статический сайт и выкладывает его на GitHub Pages.

Внешних сервисов, кроме GitHub и Telegram, не нужно. Из зависимостей только `feedparser`.

## Как это устроено

```
config.toml          источники, ключевые слова, лимиты
data/news.json       все собранные новости + флаг «уже в Telegram» (коммитится автоматически)
retronews/sources.py загрузка и разбор RSS, фильтр, картинки
retronews/storage.py хранилище и дедупликация
retronews/telegram.py публикация в канал
retronews/site.py    генерация site/index.html
.github/workflows/retro-news.yml  запуск по расписанию
```

## Настройка

### 1. Telegram

1. Создайте бота у [@BotFather](https://t.me/BotFather) (`/newbot`) и сохраните токен.
2. Добавьте бота в свой канал администратором с правом публиковать сообщения.
3. В репозитории: **Settings → Secrets and variables → Actions → New repository secret**:
   - `TELEGRAM_BOT_TOKEN`: токен бота;
   - `TELEGRAM_CHAT_ID`: `@имя_канала` (для приватного канала числовой id вида `-100…`).

### 2. Сайт

**Settings → Pages → Build and deployment → Source: GitHub Actions.**
Сайт будет доступен по адресу `https://<user>.github.io/<repo>/`.

### 3. Запуск

Расписание GitHub срабатывает только на ветке по умолчанию (`master`), поэтому сначала влейте эту ветку.
Затем откройте **Actions → retro-news → Run workflow**, чтобы запустить вручную.

При первом запуске в канал уйдут не больше `max_posts_per_run` новостей не старше `max_age_days` дней,
поэтому старые новости не зальют канал.

## Локальный запуск

```bash
cd retro-news
pip install -r requirements.txt
python -m unittest                 # тесты
python -m retronews --no-telegram  # собрать новости и сайт (site/index.html)

# с публикацией в канал:
TELEGRAM_BOT_TOKEN=... TELEGRAM_CHAT_ID=@my_channel python -m retronews
```

## Источники

Добавляются в `config.toml`:

```toml
[[sources]]
name = "Мой источник"
url = "https://example.com/feed/"
filter = true   # true — брать только новости с ключевыми словами или годами 1900–1999
```

Если источник недоступен, в лог пишется предупреждение, а остальные продолжают работать.
