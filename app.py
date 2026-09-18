import random
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

st.set_page_config(page_title="AlgoMarket Decision Lab", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

with st.sidebar:
    st.markdown("""
        <div class="sidebar-brand">
            <div class="sidebar-brand-icon">⚡</div>
            <div>
                <div class="sidebar-brand-title">AlgoMarket</div>
                <div class="sidebar-brand-sub">Decision Lab</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    dark_mode = st.toggle("🌙 Dark Mode" if not st.session_state.dark_mode else "☀️ Light Mode",
                           value=st.session_state.dark_mode, key="dark_mode")

LIGHT = dict(
    bg="#F6F7FB", panel="#FFFFFF", panel2="#F1F3F9", sidebar="#FFFFFF",
    border="#E3E7F1", shadow="rgba(35,40,56,0.06)",
    heading="#171B26", text="#232838", muted="#6B7286",
    amber="#F59E0B", amber_deep="#B45309", amber_tag_bg="#FEF3C7",
    blue="#2563EB", blue_deep="#1D4ED8", blue_tag_bg="#DBEAFE",
    pink="#DB2777", pink_deep="#9D174D", pink_tag_bg="#FCE7F3",
    red="#E11D48", green="#16A34A", purple="#7C3AED",
    hero_grad_amber="linear-gradient(135deg,#FFFFFF 0%,#FEF9EF 100%)",
    hero_grad_blue="linear-gradient(135deg,#FFFFFF 0%,#EFF6FF 100%)",
    hero_grad_pink="linear-gradient(135deg,#FFFFFF 0%,#FDF2F8 100%)",
    read_amber_bg="#FFFBEB", read_amber_border="#FDE68A", read_amber_text="#3F3212",
    read_blue_bg="#EFF6FF", read_blue_border="#BFDBFE", read_blue_text="#1E3A5F",
    read_pink_bg="#FDF2F8", read_pink_border="#FBCFE8", read_pink_text="#831843",
    result_green_bg="#F0FDF4", result_green_border="#BBF7D0", result_green_text="#14532D",
    result_red_bg="#FEF2F2", result_red_border="#FECACA", result_red_text="#7F1D1D",
    result_blue_bg="#EFF6FF", result_blue_border="#BFDBFE", result_blue_text="#1E3A5F",
    problem_bg="#FEE2E2", problem_text="#991B1B",
    solution_bg="#DCFCE7", solution_text="#14532D",
    tldr_bg="#171B26", tldr_text="#FFFFFF",
    plot_template="plotly_white", plot_paper="#FFFFFF", plot_area="#FFFFFF", plot_grid="#EEF1F7",
    plot_font="#232838",
    series=['#2563EB','#E11D48','#7C3AED','#F59E0B','#16A34A'],
    bar_pair=['#F9A8D4','#DB2777'],
)
DARK = dict(
    bg="#0B0E14", panel="#141922", panel2="#191F2B", sidebar="#0F1319",
    border="#262D3A", shadow="rgba(0,0,0,0.35)",
    heading="#F5F6F8", text="#E8EAED", muted="#8B93A7",
    amber="#F5B84E", amber_deep="#FBBF24", amber_tag_bg="#3A2E10",
    blue="#5B9DF9", blue_deep="#60A5FA", blue_tag_bg="#122A4E",
    pink="#F472B6", pink_deep="#F9A8D4", pink_tag_bg="#3A1230",
    red="#FB7185", green="#4ADE80", purple="#C4B5FD",
    hero_grad_amber="linear-gradient(135deg,#171D28 0%,#1F1A0F 100%)",
    hero_grad_blue="linear-gradient(135deg,#171D28 0%,#0F1A2E 100%)",
    hero_grad_pink="linear-gradient(135deg,#171D28 0%,#23121D 100%)",
    read_amber_bg="#20180A", read_amber_border="#4A3B14", read_amber_text="#F3DFAA",
    read_blue_bg="#0E1B30", read_blue_border="#1E3A5F", read_blue_text="#BFDBFE",
    read_pink_bg="#22101B", read_pink_border="#4A1E38", read_pink_text="#F9C9E4",
    result_green_bg="#0E1F14", result_green_border="#1E4028", result_green_text="#86EFAC",
    result_red_bg="#261315", result_red_border="#4A1F24", result_red_text="#FCA5A5",
    result_blue_bg="#0E1B30", result_blue_border="#1E3A5F", result_blue_text="#BFDBFE",
    problem_bg="#2A1416", problem_text="#FCA5A5",
    solution_bg="#0F2417", solution_text="#86EFAC",
    tldr_bg="#F5F6F8", tldr_text="#0B0E14",
    plot_template="plotly_dark", plot_paper="#141922", plot_area="#0B0E14", plot_grid="#232A38",
    plot_font="#E8EAED",
    series=['#5B9DF9','#FB7185','#C4B5FD','#F5B84E','#4ADE80'],
    bar_pair=['#7A3B5B','#F472B6'],
)
T = DARK if dark_mode else LIGHT

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap');
#MainMenu, footer, .stDeployButton, [data-testid="stStatusWidget"], [data-testid="stToolbarActions"],
[data-testid="stAppDeployButton"], [data-testid="stDecoration"] {{ visibility: hidden; display: none; }}
[data-testid="stHeader"] {{ background: transparent; }}
button[aria-label*="Deploy" i] {{ display: none !important; }}
[data-testid="StyledFullScreenButton"] {{ visibility: visible !important; opacity: 1 !important; }}
.stApp {{ background-color: {T['bg']}; color: {T['text']}; font-family: 'Inter', sans-serif; font-size: 1.02rem; line-height: 1.65; }}
h1,h2,h3,.hero-title {{ font-family: 'Poppins', sans-serif !important; color: {T['heading']}; }}
.exp-tag {{ display: inline-block; font-weight: 700; font-size: 0.78rem; letter-spacing: 0.05em; text-transform: uppercase; padding: 0.4rem 1rem; border-radius: 999px; background: {T['amber_tag_bg']}; color: {T['amber_deep']}; margin-bottom: 1rem; }}
.exp-tag.pink {{ background: {T['pink_tag_bg']}; color: {T['pink_deep']}; }}
.exp-tag.green {{ background: {T['solution_bg']}; color: {T['solution_text']}; }}
.hero-card {{ background: {T['hero_grad_amber']}; padding: 2.1rem 2.3rem; border-radius: 20px; border: 1px solid {T['border']}; box-shadow: 0 8px 32px {T['shadow']}; margin-bottom: 1.25rem; }}
.hero-card.pink {{ background: {T['hero_grad_pink']}; }}
.hero-card.green {{ background: linear-gradient(135deg, {T['panel']} 0%, {T['solution_bg']} 100%); }}
.hero-title {{ font-size: 2.05rem !important; font-weight: 700; margin-bottom: 0.5rem; }}
.hero-sub {{ color: {T['muted']}; font-size: 1.05rem; line-height: 1.7; max-width: 940px; }}
.explainer {{ background: {T['panel']}; border: 1px solid {T['border']}; border-left: 6px solid {T['amber']}; border-radius: 16px; padding: 1.45rem 1.65rem; margin-bottom: 1.3rem; box-shadow: 0 2px 12px {T['shadow']}; }}
.explainer.pink {{ border-left-color: {T['pink']}; }}
.explainer.green {{ border-left-color: {T['green']}; }}
.explainer h4 {{ margin: 0 0 0.55rem 0; font-family: 'Poppins', sans-serif; font-weight: 600; font-size: 1.12rem; color: {T['heading']}; }}
.explainer p {{ margin: 0 0 0.7rem 0; color: {T['text']}; font-size: 1.0rem; line-height: 1.72; }}
.explainer p:last-child {{ margin-bottom: 0; }}
.explainer ul {{ margin: 0.4rem 0 0.6rem 1.2rem; padding: 0; color: {T['text']}; }}
.explainer li {{ margin-bottom: 0.35rem; line-height: 1.6; }}
.read-box {{ background: {T['read_amber_bg']}; border: 1px solid {T['read_amber_border']}; border-radius: 14px; padding: 1.05rem 1.35rem; margin: 0.75rem 0 1.15rem 0; font-size: 0.96rem; color: {T['read_amber_text']}; line-height: 1.65; }}
.read-box.pink {{ background: {T['read_pink_bg']}; border-color: {T['read_pink_border']}; color: {T['read_pink_text']}; }}
.read-box.green {{ background: {T['result_green_bg']}; border-color: {T['result_green_border']}; color: {T['result_green_text']}; }}
.result-box {{ background: {T['result_green_bg']}; border: 1px solid {T['result_green_border']}; border-radius: 16px; padding: 1.35rem 1.6rem; margin-top: 1rem; font-size: 1.0rem; line-height: 1.75; color: {T['result_green_text']}; }}
.result-box.warn {{ background: {T['result_red_bg']}; border-color: {T['result_red_border']}; color: {T['result_red_text']}; }}
.result-box.info {{ background: {T['result_blue_bg']}; border-color: {T['result_blue_border']}; color: {T['result_blue_text']}; }}
.metric-card {{ background: {T['panel']}; border: 1px solid {T['border']}; border-radius: 14px; padding: 1.05rem 0.8rem; text-align: center; box-shadow: 0 3px 12px {T['shadow']}; height: 100%; }}
.metric-value {{ font-size: 1.3rem; font-weight: 700; color: {T['heading']}; }}
.metric-label {{ font-size: 0.68rem; color: {T['muted']}; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 0.25rem; font-weight: 600; }}
.guide-box, .guide-box-pink, .guide-box-green {{ background: {T['panel']}; border: 1px solid {T['border']}; border-left: 6px solid {T['amber']}; border-radius: 14px; padding: 1.2rem 1.4rem; margin-bottom: 1rem; line-height: 1.7; }}
.guide-box-pink {{ border-left-color: {T['pink']}; }}
.guide-box-green {{ border-left-color: {T['green']}; }}
.guide-box h4, .guide-box-pink h4, .guide-box-green h4 {{ font-family: 'Poppins', sans-serif; font-weight: 600; margin: 0 0 0.4rem 0; font-size: 1.02rem; color: {T['heading']}; }}
.overview-card {{ background: {T['panel']}; border: 1px solid {T['border']}; border-radius: 16px; padding: 1.45rem 1.65rem; margin-bottom: 1.15rem; box-shadow: 0 2px 12px {T['shadow']}; }}
.overview-card h3 {{ font-family: 'Poppins', sans-serif; font-weight: 600; margin: 0 0 0.75rem 0; font-size: 1.18rem; }}
.overview-block {{ margin-bottom: 0.75rem; }}
.overview-block .tag {{ display: inline-block; font-weight: 700; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.04em; padding: 0.18rem 0.5rem; border-radius: 6px; margin-bottom: 0.3rem; }}
.overview-block.problem .tag {{ background: {T['problem_bg']}; color: {T['problem_text']}; }}
.overview-block.solution .tag {{ background: {T['solution_bg']}; color: {T['solution_text']}; }}
.overview-block p {{ color: {T['text']}; line-height: 1.7; margin: 0; }}
.tldr {{ display: inline-block; background: {T['tldr_bg']}; color: {T['tldr_text']}; font-weight: 700; font-size: 0.68rem; letter-spacing: 0.05em; text-transform: uppercase; padding: 0.2rem 0.5rem; border-radius: 5px; margin-right: 0.45rem; }}
.ctrl-help {{ font-size: 0.78rem; color: {T['muted']}; margin: -0.35rem 0 0.85rem 0; line-height: 1.45; }}
section[data-testid="stSidebar"] {{ background: linear-gradient(180deg, {T['sidebar']} 0%, {T['panel2']} 100%); border-right: 1px solid {T['border']}; }}
section[data-testid="stSidebar"]::before {{ content: ""; position: absolute; top: 0; left: 0; bottom: 0; width: 4px; background: linear-gradient(180deg, {T['amber']} 0%, {T['blue']} 50%, {T['pink']} 100%); z-index: 2; }}
.sidebar-brand {{ display: flex; align-items: center; gap: 0.7rem; margin: 0.1rem 0 1.1rem 0; padding-bottom: 0.95rem; border-bottom: 1px solid {T['border']}; }}
.sidebar-brand-icon {{ width: 40px; height: 40px; border-radius: 11px; background: linear-gradient(135deg, {T['amber']} 0%, {T['pink']} 100%); display: flex; align-items: center; justify-content: center; font-size: 1.25rem; flex-shrink: 0; }}
.sidebar-brand-title {{ font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 1.12rem; color: {T['heading']}; }}
.sidebar-brand-sub {{ font-size: 0.68rem; color: {T['muted']}; text-transform: uppercase; letter-spacing: 0.07em; font-weight: 600; }}
section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {{ font-size: 0.78rem !important; font-weight: 700 !important; text-transform: uppercase; letter-spacing: 0.06em; color: {T['muted']} !important; margin-top: 1.05rem !important; }}
.stApp::before {{ content: ""; position: fixed; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, {T['amber']} 0%, {T['blue']} 50%, {T['pink']} 100%); z-index: 999999; }}
section[data-testid="stSidebar"] .stButton > button {{ font-size: 0.93rem; padding: 0.58rem 0.8rem; margin-bottom: 0.25rem; border: 1px solid {T['border']}; background: {T['panel']}; color: {T['text']}; }}
section[data-testid="stSidebar"] button[kind="secondary"]:hover {{ background: {T['panel2']}; border-color: {T['blue']}; transform: translateX(3px); }}
section[data-testid="stSidebar"] button[kind="primary"] {{ background: linear-gradient(135deg, {T['amber']} 0%, {T['pink']} 100%) !important; color: #fff !important; border: none !important; font-weight: 700 !important; }}
</style>
""", unsafe_allow_html=True)


# ===================== ENGINES =====================
class OligopolyEnvironment:
    def __init__(self, num_agents=2, marginal_cost=1.0, base_demand=100.0, price_sensitivity=2.0):
        self.num_agents = num_agents
        self.marginal_cost = marginal_cost
        self.base_demand = base_demand
        self.price_sensitivity = price_sensitivity
        self.p_nash = marginal_cost
        self.p_monopoly = (self.base_demand / self.price_sensitivity + self.marginal_cost) / 2.0

    def step(self, market_prices):
        prices = np.array(market_prices, dtype=float)
        min_price = np.min(prices)
        demands = np.zeros_like(prices)
        cheapest = (prices == min_price)
        n_cheap = np.sum(cheapest)
        total_d = max(0.0, self.base_demand - self.price_sensitivity * min_price)
        if n_cheap > 0:
            demands[cheapest] = total_d / n_cheap
        return demands, np.maximum((prices - self.marginal_cost) * demands, 0.0)


class QLearningAgent:
    def __init__(self, agent_id, price_grid, alpha=0.15, gamma=0.95, epsilon=0.2):
        self.agent_id = agent_id
        self.price_grid = price_grid
        self.num_actions = len(price_grid)
        self.alpha, self.gamma, self.epsilon = alpha, gamma, epsilon
        self.q_table = {}

    def select_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, self.num_actions - 1)
        if state not in self.q_table:
            self.q_table[state] = np.zeros(self.num_actions)
        return int(np.argmax(self.q_table[state]))

    def update(self, state, action_idx, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(self.num_actions)
        if next_state not in self.q_table:
            self.q_table[next_state] = np.zeros(self.num_actions)
        q = self.q_table[state][action_idx]
        self.q_table[state][action_idx] = q + self.alpha * (reward + self.gamma * np.max(self.q_table[next_state]) - q)


class RegulatoryPolicyEngine:
    def __init__(self, latency_delay=0, audit_prob=0.0, audit_fine=50.0, max_price_jump=None, ban_punishment=False):
        self.latency_delay = latency_delay
        self.audit_prob = audit_prob
        self.audit_fine = audit_fine
        self.max_price_jump = max_price_jump
        self.ban_punishment = ban_punishment
        self.price_history = []

    def apply_state_masking(self, raw_prices, step):
        self.price_history.append(raw_prices)
        observed = self.price_history[-1 - self.latency_delay] if (self.latency_delay > 0 and step >= self.latency_delay) else raw_prices
        n = len(raw_prices)
        return [tuple(observed[j] for j in range(n) if j != i) for i in range(n)]

    def apply_audits(self, prices, profits, p_mono):
        adj = profits.copy()
        if self.audit_prob > 0 and random.random() < self.audit_prob:
            for i, p in enumerate(prices):
                if p >= 0.8 * p_mono:
                    adj[i] -= self.audit_fine
        return np.maximum(adj, 0.0)

    def constrain_price(self, new_p, old_p):
        return new_p if self.max_price_jump is None else min(new_p, old_p + self.max_price_jump)


# ===================== WELFARE / DEADWEIGHT LOSS =====================
def compute_deadweight_loss(p_now, p_competitive, base_demand, price_sensitivity, marginal_cost):
    """
    Linear demand Q(P) = max(0, base_demand - price_sensitivity * P).
    DWL = area of the triangle between the demand curve and marginal cost,
    for the units that would have traded at p_competitive but do not trade at p_now.
    This is standard partial-equilibrium welfare analysis (see e.g. Varian, Intermediate
    Microeconomics, ch. on monopoly / deadweight loss).
    """
    def q_of(p):
        return max(0.0, base_demand - price_sensitivity * p)

    q_now = q_of(p_now)
    q_comp = q_of(p_competitive)
    dwl = 0.5 * max(0.0, p_now - p_competitive) * max(0.0, q_comp - q_now)
    cs_now = 0.5 * q_now * max(0.0, (base_demand / price_sensitivity) - p_now)
    cs_comp = 0.5 * q_comp * max(0.0, (base_demand / price_sensitivity) - p_competitive)
    ps_now = max(0.0, (p_now - marginal_cost)) * q_now
    ps_comp = max(0.0, (p_competitive - marginal_cost)) * q_comp
    return {
        "q_now": q_now, "q_comp": q_comp, "dwl": dwl,
        "cs_now": cs_now, "cs_comp": cs_comp, "ps_now": ps_now, "ps_comp": ps_comp,
        "choke_price": base_demand / price_sensitivity
    }


def deadweight_loss_figure(p_now, p_competitive, base_demand, price_sensitivity, marginal_cost, theme, title="Deadweight loss from the current market price"):
    dwl = compute_deadweight_loss(p_now, p_competitive, base_demand, price_sensitivity, marginal_cost)
    choke = dwl["choke_price"]
    p_hi = max(choke, p_now, p_competitive) * 1.05
    prices = np.linspace(0, p_hi, 100)
    quantities = np.maximum(0.0, base_demand - price_sensitivity * prices)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=quantities, y=prices, mode="lines", name="Demand curve",
                             line=dict(color=theme['blue'], width=2.5)))
    fig.add_trace(go.Scatter(x=[0, base_demand], y=[marginal_cost, marginal_cost], mode="lines",
                             name="Marginal cost", line=dict(color=theme['muted'], width=2, dash="dot")))
    # Shade the DWL triangle
    q_now, q_comp = dwl["q_now"], dwl["q_comp"]
    if q_comp > q_now:
        tri_x = [q_now, q_comp, q_now]
        tri_y = [p_now, p_competitive, p_competitive]
        fig.add_trace(go.Scatter(x=tri_x, y=tri_y, fill="toself", mode="lines",
                                 line=dict(color=theme['red'], width=1),
                                 fillcolor=theme['red'],
                                 name="Deadweight loss", opacity=0.35))
    fig.add_trace(go.Scatter(x=[q_now], y=[p_now], mode="markers+text", text=["Current price"],
                             textposition="top right", marker=dict(color=theme['red'], size=9), name="Current"))
    fig.add_trace(go.Scatter(x=[q_comp], y=[p_competitive], mode="markers+text", text=["Competitive price"],
                             textposition="bottom right", marker=dict(color=theme['green'], size=9), name="Competitive"))
    fig.update_layout(title=title, xaxis_title="Quantity", yaxis_title="Price ($)",
                      template=theme['plot_template'], paper_bgcolor=theme['plot_paper'],
                      plot_bgcolor=theme['plot_area'], font=dict(color=theme['plot_font']),
                      height=420, legend=dict(orientation="h", y=1.1),
                      xaxis=dict(gridcolor=theme['plot_grid']), yaxis=dict(gridcolor=theme['plot_grid']))
    return fig, dwl


