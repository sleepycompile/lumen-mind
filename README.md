# Bloomed Terminal

[![Made with Python](https://img.shields.io/badge/made%20with-Python-3776AB.svg)](https://www.python.org/)
[![CI](https://github.com/dev-nightshift/bloomed-terminal/actions/workflows/hourly_backrooms.yml/badge.svg)](https://github.com/dev-nightshift/bloomed-terminal/actions/workflows/hourly_backrooms.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-lightgrey.svg)](./LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=shields)](http://makeapullrequest.com)

A compact text-generation service with a consistent house style and an automated publishing loop. Bloomed Terminal runs a lightweight local model behind a clean HTTP API and delivers fresh entries to Firebase Realtime Database every hour via a secured scheduler.

<p align="center">
  <img src="assets/bloomed.png" alt="Bloomed Terminal" width="960">
</p>

---

# Table of contents

- [Overview](#overview)
- [Features](#features)
- [API](#api)
- [Hourly Automation](#hourly-automation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

# Overview

Bloomed Terminal blends a small local LLM with a minimal FastAPI surface and a personality layer for tone control. On a schedule, it produces compact, grounded entries with a six-turn exchange, then stores them with metadata for lightweight downstream use.

---

# Features

- Local, lightweight model that runs on typical workstations and uses GPU if available.
- Clean HTTP surface: /health, /v1/model_info, and /v1/chat.
- House style via built-in personas; you can supply a system message when needed.
- Automated cadence: a secured, hourly pipeline writes new entries to Firebase Realtime Database.
- Audit-friendly: entries include per-message timestamps, model identifier, and a short preview.

---

# API

Health

```
GET /health
-> { "ok": true }
```

Model info

```
GET /v1/model_info
-> basic configuration of the loaded model (directory, layers, vocab, etc.)
```

Chat

```
POST /v1/chat
Body: { "messages": [ { "role": "user", "content": "..." } ], ... }
-> { "content": "..." }
```

---

# Hourly Automation

This repository includes a workflow that runs every hour (UTC) and triggers a secured API to generate and store a fresh entry. The endpoint is protected so only the trusted scheduler can invoke it; successful generations record model details and message timestamps for traceability.

---

# Usage

- Local API: run the FastAPI app and POST prompts to /v1/chat.
- Personas: use the default house voice or include a system message to steer tone.
- Observability: check /health and /v1/model_info for quick diagnostics.
- Data: generated entries land in Firebase Realtime Database with title, participants, messages, and metadata.

---

# Project Structure

```
app/
  server.py        # FastAPI endpoints
  inference.py     # model load + generate()
  settings.py      # env-backed config
  schemas.py       # request/response models
  personalities.py # house personas
  model_info.py    # model config helper
scripts/
  quick_local.py   # local generation demo
  client_demo.py   # API caller
  download_model.py
  prewarm.py
  run_tests.bat
.github/
  workflows/
    hourly_backrooms.yml  # hourly scheduler (secured)
```

---

# Contributing

Issues and PRs are welcome. Keep changes focused and tested.

---

# License

MIT. See LICENSE.
