#!/bin/sh
python -m pip install --upgrade --no-cache-dir --disable-pip-version-check pip setuptools wheel && python -m pip install --requirement requirements.txt --upgrade --no-cache-dir --disable-pip-version-check
python -m vk_markovify_chatbot