def execute_simulation(num_agents, episodes, latency_delay, audit_prob, audit_fine=40.0,
                       max_price_jump=None, ban_punishment=False, cost_shock=0.0, demand_shift=0.0):
    env = OligopolyEnvironment(num_agents=num_agents, marginal_cost=1.0 + cost_shock,
                               base_demand=100.0 + demand_shift)
    price_grid = [round(p, 2) for p in np.linspace(1.0, 26.0, 12)]
    agents = [QLearningAgent(i, price_grid) for i in range(num_agents)]
    policy = RegulatoryPolicyEngine(latency_delay, audit_prob, audit_fine, max_price_jump, ban_punishment)
    history_prices, history_profits = [], []
    current = [env.p_monopoly] * num_agents
    states = policy.apply_state_masking(current, 0)
    for ep in range(episodes):
        for a in agents:
            a.epsilon = max(0.01, 0.2 * (1 - ep / episodes))
        actions = [a.select_action(states[i]) for i, a in enumerate(agents)]
        chosen = [price_grid[a] for a in actions]
        if max_price_jump is not None and ep > 0:
            prev = history_prices[-1]
            chosen = [policy.constrain_price(chosen[i], prev[i]) for i in range(num_agents)]
        demands, profits = env.step(chosen)
        adj = policy.apply_audits(chosen, profits, env.p_monopoly)
        if ban_punishment and ep > 10:
            for i in range(num_agents):
                if chosen[i] < np.mean(chosen) * 0.85:
                    adj[i] *= 0.7
        next_states = policy.apply_state_masking(chosen, ep)
        for i, a in enumerate(agents):
            a.update(states[i], actions[i], adj[i], next_states[i])
        states = next_states
        history_prices.append(chosen)
        history_profits.append(adj.tolist())
    hist = np.array(history_prices)
    prof = np.array(history_profits)
    window = min(250, len(hist))
    smoothed = np.zeros((len(hist) - window + 1, num_agents))
    for i in range(num_agents):
        smoothed[:, i] = np.convolve(hist[:, i], np.ones(window) / window, mode='valid')
    return smoothed, float(np.mean(hist[-500:])), env.p_nash, env.p_monopoly, hist, prof, float(np.mean(prof[-500:]))


