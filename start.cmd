py -m venv --upgrade-deps .venv
.venv\Scripts\python.exe -m pip install -U --disable-pip-version-check --editable .[non-termux]
.venv\Scripts\python.exe -m vk_markovify_chatbot
