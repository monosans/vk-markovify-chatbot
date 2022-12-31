# vk-markovify-chatbot

Бот, генерирующий сообщения Марковским процессом на основе сообщений из чата. Для каждого чата ведёт отдельную историю сообщений в SQLite.

## Установка и запуск

- [Скачиваем архив с ботом](https://github.com/monosans/vk-markovify-chatbot/archive/refs/heads/main.zip).
- Распаковываем архив.
- Переходим в группу, в которой размещаем бота:
  1. Управление
  1. Настройки
  1. Работа с API
  1. Создать ключ
  1. Выставляем галочки и создаем
  1. Копируем и вставляем полученный токен в `config.ini`
  1. При желании настраиваем прочие параметры в `config.ini`
- Настраиваем Long Poll API:
  1. Управление
  1. Настройки
  1. Работа с API
  1. Вкладка Long Poll API
  1. Long Poll API: Включено + Версия API: самая новая
  1. Вкладка Типы событий
  1. Ставим все галочки раздела "Сообщения"
- Даём группе возможность писать сообщения и позволяем добавлять её в беседы:
  1. Управление
  1. Сообщения
  1. Сообщения сообщества: Включены
  1. Настройки для бота
  1. Возможности ботов: Включены
  1. Разрешать добавлять сообщество в беседы - ставим галочку
- Устанавливаем [Python](https://python.org/downloads) (для Windows 7 нужен Python 3.8.X). Во время установки обязательно ставим галочку `Add Python to PATH (Добавить Python в PATH)`.
- Устанавливаем зависимости и запускаем скрипт. Есть 2 способа сделать это:
  - Автоматический:
    - На Windows запускаем `start.cmd`
    - На Unix-подобных ОС запускаем `start.sh`
  - Ручной:
    1. `cd` в распакованную папку
    1. Устанавливаем зависимости командой `python -m pip install --upgrade --no-cache-dir --disable-pip-version-check pip setuptools wheel; python -m pip install --requirement requirements.txt --upgrade --no-cache-dir --disable-pip-version-check`
    1. Запускаем командой `python -m vk_markovify_chatbot`

## License / Лицензия

[MIT](LICENSE)
