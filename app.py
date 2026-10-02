import math
import random
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots


# ============================================================
# App configuration and theme
# ============================================================
st.set_page_config(
    page_title="AlgoMarket Decision Lab",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
if "theme_choice" not in st.session_state:
    st.session_state.theme_choice = "Dark"
if "page" not in st.session_state:
    st.session_state.page = "Start Here"
if "results" not in st.session_state:
    st.session_state.results = {}
if "history" not in st.session_state:
    st.session_state.history = []
if "run_counter" not in st.session_state:
    st.session_state.run_counter = 0

LIGHT = {
    "bg": "#F6F7FB", "panel": "#FFFFFF", "panel2": "#F1F3F9", "sidebar": "#FFFFFF",
    "border": "#E3E7F1", "heading": "#171B26", "text": "#232838", "muted": "#6B7286",
    "amber": "#D97706", "blue": "#2563EB", "pink": "#DB2777", "red": "#E11D48",
    "green": "#16A34A", "purple": "#7C3AED", "plot": "plotly_white",
    "plot_paper": "#FFFFFF", "plot_area": "#FFFFFF", "grid": "#EEF1F7",
    "hero": "linear-gradient(135deg,#FFFFFF 0%,#EEF5FF 100%)",
}
DARK = {
    "bg": "#0B0E14", "panel": "#141922", "panel2": "#191F2B", "sidebar": "#0F1319",
    "border": "#262D3A", "heading": "#F5F6F8", "text": "#E8EAED", "muted": "#8B93A7",
    "amber": "#F5B84E", "blue": "#5B9DF9", "pink": "#F472B6", "red": "#FB7185",
    "green": "#4ADE80", "purple": "#C4B5FD", "plot": "plotly_dark",
    "plot_paper": "#141922", "plot_area": "#0B0E14", "grid": "#232A38",
    "hero": "linear-gradient(135deg,#151D2B 0%,#1D1727 100%)",
}
st.session_state.dark_mode = st.session_state.theme_choice == "Dark"
T = DARK if st.session_state.dark_mode else LIGHT

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&family=Inter:wght@400;500;600;700&display=swap');
    :root {{ color-scheme:{'dark' if st.session_state.dark_mode else 'light'}; }}
    .stApp {{ background:{T['bg']}; color:{T['text']}; font-family:Inter,sans-serif; }}
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{ background:{T['bg']} !important; }}
    h1,h2,h3,h4 {{ font-family:Poppins,sans-serif !important; color:{T['heading']} !important; }}
    p, li, label, [data-testid="stMarkdownContainer"] {{ color:{T['text']}; }}
    .hero {{ background:{T['hero']}; border:1px solid {T['border']}; border-radius:20px; padding:2rem 2.2rem; margin-bottom:1.1rem; }}
    .hero h1 {{ margin:0 0 .45rem 0; font-size:2.2rem; }}
    .hero p {{ color:{T['muted']}; max-width:900px; font-size:1.05rem; line-height:1.7; margin:0; }}
    .card {{ background:{T['panel']}; border:1px solid {T['border']}; border-radius:16px; padding:1.1rem 1.25rem; margin:.6rem 0; box-shadow:0 3px 15px rgba(0,0,0,.08); }}
    .card h3 {{ margin-top:0; }}
    .metric {{ background:{T['panel']}; border:1px solid {T['border']}; border-radius:14px; padding:.9rem .75rem; text-align:center; min-height:90px; }}
    .metric-label {{ color:{T['muted']}; font-size:.72rem; text-transform:uppercase; letter-spacing:.05em; font-weight:700; }}
    .metric-value {{ color:{T['heading']}; font-size:1.35rem; font-weight:700; margin-top:.3rem; }}
    .takeaway {{ background:{T['panel']}; border-left:5px solid {T['blue']}; border-radius:12px; padding:1rem 1.2rem; margin:1rem 0; line-height:1.65; }}
    .warning {{ border-left-color:{T['amber']}; }}
    .success {{ border-left-color:{T['green']}; }}
    .danger {{ border-left-color:{T['red']}; }}
    .small {{ color:{T['muted']}; font-size:.86rem; line-height:1.55; }}
    section[data-testid="stSidebar"] {{ background:{T['sidebar']}; border-right:1px solid {T['border']}; }}
    section[data-testid="stSidebar"] * {{ color:{T['text']}; }}
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {{ color:{T['text']} !important; }}
    section[data-testid="stSidebar"] input, section[data-testid="stSidebar"] textarea {{ color:{T['text']} !important; background:{T['panel']} !important; }}
    section[data-testid="stSidebar"] button {{ border-color:{T['border']} !important; color:{T['text']} !important; }}
    section[data-testid="stSidebar"] button[kind="primary"] {{ background:linear-gradient(135deg,{T['blue']},{T['purple']}) !important; color:#fff !important; border:0 !important; }}
    [data-testid="stMetricValue"] {{ color:{T['heading']} !important; }}
    .stCaption, [data-testid="stCaptionContainer"] {{ color:{T['muted']} !important; }}
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {{ background:{T['panel']} !important; border-color:{T['border']} !important; }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# General helpers
# ============================================================
def metric_card(label: str, value: str, color: str | None = None):
    style = f"color:{color};" if color else ""
    st.markdown(
        f'<div class="metric"><div class="metric-label">{label}</div>'
        f'<div class="metric-value" style="{style}">{value}</div></div>',
        unsafe_allow_html=True,
    )


def takeaway(title: str, body: str, tone: str = ""):
    st.markdown(
        f'<div class="takeaway {tone}"><b>{title}</b><br>{body}</div>',
        unsafe_allow_html=True,
    )


def record_run(module: str, seed: int, summary: str, parameters: dict):
    st.session_state.run_counter += 1
    st.session_state.history.insert(0, {
        "run": st.session_state.run_counter,
        "module": module,
        "seed": seed,
        "summary": summary,
        "parameters": parameters,
    })
    st.session_state.history = st.session_state.history[:8]


def run_history_panel():
    if not st.session_state.history:
        return
    with st.expander("Recent experiments", expanded=False):
        rows = [{k: x[k] for k in ("run", "module", "seed", "summary")} for x in st.session_state.history]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


def set_page(page: str):
    st.session_state.page = page


def sync_preset(prefix: str, selected: str, values: dict):
    """Apply a preset once when the user changes it, without overwriting later edits."""
    marker = f"{prefix}_last_preset"
    if st.session_state.get(marker) != selected:
        for key, value in values.items():
            st.session_state[key] = value
        st.session_state[marker] = selected


def chart_layout(fig, title: str, height: int = 420):
    fig.update_layout(
        title=title,
        template=T["plot"],
        paper_bgcolor=T["plot_paper"],
        plot_bgcolor=T["plot_area"],
        font=dict(color=T["text"]),
        height=height,
        margin=dict(t=70, l=55, r=25, b=50),
        legend=dict(orientation="h", y=1.08),
    )
    fig.update_xaxes(gridcolor=T["grid"])
    fig.update_yaxes(gridcolor=T["grid"])
    return fig


# ============================================================
# Collusion model
# ============================================================
@dataclass
class Market:
    num_agents: int = 2
    marginal_cost: float = 1.0
    base_demand: float = 100.0
    sensitivity: float = 2.0

    @property
    def competitive_price(self):
        return self.marginal_cost

    @property
    def monopoly_price(self):
        return (self.base_demand / self.sensitivity + self.marginal_cost) / 2

    def step(self, prices: List[float]):
        p = np.asarray(prices, dtype=float)
        minimum = p.min()
        winners = p == minimum
        quantity = max(0.0, self.base_demand - self.sensitivity * minimum)
        demand = np.zeros_like(p)
        demand[winners] = quantity / max(1, winners.sum())
        profit = np.maximum((p - self.marginal_cost) * demand, 0)
        return demand, profit


@st.cache_data(show_spinner=False)
def simulate_collusion(
    num_agents: int, episodes: int, latency: int, audit_probability: float,
    audit_fine: float, max_jump: float, seed: int, ceiling: float | None = None,
):
    rng = np.random.default_rng(seed)
    random.seed(seed)
    market = Market(num_agents=num_agents)
    grid = np.round(np.linspace(1.0, 26.0, 12), 2)
    q = [dict() for _ in range(num_agents)]
    alpha, gamma = .15, .95
    epsilon_start = .22
    history, profits = [], []
    price_history = []
    current = [market.monopoly_price] * num_agents

    def state_for(agent_idx: int, step: int):
        source = price_history[max(0, len(price_history) - 1 - latency)] if price_history else current
        return tuple(round(source[j], 2) for j in range(num_agents) if j != agent_idx)

    states = [state_for(i, 0) for i in range(num_agents)]
    for ep in range(episodes):
        epsilon = max(.01, epsilon_start * (1 - ep / episodes))
        actions, chosen = [], []
        for i in range(num_agents):
            s = states[i]
            if s not in q[i]:
                q[i][s] = np.zeros(len(grid))
            action = rng.integers(len(grid)) if rng.random() < epsilon else int(np.argmax(q[i][s]))
            actions.append(action)
            chosen.append(float(grid[action]))
        if max_jump > 0 and history:
            chosen = [min(chosen[i], history[-1][i] + max_jump) for i in range(num_agents)]
        if ceiling is not None and ceiling > 0:
            chosen = [min(p, ceiling) for p in chosen]
        demand, raw_profit = market.step(chosen)
        adjusted = raw_profit.copy()
        if audit_probability > 0 and rng.random() < audit_probability:
            adjusted = np.where(np.asarray(chosen) >= .8 * market.monopoly_price,
                                np.maximum(adjusted - audit_fine, 0), adjusted)
        next_states = []
        price_history.append(chosen)
        for i in range(num_agents):
            next_states.append(state_for(i, ep))
            s, ns = states[i], next_states[i]
            if ns not in q[i]:
                q[i][ns] = np.zeros(len(grid))
            target = adjusted[i] + gamma * np.max(q[i][ns])
            q[i][s][actions[i]] += alpha * (target - q[i][s][actions[i]])
        states = next_states
        history.append(chosen)
        profits.append(adjusted.tolist())

    prices = np.asarray(history)
    profit_array = np.asarray(profits)
    window = min(250, len(prices))
    smoothed = np.vstack([
        np.convolve(prices[:, i], np.ones(window) / window, mode="valid")
        for i in range(num_agents)
    ]).T
    final_window = min(500, len(prices))
    final_price = float(prices[-final_window:].mean())
    final_profit = float(profit_array[-final_window:].mean())
    return {
        "prices": prices,
        "smoothed": smoothed,
        "profits": profit_array,
        "final_price": final_price,
        "final_profit": final_profit,
        "competitive_price": market.competitive_price,
        "monopoly_price": market.monopoly_price,
        "collusion_score": float(np.clip(
            (final_price - market.competitive_price) /
            max(.01, market.monopoly_price - market.competitive_price) * 100, 0, 100
        )),
    }


def collusion_replications(params: dict, replications: int):
    outputs = []
    base_seed = int(params.pop("seed"))
    for i in range(replications):
        outputs.append(simulate_collusion(**params, seed=base_seed + i))
    prices = np.array([x["final_price"] for x in outputs])
    scores = np.array([x["collusion_score"] for x in outputs])
    return outputs, prices, scores


def render_collusion():
    st.markdown('<div class="hero"><h1>Collusion Risk Lab</h1><p>Can pricing bots quietly learn to keep prices high—even when nobody tells them to cooperate? Start with a ready-made scenario, watch the market evolve, then test the rule that changes the story.</p></div>', unsafe_allow_html=True)
    takeaway("Your mission", "Find out whether the bots settle into competition or discover a high-price pattern on their own. Then change one policy lever and see whether the market responds.")

    with st.sidebar:
        st.header("Experiment setup")
        preset = st.selectbox("Preset", ["Custom", "Quick collusion", "Audited market", "Delayed observation"])
        defaults = {
            "Quick collusion": (2, 10000, 0, .0, 40, 0),
            "Audited market": (2, 10000, 0, .25, 80, 0),
            "Delayed observation": (2, 10000, 3, .0, 40, 0),
        }
        d = defaults.get(preset, (2, 10000, 0, .0, 40, 0))
        sync_preset("collusion", preset, {"col_bots": d[0], "col_rounds": d[1], "col_latency": d[2], "col_audit": d[3], "col_fine": d[4], "col_jump": float(d[5])})
        bots = st.slider("Pricing bots", 2, 4, key="col_bots")
        rounds = st.slider("Training rounds", 3000, 18000, step=1000, key="col_rounds", help="More rounds give the bots more time to learn, but the final result is evaluated over the last 500 rounds.")
        latency = st.slider("Observation delay", 0, 5, key="col_latency")
        audit = st.slider("Audit probability", 0.0, .5, step=.05, key="col_audit")
        fine = st.slider("Audit fine", 0, 120, step=10, key="col_fine")
        jump = st.slider("Maximum price increase per round", 0.0, 8.0, step=.5, key="col_jump")
        ceiling = st.slider("Hard price ceiling; 0 = none", 0.0, 26.0, 0.0, step=.5, key="col_ceiling")
        seed = st.number_input("Random seed", min_value=0, max_value=999999, value=42, step=1, key="col_seed")
        reps = st.select_slider("Repeated runs", options=[1, 3, 5, 10, 25], value=5, key="col_reps", help="Repeated runs show whether the result is a pattern or a lucky outcome.")
        run = st.button("Run this experiment", type="primary", use_container_width=True)

    params = dict(num_agents=bots, episodes=rounds, latency=latency,
                  audit_probability=audit, audit_fine=float(fine), max_jump=jump,
                  ceiling=ceiling if ceiling > 0 else None)
    if run:
        with st.spinner(f"Running {reps} reproducible simulation{'s' if reps != 1 else ''}..."):
            outputs, prices, scores = collusion_replications({**params, "seed": int(seed)}, reps)
        st.session_state.results["collusion"] = {
            "output": outputs[0], "prices": prices, "scores": scores,
            "params": params, "seed": int(seed), "replications": reps,
        }
        record_run("Collusion", int(seed), f"median score {np.median(scores):.0f}/100", params)

    result = st.session_state.results.get("collusion")
    if not result:
        st.info("Pick a scenario on the left, then press **Run this experiment**. Your result will stay here while you explore.")
        return

    out = result["output"]
    collusive_share = float(np.mean(result["scores"] >= 60))
    verdict = "Collusive" if collusive_share >= .5 else "Mostly competitive"
    color = T["red"] if verdict == "Collusive" else T["green"]
    cols = st.columns(4)
    with cols[0]: metric_card("Median final price", f"${np.median(result['prices']):.2f}")
    with cols[1]: metric_card("Median collusion score", f"{np.median(result['scores']):.0f}/100")
    with cols[2]: metric_card("Collusive runs", f"{collusive_share:.0%}")
    with cols[3]: metric_card("Verdict", verdict, color)

    takeaway("What happened?", f"Across {result['replications']} run(s), the typical final price was ${np.median(result['prices']):.2f}, compared with a competitive benchmark of ${out['competitive_price']:.2f}. The bots crossed our collusion threshold in {collusive_share:.0%} of runs. Try changing only the audit probability or observation delay to see what breaks the pattern.", "danger" if collusive_share >= .5 else "success")

    fig = go.Figure()
    smoothed = out["smoothed"]
    x = np.arange(len(smoothed)) + 250
    for i in range(smoothed.shape[1]):
        fig.add_trace(go.Scatter(x=x, y=smoothed[:, i], mode="lines", name=f"Bot {i+1}", line=dict(color=[T["blue"], T["pink"], T["purple"], T["green"]][i], width=2)))
    fig.add_hline(y=out["competitive_price"], line_dash="dash", line_color=T["muted"], annotation_text="Competitive price")
    fig.add_hline(y=out["monopoly_price"], line_dash="dash", line_color=T["red"], annotation_text="Cartel benchmark")
    fig.update_xaxes(title="Original training round")
    fig.update_yaxes(title="Price ($)")
    st.plotly_chart(chart_layout(fig, "Smoothed price paths", 460), use_container_width=True)

    rep_df = pd.DataFrame({"Final price": result["prices"], "Collusion score": result["scores"]})
    if result["replications"] > 1:
        st.markdown("#### Distribution across repeated runs")
        st.dataframe(rep_df.style.format({"Final price": "${:.2f}", "Collusion score": "{:.0f}"}), use_container_width=True, hide_index=True)
    st.download_button("Download experiment data", rep_df.to_csv(index=False), "collusion_runs.csv", "text/csv")


# ============================================================
# Price discrimination audit
# ============================================================
@st.cache_data(show_spinner=False)
def simulate_audit(base: float, biases: Tuple[float, ...], noise: float, visits: int, seed: int):
    rng = np.random.default_rng(seed)
    # Online and synthetic proxy traits. These are not real demographic observations.
    traits = {
        "Mobile": rng.integers(0, 2, visits),
        "Location tier": rng.integers(0, 3, visits),
        "Returning": rng.integers(0, 2, visits),
        "Peak time": rng.integers(0, 2, visits),
        "Premium payment": rng.integers(0, 2, visits),
        "Deep browsing": rng.uniform(0, 1, visits),
        "Synthetic sensitive proxy": rng.integers(0, 2, visits),
        "Dress proxy": rng.integers(0, 2, visits),
        "Speech proxy": rng.integers(0, 2, visits),
        "Posture proxy": rng.integers(0, 2, visits),
        "Facial-confidence proxy": rng.integers(0, 2, visits),
    }
    prices = (base + biases[0] * traits["Mobile"] + biases[1] * traits["Location tier"] + biases[2] * traits["Returning"] + biases[3] * traits["Peak time"] + biases[4] * traits["Premium payment"] + biases[5] * traits["Deep browsing"] + biases[6] * traits["Synthetic sensitive proxy"] + biases[7] * traits["Dress proxy"] + biases[8] * traits["Speech proxy"] + biases[9] * traits["Posture proxy"] + biases[10] * traits["Facial-confidence proxy"] + rng.normal(0, noise, visits))
    return traits, np.maximum(prices, 1.0)


def welch_stats(a, b):
    a, b = np.asarray(a), np.asarray(b)
    ma, mb = float(a.mean()), float(b.mean())
    va, vb = a.var(ddof=1), b.var(ddof=1)
    se = math.sqrt(va / len(a) + vb / len(b))
    diff = ma - mb
    ci = 1.96 * se
    z = diff / se if se else 0
    p = math.erfc(abs(z) / math.sqrt(2))
    return {"mean_a": ma, "mean_b": mb, "diff": diff, "ci_low": diff-ci, "ci_high": diff+ci, "p": p, "n_a": len(a), "n_b": len(b)}


def render_auditor():
    st.markdown('<div class="hero"><h1>Price Discrimination Auditor</h1><p>Imagine the same product being quoted at different prices. Create a synthetic market, investigate the gaps, and learn which signals deserve a closer look after we account for noise and multiple testing.</p></div>', unsafe_allow_html=True)
    takeaway("A careful investigator asks two questions", "Is the price gap large enough to detect, and does it remain after other signals are considered? This synthetic exercise can flag patterns for investigation—it cannot prove unlawful discrimination, intent, or causation.", "warning")
    with st.sidebar:
        st.header("Audit setup")
        preset = st.selectbox("Preset", ["Custom", "No true bias", "Strong sensitive-proxy bias"])
        base = st.slider("Base price ($)", 20, 200, 100)
        if preset == "No true bias":
            default_biases = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        elif preset == "Strong sensitive-proxy bias":
            default_biases = (5, 3, -4, 4, 5, 6, 14, 8, 7, 5, 9)
        else:
            default_biases = (6, 3, -4, 3, 4, 5, 8, 3, 3, 2, 4)
        names = ["Mobile bias", "Location-tier bias", "Returning bias", "Peak-time bias", "Premium-payment bias", "Browsing bias", "Sensitive-proxy bias", "Dress-proxy bias", "Speech-proxy bias", "Posture-proxy bias", "Facial-confidence bias"]
        sync_preset("audit", preset, {f"audit_{i}": int(v) for i, v in enumerate(default_biases)})
        with st.expander("Advanced signals · synthetic proxies", expanded=False):
            st.caption("These variables are synthetic teaching devices. They are not recommendations for real-world pricing.")
            biases = tuple(st.slider(n, -20, 20, int(v), key=f"audit_{i}") for i, (n, v) in enumerate(zip(names, default_biases)))
        noise = st.slider("Random noise ($)", 0, 15, 4)
        visits = st.slider("Synthetic visits", 400, 8000, 2500, step=100)
        seed = st.number_input("Random seed", 0, 999999, 42, key="audit_seed")
        run = st.button("Run audit", type="primary", use_container_width=True)

    if run:
        traits, prices = simulate_audit(base, biases, noise, visits, int(seed))
        results = []
        pairs = [
            ("Mobile", traits["Mobile"] == 0, traits["Mobile"] == 1),
            ("Location tier 0 vs 2", traits["Location tier"] == 0, traits["Location tier"] == 2),
            ("New vs returning", traits["Returning"] == 0, traits["Returning"] == 1),
            ("Off-peak vs peak", traits["Peak time"] == 0, traits["Peak time"] == 1),
            ("Basic vs premium payment", traits["Premium payment"] == 0, traits["Premium payment"] == 1),
            ("Low vs high browsing", traits["Deep browsing"] < .5, traits["Deep browsing"] >= .5),
            ("Synthetic proxy A vs B", traits["Synthetic sensitive proxy"] == 0, traits["Synthetic sensitive proxy"] == 1),
            ("Dress proxy A vs B", traits["Dress proxy"] == 0, traits["Dress proxy"] == 1),
            ("Speech proxy A vs B", traits["Speech proxy"] == 0, traits["Speech proxy"] == 1),
            ("Posture proxy A vs B", traits["Posture proxy"] == 0, traits["Posture proxy"] == 1),
            ("Facial-confidence proxy A vs B", traits["Facial-confidence proxy"] == 0, traits["Facial-confidence proxy"] == 1),
        ]
        for label, a, b in pairs:
            s = welch_stats(prices[a], prices[b])
            results.append({"Trait": label, **s, "Bonferroni significant": s["p"] < .05 / len(pairs)})
        st.session_state.results["audit"] = {"prices": prices, "traits": traits, "results": pd.DataFrame(results), "seed": int(seed), "biases": biases}
        record_run("Price audit", int(seed), f"{sum(x['Bonferroni significant'] for x in results)} adjusted signals", {"visits": visits})

    result = st.session_state.results.get("audit")
    if not result:
        st.info("Choose a scenario or tune the signals, then press **Run audit** to create your synthetic shopper sample.")
        return
    df = result["results"]
    significant = int(df["Bonferroni significant"].sum())
    c = st.columns(3)
    with c[0]: metric_card("Synthetic visits", f"{len(result['prices']):,}")
    with c[1]: metric_card("Adjusted signals", str(significant))
    with c[2]: metric_card("Seed", str(result["seed"]))
    takeaway("What the audit found", f"{significant} of {len(df)} tested comparisons remain detectable after a simple Bonferroni correction. That is a reason to investigate the data more deeply—not a final legal or causal conclusion.")

    plot_df = df.sort_values("diff")
    fig = go.Figure(go.Bar(
        x=plot_df["diff"], y=plot_df["Trait"], orientation="h",
        error_x=dict(type="data", symmetric=False, array=plot_df["ci_high"] - plot_df["diff"], arrayminus=plot_df["diff"] - plot_df["ci_low"]),
        marker_color=[T["red"] if x else T["muted"] for x in plot_df["Bonferroni significant"]],
    ))
    fig.add_vline(x=0, line_dash="dash", line_color=T["muted"])
    fig.update_xaxes(title="Estimated price difference ($), group A − group B")
    st.plotly_chart(chart_layout(fig, "Estimated group differences with 95% confidence intervals", 460), use_container_width=True)
    display = df[["Trait", "mean_a", "mean_b", "diff", "ci_low", "ci_high", "p", "Bonferroni significant"]].copy()
    display.columns = ["Trait", "Mean A", "Mean B", "Difference", "CI low", "CI high", "p-value", "Adjusted significant"]
    st.dataframe(display.style.format({c: "${:.2f}" for c in ["Mean A", "Mean B", "Difference", "CI low", "CI high"]} | {"p-value": "{:.4f}"}), use_container_width=True, hide_index=True)
    st.download_button("Download audit results", df.to_csv(index=False), "price_audit.csv", "text/csv")


# ============================================================
# Regulation and policy comparison
# ============================================================
REGIMES = {
    "Laissez-faire": dict(latency=0, audit=0, fine=0, jump=0, ceiling=None, cost=0),
    "Moderate oversight": dict(latency=2, audit=.15, fine=40, jump=2, ceiling=None, cost=35),
    "Strict regulation": dict(latency=3, audit=.35, fine=80, jump=1, ceiling=8, cost=80),
}


def individual_outcome(price: float, collusion: float, income: float, confidence: float, sensitivity: float, vulnerability: float):
    fair = 5.0
    base_qty = max(.1, (0.7 + income / 100) * (0.7 + confidence / 100) * 8)
    qty = max(.1, base_qty - sensitivity * (price - fair))
    surplus = max(0, .5 * max(0, fair + base_qty / max(sensitivity, .1) - price) * qty)
    residual = max(0, income - price * qty * (.35 + .4 * vulnerability))
    welfare = max(0, .4 * min(100, surplus * 8) + .35 * min(100, residual) + .25 * confidence - collusion * .15)
    return {"price": price, "quantity": qty, "surplus": surplus, "residual": residual, "welfare": welfare}


def render_regulation():
    st.markdown('<div class="hero"><h1>Regulatory Design Lab</h1><p>Design a rule, watch firms adapt, and follow the consequences all the way to one person’s shopping experience. This is where policy stops being an abstract setting and becomes a lived outcome.</p></div>', unsafe_allow_html=True)
    takeaway("Follow the chain", "Policy changes firm incentives. Firm behavior changes the price. The price changes what a person can buy, keep, and afford. Use the controls to see where that chain strengthens—or breaks.")
    with st.sidebar:
        st.header("Market and policy")
        preset = st.selectbox("Preset", ["Custom", "Light-touch oversight", "Strict regulation"])
        defaults = {"Light-touch oversight": (2, .15, 40, 2, 0), "Strict regulation": (3, .35, 80, 1, 8)}
        d = defaults.get(preset, (0, 0, 40, 0, 0))
        sync_preset("regulation", preset, {"reg_agents": 3, "reg_rounds": 9000, "reg_latency": d[0], "reg_audit": float(d[1]), "reg_fine": int(d[2]), "reg_jump": float(d[3]), "reg_ceiling": float(d[4])})
        agents = st.slider("Number of firms", 2, 5, key="reg_agents")
        rounds = st.slider("Training rounds", 3000, 18000, step=1000, key="reg_rounds")
        latency = st.slider("Observation delay", 0, 6, key="reg_latency")
        audit = st.slider("Audit probability", 0.0, .5, step=.05, key="reg_audit")
        fine = st.slider("Audit fine", 0, 120, step=10, key="reg_fine")
        jump = st.slider("Price increase cap", 0.0, 8.0, step=.5, key="reg_jump")
        ceiling = st.slider("Price ceiling; 0 = none", 0.0, 25.0, step=.5, key="reg_ceiling")
        st.header("Consumer profile")
        income = st.slider("Income index", 20, 150, 100)
        confidence = st.slider("Confidence", 10, 100, 65)
        sensitivity = st.slider("Price sensitivity", .3, 3.0, 1.2, step=.1)
        vulnerability = st.slider("Budget vulnerability", 0.0, 1.0, .4, step=.05)
        seed = st.number_input("Random seed", 0, 999999, 42, key="reg_seed")
        run = st.button("Run policy experiment", type="primary", use_container_width=True)

    if run:
        sim = simulate_collusion(agents, rounds, latency, audit, float(fine), jump, int(seed), ceiling if ceiling > 0 else None)
        price = min(sim["final_price"], ceiling) if ceiling > 0 else sim["final_price"]
        individual = individual_outcome(price, sim["collusion_score"], income, confidence, sensitivity, vulnerability)
        st.session_state.results["regulation"] = {"sim": sim, "individual": individual, "seed": int(seed), "params": {"income": income, "confidence": confidence, "vulnerability": vulnerability}}
        record_run("Regulation", int(seed), f"welfare {individual['welfare']:.0f}/100", {"audit": audit, "ceiling": ceiling})

    result = st.session_state.results.get("regulation")
    if not result:
        st.info("Choose a policy scenario or adjust the controls, then press **Run policy experiment** to follow the full chain.")
        return
    sim, ind = result["sim"], result["individual"]
    cols = st.columns(5)
    for c, label, value in zip(cols, ["Market price", "Collusion score", "Price faced", "Quantity", "Welfare"], [f"${sim['final_price']:.2f}", f"{sim['collusion_score']:.0f}/100", f"${ind['price']:.2f}", f"{ind['quantity']:.1f}", f"{ind['welfare']:.0f}/100"]):
        with c: metric_card(label, value)
    tone = "danger" if sim["collusion_score"] >= 60 else "success"
    takeaway("From rule to real life", f"The firms ended at a collusion score of {sim['collusion_score']:.0f}/100. The selected consumer faces ${ind['price']:.2f}, buys {ind['quantity']:.1f} units, and receives an illustrative welfare score of {ind['welfare']:.0f}/100. Now change one rule or one part of the consumer profile and watch which link moves first.", tone)

    fig = go.Figure()
    x = np.arange(len(sim["smoothed"])) + 250
    for i in range(sim["smoothed"].shape[1]):
        fig.add_trace(go.Scatter(x=x, y=sim["smoothed"][:, i], mode="lines", name=f"Firm {i+1}"))
    fig.add_hline(y=sim["competitive_price"], line_dash="dash", line_color=T["muted"], annotation_text="Competitive")
    fig.add_hline(y=sim["monopoly_price"], line_dash="dash", line_color=T["red"], annotation_text="Cartel benchmark")
    st.plotly_chart(chart_layout(fig, "Firm prices under the selected rules", 430), use_container_width=True)


# ============================================================
# Comparison, calibration, notes, and navigation
# ============================================================
def render_comparison():
    st.markdown('<div class="hero"><h1>Policy Comparison</h1><p>Three regimes. One market. A fair comparison. See what each approach buys you in consumer welfare, what it costs to enforce, and where the trade-offs become impossible to ignore.</p></div>', unsafe_allow_html=True)
    with st.sidebar:
        agents = st.slider("Number of firms", 2, 5, 3, key="cmp_agents")
        rounds = st.slider("Training rounds", 3000, 16000, 8000, step=1000, key="cmp_rounds")
        seed = st.number_input("Shared random seed", 0, 999999, 42, key="cmp_seed")
        run = st.button("Compare regimes", type="primary", use_container_width=True)
    if run:
        rows = []
        for name, r in REGIMES.items():
            sim = simulate_collusion(agents, rounds, r["latency"], r["audit"], r["fine"], r["jump"], int(seed), r["ceiling"])
            ind = individual_outcome(sim["final_price"], sim["collusion_score"], 100, 65, 1.2, .4)
            rows.append({"Regime": name, "Market price": sim["final_price"], "Collusion score": sim["collusion_score"], "Welfare": ind["welfare"], "Enforcement cost": r["cost"]})
        st.session_state.results["comparison"] = pd.DataFrame(rows)
    df = st.session_state.results.get("comparison")
    if df is None:
        st.info("Press **Compare regimes** to put the three approaches on the same playing field.")
        return
    c = st.columns(3)
    with c[0]: metric_card("Lowest price", df.loc[df["Market price"].idxmin(), "Regime"])
    with c[1]: metric_card("Highest welfare", df.loc[df["Welfare"].idxmax(), "Regime"])
    with c[2]: metric_card("Lowest cost", df.loc[df["Enforcement cost"].idxmin(), "Regime"])
    fig = go.Figure(go.Scatter(x=df["Enforcement cost"], y=df["Welfare"], mode="markers+text", text=df["Regime"], textposition="top center", marker=dict(size=16, color=df["Collusion score"], colorscale="RdYlGn_r", showscale=True, colorbar=dict(title="Collusion"))))
    fig.update_xaxes(title="Relative enforcement-cost units")
    fig.update_yaxes(title="Illustrative consumer welfare")
    st.plotly_chart(chart_layout(fig, "Policy trade-off: welfare versus enforcement cost", 440), use_container_width=True)
    st.dataframe(df.style.format({"Market price": "${:.2f}", "Collusion score": "{:.0f}", "Welfare": "{:.1f}", "Enforcement cost": "{:.0f}"}), use_container_width=True, hide_index=True)
    st.download_button("Download comparison", df.to_csv(index=False), "policy_comparison.csv", "text/csv")


def render_calibration():
    st.markdown('<div class="hero"><h1>Empirical Calibration</h1><p>Markets do not all react to price changes in the same way. Explore how different elasticity assumptions reshape demand—and why the same policy can feel very different in gasoline, airfare, housing, or online retail.</p></div>', unsafe_allow_html=True)
    presets = {"Retail gasoline": -.3, "Airline fares": -1.2, "E-commerce": -1.8, "Rental housing": -.5}
    market = st.selectbox("Market type", list(presets))
    elasticity = presets[market]
    ref_p, ref_q = 5, 60
    slope = abs(elasticity) * ref_q / ref_p
    p = np.linspace(.5, 11, 100)
    q = np.maximum(0, ref_q + slope * (ref_p - p))
    fig = go.Figure(go.Scatter(x=q, y=p, mode="lines", name=market))
    fig.add_trace(go.Scatter(x=[ref_q], y=[ref_p], mode="markers+text", text=["Reference point"], textposition="top right"))
    fig.update_xaxes(title="Quantity")
    fig.update_yaxes(title="Price ($)")
    st.plotly_chart(chart_layout(fig, f"Illustrative demand curve · elasticity {elasticity}", 420), use_container_width=True)
    takeaway("Interpretation", f"At a reference price of ${ref_p:.2f} and quantity {ref_q:.0f}, the elasticity assumption implies a linear slope of about {slope:.2f} units per dollar. Use it to understand sensitivity, not to forecast actual market demand.")


def render_notes():
    st.markdown('<div class="hero"><h1>Research Notes</h1><p>Want to go deeper? These notes connect the experiments to the ideas behind them, explain what the model leaves out, and show how to use the results responsibly.</p></div>', unsafe_allow_html=True)
    tabs = st.tabs(["Mechanisms", "Limitations", "Glossary"])
    with tabs[0]:
        st.markdown("""
        ### Algorithmic collusion
        Independent learning agents can discover high-price strategies through repeated interaction, even without direct communication.

        ### Price discrimination audits
        Group comparisons and controlled regressions can identify patterns worth investigating, while controlling for other observed signals.

        ### Regulation
        Policy should be evaluated through the entire causal chain: rule → firm behavior → price → consumer outcome.
        """)
    with tabs[1]:
        st.markdown("""
        - Firms are simplified tabular Q-learning agents on a small price grid.
        - Demand is linear and single-product.
        - Welfare is an illustrative normalized index.
        - Audit data are synthetic and do not establish intent or causation.
        - Enforcement costs are relative units, not agency budget estimates.
        - Results should be checked across seeds and sensitivity ranges.
        """)
    with tabs[2]:
        glossary = {
            "Tacit collusion": "Coordination-like high prices that emerge without an explicit agreement.",
            "Consumer surplus": "The difference between what a consumer would be willing to pay and what they actually pay.",
            "Deadweight loss": "Value from mutually beneficial trades that do not occur because of market power or another distortion.",
            "Elasticity": "The percentage change in quantity associated with a one-percent change in price.",
            "Confidence interval": "A range expressing uncertainty around an estimated effect.",
            "Multiple testing": "The risk of false positives when many hypotheses are tested at once.",
        }
        for term, definition in glossary.items():
            st.markdown(f"**{term}** — {definition}")


def render_reading_guide():
    st.markdown('<div class="hero"><h1>How to Read the Lab</h1><p>Charts are not just decoration here. Each one answers a different question about behavior, evidence, or impact.</p></div>', unsafe_allow_html=True)
    sections = [
        ("Price paths", "Follow the colored lines from left to right. The grey benchmark is the competitive price; the red benchmark is the cartel-style reference. A sustained move toward the red line is more interesting than a short-lived spike."),
        ("Repeated-run summaries", "One run can be lucky. The repeated-run cards tell you how often the pattern appears across different random seeds. A strong claim should survive more than one seed."),
        ("Audit effect chart", "Each bar is an estimated difference between two synthetic groups. The whiskers are 95% confidence intervals. Red indicates a signal that remains detectable after the simple multiple-testing correction."),
        ("Policy trade-off chart", "A point higher on the chart delivers more illustrative welfare; a point farther right costs more relative enforcement effort. There is no automatic winner: the best choice depends on the objective you value."),
        ("Welfare outputs", "Price, quantity, surplus, residual income, and welfare are connected but not identical. A lower price can help, but the size of the benefit depends on the consumer profile and the model assumptions."),
    ]
    for title, body in sections:
        st.markdown(f'<div class="card"><h3>{title}</h3><p>{body}</p></div>', unsafe_allow_html=True)
    takeaway("A useful habit", "Before changing several controls, write down your prediction. After the run, ask: did the result match it, and which assumption explains the difference?")


def render_overview():
    st.markdown('<div class="hero"><h1>Project Overview</h1><p>AlgoMarket is an interactive decision lab about algorithmic markets, evidence, and the policy choices that shape consumer outcomes.</p></div>', unsafe_allow_html=True)
    st.markdown("### The story across the modules")
    overview = [
        ("01 · Collusion Risk Lab", "Independent pricing bots can learn high-price patterns through repeated interaction. This module lets you watch that pattern emerge and test whether delay, audits, fines, or price caps change it."),
        ("02 · Price Discrimination Auditor", "Synthetic shopper data lets you compare groups, quantify uncertainty, and see why a raw price gap is only the beginning of a careful investigation."),
        ("03 · Regulatory Design Lab", "Policy becomes meaningful when it changes firm incentives and then changes what an individual can buy, keep, or afford."),
        ("04 · Policy Comparison", "The strongest rule is not automatically the best rule. Compare welfare, market price, collusion, and relative enforcement cost together."),
        ("05 · Empirical Calibration", "Elasticity assumptions change how strongly quantity responds to price. Calibration helps you understand why the same policy can behave differently in different markets."),
    ]
    for title, body in overview:
        st.markdown(f'<div class="card"><h3>{title}</h3><p>{body}</p></div>', unsafe_allow_html=True)
    st.markdown("### Design principles")
    st.markdown("**Explore before you conclude.** Results are signals to investigate, not answers that remove judgment. **Compare, do not cherry-pick.** Use seeds, repeated runs, and sensitivity checks. **Keep the person in view.** A market outcome matters because it changes real choices and constraints.")


def render_start():
    st.markdown('<div class="hero"><h1>AlgoMarket Decision Lab</h1><p>Markets are shaped by the rules algorithms learn, the signals firms observe, and the choices regulators make. Run the experiments, challenge the assumptions, and see the human consequences behind the headline number.</p></div>', unsafe_allow_html=True)
    takeaway("A good first journey", "Start with collusion, change one policy variable, then follow the result into the Regulatory Design Lab. Every run has a seed and configuration, so you can come back, compare, and build your own evidence trail.")
    cols = st.columns(3)
    cards = [
        ("Catch the bots coordinating", "Run independent pricing bots and see whether they quietly drift toward a high-price pattern.", "Collusion Risk Lab"),
        ("Become the pricing investigator", "Create a synthetic shopper sample and find out which price gaps survive a careful audit.", "Price Discrimination Auditor"),
        ("Design a rule that matters", "Change policy, watch firms respond, and follow the consequences to an individual consumer.", "Regulatory Design Lab"),
    ]
    for col, (title, body, page) in zip(cols, cards):
        with col:
            st.markdown(f'<div class="card"><h3>{title}</h3><p>{body}</p></div>', unsafe_allow_html=True)
            if st.button("Open experiment", key=f"start_{page}", use_container_width=True):
                set_page(page)
                st.rerun()
    st.markdown("### What this tool is — and is not")
    st.markdown("This is a mechanism-learning simulator. It uses simplified, synthetic models to make economic ideas visible. It is not a forecast of a real company, a legal conclusion, or a substitute for empirical research.")


# ============================================================
# Navigation and app entry point
# ============================================================
PAGES = [
    "Start Here", "Collusion Risk Lab", "Price Discrimination Auditor",
    "Regulatory Design Lab", "Policy Comparison", "Empirical Calibration",
    "Research Notes", "How to Read the Lab", "Project Overview",
]

with st.sidebar:
    st.markdown("## ⚡ AlgoMarket")
    st.caption("Decision Lab · learn by experimenting")
    st.radio("Appearance", ["Dark", "Light"], horizontal=True, key="theme_choice", help="Choose the reading mode that feels most comfortable. Your experiments stay intact.")
    st.divider()
    st.markdown("**Choose your next move**")
    for page in PAGES:
        if st.button(page, key=f"nav_{page}", use_container_width=True, type="primary" if page == st.session_state.page else "secondary"):
            st.session_state.page = page
            st.rerun()
    st.divider()
    st.caption("Best way to learn: run a preset, change one setting, then compare the result.")

page = st.session_state.page
if page == "Start Here":
    render_start()
elif page == "Collusion Risk Lab":
    render_collusion()
elif page == "Price Discrimination Auditor":
    render_auditor()
elif page == "Regulatory Design Lab":
    render_regulation()
elif page == "Policy Comparison":
    render_comparison()
elif page == "Empirical Calibration":
    render_calibration()
elif page == "Research Notes":
    render_notes()
elif page == "How to Read the Lab":
    render_reading_guide()
elif page == "Project Overview":
    render_overview()

run_history_panel()
