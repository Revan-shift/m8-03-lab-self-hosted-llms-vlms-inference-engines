# Self-Hosting Report

## Task 1 — Benchmark: Two Local Models

**Prompt used for both models:**
> "Explain what a large language model is in 3 sentences."

### Results Table

| Metric | llama3.2:3b | qwen2.5:0.5b |
|---|---|---|
| **Model size** | 2.0 GB | 397 MB |
| **Load time (first run)** | 5.98 s | 1.67 s |
| **Prompt eval rate** | 35.69 tokens/s | 578.97 tokens/s |
| **Generation rate** | 88.04 tokens/s | 204.74 tokens/s |
| **GPU VRAM used** | ~2.5 GB | ~2.5 GB |
| **Subjective quality** | Clear, well-structured answer with precise technical vocabulary | Correct but simpler phrasing; minor repetition ("summarizing texts... writing articles") |

> *Measured on Windows 11, NVIDIA GeForce RTX GPU, 32 GB RAM. Ollama ran models on GPU (VRAM offload).*

### Trade-off Analysis

The smaller `qwen2.5:0.5b` model loaded 3.6× faster (1.67s vs 5.98s) and processed prompts at an extraordinary 579 tokens/s — over 16× faster than llama3.2:3b on prompt evaluation. However, `llama3.2:3b` produced noticeably more coherent and precise language with better technical depth, while the 0.5b output was correct but repetitive in places. The core trade-off is **output quality vs. speed**: for simple or high-throughput tasks qwen2.5:0.5b is dramatically faster, but for nuanced explanations llama3.2:3b delivers significantly better results.

---

## Task 2 — Local Client

See `local_client.py`. The key insight captured in the comment block:

> Calling a local Ollama model is *structurally identical* to calling a hosted API — both are HTTP POST requests to a `/v1/chat/completions` endpoint with the same JSON body and response format. Only the `base_url` changes (`localhost:11434` instead of a remote server). The OpenAI Python SDK works unchanged.

---

## Task 3 — VLM Comparison: moondream (local) vs Gemini 2.0 Flash (hosted)

**Image used:** `sample_chart.png` — "Inference Speed by Model" bar chart (4 bars: Qwen2.5 0.5B=98, Llama 3.2 3B=61, Gemma 3 4B=44, Llama 3.1 8B=27 tok/s)  
**Task asked:** *"How many bars are in this chart and what is the tallest bar's label?"*

### Results Table

| Metric | moondream (local, ~1.7 GB) | Gemini 2.0 Flash (hosted, free tier) |
|---|---|---|
| **Answer** | "There are four bars. The tallest bar has the word 'faster' written above it." | "There are 4 bars. The tallest bar's label is Qwen2.5 0.5B." |
| **Bar count accuracy** | ✅ Correct (4) | ✅ Correct (4) |
| **Label accuracy** | ❌ Incorrect (hallucinated "faster") | ✅ Correct ("Qwen2.5 0.5B") |
| **Response time** | ~3 s (local GPU) | ~3.7 s (network + inference) |
| **Cost** | $0 (electricity only) | $0 (free tier quota) |

### Analysis

Gemini clearly outperformed moondream on OCR and label recognition — it correctly identified "Qwen2.5 0.5B" as the tallest bar's label while moondream hallucinated "faster," likely misreading the subtitle text ("higher is faster") from the chart. Both models correctly counted 4 bars, showing that basic visual counting is within reach of even a tiny local VLM. Response times were surprisingly similar (~3s each) but for different reasons: moondream ran locally on an NVIDIA GPU with no network overhead, while Gemini's extra 0.7s came from network round-trip latency. Cost is zero for both in this scenario, but at scale the hosted model incurs per-token fees while the local model's only cost is electricity and amortized hardware.

---

## Overall Findings

Running models locally is surprisingly straightforward: one binary (Ollama), one pull command, and you have an OpenAI-compatible inference server on your laptop. The workflow is identical to calling a hosted API — just change the `base_url`. The real constraints are RAM (models need to fit entirely in memory for reasonable speed) and compute (a GPU accelerates inference 5–20×, but CPU is workable for small models). For production use cases, hosted APIs win on speed and capability; for privacy-sensitive or offline scenarios, local inference is a genuine alternative.
