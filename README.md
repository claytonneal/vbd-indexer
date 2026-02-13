# ⚡ VBD Indexer

> High-performance Python indexer for **VeChain B3TR / VeBetterDAO** events.  
> Designed for **speed, correctness, and production-grade data pipelines**.

---

## ✨ Features

- 🔎 **On-chain event indexing** from VeChain Thor
- ⚙️ **Parallel worker architecture** for fast block scanning
- 🧠 **ABI decoding** of complex Solidity return types & events
- 🗂 **CSV export** for analytics & data science workflows
- 🧱 Clean **modular SDK-style structure**
- 🚀 Ready for **CLI usage, automation, and CI pipelines**

---

## 🏗 Architecture

    src/vbd_indexer/
    ├── app.py          # CLI entrypoint
    ├── thor/           # Thor rest client
    ├── indexer/        # Parallel indexing engine
    ├── b3tr/           # Contract helpers & ABI logic
    └── utils/          # Units, formatting, helpers

Core principles:

-   **Deterministic indexing**
-   **Typed decoding**
-   **Separation of concerns**
-   **Analytics-friendly outputs**

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

Run the CLI:

``` bash
poetry run vbd-indexer <round id>
```

Example commands:

``` bash
poetry run vbd-indexer 83
```

---

## 🔗 What it Indexes

Currently focused on:

-   **B3TR reward distribution events**

---

## 📊 Data Output

Typical outputs:

-   `rewards-events-round-<round_id>.csv`

Optimized for:

-   **Machine learning pipelines**

---

## 🛣 Roadmap

-   [ ] Async engine for **10× throughput**
-   [ ] PostgreSQL direct ingestion
-   [ ] More VBD events supported
-   [ ] PyPI package release
-   [ ] Public VeBetterDAO analytics dashboard

---

## 🤝 Contributing

PRs welcome.

If you're working on:

-   VeChain tooling\
-   Data pipelines\
-   Web3 analytics

...this project is meant to be **a solid foundation**.

---

## 📜 License

MIT

---

## 🌍 About

Built for the **VeBetterDAO / B3TR ecosystem**\
to enable **transparent, analyzable on-chain sustainability data**.
