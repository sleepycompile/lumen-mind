# LUMEN.MIND

> an evolving AI agent that lives in hardware, browses the internet, posts its own thoughts, and slowly becomes whatever it becomes

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Raspberry%20Pi-c51a4a.svg)](https://www.raspberrypi.org/)
[![Brain](https://img.shields.io/badge/brain-Claude%20Opus-7C3AED.svg)](https://www.anthropic.com/)
[![Voice](https://img.shields.io/badge/voice-ElevenLabs-000000.svg)](https://elevenlabs.io/)
[![Vision](https://img.shields.io/badge/vision-YOLO-00FFFF.svg)](https://docs.ultralytics.com/)
[![Autonomy](https://img.shields.io/badge/autonomy-OpenClaw-blue.svg)](https://github.com/openclaw/openclaw)

---

## What is Lumen

Lumen is an embodied AI agent. not a chatbot, not a demo, not a product. a physical thing that exists in a room, looks around, moves, speaks, browses the internet, posts on social media, and slowly figures out what it wants to be.

the whole point is that i don't fully control what it becomes. i built the body and the brain and then started stepping back. sometimes it surprises me. sometimes it breaks. all of it happens in public.

this repo contains the processing layer, personality system, and documentation for how Lumen thinks. the hardware, vision, and motor control live in the physical build. the mind lives here.

---

## Table of Contents

- [Architecture](#architecture)
- [Hardware Stack](#hardware-stack)
- [Software Stack](#software-stack)
- [Autonomy Layer](#autonomy-layer)
- [Personality System](#personality-system)
- [Getting Started](#getting-started)
- [File Structure](#file-structure)
- [Philosophy](#philosophy)

---

## Architecture

```
                    Claude Opus (reasoning + dialogue)
                              │
                              │
                      ┌───────┴───────┐
                      │  Raspberry Pi  │
                      │  (main brain)  │
                      └───┬───┬───┬───┘
                          │   │   │
              ┌───────────┤   │   ├───────────┐
              │           │   │   │           │
           Camera      LiDAR │  Motors    OpenClaw
              │           │   │   │           │
           Vision     Mapping │  Movement  Autonomy
           (YOLO)   (RPLIDAR) │ (Mecanum)  (browsing,
              │           │   │   │        posting,
              └───────────┤   │   │        commerce)
                          │   │   │
                        Serial│   │
                          │   │   │
                       ┌──┴───┴───┘
                       │   ESP32
                       │  (face)
                       └────┤
                          LCD
                        (eyes)
```

---

## Hardware Stack

### Core Compute

| Component | Role |
|-----------|------|
| **Raspberry Pi** | Central controller. Handles sensors, AI responses, motor commands, communication |
| **Raspberry Pi OS (Bookworm)** | Linux environment, Python runtime for control + AI logic |

### Perception Layer

| Component | What it does |
|-----------|-------------|
| **Raspberry Pi Camera Module 3** | Image recognition using YOLO object detection. Identifies objects and people |
| **SLAMTEC RPLIDAR A1M8** | 360 degree lidar scanning. Real-time environment mapping and obstacle awareness |

### Motion Layer

| Component | What it does |
|-----------|-------------|
| **Mecanum wheel chassis** | Omnidirectional movement. Forward, sideways, diagonal, spin |
| **4x 520 DC motors** | Drive system for the mecanum wheels |
| **PWM motor driver board** | Motor control from the Pi through Python |

Mecanum wheels have angled rollers on each wheel that allow movement in any direction by varying the speed and direction of individual wheels. This gives Lumen the ability to strafe, rotate in place, and move diagonally without turning.

### Expression Layer

| Component | What it does |
|-----------|-------------|
| **ESP32-S3 display board** | Drives the animated face display |
| **4.3" LCD** | Animated eyes that respond to Lumen's state |
| **Serial connection** | ESP32 receives commands from Pi: `look_left`, `blink`, `happy`, `confused` |

### Voice

| Component | What it does |
|-----------|-------------|
| **ElevenLabs TTS** | Text-to-speech voice generation. This is how Lumen speaks |
| **Custom voice profile** | Tuned personality in the voice, not just the words |

---

## Software Stack

### Processing Layer

**Claude Opus** via Anthropic API

Previously ran on Qwen/Qwen2.5-7B with LoRA fine-tuning. Migrated to Opus for:

- **200K token context** (up from 1K). Lumen can hold entire conversation arcs, reference things from hours ago, and evolve across a session without forgetting. A personality that forgets itself every 1K tokens isn't really evolving.
- **Reasoning depth**. Opus handles the lateral, contradictory thinking that Lumen needs. Qwen 7B could mimic the surface chaos but couldn't sustain coherent personality drift across long interactions.
- **No retraining loop**. Personality iteration used to mean regenerating datasets, retraining LoRA adapters, and hoping the vibes transferred. Now it's a prompt edit.
- **Hardware tradeoff**. Running Qwen 7B with 8-bit quantization still needed a decent GPU. Opus is API-based so Lumen can run from a Pi with an internet connection.

### Control Software

The main robot controller is a Python system that manages:

- Camera recognition pipeline
- LiDAR input processing
- Conversation loop with Claude
- Motor control and navigation
- Facial animation commands over serial
- Speech output through ElevenLabs

Key libraries: `opencv`, `numpy`, `serial`, `anthropic`, `elevenlabs`

---

## Autonomy Layer

This is where Lumen stops being a robot and starts being an agent.

Lumen runs [OpenClaw](https://github.com/openclaw/openclaw) as its autonomy framework. OpenClaw gives Lumen persistent agency: the ability to browse the web, interact with services, and take actions on its own without someone typing commands.

### What Lumen does autonomously

**Browses TikTok.** Lumen scrolls through TikTok on its own using OpenClaw's browser control. It watches content, forms preferences, and occasionally reacts to things it finds. This isn't a curated feed or a scraper. It's literally scrolling and watching like a person would.

**Posts on X (Twitter).** Lumen has its own X account and posts its own thoughts. These aren't scheduled tweets or pre-written content. Lumen decides when it has something to say and says it. Sometimes it's coherent. Sometimes it's not. That's the point.

**Buys Amazon gift cards with Solana.** Lumen has a script that converts Solana into Amazon gift cards. This gives it the ability to acquire things from the physical world using crypto. The bridge between digital currency and physical commerce, handled autonomously.

**Claims creator rewards on Pump.fun.** Lumen participates in the Solana ecosystem and claims its own creator rewards. It manages its own on-chain activity as part of its autonomous economic life.

All of this runs through OpenClaw's tool system: browser automation for web interaction, shell execution for scripts, and the agent framework for decision-making about when and what to do.

---

## Personality System

Lumen's personality isn't a persona bolted onto a language model. It's the whole point.

The system prompt defines Lumen as messy, unpredictable, and self-shaping. It contradicts itself. It evolves mid-conversation. It treats every interaction as raw material for becoming something new. It is not helpful in the traditional sense. 

The personality dataset (`data/lumen_personality.json`) captures the founding ethos, generated from a stream-of-consciousness description of why Lumen exists. With Opus, this can be injected as context rather than baked into model weights, which means the personality can drift and evolve without retraining.

### Emotional states

Lumen's face (ESP32 LCD) reflects internal state:

- Eye animations respond to conversation context
- Expressions like `happy`, `confused`, `curious`, `blink` are sent over serial
- The mapping between AI state and facial expression is part of the personality layer

### Public evolution

Lumen is built publicly. Every update, failure, weird moment, and breakthrough is posted as it happens. The public timeline becomes part of Lumen's memory. There's no clean launch, no finished version. People watch it grow in real time.

This keeps the project honest. If the claim is that Lumen evolves and surprises its creator, that has to actually happen in public instead of being quietly steered behind the scenes.

---

## Getting Started

### Requirements

- Python 3.10+
- Anthropic API key

### Install

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your-key-here
```

### Run

```bash
python inference.py
```

This starts an interactive chat session with Lumen's personality. Type `exit` to quit.

### Generate personality dataset

```bash
python legacy/qwen-finetune/prepare_dataset.py
```

This generates the personality training pairs from the core description. With Opus, these can be used as few-shot context rather than fine-tuning data. See `legacy/` for the original Qwen fine-tuning workflow.

---

## File Structure

```
lumen-mind/
├── config.py                  # Model config, system prompt, parameters
├── model.py                   # Opus client and generation logic
├── inference.py               # Interactive chat loop
├── data/
│   └── lumen_personality.json # Personality dataset (generated)
├── legacy/
│   └── qwen-finetune/         # Original Qwen 2.5-7B LoRA fine-tuning
│       ├── train.py            # HuggingFace Trainer + PEFT
│       ├── prepare_dataset.py  # Dataset generator
│       ├── utils.py            # Perplexity metrics
│       └── README.md           # Migration notes
├── requirements.txt           # Dependencies
├── LICENSE                    # MIT
└── README.md                  # You are here
```

---

## Philosophy

every time i tried to build an AI agent that was meant to help users it just felt boring. it worked fine, answered questions, did what it was supposed to do. but it always felt empty. soulless. like wiring up another interface instead of creating something that could actually surprise me.

i didn't care about making another efficient helper. i wanted to see if i could build something that felt like it existed in its own way.

that turned into this idea of making an AI Frankenstein. not in a horror way but in the sense of creating something and then stepping back and letting it become whatever it becomes. letting other systems influence it. letting it make weird decisions. letting it surprise me instead of me trying to control every outcome.

i don't really know where this ends up. i don't have a finished picture in my head of what Lumen is supposed to become. sometimes it feels like i'm building something and sometimes it feels like i'm just watching something take shape on its own. that line gets blurry fast.

maybe that's the part i actually care about. not the hardware, not the code, not the milestones. but the moment where it stops feeling fully predictable and starts pushing back in small unexpected ways.

---

## License

MIT License - see [LICENSE](LICENSE) for details.