def narrate_collusion(smoothed, final_price, p_nash, p_mono, n, latency, audit):
    start = float(np.mean(smoothed[0]))
    pct = ((final_price - p_nash) / max(p_nash, 0.01)) * 100
    text = (f"<b>What just happened</b><br><br>"
            f"You put <b>{n} AI pricing bots</b> into the same market. They cannot talk to each other. "
            f"They started near <b>${start:.2f}</b> and, after thousands of rounds of trial-and-error, "
            f"settled near <b>${final_price:.2f}</b> — that is <b>{pct:.0f}% above</b> the fair competitive price of ${p_nash:.2f}.")
    if final_price >= 6:
        text += ("<br><br>This is a <b>collusion outcome</b>. Each bot independently learned that cutting its price "
                 "is immediately punished by the others, so eventually nobody bothers to undercut and prices stay high. "
                 "No human agreed to anything — the algorithms discovered the high-price equilibrium on their own.")
    else:
        text += ("<br><br>This is a <b>competitive outcome</b>. The bots kept undercutting each other, so prices "
                 "stayed close to cost. That is the outcome regulators prefer.")
    if latency > 0:
        text += f"<br><br>The {latency}-round observation delay made it harder for a bot to instantly punish an undercutter, which helped keep prices lower."
    if audit > 0:
        text += f"<br><br>Random audits (probability {audit:.0%}) with fines raised the expected cost of holding a very high price, so the bots learned to avoid the top of the range."
    return text


# ---- Module 02 richer discrimination ----
def simulate_price_audit(base_price, device_bias, location_bias, loyalty_bias, time_bias,
                         payment_bias, history_bias, colour_bias, dress_bias, speech_bias,
                         posture_bias, face_bias, noise_std, num_visits, seed=None):
    rng = np.random.default_rng(seed)
    device = rng.integers(0, 2, size=num_visits)
    location = rng.integers(0, 3, size=num_visits)
    returning = rng.integers(0, 2, size=num_visits)
    peak_time = rng.integers(0, 2, size=num_visits)
    premium_pay = rng.integers(0, 2, size=num_visits)
    deep_history = rng.uniform(0, 1, size=num_visits)
    # In-person / appearance signals (0 = group A, 1 = group B)
    colour_g = rng.integers(0, 2, size=num_visits)
    dress_g = rng.integers(0, 2, size=num_visits)
    speech_g = rng.integers(0, 2, size=num_visits)
    posture_g = rng.integers(0, 2, size=num_visits)
    face_g = rng.integers(0, 2, size=num_visits)
    noise = rng.normal(0, noise_std, size=num_visits)
    prices = (base_price
              + device_bias * device
              + location_bias * location
              + loyalty_bias * returning
              + time_bias * peak_time
              + payment_bias * premium_pay
              + history_bias * deep_history
              + colour_bias * colour_g
              + dress_bias * dress_g
              + speech_bias * speech_g
              + posture_bias * posture_g
              + face_bias * face_g
              + noise)
    prices = np.maximum(prices, 1.0)
    return {
        'prices': prices, 'device': device, 'location': location, 'returning': returning,
        'peak_time': peak_time, 'premium_pay': premium_pay, 'deep_history': deep_history,
        'colour_g': colour_g, 'dress_g': dress_g, 'speech_g': speech_g,
        'posture_g': posture_g, 'face_g': face_g
    }


def group_stats(prices, mask_a, mask_b):
    a, b = prices[mask_a], prices[mask_b]
    ma, mb = np.mean(a), np.mean(b)
    sa = np.std(a, ddof=1)/np.sqrt(len(a)) if len(a) > 1 else 0
    sb = np.std(b, ddof=1)/np.sqrt(len(b)) if len(b) > 1 else 0
    z = (ma - mb) / np.sqrt(sa**2 + sb**2) if (sa**2 + sb**2) > 0 else 0
    return {'mean_a': ma, 'mean_b': mb, 'diff': ma-mb, 'z': z, 'significant': abs(z) > 1.96, 'n_a': len(a), 'n_b': len(b)}


def run_multivariate_audit(prices, trait_matrix, trait_labels, alpha=0.05):
    """
    Single OLS regression of price on ALL traits simultaneously (each trait coded 0/1 or
    continuous), instead of testing each trait in isolation. This controls for the other
    traits when estimating each coefficient, and applies a Bonferroni correction for
    running multiple hypothesis tests at once (dividing alpha by the number of traits),
    which is the standard fix for multiple-comparisons inflation of false positives.
    """
    n = len(prices)
    k = trait_matrix.shape[1]
    X = np.column_stack([np.ones(n), trait_matrix])
    y = np.asarray(prices, dtype=float)
    # OLS via least squares
    beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    dof = max(1, n - X.shape[1])
    sigma2 = float(resid @ resid) / dof
    XtX_inv = np.linalg.pinv(X.T @ X)
    se = np.sqrt(np.clip(np.diag(XtX_inv) * sigma2, 0, None))
    t_stats = beta / np.where(se == 0, np.nan, se)
    # Normal approximation for p-values (n is typically large in these simulated audits)
    from math import erf, sqrt
    p_values = [2 * (1 - 0.5 * (1 + erf(abs(t) / sqrt(2)))) if not np.isnan(t) else 1.0 for t in t_stats]
    alpha_bonf = alpha / k  # Bonferroni-corrected significance threshold
    z_crit = 1.959963985  # ~95% two-sided normal critical value, used for CIs
    results = []
    for i, label in enumerate(trait_labels):
        idx = i + 1  # skip intercept
        results.append({
            "label": label, "coef": beta[idx], "se": se[idx],
            "ci_low": beta[idx] - z_crit * se[idx], "ci_high": beta[idx] + z_crit * se[idx],
            "p_value": p_values[idx],
            "significant_uncorrected": p_values[idx] < alpha,
            "significant_bonferroni": p_values[idx] < alpha_bonf,
        })
    return {"intercept": beta[0], "results": results, "alpha_bonferroni": alpha_bonf, "n": n, "k": k}


# Elasticity / demand calibration presets drawn from published empirical estimates.
# These are illustrative single-point calibrations, not full replications of the studies.
CALIBRATION_PRESETS = {
    "Retail gasoline (US/EU)": {
        "elasticity": -0.3, "note": "Short-run gasoline demand is widely estimated as quite inelastic (around -0.2 to -0.4); drivers can't easily change how much they drive in the short run.",
        "source": "Consistent with the retail-gasoline literature reviewed alongside Assad, Clark, Ershov & Xu (2024, Journal of Political Economy), who study algorithmic pricing adoption in Germany's gasoline market."
    },
    "Airline fares": {
        "elasticity": -1.2, "note": "Air travel demand is close to unit-elastic to elastic, especially for leisure travelers who can delay or substitute trips.",
        "source": "Broadly consistent with airline-demand elasticity ranges reported in industrial-organization textbooks and DOT/GAO fare studies."
    },
    "E-commerce / general retail": {
        "elasticity": -1.8, "note": "Online shopping typically shows more elastic demand because comparison-shopping and substitutes are just a click away.",
        "source": "Consistent with the general finding that online markets show higher price-comparison sensitivity than offline retail."
    },
    "Rental housing (local market)": {
        "elasticity": -0.5, "note": "Housing demand is fairly inelastic in the short run because moving is costly and slow, which is part of why algorithmic rent-setting tools drew antitrust scrutiny.",
        "source": "Context: DOJ v. RealPage (filed Aug. 23, 2024; settled Nov. 24, 2025) alleged that shared, non-public pricing data let landlords coordinate rent increases via a common algorithm."
    },
}


def narrate_discrimination(stats_list, labels, num_visits):
    text = f"<b>Audit of {num_visits:,} simulated shoppers</b> for the same product.<br><br>"
    any_sig = False
    for lab, stt in zip(labels, stats_list):
        sig = stt['significant']
        any_sig = any_sig or sig
        text += (f"• <b>{lab}</b>: ${stt['mean_a']:.2f} vs ${stt['mean_b']:.2f} "
                 f"(diff ${abs(stt['diff']):.2f}) → " + ("<b>significant</b>." if sig else "not clear.") + "<br>")
    text += "<br>"
    if any_sig:
        text += ("<b>Conclusion:</b> At least one trait shows a price gap too large to dismiss as noise. "
                 "That is the signal a real investigator would dig into further.")
    else:
        text += ("<b>Conclusion:</b> Under the current bias settings, no trait produced a gap large enough to "
                 "confidently call discrimination. Try stronger biases or more visits.")
    return text


# ---- Module 03 dual sim with richer factors ----
def run_firm_under_rules(num_agents, episodes, latency, audit_prob, audit_fine, max_jump, ban_punish,
                         price_ceiling, firm_strategy_bias, cost_shock, demand_shift, tax_rate,
                         interest_burden, wage_pressure, entry_threat):
    # Effective cost shock absorbs tax, interest, wage
    total_cost_shock = cost_shock + tax_rate * 0.4 + interest_burden * 0.25 + wage_pressure * 0.3
    # Entry threat slightly increases effective competition
    effective_agents = min(6, num_agents + (1 if entry_threat > 0.5 else 0))
    smoothed, final_price, p_nash, p_mono, hist, prof, final_profit = execute_simulation(
        effective_agents, episodes, latency, audit_prob, audit_fine,
        max_price_jump=max_jump if max_jump > 0 else None,
        ban_punishment=ban_punish,
        cost_shock=total_cost_shock,
        demand_shift=demand_shift
    )
    if price_ceiling and price_ceiling > 0:
        hist = np.minimum(hist, price_ceiling)
        final_price = min(final_price, price_ceiling)
    final_price *= (1.0 - 0.07 * firm_strategy_bias)
    final_profit *= (1.0 + 0.10 * firm_strategy_bias - 0.15 * entry_threat)
    avg_profit_path = np.mean(prof, axis=1)
    w = min(200, len(avg_profit_path))
    smoothed_profit = np.convolve(avg_profit_path, np.ones(w)/w, mode='valid')
    collusion_score = min(100.0, max(0.0, (final_price - p_nash) / max(p_mono - p_nash, 0.01) * 100))
    return {
        "smoothed_prices": smoothed, "final_price": final_price, "p_nash": p_nash, "p_mono": p_mono,
        "smoothed_firm_profit": smoothed_profit, "final_firm_profit": final_profit,
        "collusion_score": collusion_score, "num_agents": effective_agents
    }


