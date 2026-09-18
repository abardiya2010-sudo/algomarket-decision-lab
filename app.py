import html
from dataclasses import dataclass

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="AlgoMarket Decision Lab",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# THEME
# ============================================================

THEMES = {
    "Dark": {
        "bg": "#080B12", "panel": "#111827", "panel2": "#172033", "border": "#273449",
        "text": "#E7EEF8", "muted": "#95A4BD", "heading": "#FFFFFF",
        "purple": "#8B5CF6", "cyan": "#22D3EE", "amber": "#F59E0B",
        "green": "#34D399", "red": "#FB7185", "plot": "plotly_dark",
    },
    "Light": {
        "bg": "#F5F7FB", "panel": "#FFFFFF", "panel2": "#EEF2F7", "border": "#D9E1ED",
        "text": "#243044", "muted": "#66748B", "heading": "#111827",
        "purple": "#6D28D9", "cyan": "#0891B2", "amber": "#D97706",
        "green": "#059669", "red": "#E11D48", "plot": "plotly_white",
    },
}

if "theme" not in st.session_state:
    st.session_state.theme = "Dark"
if "page" not in st.session_state:
    st.session_state.page = "Home"

T = THEMES[st.session_state.theme]

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    .stApp {{ background:{T['bg']}; color:{T['text']}; font-family:'DM Sans',sans-serif; }}
    h1,h2,h3,h4 {{ color:{T['heading']} !important; font-family:'Space Grotesk',sans-serif !important; }}
    [data-testid="stHeader"] {{ background:transparent; }}
    #MainMenu, footer, .stDeployButton {{ visibility:hidden; }}
    .stApp::before {{ content:""; position:fixed; top:0; left:0; right:0; height:4px; z-index:9999;
        background:linear-gradient(90deg,{T['purple']},{T['cyan']},{T['amber']}); }}
    section[data-testid="stSidebar"] {{ background:linear-gradient(180deg,{T['panel']},{T['panel2']}); border-right:1px solid {T['border']}; }}
    .brand {{ display:flex; align-items:center; gap:12px; padding:8px 0 18px; border-bottom:1px solid {T['border']}; margin-bottom:14px; }}
    .brand-icon {{ display:grid; place-items:center; width:43px; height:43px; border-radius:13px; color:#fff; font-size:22px;
        background:linear-gradient(135deg,{T['purple']},{T['cyan']}); }}
    .brand-title {{ color:{T['heading']}; font:700 20px 'Space Grotesk'; }}
    .brand-sub {{ color:{T['muted']}; font-size:11px; font-weight:700; letter-spacing:1px; text-transform:uppercase; }}
    .hero {{ background:radial-gradient(circle at 92% 12%,rgba(139,92,246,.25),transparent 31%),linear-gradient(135deg,{T['panel']},{T['panel2']});
        border:1px solid {T['border']}; border-radius:24px; padding:34px; margin:2px 0 20px; box-shadow:0 16px 42px rgba(0,0,0,.14); }}
    .eyebrow {{ color:{T['cyan']}; font-size:12px; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; }}
    .hero-title {{ color:{T['heading']}; font:700 clamp(30px,4vw,52px) 'Space Grotesk'; line-height:1.07; margin:8px 0 12px; }}
    .hero-copy {{ color:{T['muted']}; font-size:17px; max-width:920px; line-height:1.7; }}
    .card {{ background:{T['panel']}; border:1px solid {T['border']}; border-radius:18px; padding:20px; margin:12px 0; }}
    .metric {{ background:{T['panel']}; border:1px solid {T['border']}; border-radius:16px; padding:16px; min-height:92px; }}
    .metric-label {{ color:{T['muted']}; font-size:11px; letter-spacing:.8px; font-weight:700; text-transform:uppercase; }}
    .metric-value {{ color:{T['heading']}; font:700 24px 'Space Grotesk'; margin-top:7px; }}
    .callout {{ border-left:4px solid {T['cyan']}; background:{T['panel2']}; padding:16px 18px; border-radius:12px; line-height:1.7; margin:14px 0; }}
    .good {{ border-left-color:{T['green']}; }} .warn {{ border-left-color:{T['red']}; }}
    .small {{ color:{T['muted']}; font-size:13px; line-height:1.65; }}
    .stButton>button {{ border-radius:11px; font-weight:700; }}
    .stButton>button[kind="primary"] {{ background:linear-gradient(135deg,{T['purple']},{T['cyan']}); border:0; color:white; }}
    </style>
    """,
    unsafe_allow_html=True,
)


def clean(value):
    return html.escape(str(value))


def hero(label, title, description):
    st.markdown(
        f'<div class="hero"><div class="eyebrow">{clean(label)}</div><div class="hero-title">{clean(title)}</div><div class="hero-copy">{clean(description)}</div></div>',
        unsafe_allow_html=True,
    )


def metric(label, value, color=None):
    color_style = f"color:{color};" if color else ""
    return f'<div class="metric"><div class="metric-label">{clean(label)}</div><div class="metric-value" style="{color_style}">{clean(value)}</div></div>'


def note(text, kind=""):
    st.markdown(f'<div class="callout {kind}">{text}</div>', unsafe_allow_html=True)


def style_figure(fig, title, height=430):
    fig.update_layout(
        title=title,
        template=T["plot"],
        paper_bgcolor=T["panel"],
        plot_bgcolor=T["bg"],
        font=dict(color=T["text"], family="DM Sans"),
        height=height,
        margin=dict(l=30, r=25, t=65, b=35),
        legend=dict(orientation="h", y=1.12),
    )
    fig.update_xaxes(gridcolor=T["border"])
    fig.update_yaxes(gridcolor=T["border"])
    return fig


# ============================================================
# MODEL
# ============================================================

@dataclass
class MarketConfig:
    num_firms: int = 3
    episodes: int = 6000
    base_demand: float = 100.0
    price_sensitivity: float = 2.0
    marginal_cost: float = 1.0
    price_points: int = 15


def demand(price, cfg):
    return max(0.0, cfg.base_demand - cfg.price_sensitivity * price)


def benchmarks(cfg):
    competitive = cfg.marginal_cost
    monopoly = (cfg.base_demand / cfg.price_sensitivity + cfg.marginal_cost) / 2
    return competitive, monopoly


def market_outcome(prices, cfg):
    prices = np.asarray(prices, dtype=float)
    lowest = np.min(prices)
    winners = np.isclose(prices, lowest)
    total_quantity = demand(lowest, cfg)
    quantities = np.where(winners, total_quantity / winners.sum(), 0.0)
    profits = np.maximum(0.0, prices - cfg.marginal_cost) * quantities
    return quantities, profits


def single_run(cfg, delay, audit_probability, audit_fine, max_jump, seed):
    """Stylised independent reinforcement-learning price experiment."""
    rng = np.random.default_rng(seed)
    grid = np.round(np.linspace(cfg.marginal_cost, 26.0, cfg.price_points), 2)
    q_values = np.zeros((cfg.num_firms, len(grid)))
    last_prices = np.full(cfg.num_firms, grid[len(grid) // 2])
    observed_history = [last_prices.copy()]
    price_history, profit_history = [], []

    for round_number in range(cfg.episodes):
        epsilon = max(0.02, 0.25 * (1 - round_number / cfg.episodes))
        actions = []
        for firm in range(cfg.num_firms):
            if rng.random() < epsilon:
                action = int(rng.integers(0, len(grid)))
            else:
                action = int(np.argmax(q_values[firm]))
            actions.append(action)
        chosen = grid[actions]

        if max_jump > 0:
            chosen = np.minimum(chosen, last_prices + max_jump)

        _, profits = market_outcome(chosen, cfg)
        _, monopoly = benchmarks(cfg)
        if rng.random() < audit_probability:
            high_price = chosen >= 0.80 * monopoly
            profits = np.maximum(0.0, profits - audit_fine * high_price)

        for firm, action in enumerate(actions):
            target = profits[firm] + 0.95 * np.max(q_values[firm])
            q_values[firm, action] += 0.12 * (target - q_values[firm, action])

        last_prices = chosen.copy()
        price_history.append(chosen.copy())
        profit_history.append(profits.copy())
        observed_history.append(chosen.copy())

    history = np.asarray(price_history)
    profits = np.asarray(profit_history)
    window = min(250, len(history))
    smooth = np.vstack([
        np.convolve(history[:, firm], np.ones(window) / window, mode="valid")
        for firm in range(cfg.num_firms)
    ]).T
    return history, profits, smooth


def multi_seed_experiment(cfg, delay, audit_probability, audit_fine, max_jump, seeds):
    final_prices, final_profits, examples = [], [], None
    for seed in seeds:
        history, profits, smooth = single_run(cfg, delay, audit_probability, audit_fine, max_jump, seed)
        final_prices.append(float(np.mean(history[-min(300, len(history)):])) )
        final_profits.append(float(np.mean(profits[-min(300, len(profits)):])) )
        if examples is None:
            examples = smooth
    return np.asarray(final_prices), np.asarray(final_profits), examples


def welfare_summary(price, cfg):
    competitive, monopoly = benchmarks(cfg)
    q_now = demand(price, cfg)
    q_competitive = demand(competitive, cfg)
    choke_price = cfg.base_demand / cfg.price_sensitivity
    consumer_surplus_now = 0.5 * q_now * max(0.0, choke_price - price)
    consumer_surplus_competitive = 0.5 * q_competitive * max(0.0, choke_price - competitive)
    deadweight_loss = 0.5 * max(0.0, price - competitive) * max(0.0, q_competitive - q_now)
    risk = 100 * (price - competitive) / max(0.01, monopoly - competitive)
    return {
        "competitive": competitive,
        "monopoly": monopoly,
        "quantity": q_now,
        "consumer_surplus": consumer_surplus_now,
        "consumer_surplus_lost": max(0.0, consumer_surplus_competitive - consumer_surplus_now),
        "deadweight_loss": deadweight_loss,
        "risk": float(np.clip(risk, 0, 100)),
    }


def audit_dataset(base_price, device_effect, location_effect, returning_effect, protected_effect, noise, n, seed):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "Mobile device": rng.integers(0, 2, n),
        "Location tier": rng.integers(0, 3, n),
        "Returning visitor": rng.integers(0, 2, n),
        "Sensitive-trait proxy": rng.integers(0, 2, n),
    })
    df["Quoted price"] = (
        base_price
        + device_effect * df["Mobile device"]
        + location_effect * df["Location tier"]
        + returning_effect * df["Returning visitor"]
        + protected_effect * df["Sensitive-trait proxy"]
        + rng.normal(0, noise, n)
    )
    return df


def ols_with_intervals(df):
    columns = ["Mobile device", "Location tier", "Returning visitor", "Sensitive-trait proxy"]
    X = np.column_stack([np.ones(len(df)), df[columns].to_numpy(float)])
    y = df["Quoted price"].to_numpy(float)
    beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    residual = y - X @ beta
    degrees_of_freedom = max(1, len(y) - X.shape[1])
    variance = (residual @ residual) / degrees_of_freedom
    se = np.sqrt(np.diag(np.linalg.pinv(X.T @ X)) * variance)
    result = pd.DataFrame({
        "Signal": columns,
        "Estimated effect": beta[1:],
        "95% lower": beta[1:] - 1.96 * se[1:],
        "95% upper": beta[1:] + 1.96 * se[1:],
    })
    result["Clear from zero"] = (result["95% lower"] > 0) | (result["95% upper"] < 0)
    return result


# ============================================================
# PAGES
# ============================================================

def home_page():
    hero(
        "Interactive economics project",
        "AlgoMarket Decision Lab",
        "Explore how algorithmic pricing can affect competition, fairness and consumer welfare under transparent, simplified market assumptions.",
    )
    st.markdown("### The learning journey")
    cols = st.columns(3)
    content = [
        ("01 · Experiment", "Run a baseline market, change one condition and test what happens."),
        ("02 · Inspect", "Use benchmarks, uncertainty and welfare measures instead of relying on one chart."),
        ("03 · Explain", "Describe why the model changed, what it assumes and what it cannot prove."),
    ]
    for col, (title, text) in zip(cols, content):
        col.markdown(f'<div class="card"><div class="eyebrow">{clean(title)}</div><p class="small">{clean(text)}</p></div>', unsafe_allow_html=True)

    st.markdown("### Recommended first experiment")
    st.markdown("1. Open **Collusion Lab** and run the baseline with no intervention.\n2. Add a two-round observation delay.\n3. Add audits and fines.\n4. Compare the average result across multiple random seeds.")
    note("<b>Important:</b> This website is an educational simulation. It illustrates mechanisms and does not prove that a real firm colluded, discriminated, or broke the law.")


def collusion_page():
    hero(
        "Module 01 · repeated competition",
        "Collusion Risk Lab",
        "Run independent pricing bots many times. Compare their prices with competitive and monopoly benchmarks, then check whether the pattern survives different random seeds.",
    )

    with st.sidebar:
        st.subheader("Market setup")
        firms = st.slider("Number of firms", 2, 5, 3)
        rounds = st.slider("Training rounds", 2000, 15000, 6000, step=1000)
        delay = st.slider("Price observation delay", 0, 5, 0)
        audit_probability = st.slider("Audit probability", 0.0, 0.5, 0.0, step=0.05)
        audit_fine = st.slider("Fine when audited", 0.0, 120.0, 40.0, step=5.0)
        max_jump = st.slider("Maximum price jump", 0.0, 8.0, 0.0, step=0.5)
        seed_start = st.number_input("Starting random seed", 1, 9999, 100)
        repetitions = st.slider("Repeated runs", 5, 50, 20, step=5)
        run = st.button("Run experiment", type="primary", use_container_width=True)

    if run or "collusion_data" not in st.session_state:
        cfg = MarketConfig(num_firms=firms, episodes=rounds)
        seeds = list(range(int(seed_start), int(seed_start) + repetitions))
        with st.spinner("Running repeated simulations..."):
            prices, profits, example_path = multi_seed_experiment(cfg, delay, audit_probability, audit_fine, max_jump, seeds)
        st.session_state.collusion_data = (cfg, prices, profits, example_path, delay, audit_probability)

    cfg, prices, profits, example_path, delay, audit_probability = st.session_state.collusion_data
    price_mean, price_sd = float(prices.mean()), float(prices.std(ddof=1))
    summary = welfare_summary(price_mean, cfg)
    high_threshold = (summary["competitive"] + summary["monopoly"]) / 2
    high_share = 100 * np.mean(prices >= high_threshold)
    risk_label = "High" if summary["risk"] >= 67 else "Moderate" if summary["risk"] >= 34 else "Low"

    cols = st.columns(5)
    values = [
        metric("Mean final price", f"${price_mean:.2f}"),
        metric("Run-to-run spread", f"± ${price_sd:.2f}"),
        metric("Competitive benchmark", f"${summary['competitive']:.2f}"),
        metric("High-price runs", f"{high_share:.0f}%"),
        metric("Risk indicator", f"{risk_label} · {summary['risk']:.0f}/100", T["red"] if risk_label == "High" else T["amber"]),
    ]
    for col, value in zip(cols, values):
        col.markdown(value, unsafe_allow_html=True)

    fig = go.Figure()
    for firm in range(cfg.num_firms):
        fig.add_trace(go.Scatter(y=example_path[:, firm], mode="lines", name=f"Firm {firm + 1}"))
    fig.add_hline(y=summary["competitive"], line_dash="dash", line_color=T["muted"], annotation_text="Competitive price")
    fig.add_hline(y=summary["monopoly"], line_dash="dash", line_color=T["red"], annotation_text="Monopoly benchmark")
    st.plotly_chart(style_figure(fig, "One representative run: smoothed price paths"), use_container_width=True)

    distribution = go.Figure()
    distribution.add_trace(go.Histogram(x=prices, nbinsx=min(18, len(prices)), marker_color=T["purple"], name="Final prices"))
    distribution.add_vline(x=summary["competitive"], line_dash="dash", line_color=T["muted"], annotation_text="Competitive")
    distribution.add_vline(x=summary["monopoly"], line_dash="dash", line_color=T["red"], annotation_text="Monopoly")
    st.plotly_chart(style_figure(distribution, "Distribution across repeated runs", 360), use_container_width=True)

    st.markdown("### Welfare measures")
    cols = st.columns(4)
    welfare_metrics = [
        metric("Quantity demanded", f"{summary['quantity']:.1f}"),
        metric("Consumer surplus", f"${summary['consumer_surplus']:.1f}"),
        metric("Consumer surplus lost", f"${summary['consumer_surplus_lost']:.1f}"),
        metric("Deadweight loss", f"${summary['deadweight_loss']:.1f}"),
    ]
    for col, value in zip(cols, welfare_metrics):
        col.markdown(value, unsafe_allow_html=True)

    note(
        f"<b>Interpretation:</b> With delay = {delay} and audit probability = {audit_probability:.0%}, the mean final price is ${price_mean:.2f}. "
        f"The reported risk indicator measures where that average sits between the competitive and monopoly benchmarks. "
        "It is a model-specific indicator, not evidence of illegal collusion.",
        "warn" if risk_label == "High" else "good",
    )

    csv = pd.DataFrame({"seed_run": range(1, len(prices) + 1), "final_price": prices, "mean_profit": profits})
    st.download_button("Download experiment results (CSV)", csv.to_csv(index=False).encode("utf-8"), "collusion_results.csv", "text/csv")


def fairness_page():
    hero(
        "Module 02 · pricing audit",
        "Fairness Audit",
        "Generate a synthetic set of quoted prices, inspect group differences, and then estimate each signal's effect while controlling for the other observed signals.",
    )

    with st.sidebar:
        st.subheader("Synthetic-market settings")
        base = st.slider("Base quoted price", 20, 200, 100)
        device_effect = st.slider("Mobile-device effect", -20, 20, 6)
        location_effect = st.slider("Location-tier effect", -20, 20, 5)
        returning_effect = st.slider("Returning-visitor effect", -20, 20, -4)
        protected_effect = st.slider("Sensitive-trait proxy effect", -20, 20, 8)
        noise = st.slider("Unexplained variation", 0, 20, 5)
        sample = st.slider("Number of shoppers", 500, 10000, 3000, step=500)
        seed = st.number_input("Random seed", 1, 9999, 21, key="fairness_seed")
        run = st.button("Run audit", type="primary", use_container_width=True)

    if run or "fairness_data" not in st.session_state:
        st.session_state.fairness_data = audit_dataset(base, device_effect, location_effect, returning_effect, protected_effect, noise, sample, int(seed))

    df = st.session_state.fairness_data
    group_rows = []
    comparisons = [
        ("Desktop vs mobile", "Mobile device", 0, 1),
        ("Location tier 1 vs 3", "Location tier", 0, 2),
        ("New vs returning visitor", "Returning visitor", 0, 1),
        ("Reference vs comparison group", "Sensitive-trait proxy", 0, 1),
    ]
    for label, column, left_value, right_value in comparisons:
        left = df.loc[df[column] == left_value, "Quoted price"]
        right = df.loc[df[column] == right_value, "Quoted price"]
        group_rows.append({
            "Comparison": label,
            "First-group average": left.mean(),
            "Second-group average": right.mean(),
            "Raw difference": right.mean() - left.mean(),
            "Minimum group n": min(len(left), len(right)),
        })
    groups = pd.DataFrame(group_rows)

    st.markdown("### Descriptive group comparison")
    st.dataframe(groups.style.format({"First-group average": "${:.2f}", "Second-group average": "${:.2f}", "Raw difference": "${:.2f}"}), use_container_width=True, hide_index=True)

    chart = go.Figure()
    chart.add_trace(go.Bar(x=groups["Comparison"], y=groups["First-group average"], name="First group", marker_color=T["purple"]))
    chart.add_trace(go.Bar(x=groups["Comparison"], y=groups["Second-group average"], name="Second group", marker_color=T["cyan"]))
    chart.update_layout(barmode="group")
    st.plotly_chart(style_figure(chart, "Average price by comparison"), use_container_width=True)

    st.markdown("### Controlled audit")
    regression = ols_with_intervals(df)
    controlled = go.Figure()
    controlled.add_trace(go.Bar(
        x=regression["Estimated effect"],
        y=regression["Signal"],
        orientation="h",
        error_x=dict(
            type="data", symmetric=False,
            array=regression["95% upper"] - regression["Estimated effect"],
            arrayminus=regression["Estimated effect"] - regression["95% lower"],
        ),
        marker_color=[T["red"] if flag else T["muted"] for flag in regression["Clear from zero"]],
    ))
    controlled.add_vline(x=0, line_dash="dash", line_color=T["muted"])
    st.plotly_chart(style_figure(controlled, "Estimated price effects after controlling for observed signals"), use_container_width=True)
    st.dataframe(regression.style.format({"Estimated effect": "${:.2f}", "95% lower": "${:.2f}", "95% upper": "${:.2f}"}), use_container_width=True, hide_index=True)

    note(
        "<b>Audit status: preliminary.</b> A statistical pattern can justify further investigation, but it does not by itself prove intent, causation, unfairness or legal liability. "
        "Real audits need representative data, valid measurements, relevant business explanations and information about unobserved factors."
    )
    st.download_button("Download synthetic audit data (CSV)", df.to_csv(index=False).encode("utf-8"), "fairness_audit_data.csv", "text/csv")


def policy_page():
    hero(
        "Module 03 · policy comparison",
        "Policy Studio",
        "Compare policy packages across the same simulated market. Focus on trade-offs: prices, consumer welfare, uncertainty and an illustrative implementation-cost index.",
    )

    packages = {
        "Baseline": {"delay": 0, "audit": 0.0, "fine": 0.0, "jump": 0.0, "cost": 0},
        "Transparency & monitoring": {"delay": 1, "audit": 0.10, "fine": 25.0, "jump": 0.0, "cost": 20},
        "Targeted enforcement": {"delay": 2, "audit": 0.25, "fine": 50.0, "jump": 1.5, "cost": 55},
        "Strong intervention": {"delay": 4, "audit": 0.40, "fine": 85.0, "jump": 0.75, "cost": 95},
    }

    with st.sidebar:
        st.subheader("Comparison setup")
        chosen = st.multiselect("Policy packages", list(packages), default=list(packages))
        firms = st.slider("Number of firms", 2, 5, 3, key="policy_firms")
        rounds = st.slider("Training rounds", 2000, 12000, 5000, step=1000, key="policy_rounds")
        repetitions = st.slider("Repeated runs", 5, 30, 10, step=5, key="policy_repetitions")
        seed_start = st.number_input("Starting random seed", 1, 9999, 500, key="policy_seed")
        run = st.button("Compare policies", type="primary", use_container_width=True)

    if run or "policy_data" not in st.session_state:
        rows = []
        active = chosen if chosen else list(packages)
        with st.spinner("Running policy scenarios..."):
            for package_index, name in enumerate(active):
                cfg = MarketConfig(num_firms=firms, episodes=rounds)
                policy = packages[name]
                seeds = list(range(int(seed_start) + package_index * 100, int(seed_start) + package_index * 100 + repetitions))
                prices, _, _ = multi_seed_experiment(cfg, policy["delay"], policy["audit"], policy["fine"], policy["jump"], seeds)
                mean_price = float(prices.mean())
                welfare = welfare_summary(mean_price, cfg)
                rows.append({
                    "Policy": name,
                    "Mean final price": mean_price,
                    "Price uncertainty": float(prices.std(ddof=1)),
                    "Consumer surplus": welfare["consumer_surplus"],
                    "Deadweight loss": welfare["deadweight_loss"],
                    "Implementation-cost index": policy["cost"],
                })
        st.session_state.policy_data = pd.DataFrame(rows)

    result = st.session_state.policy_data
    st.dataframe(
        result.style.format({
            "Mean final price": "${:.2f}", "Price uncertainty": "± ${:.2f}",
            "Consumer surplus": "${:.2f}", "Deadweight loss": "${:.2f}",
        }),
        use_container_width=True,
        hide_index=True,
    )

    chart = go.Figure()
    chart.add_trace(go.Bar(x=result["Policy"], y=result["Mean final price"], name="Mean final price", marker_color=T["purple"]))
    chart.add_trace(go.Bar(x=result["Policy"], y=result["Deadweight loss"], name="Deadweight loss", marker_color=T["red"]))
    chart.update_layout(barmode="group")
    st.plotly_chart(style_figure(chart, "Market outcomes by policy package"), use_container_width=True)

    best = result.loc[result["Deadweight loss"].idxmin(), "Policy"]
    note(
        f"<b>Model result:</b> <b>{clean(best)}</b> has the lowest deadweight-loss estimate in this comparison. "
        "That is not a universal recommendation because policy effects, enforcement costs and market conditions differ in real life."
    )
    st.download_button("Download policy comparison (CSV)", result.to_csv(index=False).encode("utf-8"), "policy_comparison.csv", "text/csv")


def experiments_page():
    hero(
        "Experiment library",
        "Guided Investigations",
        "Use these questions as a proper research workflow. Change one variable at a time, repeat the runs and explain both the result and the limitation.",
    )
    investigations = [
        ("1. Baseline competition", "Can independent pricing bots produce prices above the competitive benchmark?", "Use 3 firms, no delay, no audits and at least 20 repeated runs."),
        ("2. Information delay", "Does delayed rival-price information reduce high-price outcomes?", "Compare delay = 0, 2 and 4 while holding every other setting fixed."),
        ("3. Audit incentives", "Do audits and fines change the model's pricing outcomes?", "Compare audit probability = 0%, 10%, 25% and 40%."),
        ("4. Confounding in audits", "Can a raw group gap be explained by other observed variables?", "Set the sensitive-trait effect to zero but add location and device effects, then compare raw and controlled results."),
        ("5. Policy trade-off", "Which package lowers model welfare loss with the least implementation burden?", "Use Policy Studio and discuss why an illustrative cost index is not a real government budget."),
    ]
    for title, question, method in investigations:
        st.markdown(f'<div class="card"><div class="eyebrow">{clean(title)}</div><h3>{clean(question)}</h3><p class="small"><b>Method:</b> {clean(method)}</p></div>', unsafe_allow_html=True)


def methodology_page():
    hero(
        "Model transparency",
        "Assumptions, equations and limits",
        "A good simulation is clear about what it represents, what it measures and where its conclusions stop.",
    )
    tabs = st.tabs(["Assumptions", "Measures", "Limitations", "How to report"])
    with tabs[0]:
        st.markdown("- Firms sell one identical product.\n- Demand follows a linear rule: quantity falls as price rises.\n- The cheapest firm receives demand; tied cheapest firms share it.\n- Firms choose from a limited set of prices and learn from repeated rewards.\n- Policy interventions are simplified parameters, not complete real-world laws.")
        st.latex(r"Q(P) = \max(0, A - bP)")
        st.latex(r"\Pi_i = (P_i - c)Q_i")
    with tabs[1]:
        st.markdown("- **Competitive benchmark:** marginal cost in this stylised Bertrand market.\n- **Monopoly benchmark:** the profit-maximising price for the model's linear demand curve.\n- **Risk indicator:** where the average simulated price sits between those two benchmarks.\n- **Consumer surplus and deadweight loss:** partial-equilibrium welfare measures under the same demand assumptions.")
    with tabs[2]:
        note("The app does not use real company data, does not model every pricing algorithm, does not establish legal liability, and does not produce a reliable forecast. Results may change with random seeds, parameter choices and omitted real-world factors.", "warn")
    with tabs[3]:
        st.markdown("1. State the research question.\n2. State the baseline settings.\n3. Change one variable at a time.\n4. Run multiple seeds.\n5. Report averages and spread, not just one result.\n6. Explain the mechanism.\n7. Name at least one limitation.")


# ============================================================
# APP SHELL
# ============================================================

with st.sidebar:
    st.markdown('<div class="brand"><div class="brand-icon">⚡</div><div><div class="brand-title">AlgoMarket</div><div class="brand-sub">Decision Lab</div></div></div>', unsafe_allow_html=True)
    selected_theme = st.radio("Appearance", ["Dark", "Light"], index=0 if st.session_state.theme == "Dark" else 1)
    if selected_theme != st.session_state.theme:
        st.session_state.theme = selected_theme
        st.rerun()
    st.markdown("#### Navigate")
    pages = ["Home", "Collusion Lab", "Fairness Audit", "Policy Studio", "Guided Investigations", "Model Transparency"]
    for page in pages:
        if st.button(page, use_container_width=True, type="primary" if st.session_state.page == page else "secondary"):
            st.session_state.page = page
            st.rerun()
    st.markdown("---")
    st.caption("Educational simulation · Version 3")

page_functions = {
    "Home": home_page,
    "Collusion Lab": collusion_page,
    "Fairness Audit": fairness_page,
    "Policy Studio": policy_page,
    "Guided Investigations": experiments_page,
    "Model Transparency": methodology_page,
}

page_functions[st.session_state.page]()
