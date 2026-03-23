# funstat-api

Python-клиент для [Funstat](http://funstat.in/?start=0108FC1E9BEF75617466) API — статистика пользователей и групп Telegram.

Поддерживает **синхронный** и **асинхронный** режимы работы.

## Установка

```bash
pip install funstat-api
```

## Быстрый старт

### Синхронно

```python
from funstat_api import FunstatClient

fs = FunstatClient("your_token")

# Статистика пользователя
stats = fs.stats("durov")
print(stats.data.total_msg_count)

# Участники группы
members = fs.get_group_members("https://t.me/mychat")

# Использование как контекстный менеджер
with FunstatClient("your_token") as fs:
    print(fs.ping())
```

### Асинхронно

```python
import asyncio
from funstat_api import AsyncFunstatClient

async def main():
    async with AsyncFunstatClient("your_token") as fs:
        stats = await fs.stats("durov")
        print(stats.data.total_msg_count)

asyncio.run(main())
```

## Доступные методы

| Метод | Описание |
|-------|----------|
| `ping()` | Проверить доступность API и задержку |
| `get_balance()` | Получить баланс токена |
| `resolve_username(username)` | Получить информацию по username |
| `basic_info_by_id(ids)` | Базовая информация по ID пользователя(ей) |
| `stats_min(user)` | Минимальная статистика пользователя |
| `stats(user)` | Полная статистика пользователя |
| `messages_count(user)` | Общее количество сообщений |
| `groups_count(user)` | Количество групп |
| `get_messages(user, ...)` | Список сообщений с пагинацией |
| `get_chats(user)` | Список чатов пользователя |
| `get_names(user)` | История имён |
| `get_usernames(user)` | История username'ов |
| `get_stickers(user)` | Использованные стикерпаки |
| `get_gifts(user)` | Подарки и их отправители |
| `common_groups(user)` | Статистика общих групп |
| `username_usage(username)` | Кто использует или использовал username |
| `get_group_info(group)` | Информация о группе/канале |
| `get_group_members(group)` | Участники группы |
| `search_text(query)` | Поиск сообщений по тексту |

Аргументы `user` и `group` принимают: числовой ID, `@username` или ссылку `https://t.me/...`.

## Зависимости

- `pydantic >= 2.0`
- `requests >= 2.28` (синхронный клиент)
- `httpx >= 0.24` (асинхронный клиент)

## Лицензия

MIT
