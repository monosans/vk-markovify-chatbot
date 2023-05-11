# vk-markovify-chatbot

[![CI](https://github.com/monosans/vk-markovify-chatbot/actions/workflows/ci.yml/badge.svg)](https://github.com/monosans/vk-markovify-chatbot/actions/workflows/ci.yml)

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
- Устанавливаем [Python](https://python.org/downloads) (минимальная требуемая версия - 3.7).
- Устанавливаем зависимости и запускаем скрипт. Есть 2 способа сделать это:

  - Автоматический:
    - На Windows запускаем `start.cmd`
    - На Unix-подобных ОС запускаем `start.sh`
  - Ручной:
    <details>
      <summary>Windows (нажмите, чтобы развернуть)</summary>

    1. `cd` в распакованную папку

    1. Устанавливаем зависимости командой:

       ```bash
       py -m pip install -U --no-cache-dir --disable-pip-version-check pip setuptools wheel; py -m pip install -U --no-cache-dir --disable-pip-version-check -r requirements.txt
       ```

    1. Запускаем командой:

       ```bash
       py -m vk_markovify_chatbot
       ```

    </details>
    <details>
      <summary>Unix-подобные ОС (нажмите, чтобы развернуть)</summary>

    1. `cd` в распакованную папку

    1. Устанавливаем зависимости командой:

       ```bash
       python3 -m pip install -U --no-cache-dir --disable-pip-version-check pip setuptools wheel && python3 -m pip install -U --no-cache-dir --disable-pip-version-check -r requirements.txt
       ```

    1. Запускаем командой:

       ```bash
       python3 -m vk_markovify_chatbot
       ```

    </details>

## License / Лицензия

[MIT](LICENSE)
