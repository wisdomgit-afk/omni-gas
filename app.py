import streamlit as st
import requests
import pandas as pd

# Global Configuration
st.set_page_config(
    page_title="OmniGas Engine",
    page_icon="⛽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Glassmorphism Theme Accents
st.markdown("""
    <style>
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        div[data-testid="stMetric"] {
            background-color: #1e293b;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #334155;
        }
        div[data-testid="stMetricLabel"] { color: #94a3b8 !important; font-size: 14px !important; }
        div[data-testid="stMetricValue"] { font-size: 24px !important; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

st.title("⛽ OmniGas: Multi-Chain Routing Engine")
st.write("Real-time gas monitoring, threshold alerting, and bridge execution matrix.")
st.markdown("---")

# 1. Sidebar - Configuration Panel & Threshold Alerts
with st.sidebar:
    st.header("⚙️ Engine Control")
    amount = st.number_input("💵 Capital to Transfer ($)", min_value=1.0, value=100.0, step=50.0)
    
    st.markdown("---")
    st.header("🚨 Gas Watcher Alerts")
    enable_alerts = st.checkbox("Enable Budget Filter", value=False)
    max_budget = st.slider("Max Acceptable Fee ($)", min_value=0.01, max_value=5.00, value=0.50, step=0.05)
    
    st.markdown("---")
    refresh_clicked = st.button("🔄 Sync Live Networks", type="primary", use_container_width=True)
    if refresh_clicked:
        st.rerun()

# 2. Resilient Data Aggregation Engines
def get_live_prices():
    prices = {
        "ETH": 3500.0, "BNB": 550.0, "POL": 0.45, "SOL": 140.0, 
        "CELO": 0.60, "AVAX": 28.0, "HYPE": 64.0, "TRX": 0.12,
        "MNT": 0.75, "CRO": 0.15
    }
    symbols = {
        "ETHUSDT": "ETH", "BNBUSDT": "BNB", "POLUSDT": "POL", 
        "SOLUSDT": "SOL", "CELOUSDT": "CELO", "AVAXUSDT": "AVAX",
        "HYPEUSDT": "HYPE", "TRXUSDT": "TRX", "MNTUSDT": "MNT",
        "CROUSDT": "CRO"
    }
    for symbol, token in symbols.items():
        try:
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
            res = requests.get(url, timeout=2).json()
            if "price" in res:
                prices[token] = float(res["price"])
        except Exception:
            pass 
    return prices

def fetch_evm_fee(rpc_urls, gas_limit, token_price):
    payload = {"jsonrpc": "2.0", "method": "eth_gasPrice", "params": [], "id": 1}
    headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    for url in rpc_urls:
        try:
            res = requests.post(url, json=payload, headers=headers, timeout=3).json()
            if "result" in res:
                gas_wei = int(res["result"], 16)
                fee_native = (gas_wei * gas_limit) / 1e18
                return gas_wei / 1e9, fee_native * token_price
        except Exception:
            continue
    return None, None

def fetch_solana_fee(token_price):
    rpc_url = "https://api.mainnet-beta.solana.com"
    payload = {"jsonrpc": "2.0", "id": 1, "method": "getRecentPrioritizationFees"}
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.post(rpc_url, json=payload, headers=headers, timeout=3).json()
        samples = res.get("result", [])
        micro_lamports_per_cu = samples[-1]["prioritizationFee"] if samples else 0
        base_fee = 5000
        priority_fee = (micro_lamports_per_cu * 300000) / 1_000_000
        return micro_lamports_per_cu, ((base_fee + priority_fee) / 1e9) * token_price
    except Exception:
        return None, None

token_prices = get_live_prices()

# 13-Network Parameters Mapping Matrix
networks = {
    "Ethereum Mainnet": {"type": "EVM", "rpc": ["https://ethereum-rpc.publicnode.com", "https://eth.drpc.org"], "ticker": "ETH", "limit": 65000, "bridge": "https://jumper.exchange"},
    "Solana Mainnet": {"type": "Solana", "ticker": "SOL", "bridge": "https://debridge.finance"},
    "Tron Mainnet": {"type": "Tron", "ticker": "TRX", "bridge": "https://jumper.exchange"},
    "Plasma Mainnet Beta": {"type": "Plasma", "ticker": "XPL", "bridge": "https://jumper.exchange"},
    "Hyperliquid (HyperEVM)": {"type": "EVM", "rpc": ["https://rpc.hyperliquid.xyz/evm"], "ticker": "HYPE", "limit": 65000, "bridge": "https://app.hyperliquid.xyz/bridge"},
    "Polygon PoS Network": {"type": "EVM", "rpc": ["https://polygon.drpc.org", "https://polygon-rpc.com"], "ticker": "POL", "limit": 65000, "bridge": "https://jumper.exchange"},
    "Base Network": {"type": "EVM", "rpc": ["https://mainnet.base.org", "https://base.drpc.org"], "ticker": "ETH", "limit": 65000, "bridge": "https://jumper.exchange"},
    "Arbitrum One": {"type": "EVM", "rpc": ["https://arb1.arbitrum.io/rpc", "https://arbitrum.drpc.org"], "ticker": "ETH", "limit": 200000, "bridge": "https://jumper.exchange"},
    "OP Mainnet": {"type": "EVM", "rpc": ["https://mainnet.optimism.io", "https://optimism.drpc.org"], "ticker": "ETH", "limit": 65000, "bridge": "https://jumper.exchange"},
    "BNB Smart Chain": {"type": "EVM", "rpc": ["https://bsc-dataseed.binance.org", "https://bsc.drpc.org"], "ticker": "BNB", "limit": 65000, "bridge": "https://jumper.exchange"},
    "Avalanche C-Chain": {"type": "EVM", "rpc": ["https://api.avax.network/ext/bc/C/rpc", "https://avalanche.drpc.org"], "ticker": "AVAX", "limit": 65000, "bridge": "https://jumper.exchange"},
    "Celo Network": {"type": "EVM", "rpc": ["https://forno.celo.org", "https://celo.drpc.org"], "ticker": "CELO", "limit": 65000, "bridge": "https://jumper.exchange"},
    "Mantle Network": {"type": "EVM", "rpc": ["https://rpc.mantle.xyz", "https://mantle.drpc.org"], "ticker": "MNT", "limit": 65000, "bridge": "https://jumper.exchange"}
}

raw_data = []
for name, config in networks.items():
    ticker = config["ticker"]
    native_price = token_prices.get(ticker, 1.0)
    
    if config["type"] == "EVM":
        metric, usd_fee = fetch_evm_fee(config["rpc"], config["limit"], native_price)
        metric_str = f"{metric:.1f} Gwei" if metric else "🛑 Node Timeout"
    elif config["type"] == "Solana":
        metric, usd_fee = fetch_solana_fee(native_price)
        metric_str = f"{metric:,} m-lamports" if metric is not None else "🛑 Node Timeout"
    elif config["type"] == "Tron":
        usd_fee = 27.0 * native_price
        metric_str = "Standard Burn (~27 TRX)"
    elif config["type"] == "Plasma":
        usd_fee = 0.0
        metric_str = "Zero-Fee Route"

    if usd_fee is not None:
        amt_rec = max(0.0, amount - usd_fee)
        pct_kept = (amt_rec / amount) * 100
        raw_data.append({
            "Network Rail": name,
            "Live Congestion Metric": metric_str,
            "Network Fee (USD)": usd_fee,
            "Recipient Receives ($)": amt_rec,
            "Capital Efficiency (%)": pct_kept,
            "Action Link": config["bridge"]
        })
else:
    df = pd.DataFrame(raw_data).sort_values(by="Network Fee (USD)", ascending=True)

# Apply Live Budget Watcher Filter
if enable_alerts:
    under_budget_count = len(df[df["Network Fee (USD)"] <= max_budget])
    if under_budget_count > 0:
        st.toast(f"🎉 {under_budget_count} networks are currently within your budget!", icon="✅")
    df = df[df["Network Fee (USD)"] <= max_budget]

# 3. Dynamic Key Performance Indicators
valid_df = df[df["Live Congestion Metric"].str.contains("🛑") == False]

if not valid_df.empty:
    best_route = valid_df.iloc[0]
    worst_route = valid_df.iloc[-1]
    
    st.write("### 🚨 Top Routing Analytics")
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.metric(label="🏆 Optimal Settlement Rail", value=best_route["Network Rail"])
    with m_col2:
        st.metric(label="💸 Minimum Network Gas Cost", value=f"${best_route['Network Fee (USD)']:.4f}")
    with m_col3:
        st.metric(label="⚠️ Maximum Network Gas Cost", value=f"{worst_route['Network Rail']} (${worst_route['Network Fee (USD)']:.2f})")
else:
    st.warning("No networks matched your budget criteria. Loosen your budget slider in the sidebar.")

# 4. Interactive Data Presentation Dataframe
st.write("### 🏁 OmniGas Live Matrix")
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Network Rail": st.column_config.TextColumn("Network Rail", width="medium"),
        "Live Congestion Metric": st.column_config.TextColumn("Live Load Metric", width="medium"),
        "Network Fee (USD)": st.column_config.NumberColumn("Est. Fee (USD)", format="$%.4f"),
        "Recipient Receives ($)": st.column_config.NumberColumn("Final Delivered Value", format="$%.4f"),
        "Capital Efficiency (%)": st.column_config.ProgressColumn("Capital Efficiency", format="%.2f%%", min_value=0.0, max_value=100.0),
        "Action Link": st.column_config.LinkColumn("Execute Transfer", display_text="Open Bridge ↗️")
    }
)