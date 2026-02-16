# ⚡ VBD Indexer

> High-performance Python indexer & analyzer for **VeChain B3TR / VeBetterDAO** events.  
> Designed for **speed, correctness, and production-grade data pipelines**.

---

## ✨ Features

- 🔎 **On-chain event indexing** from VeChain Thor
- ⚙️ **Parallel worker architecture** for fast block scanning
- 🧠 **ABI decoding** of complex Solidity return types & events
- 🗂 **CSV export** of event data for data analytics workflows
- 📊 **JSON export** of summaries & analysis for frontend applications
- 🧱 Clean **modular SDK-style structure**
- 🚀 Ready for **CLI usage, automation, and CI pipelines**

---

## 🏗 Architecture

    src/vbd_indexer/
    ├── app.py          # CLI entrypoint
    ├── thor/           # Thor rest client
    ├── indexer/        # Parallel indexing engine
    ├── b3tr/           # Contract helpers, decoders, transformers
    └── utils/          # Units, formatting, helpers

Core principles:

-   **Deterministic indexing**
-   **Typed decoding**
-   **Separation of concerns**
-   **Analytics-friendly outputs**
-   **Follows principles of extract, decode, transform, analyse**

---

## 📦 Installation

### Requirements

- Python **3.11+**
- [Poetry](https://python-poetry.org)

### Setup

```bash
git clone https://github.com/yourname/vbd-indexer.git
cd vbd-indexer
poetry install
```

---

## 🚀 Usage

To extract event data for a round into a CSV file:

``` bash
poetry run vbd-indexer extract <round id>
```

To produce a json summary from the generated CSV file:

``` bash
poetry run vbd-indexer summarize <round id>
```

---

## 🔗 What it Indexes

Currently focused on:

-   **B3TR reward distribution events**

---

## 📊 Data Output

CSV output:

-   `rewards-events-round-<round_id>.csv`

Optimized for:

-   **Data analysis & Machine learning pipelines**

JSON output:

- `rewards-events-summary-round-<round_id>.json`

Optimized for:

-   **Front end applications**

---

## 🛣 Roadmap

-   [ ] More VBD events supported
-   [ ] PyPI package release
-   [ ] Public VeBetterDAO analytics dashboard

---

## 🤝 Contributing

PRs welcome.

If you're working on:

-   VeChain tooling
-   Data pipelines
-   Web3 analytics

...this project is meant to be **a solid foundation**.

---

## 📜 License

MIT

---

## 🌍 About

Built for the **VeBetterDAO / B3TR ecosystem**\
to enable **transparent, analyzable on-chain sustainability data**.
