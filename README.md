# vk-markovify-chatbot

[![CI](https://github.com/monosans/vk-markovify-chatbot/actions/workflows/ci.yml/badge.svg)](https://github.com/monosans/vk-markovify-chatbot/actions/workflows/ci.yml)

Бот, генерирующий сообщения Марковским процессом на основе сообщений из чата. Для каждого чата ведёт отдельную историю сообщений в SQLite.

## Получение токена бота

- Перейдите в группу, в которой размещаете бота:
  1. Управление
  1. Настройки
  1. Работа с API
  1. Создать ключ
  1. Поставьте все галочки и нажмите "Создать"
  1. Скопируйте полученный токен
- Настройте Long Poll API:
  1. Управление
  1. Настройки
  1. Работа с API
  1. Вкладка Long Poll API
  1. Long Poll API: включено
  1. Версия API: самая новая
  1. Вкладка Типы событий
  1. Поставьте все галочки раздела "Сообщения"
- Дайте группе возможность писать сообщения и позвольте добавлять её в беседы:
  1. Управление
  1. Сообщения
  1. Сообщения сообщества: Включены
  1. Настройки для бота
  1. Возможности ботов: Включены
  1. Поставьте галочку "Разрешать добавлять сообщество в беседы"

## Установка и запуск

### Исполняемый файл

Это самый простой способ, но он доступен только для x86_64 Windows, x86_64/arm64 macOS и x86_64 Linux. Просто скачайте архив для вашей ОС с [nightly.link](https://nightly.link/monosans/vk-markovify-chatbot/workflows/ci/main?preview), распакуйте его, отредактируйте `config.toml` и запустите исполняемый файл.

Если Защитник Windows обнаружит исполняемый файл как вирус, прочтите [это](https://github.com/Nuitka/Nuitka/issues/2495#issuecomment-1762836583).

### Docker

- [Установите `Docker Compose`](https://docs.docker.com/compose/install/).
- Скачайте и распакуйте [архив с программой](https://github.com/monosans/vk-markovify-chatbot/archive/refs/heads/main.zip).
- Отредактируйте `config.toml`.
- Выполните следующие команды:
  ```bash
  docker compose build --pull
  docker compose up --no-log-prefix
  ```

### Запуск из исходного кода

#### ПК

- Установите [Python](https://python.org/downloads). Минимальная необходимая версия - 3.8.
- Скачайте и распакуйте [архив с программой](https://github.com/monosans/vk-markovify-chatbot/archive/refs/heads/main.zip).
- Отредактируйте `config.toml`.
- Запустите скрипт, который устанавливает зависимости и запускает `vk-markovify-chatbot`:
  - В Windows запустите `start.cmd`.
  - В Unix-подобных операционных системах запустите `start.sh`.

#### Termux

Чтобы использовать `vk-markovify-chatbot` в Termux, необходимо знание интерфейса командной строки Unix.

- Загрузите Termux с сайта [F-Droid](https://f-droid.org/en/packages/com.termux/). [Не загружайте его из Google Play](https://github.com/termux/termux-app#google-play-store-deprecated).
- Выполните следующую команду (она автоматически обновит пакеты Termux, установит Python, а также загрузит и установит `vk-markovify-chatbot`):

  ```bash
  bash <(curl -fsSL 'https://raw.githubusercontent.com/monosans/vk-markovify-chatbot/main/install-termux.sh')
  ```

- Отредактируйте `~/vk-markovify-chatbot/config.toml` с помощью текстового редактора (vim/nano).
- Для запуска `vk-markovify-chatbot` используйте следующую команду:
  ```bash
  cd ~/vk-markovify-chatbot && sh start-termux.sh
  ```

## License / Лицензия

[MIT](LICENSE)