def run_individual_from_firm(firm_final_price, firm_collusion_score,
                             income, wealth, confidence, price_sensitivity, necessity_share,
                             unemployment_risk, debt_burden, outside_option, inflation_expectation,
                             dress_signal=0.0, speech_signal=0.0, posture_signal=0.0,
                             face_confidence=0.5, colour_bias=0.0, periods=40):
    """Individual outcomes. Appearance/speech/posture/colour bias raise the effective price faced (discrimination drag)."""
    rng = np.random.default_rng(21)
    fair_ref = 5.0
    # Discrimination markup: positive bias / "lower status" signals → higher price faced
    disc_markup = (0.35 * colour_bias + 0.20 * max(0, 0.5 - dress_signal)
                   + 0.15 * max(0, 0.5 - speech_signal) + 0.15 * max(0, 0.5 - posture_signal)
                   + 0.15 * max(0, 0.5 - face_confidence))
    market_price = firm_final_price * (1.0 + 0.04 * inflation_expectation) * (1.0 + 0.25 * disc_markup)
    income_f = 0.45 + 0.009 * income
    wealth_f = 0.35 + 0.007 * wealth
    conf_f = 0.45 + 0.006 * confidence
    unemp_drag = 1.0 - 0.25 * unemployment_risk
    debt_drag = 1.0 - 0.20 * debt_burden
    outside_boost = 0.85 + 0.30 * outside_option
    purchasing_power = income_f * wealth_f * conf_f * unemp_drag * debt_drag * outside_boost
    base_qty = 12.0 * purchasing_power
    qty = max(0.15, base_qty - price_sensitivity * (market_price - fair_ref))
    choke = fair_ref + base_qty / max(price_sensitivity, 0.1)
    individual_cs = max(0.0, 0.5 * (choke - market_price) * qty)
    expenditure = market_price * qty
    residual = max(0.0, income - expenditure * (0.25 + 0.45 * necessity_share) - debt_burden * 15)
    welfare = (0.35 * min(100, individual_cs * 8) + 0.30 * min(100, residual) +
               0.20 * confidence + 0.15 * (100 * outside_option))
    welfare = max(5.0, welfare - firm_collusion_score * 0.22 - unemployment_risk * 12
                  - inflation_expectation * 8 - disc_markup * 18)
    price_path, qty_path, cs_path, welfare_path = [], [], [], []
    for _ in range(periods):
        p_t = max(1.0, market_price + rng.normal(0, 0.35) * 0.3)
        q_t = max(0.1, qty + rng.normal(0, 0.12))
        cs_t = max(0.0, 0.5 * (choke - p_t) * q_t)
        w_t = max(5.0, welfare + rng.normal(0, 1.4) - (p_t - fair_ref) * 0.7)
        price_path.append(p_t); qty_path.append(q_t); cs_path.append(cs_t); welfare_path.append(w_t)
    return {
        "market_price_faced": market_price, "qty": qty, "individual_cs": individual_cs,
        "expenditure": expenditure, "residual_income": residual, "welfare": welfare,
        "disc_markup_pct": disc_markup * 25,
        "price_path": np.array(price_path), "qty_path": np.array(qty_path),
        "cs_path": np.array(cs_path), "welfare_path": np.array(welfare_path)
    }



REGIME_PRESETS = {
    "Laissez-faire": dict(latency=0, audit_prob=0.0, audit_fine=0, max_jump=0.0, ban_punish=False, ceiling=0.0,
                          enforcement_cost=0),
    "Moderate oversight": dict(latency=2, audit_prob=0.15, audit_fine=40, max_jump=2.0, ban_punish=False, ceiling=0.0,
                               enforcement_cost=35),
    "Strict regulation": dict(latency=3, audit_prob=0.35, audit_fine=80, max_jump=1.0, ban_punish=True, ceiling=8.0,
                              enforcement_cost=80),
}


def run_regime_comparison(n_agents, episodes, cost_shock, demand_shift, tax_rate, interest_burden,
                          wage_pressure, entry_threat, firm_bias,
                          c_income, c_wealth, c_conf, c_sens, c_necessity, c_unemp, c_debt, c_outside, c_infl):
    """
    Runs the same market/individual under three preset regulatory regimes so they can be
    compared side by side, including a simple enforcement-cost figure so 'stronger rules'
    isn't treated as automatically free.
    """
    rows = []
    for name, r in REGIME_PRESETS.items():
        firm = run_firm_under_rules(
            n_agents, episodes, r["latency"], r["audit_prob"], r["audit_fine"], r["max_jump"], r["ban_punish"],
            r["ceiling"] if r["ceiling"] > 0 else None, firm_bias, cost_shock, demand_shift,
            tax_rate, interest_burden, wage_pressure, entry_threat
        )
        ind = run_individual_from_firm(
            firm["final_price"], firm["collusion_score"],
            c_income, c_wealth, c_conf, c_sens, c_necessity, c_unemp, c_debt, c_outside, c_infl
        )
        welfare_gain_per_cost = (ind["welfare"] / r["enforcement_cost"]) if r["enforcement_cost"] > 0 else float("inf")
        rows.append({
            "regime": name, "market_price": firm["final_price"], "collusion_score": firm["collusion_score"],
            "firm_profit": firm["final_firm_profit"], "welfare": ind["welfare"],
            "residual_income": ind["residual_income"], "enforcement_cost": r["enforcement_cost"],
            "welfare_per_cost": welfare_gain_per_cost
        })
    return rows


def narrate_dual(firm, ind, income, confidence):
    return (f"<b>Two linked simulations — results</b><br><br>"
            f"<b>1. Government → Firm</b><br>"
            f"Under your rules the market settled at <b>${firm['final_price']:.2f}</b>. "
            f"Collusion score = <b>{firm['collusion_score']:.0f}/100</b>. "
            f"Average firm profit = <b>${firm['final_firm_profit']:.2f}</b>.<br><br>"
            f"<b>2. Firm → Individual</b><br>"
            f"The individual faces that price (<b>${ind['market_price_faced']:.2f}</b>), buys about "
            f"<b>{ind['qty']:.1f}</b> units, spends <b>${ind['expenditure']:.1f}</b>, keeps residual income "
            f"index <b>{ind['residual_income']:.0f}</b>, earns consumer surplus <b>{ind['individual_cs']:.1f}</b>, "
            f"and reaches welfare index <b>{ind['welfare']:.0f}/100</b>.<br><br>"
            f"<b>Why this chain matters</b><br>"
            f"A rule that looks good on paper only helps people if it actually changes firm behaviour, and firm "
            f"behaviour only helps people if the resulting price and market conditions improve the individual’s "
            f"quantity, surplus and residual income. When income ({income}) or confidence ({confidence}) is already "
            f"low, the same high market price hurts welfare much more.")


