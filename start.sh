#!/bin/sh
python -m pip install -U --no-cache-dir --disable-pip-version-check pip setuptools wheel && python -m pip install -U --no-cache-dir --disable-pip-version-check -r requirements.txt && python -m vk_markovify_chatbot
