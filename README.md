# ⛽ OmniGas: Multi-Chain Stablecoin Routing Engine

OmniGas is a real-time capital preservation and network routing engine built for Web3 operators. It monitors transaction friction, live gas congestion, and asset-delivery data across 13 distinct blockchain networks simultaneously—empowering users to eliminate capital erosion before executing transfers.

![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

---

## ⚡ Key Features

* **Multi-Rail Surveillance:** Monitors gas rates across EVM layers, Solana Mainnet, Tron Mainnet, and zero-fee architectures.
* **Smart Multi-Node Fallbacks:** Built-in endpoint redundancy cycles through multiple public RPC arrays automatically if a node throttles or drops.
* **Dynamic Analytics Cards:** Surface-level indicators displaying the absolute cheapest path, lowest network overhead, and the most expensive rails to avoid.
* **Budget Threshold Guard:** Interactive sidebar filtering that hides high-friction networks based on user-defined max transaction tolerances.
* **Capital Efficiency Tracker:** Interactive data matrix utilizing algorithmic progress bars tracking exactly how much value hits the recipient destination.
* **One-Click Cross-Chain Execution:** Deep-linked direct bridge routing maps (Jumper, deBridge, Hyperliquid native) pre-mapped per chain.

---

## 🛠️ Tech Stack & Architecture

* **Frontend Framework:** Streamlit (Custom Glassmorphic injection layer)
* **Data Structures & Manipulation:** Pandas DataFrames
* **Network Request Architecture:** Concurrency-safe HTTP session handling via Python Requests
* **Live Token Feed:** Real-time spot price indexing using the public Binance API matrix

---

## 🚀 Local Installation & Deployment

### 1. Clone the Architecture
```bash
git clone [https://github.com/YOUR_USERNAME/omnigas.git](https://github.com/YOUR_USERNAME/omnigas.git)
cd omnigas