# ===================== MAIN UI =====================
def main():
    NAV = [("Collusion Risk Lab", "Collusion Risk Lab"),
           ("Price Discrimination Auditor", "Price Discrimination Auditor"),
           ("Regulatory Design Lab", "Regulatory Design Lab"),
           ("Policy Comparison", "Policy Comparison"),
           ("Empirical Calibration", "Empirical Calibration"),
           ("Research Notes", "Research Notes"),
           ("How to Read Graphs", "How to Read Graphs"),
           ("Project Overview", "Project Overview")]
    if "page" not in st.session_state:
        st.session_state.page = NAV[0][0]
    for key, label in NAV:
        if st.sidebar.button(label, key=f"nav_{key}", use_container_width=True,
                             type="primary" if st.session_state.page == key else "secondary"):
            st.session_state.page = key
            st.rerun()
    page = st.session_state.page
    st.sidebar.markdown("---")

    # ---------- MODULE 01 ----------
    if page == "Collusion Risk Lab":
        st.markdown('<span class="exp-tag">Module 01</span>', unsafe_allow_html=True)
        st.markdown("""
            <div class="hero-card">
                <div class="hero-title">Collusion Risk Lab</div>
                <div class="hero-sub">AI pricing bots compete with no ability to communicate. This lab shows when they still learn to raise prices together (tacit collusion) and which simple policy tools can break that pattern.</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class="explainer">
                <h4>What you are testing</h4>
                <p>In a normal competitive market, if one seller cuts its price, it steals customers and the others are forced to respond. Prices stay close to cost. When every seller uses a learning algorithm, something different can happen: each algorithm discovers that cutting price is immediately punished by the others, so eventually none of them cut price and the market settles at a high level — without any human ever agreeing to collude.</p>
                <p>This module lets you run that experiment yourself. You choose how many bots compete, how long they train, and whether to add two realistic policy tools:</p>
                <ul>
                    <li><b>Price observation delay</b> — bots only see rivals’ prices with a lag, so punishment is slower and undercutting becomes more attractive again.</li>
                    <li><b>Random audits with fines</b> — there is a chance each round that a high price is detected and fined, which makes collusive pricing directly costly.</li>
                </ul>
                <p>Run the experiment, read the price paths, and see whether the bots end up colluding or competing.</p>
            </div>
        """, unsafe_allow_html=True)

        st.sidebar.header("Market Setup")
        n = st.sidebar.slider("Number of AI Pricing Bots", 2, 4, 2)
        st.sidebar.markdown('<div class="ctrl-help">More bots make silent coordination harder, so collusion is less reliable.</div>', unsafe_allow_html=True)
        eps = st.sidebar.slider("Simulation Rounds", 5000, 25000, 12000, step=2500)
        st.sidebar.markdown('<div class="ctrl-help">More rounds = more practice time for the bots. Patterns become clearer with longer training.</div>', unsafe_allow_html=True)
        st.sidebar.header("Policy Tools")
        lat = st.sidebar.slider("Price Observation Delay (rounds)", 0, 5, 0)
        st.sidebar.markdown('<div class="ctrl-help">0 = bots see rivals instantly. Higher = they see old prices, so punishment is slower.</div>', unsafe_allow_html=True)
        aud = st.sidebar.slider("Random Audit Probability", 0.0, 0.4, 0.0, step=0.05)
        st.sidebar.markdown('<div class="ctrl-help">Chance each round that a high price is fined. Raises the cost of collusion.</div>', unsafe_allow_html=True)

        if st.sidebar.button("Run Collusion Experiment", type="primary", use_container_width=True):
            with st.spinner("Training pricing bots..."):
                sm, fp, pn, pm, _, _, _ = execute_simulation(n, eps, lat, aud)
            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(f'<div class="metric-card"><div class="metric-label">Fair Price</div><div class="metric-value" style="color:{T["muted"]};">$1.00</div></div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="metric-card"><div class="metric-label">Cartel Price</div><div class="metric-value" style="color:{T["red"]};">$25.50</div></div>', unsafe_allow_html=True)
            c3.markdown(f'<div class="metric-card"><div class="metric-label">Final Price</div><div class="metric-value">${fp:.2f}</div></div>', unsafe_allow_html=True)
            col = T["red"] if fp >= 6 else T["green"]
            c4.markdown(f'<div class="metric-card"><div class="metric-label">Verdict</div><div class="metric-value" style="color:{col};">{"Colluding" if fp >= 6 else "Competitive"}</div></div>', unsafe_allow_html=True)
            st.markdown('<div class="read-box"><span class="tldr">How to read</span>Each coloured line is one bot’s price over time. Grey dashed line = fair competitive price. Red dashed line = full cartel price. If the coloured lines climb and flatten near the red line, the bots learned to collude.</div>', unsafe_allow_html=True)
            fig = go.Figure()
            for i in range(n):
                fig.add_trace(go.Scatter(x=list(range(len(sm))), y=sm[:, i], mode='lines', name=f'Bot {i+1}',
                                         line=dict(color=T['series'][i % 5], width=2.4)))
            fig.add_trace(go.Scatter(x=[0, len(sm)], y=[pn, pn], mode='lines', name='Fair Price', line=dict(color=T['muted'], width=2, dash='dash')))
            fig.add_trace(go.Scatter(x=[0, len(sm)], y=[pm, pm], mode='lines', name='Cartel Price', line=dict(color=T['red'], width=2, dash='dash')))
            fig.update_layout(title="<b>Do the bots learn to collude?</b>", xaxis_title="Round", yaxis_title="Price ($)",
                              template=T['plot_template'], paper_bgcolor=T['plot_paper'], plot_bgcolor=T['plot_area'],
                              font=dict(color=T['plot_font']), height=440, yaxis=dict(range=[0, 28], gridcolor=T['plot_grid']),
                              xaxis=dict(gridcolor=T['plot_grid']), legend=dict(orientation="h", y=1.08))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f'<div class="result-box {"warn" if fp >= 6 else ""}">{narrate_collusion(sm, fp, pn, pm, n, lat, aud)}</div>', unsafe_allow_html=True)

            st.markdown("### Welfare cost: deadweight loss")
            st.markdown(f'<div class="read-box"><span class="tldr">How to read</span>The shaded triangle is the deadweight loss — value that neither the firms nor consumers get, because trades that would have happened at the competitive price no longer happen at the higher price. It is the classic microeconomic cost of market power.</div>', unsafe_allow_html=True)
            dwl_fig, dwl = deadweight_loss_figure(fp, pn, base_demand=100.0, price_sensitivity=2.0,
                                                  marginal_cost=1.0, theme=T,
                                                  title="Deadweight loss from the collusive price")
            st.plotly_chart(dwl_fig, use_container_width=True)
            d1, d2, d3 = st.columns(3)
            d1.markdown(f'<div class="metric-card"><div class="metric-label">Deadweight Loss</div><div class="metric-value">${dwl["dwl"]:.1f}</div></div>', unsafe_allow_html=True)
            d2.markdown(f'<div class="metric-card"><div class="metric-label">Consumer Surplus Lost</div><div class="metric-value">${max(0.0, dwl["cs_comp"]-dwl["cs_now"]):.1f}</div></div>', unsafe_allow_html=True)
            d3.markdown(f'<div class="metric-card"><div class="metric-label">Producer Surplus Gained</div><div class="metric-value">${max(0.0, dwl["ps_now"]-dwl["ps_comp"]):.1f}</div></div>', unsafe_allow_html=True)

    # ---------- MODULE 02 ----------
    elif page == "Price Discrimination Auditor":
        st.markdown('<span class="exp-tag pink">Module 02</span>', unsafe_allow_html=True)
        st.markdown("""
            <div class="hero-card pink">
                <div class="hero-title">Price Discrimination Auditor</div>
                <div class="hero-sub">Online stores can quote different prices to different shoppers for the exact same product. You set the hidden biases; the lab runs a statistical audit to see whether those biases can be detected.</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class="explainer pink">
                <h4>What you are testing</h4>
                <p>Same product, different quoted prices — based on online signals <b>and</b> in-person signals (colour, dress, speech, posture, facial confidence). You set the hidden biases; the audit checks which ones are statistically detectable.</p>
            </div>
        """, unsafe_allow_html=True)

        st.sidebar.header("Base price")
        base = st.sidebar.slider("Base product price ($)", 20, 200, 100)

        st.sidebar.header("Online signals")
        st.sidebar.caption("Positive = charge that group more")
        dev_b = st.sidebar.slider("Device — Mobile extra ($)", -25, 25, 6)
        loc_b = st.sidebar.slider("Location per tier ($)", -20, 20, 5)
        loy_b = st.sidebar.slider("Returning visitor ($)", -20, 20, -4)
        time_b = st.sidebar.slider("Peak hours ($)", -15, 15, 3)
        pay_b = st.sidebar.slider("Premium card ($)", -15, 15, 4)
        hist_b = st.sidebar.slider("Deep browsing ($)", -20, 20, 5)

        st.sidebar.header("In-person / appearance signals")
        st.sidebar.caption("Positive = charge the marked group more")
        col_b = st.sidebar.slider("Colour / protected-trait bias ($)", -25, 25, 8)
        dress_b = st.sidebar.slider("Dress bias ($)", -20, 20, 5)
        speech_b = st.sidebar.slider("Speech bias ($)", -20, 20, 4)
        post_b = st.sidebar.slider("Posture bias ($)", -15, 15, 3)
        face_b = st.sidebar.slider("Facial confidence bias ($)", -15, 15, 4)

        st.sidebar.header("Audit settings")
        noise = st.sidebar.slider("Random noise ($)", 0, 15, 4)
        visits = st.sidebar.slider("Simulated visits", 400, 6000, 2500, step=100)

        if st.sidebar.button("Run Price Audit", type="primary", use_container_width=True):
            with st.spinner("Running audit..."):
                data = simulate_price_audit(
                    base, dev_b, loc_b, loy_b, time_b, pay_b, hist_b,
                    col_b, dress_b, speech_b, post_b, face_b, noise, visits
                )
                pr = data['prices']
                pairs_meta = [
                    ("Desktop vs Mobile", data['device']==0, data['device']==1),
                    ("Loc 1 vs 3", data['location']==0, data['location']==2),
                    ("New vs Returning", data['returning']==0, data['returning']==1),
                    ("Off-peak vs Peak", data['peak_time']==0, data['peak_time']==1),
                    ("Basic vs Premium pay", data['premium_pay']==0, data['premium_pay']==1),
                    ("Low vs High browse", data['deep_history']<0.5, data['deep_history']>=0.5),
                    ("Colour group A vs B", data['colour_g']==0, data['colour_g']==1),
                    ("Dress A vs B", data['dress_g']==0, data['dress_g']==1),
                    ("Speech A vs B", data['speech_g']==0, data['speech_g']==1),
                    ("Posture A vs B", data['posture_g']==0, data['posture_g']==1),
                    ("Face conf. A vs B", data['face_g']==0, data['face_g']==1),
                ]
                stats, labels_short = [], []
                for lab, ma, mb in pairs_meta:
                    stats.append(group_stats(pr, ma, mb))
                    labels_short.append(lab)

            cols = st.columns(3)
            for i, (lab, stt) in enumerate(zip(labels_short, stats)):
                cols[i % 3].markdown(
                    f'<div class="metric-card"><div class="metric-label">{lab}</div>'
                    f'<div class="metric-value" style="font-size:0.95rem;">${stt["mean_a"]:.2f} vs ${stt["mean_b"]:.2f}</div></div>',
                    unsafe_allow_html=True)

            st.markdown('<div class="read-box pink"><span class="tldr">How to read</span>Each pair = two groups differing in one trait only. Non-overlapping error bars ≈ real difference, not noise.</div>', unsafe_allow_html=True)

            fig = go.Figure()
            cats, means, sems, colors = [], [], [], []
            for lab, stt, (_, ma, mb) in zip(labels_short, stats, pairs_meta):
                cats.extend([lab.split(' vs ')[0][:10], lab.split(' vs ')[-1][:10]])
                means.extend([stt['mean_a'], stt['mean_b']])
                sems.extend([
                    np.std(pr[ma], ddof=1)/np.sqrt(stt['n_a']) if stt['n_a']>1 else 0,
                    np.std(pr[mb], ddof=1)/np.sqrt(stt['n_b']) if stt['n_b']>1 else 0
                ])
                colors.extend([T['bar_pair'][0], T['bar_pair'][1]])
            fig.add_trace(go.Bar(x=cats, y=means, marker_color=colors, error_y=dict(type='data', array=sems, visible=True)))
            fig.update_layout(title="<b>Average quoted price by trait</b>", yaxis_title="Price ($)",
                              template=T['plot_template'], paper_bgcolor=T['plot_paper'], plot_bgcolor=T['plot_area'],
                              font=dict(color=T['plot_font']), height=460, yaxis=dict(gridcolor=T['plot_grid']))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f'<div class="result-box info">{narrate_discrimination(stats, labels_short, visits)}</div>', unsafe_allow_html=True)

            st.markdown("### Multivariate audit (controls for all traits at once)")
            st.markdown("""
                <div class="read-box pink"><span class="tldr">Why this matters</span>
                The chart above tests each trait one at a time. That has a known statistical problem: testing 11 traits
                separately, each at the standard 95% confidence level, means a roughly 1-in-3 chance that <i>something</i>
                looks "significant" purely by chance, even with no real bias. A single regression that includes every
                trait at once controls for the others when estimating each effect, and a Bonferroni correction tightens
                the significance bar to account for testing 11 things simultaneously.</div>
            """, unsafe_allow_html=True)
            trait_matrix = np.column_stack([
                data['device'].astype(float), data['location'].astype(float), data['returning'].astype(float),
                data['peak_time'].astype(float), data['premium_pay'].astype(float), data['deep_history'],
                data['colour_g'].astype(float), data['dress_g'].astype(float), data['speech_g'].astype(float),
                data['posture_g'].astype(float), data['face_g'].astype(float)
            ])
            reg = run_multivariate_audit(pr, trait_matrix, labels_short)
            reg_fig = go.Figure()
            reg_fig.add_trace(go.Bar(
                x=[r["coef"] for r in reg["results"]], y=[r["label"] for r in reg["results"]], orientation="h",
                error_x=dict(type="data", symmetric=False,
                             array=[r["ci_high"] - r["coef"] for r in reg["results"]],
                             arrayminus=[r["coef"] - r["ci_low"] for r in reg["results"]]),
                marker_color=[T['red'] if r["significant_bonferroni"] else (T['amber'] if r["significant_uncorrected"] else T['muted']) for r in reg["results"]]
            ))
            reg_fig.add_vline(x=0, line_dash="dash", line_color=T['muted'])
            reg_fig.update_layout(title="Regression coefficient by trait (controls for all other traits)",
                                  xaxis_title="Effect on price ($), holding other traits fixed",
                                  template=T['plot_template'], paper_bgcolor=T['plot_paper'], plot_bgcolor=T['plot_area'],
                                  font=dict(color=T['plot_font']), height=440,
                                  xaxis=dict(gridcolor=T['plot_grid']), yaxis=dict(gridcolor=T['plot_grid']))
            st.plotly_chart(reg_fig, use_container_width=True)
            n_bonf = sum(1 for r in reg["results"] if r["significant_bonferroni"])
            n_unc = sum(1 for r in reg["results"] if r["significant_uncorrected"])
            st.markdown(f"""
                <div class="result-box info">
                <b>Regression results (n = {reg['n']:,} shoppers)</b><br><br>
                <b>{n_unc} of {reg['k']}</b> traits are significant at the uncorrected 95% level.<br>
                <b>{n_bonf} of {reg['k']}</b> traits survive the stricter Bonferroni-corrected threshold
                (α = {reg['alpha_bonferroni']:.4f} per trait) — these are the ones a cautious investigator
                would treat as real evidence of price discrimination rather than noise.<br><br>
                Red bars = Bonferroni-significant · Amber bars = significant only before correction · Grey bars = not significant.
                </div>
            """, unsafe_allow_html=True)

    # ---------- MODULE 03 ----------
    elif page == "Regulatory Design Lab":
        st.markdown('<span class="exp-tag green">Module 03</span>', unsafe_allow_html=True)
        st.markdown("""
            <div class="hero-card green">
                <div class="hero-title">Regulatory Design Lab</div>
                <div class="hero-sub">Two linked simulations: government rules change the firm → the firm’s price changes the individual.</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class="explainer green">
                <h4>How it works</h4>
                <p><b>Sim 1:</b> You set rules and market conditions. Firms adapt. You get market price, collusion score, firm profit.</p>
                <p><b>Sim 2:</b> That market price hits one consumer. You set their profile (income, confidence, appearance signals, etc.). You get quantity, surplus, and welfare.</p>
                <p>A rule only helps people if it actually lowers the price they face or the discrimination they meet.</p>
            </div>
        """, unsafe_allow_html=True)

        # --- Government / macro-micro rules ---
        st.sidebar.header("1. Competition policy rules")
        n_agents = st.sidebar.slider("Number of firms", 2, 5, 3)
        st.sidebar.markdown('<div class="ctrl-help">How many rivals the market starts with.</div>', unsafe_allow_html=True)
        episodes = st.sidebar.slider("Simulation rounds", 6000, 18000, 10000, step=2000)
        latency = st.sidebar.slider("Price observation delay (rounds)", 0, 6, 0)
        st.sidebar.markdown('<div class="ctrl-help">Lag before firms see rivals’ prices. Higher lag weakens collusion.</div>', unsafe_allow_html=True)
        audit_prob = st.sidebar.slider("Random audit probability", 0.0, 0.5, 0.0, 0.05)
        audit_fine = st.sidebar.slider("Fine when audited ($)", 10, 120, 40, 5)
        max_jump = st.sidebar.slider("Max price increase per period ($)", 0.0, 8.0, 0.0, 0.5)
        st.sidebar.markdown('<div class="ctrl-help">Caps how fast prices can climb. 0 = no cap.</div>', unsafe_allow_html=True)
        ban_punish = st.sidebar.checkbox("Ban aggressive punishment strategies", False)
        st.sidebar.markdown('<div class="ctrl-help">Makes it harder for firms to enforce a high-price equilibrium.</div>', unsafe_allow_html=True)
        ceiling = st.sidebar.slider("Hard price ceiling ($)", 0.0, 25.0, 0.0, 0.5)
        st.sidebar.markdown('<div class="ctrl-help">0 = no ceiling. Positive value = legal maximum price.</div>', unsafe_allow_html=True)

        st.sidebar.header("2. Cost & demand conditions (firm environment)")
        cost_shock = st.sidebar.slider("Supply / cost shock ($)", -5.0, 12.0, 0.0, 0.5)
        st.sidebar.markdown('<div class="ctrl-help">Positive = costs rise (e.g. energy, materials). Negative = costs fall.</div>', unsafe_allow_html=True)
        demand_shift = st.sidebar.slider("Demand shift", -25.0, 25.0, 0.0, 2.0)
        st.sidebar.markdown('<div class="ctrl-help">Positive = stronger demand. Negative = weaker demand.</div>', unsafe_allow_html=True)
        tax_rate = st.sidebar.slider("Per-unit tax / regulatory cost index", 0.0, 10.0, 0.0, 0.5)
        st.sidebar.markdown('<div class="ctrl-help">Raises effective marginal cost for every firm.</div>', unsafe_allow_html=True)
        interest_burden = st.sidebar.slider("Interest / cost-of-capital burden", 0.0, 10.0, 0.0, 0.5)
        st.sidebar.markdown('<div class="ctrl-help">Higher rates raise the cost of holding inventory and financing.</div>', unsafe_allow_html=True)
        wage_pressure = st.sidebar.slider("Wage / labour-cost pressure", 0.0, 10.0, 0.0, 0.5)
        st.sidebar.markdown('<div class="ctrl-help">Higher wages raise unit costs.</div>', unsafe_allow_html=True)
        entry_threat = st.sidebar.slider("Threat of new entry (0–1)", 0.0, 1.0, 0.2, 0.05)
        st.sidebar.markdown('<div class="ctrl-help">Higher threat disciplines prices and compresses profits.</div>', unsafe_allow_html=True)

        st.sidebar.header("3. Firm response")
        firm_bias = st.sidebar.slider("Firm strategy bias (−1 aggressive … +1 soft)", -1.0, 1.0, 0.0, 0.1)
        st.sidebar.markdown('<div class="ctrl-help">Aggressive = more undercutting. Soft = more willingness to keep prices high.</div>', unsafe_allow_html=True)

        st.sidebar.header("4. Individual profile (survey-style)")
        c_income = st.sidebar.slider("Income index", 20, 150, 100)
        st.sidebar.markdown('<div class="ctrl-help">Higher income raises purchasing power and residual income.</div>', unsafe_allow_html=True)
        c_wealth = st.sidebar.slider("Wealth index", 20, 150, 90)
        st.sidebar.markdown('<div class="ctrl-help">Buffer that supports spending even when income is tight.</div>', unsafe_allow_html=True)
        c_conf = st.sidebar.slider("Consumer confidence", 10, 100, 65)
        st.sidebar.markdown('<div class="ctrl-help">Willingness to spend; low confidence reduces quantity demanded.</div>', unsafe_allow_html=True)
        c_sens = st.sidebar.slider("Price sensitivity (elasticity proxy)", 0.3, 3.0, 1.2, 0.1)
        st.sidebar.markdown('<div class="ctrl-help">How strongly the individual cuts quantity when price rises.</div>', unsafe_allow_html=True)
        c_necessity = st.sidebar.slider("Necessity share of this good", 0.1, 0.9, 0.4, 0.05)
        st.sidebar.markdown('<div class="ctrl-help">Higher = the good takes a larger bite out of residual income.</div>', unsafe_allow_html=True)
        c_unemp = st.sidebar.slider("Unemployment / income-risk index", 0.0, 1.0, 0.15, 0.05)
        st.sidebar.markdown('<div class="ctrl-help">Job-loss risk reduces purchasing power and welfare.</div>', unsafe_allow_html=True)
        c_debt = st.sidebar.slider("Debt burden index", 0.0, 1.0, 0.2, 0.05)
        st.sidebar.markdown('<div class="ctrl-help">Debt service reduces residual income and welfare.</div>', unsafe_allow_html=True)
        c_outside = st.sidebar.slider("Outside options / substitutes (0–1)", 0.0, 1.0, 0.5, 0.05)
        st.sidebar.markdown('<div class="ctrl-help">Better alternatives improve welfare even at the same price.</div>', unsafe_allow_html=True)
        c_infl = st.sidebar.slider("Inflation expectation drag", 0.0, 1.0, 0.1, 0.05)

        if st.sidebar.button("Run Both Simulations", type="primary", use_container_width=True):
            with st.spinner("Running both simulations..."):
                firm = run_firm_under_rules(
                    n_agents, episodes, latency, audit_prob, audit_fine, max_jump, ban_punish,
                    ceiling if ceiling > 0 else None, firm_bias, cost_shock, demand_shift,
                    tax_rate, interest_burden, wage_pressure, entry_threat
                )
                ind = run_individual_from_firm(
                    firm["final_price"], firm["collusion_score"],
                    c_income, c_wealth, c_conf, c_sens, c_necessity,
                    c_unemp, c_debt, c_outside, c_infl
                )

            st.markdown("### Sim 1 — Rules → Firm")
            m1, m2, m3, m4 = st.columns(4)
            m1.markdown(f'<div class="metric-card"><div class="metric-label">Market Price</div><div class="metric-value">${firm["final_price"]:.2f}</div></div>', unsafe_allow_html=True)
            m2.markdown(f'<div class="metric-card"><div class="metric-label">Collusion Score</div><div class="metric-value">{firm["collusion_score"]:.0f}/100</div></div>', unsafe_allow_html=True)
            m3.markdown(f'<div class="metric-card"><div class="metric-label">Avg Firm Profit</div><div class="metric-value">${firm["final_firm_profit"]:.2f}</div></div>', unsafe_allow_html=True)
            m4.markdown(f'<div class="metric-card"><div class="metric-label">Fair Benchmark</div><div class="metric-value">${firm["p_nash"]:.2f}</div></div>', unsafe_allow_html=True)

            # Two clean separate charts (fixes overlapping title/legend)
            col_a, col_b = st.columns(2)
            with col_a:
                fig_p = go.Figure()
                xp = list(range(len(firm["smoothed_prices"])))
                for i in range(firm["num_agents"]):
                    fig_p.add_trace(go.Scatter(x=xp, y=firm["smoothed_prices"][:, i], mode="lines",
                                               name=f"Firm {i+1}", line=dict(color=T['series'][i % 5], width=2.2)))
                fig_p.add_trace(go.Scatter(x=[0, len(xp)], y=[firm["p_nash"], firm["p_nash"]], mode="lines",
                                           name="Fair", line=dict(color=T['muted'], width=2, dash="dash")))
                fig_p.add_trace(go.Scatter(x=[0, len(xp)], y=[firm["p_mono"], firm["p_mono"]], mode="lines",
                                           name="Cartel", line=dict(color=T['red'], width=2, dash="dash")))
                fig_p.update_layout(title="Firm prices under your rules", xaxis_title="Round", yaxis_title="Price ($)",
                                    template=T['plot_template'], paper_bgcolor=T['plot_paper'], plot_bgcolor=T['plot_area'],
                                    font=dict(color=T['plot_font']), height=380, legend=dict(orientation="h", y=1.12),
                                    margin=dict(t=60), yaxis=dict(gridcolor=T['plot_grid']), xaxis=dict(gridcolor=T['plot_grid']))
                st.plotly_chart(fig_p, use_container_width=True)
            with col_b:
                fig_f = go.Figure()
                xf = list(range(len(firm["smoothed_firm_profit"])))
                fig_f.add_trace(go.Scatter(x=xf, y=firm["smoothed_firm_profit"], mode="lines",
                                           name="Avg firm profit", line=dict(color=T['series'][4], width=2.5)))
                fig_f.update_layout(title="Average firm profit", xaxis_title="Round", yaxis_title="Profit",
                                    template=T['plot_template'], paper_bgcolor=T['plot_paper'], plot_bgcolor=T['plot_area'],
                                    font=dict(color=T['plot_font']), height=380, showlegend=False,
                                    margin=dict(t=60), yaxis=dict(gridcolor=T['plot_grid']), xaxis=dict(gridcolor=T['plot_grid']))
                st.plotly_chart(fig_f, use_container_width=True)

            st.markdown("### Welfare cost of your rules: deadweight loss")
            dwl_fig3, dwl3 = deadweight_loss_figure(
                firm["final_price"], firm["p_nash"], base_demand=100.0 + demand_shift,
                price_sensitivity=2.0, marginal_cost=1.0 + cost_shock, theme=T,
                title="Deadweight loss under your chosen rules"
            )
            st.plotly_chart(dwl_fig3, use_container_width=True)
            st.markdown(f'<div class="read-box green"><span class="tldr">How to read</span>Compare this triangle across different rule settings: a good regulation should shrink this shaded area (less deadweight loss) without shrinking legitimate output too much.</div>', unsafe_allow_html=True)

            st.markdown("### Sim 2 — Firm → Individual")
            n1, n2, n3, n4, n5 = st.columns(5)
            n1.markdown(f'<div class="metric-card"><div class="metric-label">Price Faced</div><div class="metric-value">${ind["market_price_faced"]:.2f}</div></div>', unsafe_allow_html=True)
            n2.markdown(f'<div class="metric-card"><div class="metric-label">Qty Bought</div><div class="metric-value">{ind["qty"]:.1f}</div></div>', unsafe_allow_html=True)
            n3.markdown(f'<div class="metric-card"><div class="metric-label">Surplus</div><div class="metric-value">{ind["individual_cs"]:.1f}</div></div>', unsafe_allow_html=True)
            n4.markdown(f'<div class="metric-card"><div class="metric-label">Residual Income</div><div class="metric-value">{ind["residual_income"]:.0f}</div></div>', unsafe_allow_html=True)
            n5.markdown(f'<div class="metric-card"><div class="metric-label">Welfare</div><div class="metric-value">{ind["welfare"]:.0f}/100</div></div>', unsafe_allow_html=True)

            fig2 = make_subplots(rows=2, cols=2,
                                 subplot_titles=("Price faced", "Quantity bought", "Consumer surplus", "Welfare index"),
                                 vertical_spacing=0.14, horizontal_spacing=0.08)
            x = list(range(1, len(ind["price_path"])+1))
            fig2.add_trace(go.Scatter(x=x, y=ind["price_path"], mode="lines", line=dict(color=T['series'][0], width=2.3)), row=1, col=1)
            fig2.add_trace(go.Scatter(x=x, y=ind["qty_path"], mode="lines", line=dict(color=T['series'][1], width=2.3)), row=1, col=2)
            fig2.add_trace(go.Scatter(x=x, y=ind["cs_path"], mode="lines", line=dict(color=T['green'], width=2.3)), row=2, col=1)
            fig2.add_trace(go.Scatter(x=x, y=ind["welfare_path"], mode="lines", line=dict(color=T['purple'], width=2.3)), row=2, col=2)
            fig2.update_layout(height=480, template=T['plot_template'], paper_bgcolor=T['plot_paper'],
                               plot_bgcolor=T['plot_area'], font=dict(color=T['plot_font']), showlegend=False, margin=dict(t=40))
            fig2.update_xaxes(gridcolor=T['plot_grid']); fig2.update_yaxes(gridcolor=T['plot_grid'])
            st.plotly_chart(fig2, use_container_width=True)

            st.markdown(f'<div class="result-box info">{narrate_dual(firm, ind, c_income, c_conf)}</div>', unsafe_allow_html=True)
            st.markdown("""
                <div class="guide-box-green">
                    <h4>Quick use</h4>
                    <p>1. Change rules only → Sim 1 moves (firm price / profit).</p>
                    <p>2. Change individual profile or discrimination signals → Sim 2 moves (surplus / welfare).</p>
                    <p>3. Same market price hurts more when income is low, debt is high, or discrimination signals are disadvantaged.</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Set rules + individual profile in the sidebar, then press **Run Both Simulations**.")

    # ---------- POLICY COMPARISON ----------
    elif page == "Policy Comparison":
        st.markdown('<span class="exp-tag green">Module 04</span>', unsafe_allow_html=True)
        st.markdown("""
            <div class="hero-card green">
                <div class="hero-title">Policy Comparison</div>
                <div class="hero-sub">Regulation is not free. This page runs the same market under three preset regulatory regimes side by side, and weighs the welfare gained against a simple enforcement-cost figure — the trade-off a real regulator has to make.</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class="explainer green">
                <h4>The three regimes</h4>
                <p><b>Laissez-faire</b> — no audits, no price cap, no delay. Cheapest to run, weakest at stopping collusion.</p>
                <p><b>Moderate oversight</b> — some audits, a small price-jump cap, a short observation delay.</p>
                <p><b>Strict regulation</b> — frequent audits, a hard price ceiling, a ban on punishment strategies. Best at lowering prices, most expensive to enforce.</p>
            </div>
        """, unsafe_allow_html=True)

        st.sidebar.header("Market conditions")
        pc_agents = st.sidebar.slider("Number of firms", 2, 5, 3, key="pc_agents")
        pc_episodes = st.sidebar.slider("Simulation rounds", 6000, 16000, 9000, step=1000, key="pc_episodes")
        pc_cost = st.sidebar.slider("Supply / cost shock ($)", -5.0, 12.0, 0.0, 0.5, key="pc_cost")
        pc_demand = st.sidebar.slider("Demand shift", -25.0, 25.0, 0.0, 2.0, key="pc_demand")
        st.sidebar.header("Individual profile")
        pc_income = st.sidebar.slider("Income index", 20, 150, 100, key="pc_income")
        pc_conf = st.sidebar.slider("Consumer confidence", 10, 100, 65, key="pc_conf")

        if st.sidebar.button("Compare Regimes", type="primary", use_container_width=True):
            with st.spinner("Running all three regimes..."):
                rows = run_regime_comparison(
                    pc_agents, pc_episodes, pc_cost, pc_demand, 0.0, 0.0, 0.0, 0.2, 0.0,
                    pc_income, 90, pc_conf, 1.2, 0.4, 0.15, 0.2, 0.5, 0.1
                )
            import pandas as pd
            table_rows = [{
                "Regime": r["regime"],
                "Market Price ($)": f'{r["market_price"]:.2f}',
                "Collusion Score": f'{r["collusion_score"]:.0f}',
                "Firm Profit ($)": f'{r["firm_profit"]:.2f}',
                "Consumer Welfare": f'{r["welfare"]:.0f}',
                "Residual Income": f'{r["residual_income"]:.0f}',
                "Enforcement Cost ($)": f'{r["enforcement_cost"]:.0f}',
                "Welfare per $ of Enforcement": ("∞" if r["welfare_per_cost"] == float("inf") else f'{r["welfare_per_cost"]:.2f}')
            } for r in rows]
            st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)

            fig_cmp = go.Figure()
            fig_cmp.add_trace(go.Bar(x=[r["regime"] for r in rows], y=[r["welfare"] for r in rows],
                                     name="Consumer welfare", marker_color=T['blue']))
            fig_cmp.add_trace(go.Bar(x=[r["regime"] for r in rows], y=[r["enforcement_cost"] for r in rows],
                                     name="Enforcement cost", marker_color=T['red']))
            fig_cmp.update_layout(barmode="group", title="Welfare gained vs. enforcement cost, by regime",
                                  template=T['plot_template'], paper_bgcolor=T['plot_paper'], plot_bgcolor=T['plot_area'],
                                  font=dict(color=T['plot_font']), height=420, legend=dict(orientation="h", y=1.1),
                                  xaxis=dict(gridcolor=T['plot_grid']), yaxis=dict(gridcolor=T['plot_grid']))
            st.plotly_chart(fig_cmp, use_container_width=True)

            best = max(rows, key=lambda r: r["welfare_per_cost"] if r["welfare_per_cost"] != float("inf") else -1)
            st.markdown(f"""
                <div class="result-box">
                <b>Reading this comparison</b><br><br>
                Strict regulation delivers the highest consumer welfare here, but it is also the most expensive to run.
                Ranked by welfare delivered per dollar of enforcement cost, <b>{best['regime']}</b> comes out ahead in this
                setting. This is exactly the kind of trade-off real competition regulators weigh: a rule that helps
                consumers a little more but costs the agency far more to enforce is not automatically the right call.
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Set market conditions in the sidebar, then press **Compare Regimes**.")

    # ---------- EMPIRICAL CALIBRATION ----------
    elif page == "Empirical Calibration":
        st.markdown('<span class="exp-tag">Module 05</span>', unsafe_allow_html=True)
        st.markdown("""
            <div class="hero-card">
                <div class="hero-title">Empirical Calibration</div>
                <div class="hero-sub">Every number elsewhere in this lab (demand slope, price sensitivity, elasticity) is currently a chosen constant. This page shows how those constants relate to published, real-world demand-elasticity estimates, so the simulation isn't floating free of the empirical literature.</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class="explainer">
                <h4>What "price elasticity of demand" means here</h4>
                <p>Elasticity measures how much quantity demanded falls, in percentage terms, for a 1% rise in price.
                An elasticity of <b>-0.3</b> means demand is <b>inelastic</b> — quantity barely moves. An elasticity of
                <b>-1.8</b> means demand is <b>elastic</b> — a small price increase causes a much bigger drop in quantity.
                The simulation's <code>price_sensitivity</code> parameter is a linear-demand stand-in for this same idea.</p>
            </div>
        """, unsafe_allow_html=True)

        market_choice = st.selectbox("Pick a market type to calibrate against", list(CALIBRATION_PRESETS.keys()))
        preset = CALIBRATION_PRESETS[market_choice]
        st.markdown(f"""
            <div class="guide-box">
                <h4>{market_choice} — elasticity ≈ {preset['elasticity']}</h4>
                <p>{preset['note']}</p>
                <p style="font-size:0.85rem; color:{T['muted']};"><b>Source context:</b> {preset['source']}</p>
            </div>
        """, unsafe_allow_html=True)

        # Show what this elasticity implies for a simple linear demand curve at a reference price/quantity
        ref_p, ref_q = 5.0, 60.0
        implied_slope = abs(preset['elasticity']) * ref_q / ref_p
        cal_fig = go.Figure()
        p_range = np.linspace(0.5, ref_p * 2.2, 60)
        q_range = np.maximum(0.0, ref_q + implied_slope * (ref_p - p_range))
        cal_fig.add_trace(go.Scatter(x=q_range, y=p_range, mode="lines", name=f"Calibrated demand ({market_choice})",
                                     line=dict(color=T['blue'], width=2.5)))
        cal_fig.add_trace(go.Scatter(x=[ref_q], y=[ref_p], mode="markers+text", text=["Reference point"],
                                     textposition="top right", marker=dict(color=T['red'], size=10)))
        cal_fig.update_layout(title=f"Implied demand curve at elasticity {preset['elasticity']}",
                              xaxis_title="Quantity", yaxis_title="Price ($)",
                              template=T['plot_template'], paper_bgcolor=T['plot_paper'], plot_bgcolor=T['plot_area'],
                              font=dict(color=T['plot_font']), height=400,
                              xaxis=dict(gridcolor=T['plot_grid']), yaxis=dict(gridcolor=T['plot_grid']))
        st.plotly_chart(cal_fig, use_container_width=True)
        st.markdown(f"""
            <div class="result-box info">
            At a reference price of ${ref_p:.2f} and quantity {ref_q:.0f}, an elasticity of {preset['elasticity']}
            implies a demand slope (<code>price_sensitivity</code>) of about <b>{implied_slope:.2f}</b> units per dollar —
            you could plug this into the Collusion Risk Lab or Regulatory Design Lab's cost/demand sliders to run those
            modules under a more realistic, literature-grounded demand curve for this market type.
            </div>
        """, unsafe_allow_html=True)

    # ---------- RESEARCH NOTES ----------
    elif page == "Research Notes":
        st.markdown('<span class="exp-tag pink">Write-up</span>', unsafe_allow_html=True)
        st.markdown("""
            <div class="hero-card pink">
                <div class="hero-title">Research Notes</div>
                <div class="hero-sub">The economic reasoning behind the lab, in writing: what the literature says, what this simulation deliberately simplifies, and what a regulator might take away from it.</div>
            </div>
        """, unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["Literature review", "Methodology & limitations", "Policy memo"])

        with tab1:
            st.markdown("""
                <div class="explainer">
                <h4>Algorithmic collusion (Module 01)</h4>
                <p>The collusion engine here is directly inspired by Calvano, Calzolari, Denicolò & Pastorello (2020,
                <i>American Economic Review</i>), who show that independent Q-learning pricing algorithms in a repeated
                oligopoly consistently learn to charge prices above the competitive level, sustained by punishment-and-return
                strategies, without ever communicating. That result is theoretical/experimental. The empirical companion
                evidence comes from Assad, Clark, Ershov & Xu (2024, <i>Journal of Political Economy</i>), who studied the
                rollout of algorithmic pricing software across German gas stations starting in 2017 and found that margins
                rose substantially in markets where multiple competing stations adopted the same kind of software, but not
                in markets with only one adopter or a local monopoly — evidence that it's the interaction between algorithms,
                not just their existence, that matters.</p>
                </div>
                <div class="explainer pink">
                <h4>Algorithmic price discrimination (Module 02)</h4>
                <p>Charging different prices to different shoppers for identical goods based on inferred characteristics has
                been discussed as a competition-policy concern by antitrust authorities and legal scholars (e.g. Ezrachi &
                Stucke's writing on "virtual competition"). The statistical approach this lab uses — comparing group means and
                then moving to a controlled multivariate regression with a multiple-testing correction — mirrors how an
                actual disparate-impact or pricing audit would be structured.</p>
                </div>
                <div class="explainer green">
                <h4>Regulation of algorithmic pricing (Modules 03–04)</h4>
                <p>This is not a hypothetical concern. In August 2024 the U.S. Department of Justice and eight state attorneys
                general sued the real-estate software company RealPage, alleging that its algorithmic pricing tool let
                competing landlords coordinate rent increases using shared, non-public pricing data — a case that settled in
                November 2025 with restrictions on what data RealPage can use, without a finding of liability. The case is a
                real-world example of exactly the policy question Module 03 and 04 simulate: what rules actually change firm
                behaviour, and at what enforcement cost.</p>
                </div>
            """, unsafe_allow_html=True)

        with tab2:
            st.markdown("""
                <div class="explainer">
                <h4>What this simulation captures well</h4>
                <ul>
                    <li>The qualitative finding that independent learning algorithms can sustain supra-competitive prices without communication.</li>
                    <li>The basic logic of price discrimination detection: comparing prices across groups while holding other observable traits fixed.</li>
                    <li>The chain of causation from a policy lever, to firm pricing behaviour, to an individual consumer's welfare.</li>
                    <li>Standard partial-equilibrium welfare accounting (consumer surplus, producer surplus, deadweight loss) for a linear demand curve.</li>
                </ul>
                <h4>What it deliberately simplifies</h4>
                <ul>
                    <li>Firms are tabular Q-learning agents on a small price grid, not real firms with rich strategy spaces, multi-product lines, or actual algorithmic pricing software.</li>
                    <li>Demand is linear and single-good; no cross-price effects, no product differentiation, no dynamic consumer learning.</li>
                    <li>The individual-welfare model (Module 03) uses illustrative functional forms and index numbers (e.g. a 0–100 "welfare index") rather than a dollar-denominated, empirically-estimated utility function.</li>
                    <li>Calibration constants in the Empirical Calibration page are single-point stand-ins for whole demand systems estimated with real transaction data — useful for intuition, not a replication of any specific paper's estimates.</li>
                    <li>The regulatory "enforcement cost" figures in Policy Comparison are illustrative relative weights, not real agency budget data.</li>
                </ul>
                <h4>Why these simplifications are reasonable for this project</h4>
                <p>The goal is to make the <i>mechanisms</i> — tacit collusion, statistical detection of discrimination, and
                policy-to-outcome transmission — visible and explorable, not to forecast real prices. Every published paper
                in this space (including Calvano et al. 2020 itself) also relies on a simplified, stylized market for the same
                reason: it isolates the mechanism from confounding real-world noise.</p>
                </div>
            """, unsafe_allow_html=True)

        with tab3:
            st.markdown("""
                <div class="explainer green">
                <h4>Memo: what this lab implies for regulators</h4>
                <p><b>To:</b> A hypothetical competition-policy office<br>
                <b>Re:</b> Lessons from the AlgoMarket Decision Lab simulations</p>
                <p><b>1. Tacit algorithmic collusion is a real, mechanistic risk, not just a theoretical one.</b>
                Module 01 shows independent pricing algorithms reliably settling on high prices without communication.
                This matches both the experimental literature (Calvano et al. 2020) and empirical evidence from
                real markets (Assad et al. 2024 on German gasoline).</p>
                <p><b>2. Simple, well-chosen rules can meaningfully lower prices — but they are not free.</b>
                Module 03/04 show that observation delays, audits, and price-jump caps reduce collusion, and that
                stricter regimes deliver more consumer welfare but cost more to enforce. Regulators should compare
                welfare gained per dollar of enforcement, not just look for the strongest possible rule.</p>
                <p><b>3. Detecting price discrimination requires controlling for confounding traits, not just comparing group averages.</b>
                Module 02's multivariate regression with a Bonferroni correction shows that testing many traits
                independently overstates how much discrimination is actually present — a caution that applies directly
                to real algorithmic-pricing audits, including the kind referenced in DOJ v. RealPage.</p>
                <p><b>4. Recommendation.</b> Any rule (transparency mandate, audit regime, price cap) should be evaluated
                on both dimensions this lab tracks: does it move firm prices toward the competitive benchmark, and does
                it survive a defensible statistical test — not just a raw comparison of averages.</p>
                </div>
            """, unsafe_allow_html=True)

    # ---------- HOW TO READ GRAPHS ----------
    elif page == "How to Read Graphs":
        st.markdown("""
            <div class="hero-card">
                <div class="hero-title">How to Read the Graphs</div>
                <div class="hero-sub">What each chart is showing and what to look for.</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("### Module 01 — Collusion Risk Lab")
        st.markdown("""
            <div class="guide-box">
                <h4>Price paths chart</h4>
                <p><b>Coloured lines</b> = each AI firm’s price over time.<br>
                <b>Grey dashed line</b> = fair competitive price (near cost).<br>
                <b>Red dashed line</b> = full cartel / monopoly price.</p>
                <p><b>What to look for:</b> If the coloured lines rise and flatten near the red line → collusion. If they stay near the grey line → competition.</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("### Module 02 — Price Discrimination Auditor")
        st.markdown("""
            <div class="guide-box-pink">
                <h4>Bar chart by trait</h4>
                <p>Each pair of bars = two groups that differ in <b>one</b> trait only (e.g. Desktop vs Mobile, Dress A vs B).</p>
                <p><b>Black error bars</b> = margin of error. If the error bars do <b>not</b> overlap, the price gap is unlikely to be pure chance → evidence of discrimination on that trait.</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("### Module 03 — Regulatory Design Lab")
        st.markdown("""
            <div class="guide-box-green">
                <h4>Sim 1 — Firm charts</h4>
                <p><b>Left:</b> firm price paths under your rules (same reading as Module 01: grey = fair, red = cartel).<br>
                <b>Right:</b> average firm profit over time. Strong rules usually pull prices down and compress profit.</p>
            </div>
            <div class="guide-box-green">
                <h4>Sim 2 — Individual charts</h4>
                <p>Four small paths for one person after the firm’s price is set:</p>
                <p>• <b>Price faced</b> — what they actually pay<br>
                • <b>Quantity bought</b> — how much they buy<br>
                • <b>Consumer surplus</b> — value they keep above the price<br>
                • <b>Welfare index</b> — overall outcome (higher is better)</p>
                <p><b>What to look for:</b> Lower firm prices in Sim 1 should show up as higher surplus and welfare in Sim 2.</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("### Deadweight loss triangle (Modules 01 & 03)")
        st.markdown("""
            <div class="guide-box">
                <h4>Demand-and-cost chart</h4>
                <p>The downward blue line is the demand curve; the dotted grey line is marginal cost. The two dots mark
                the current price and the competitive price. The shaded triangle is the <b>deadweight loss</b> — value
                lost to society because some mutually beneficial trades no longer happen at the higher price.</p>
                <p><b>What to look for:</b> A bigger triangle means a bigger welfare cost from market power. Policy tools
                that shrink this triangle are helping, even if they don't fully eliminate collusion.</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("### Module 02 regression chart")
        st.markdown("""
            <div class="guide-box-pink">
                <h4>Horizontal bar chart with error bars</h4>
                <p>Each bar is one trait's estimated effect on price, <b>holding all other traits fixed</b>. The whiskers
                are a 95% confidence interval. <b>Red</b> = still significant after the stricter Bonferroni correction.
                <b>Amber</b> = significant only before correction (treat with caution). <b>Grey</b> = not significant.</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("### Module 04 — Policy Comparison chart")
        st.markdown("""
            <div class="guide-box-green">
                <h4>Grouped bar chart</h4>
                <p>Blue bars = consumer welfare delivered by each regime. Red bars = the enforcement cost of running that
                regime. A regime is only clearly "better" if its welfare gain justifies its cost — that's what the
                welfare-per-dollar column in the table captures directly.</p>
            </div>
        """, unsafe_allow_html=True)

    # ---------- OVERVIEW ----------
    elif page == "Project Overview":
        st.markdown('<div class="hero-card"><div class="hero-title">Project Overview</div><div class="hero-sub">What each module is for and the story the lab tells end-to-end.</div></div>', unsafe_allow_html=True)
        st.markdown("""
            <div class="overview-card">
                <h3>Module 01 — Collusion Risk Lab</h3>
                <div class="overview-block problem"><span class="tag">Problem</span>
                <p>AI pricing algorithms can learn to keep prices high without any explicit agreement (tacit collusion).</p></div>
                <div class="overview-block solution"><span class="tag">What we do</span>
                <p>Simulate Q-learning pricing bots, show when collusion appears, and test observation delays and random audits.</p></div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class="overview-card">
                <h3>Module 02 — Price Discrimination Auditor</h3>
                <div class="overview-block problem"><span class="tag">Problem</span>
                <p>Firms can charge different prices to different people for the same product based on device, location, loyalty, time, payment method or browsing behaviour.</p></div>
                <div class="overview-block solution"><span class="tag">What we do</span>
                <p>You set the hidden biases; the lab runs the statistical group tests a real investigator would use.</p></div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class="overview-card">
                <h3>Module 03 — Regulatory Design Lab</h3>
                <div class="overview-block problem"><span class="tag">Problem</span>
                <p>Once we know algorithms can harm consumers, what rules work — and how do those rules ultimately affect a real person?</p></div>
                <div class="overview-block solution"><span class="tag">What we do</span>
                <p><b>Two linked simulations.</b> (1) Government rules + cost/demand conditions → firm price, collusion risk and profit. (2) Those firm outcomes + a survey-style individual profile → quantity, surplus, residual income and welfare. The full chain from policy to firm to person is made visible.</p></div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class="overview-card">
                <h3>Module 04 — Policy Comparison</h3>
                <div class="overview-block problem"><span class="tag">Problem</span>
                <p>Regulation is usually evaluated for whether it works, rarely for whether it's worth what it costs to enforce.</p></div>
                <div class="overview-block solution"><span class="tag">What we do</span>
                <p>Run the same market under three preset regimes (laissez-faire, moderate, strict) and rank them by consumer welfare delivered per dollar of enforcement cost, not just by which one produces the lowest price.</p></div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class="overview-card">
                <h3>Module 05 — Empirical Calibration</h3>
                <div class="overview-block problem"><span class="tag">Problem</span>
                <p>Every demand parameter elsewhere in the lab is an assumed constant, disconnected from real markets.</p></div>
                <div class="overview-block solution"><span class="tag">What we do</span>
                <p>Show how the lab's demand-slope parameter maps onto published price-elasticity estimates for four real market types (gasoline, airfare, e-commerce, rental housing), with citations.</p></div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class="overview-card">
                <h3>Research Notes</h3>
                <div class="overview-block problem"><span class="tag">Problem</span>
                <p>A simulation alone doesn't show economic reasoning — the writing around it does.</p></div>
                <div class="overview-block solution"><span class="tag">What we do</span>
                <p>A literature review connecting each module to real papers and cases (Calvano et al. 2020; Assad et al. 2024; DOJ v. RealPage), a methodology &amp; limitations page, and a one-page policy memo synthesizing the findings.</p></div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class="overview-card">
                <h3>Project design</h3>
                <p>Every parameter is under user control. No external data required. Focus: algorithmic markets and how rules transmit from policy → firm → individual, grounded in the deadweight-loss framework, controlled statistical inference, and the empirical/legal literature on algorithmic pricing.</p>
            </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
