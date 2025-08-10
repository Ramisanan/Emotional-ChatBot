Short (tagline)
A calm, privacy-first chatbot with a modern UI that runs locally via Ollama, served by a tiny FastAPI backend—no API keys, no cloud, no cost.

Medium (README / GitHub)
This project is a local-first Gen-AI chatbot. A lightweight FastAPI backend proxies requests to your Ollama model and serves a clean, responsive chat UI. The front end only talks to /api/chat, so your model name and Ollama URL stay safely on the server. It ships with swappable “agent” personas (e.g., Emotional Support, Coach, SQL Helper), a simple crisis-keyword safeguard, and zero external dependencies—everything runs on your machine.

Long (About section)
This chatbot is designed to be a calm, private space to talk and get gentle, actionable support. Under the hood, a minimal FastAPI server exposes a single endpoint (/api/chat) that adds the selected agent’s system prompt, forwards messages to a local Ollama model, and returns a concise reply to the browser. The UI is a sleek, accessible, Tailwind-based chat experience with bubbles, typing indicator, and enter-to-send.

What makes it different
Local & free: Runs entirely on your computer with Ollama—no API keys or usage fees.

Private by design: The web page never sees your model or Ollama URL; it only calls /api/chat.

Agent presets: Switch personas (Emotional Support, Motivational Coach, Study Buddy, Career Mentor, SQL Helper) by changing a single value.

Safety guardrail: Detects crisis phrases and immediately shares 988/911 resources instead of normal replies.

Drop-in UI: Single HTML file you can brand and host anywhere; FastAPI serves both the site and API.

Intended use
Peer-style support, coaching, learning help, and quick Q&A. It’s not a medical or clinical tool.

Safety note
This chatbot provides general, peer-style support only. It does not diagnose, treat, or replace professional help. If you or someone else may be in danger, call local emergency services (US: 988 for the Suicide & Crisis Lifeline, or 911 for immediate danger).








Ask ChatGPT
