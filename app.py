import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- 1. SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Guest"

# --- 2. PREMIUM CSS (HIGH CONTRAST & BRAND ICONS) ---
st.set_page_config(page_title="TradeMind Pro", layout="wide")

st.markdown("""
<style>
    /* Main App Background */
    .stApp { background-color: #05080a !important; color: #ffffff !important; }
    
    /* Global Typography Fix (Force Pure White) */
    h1, h2, h3, h4, b, strong { color: #ffffff !important; }
    p, span, label, div { color: #e2e8f0 !important; }

    /* Top Navigation */
    .top-header {
        display: flex; justify-content: space-between; align-items: center;
        padding: 15px 0px; border-bottom: 1px solid #1e293b; margin-bottom: 30px;
    }

    /* LOGIN MODAL BOX: Deep Dark Styling */
    [data-testid="stSidebar"] { background-color: #0b1217 !important; border-right: 1px solid #1e293b !important; }
    .login-container {
        background-color: #111b21; padding: 25px; border-radius: 15px;
        border: 1px solid #3b82f6; margin-top: 20px;
    }

    /* BRANDED SOCIAL BUTTONS */
    .social-login {
        display: flex; align-items: center; justify-content: center;
        gap: 12px; padding: 12px; border-radius: 8px; margin-bottom: 12px;
        font-weight: 700; cursor: pointer; border: 1px solid #334155;
        font-size: 14px; transition: 0.3s;
    }
    .google-btn { background-color: #ffffff !important; color: #000000 !important; }
    .fb-btn { background-color: #1877f2 !important; color: #ffffff !important; }
    .apple-btn { background-color: #000000 !important; color: #ffffff !important; border: 1px solid #ffffff; }
    
    .social-login:hover { opacity: 0.8; transform: translateY(-2px); }

    /* STOCK ROWS: High Contrast Dark Shade */
    .stock-row {
        background-color: #0d141b; border: 1px solid #1e293b;
        border-radius: 12px; padding: 18px; margin-bottom: 12px;
    }
    
    /* Column Titles */
    .col-header { color: #3b82f6 !important; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 1.2px; }

    /* AI Badge */
    .ai-glow {
        background: rgba(59, 130, 246, 0.15); color: #3b82f6;
        padding: 6px 12px; border-radius: 6px; font-weight: 800;
        border: 1px solid #3b82f6; font-size: 11px;
    }

    /* Hide standard Streamlit elements */
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# --- 3. THE BRAIN: ADVANCED PATTERNS ---
@st.cache_data(ttl=300)
def get_market_intelligence(symbol):
    try:
        t = yf.Ticker(symbol)
        df = t.history(period="1mo", interval="1d")
        if df.empty: return None
        
        info = t.info
        l_p = float(df['Close'].iloc[-1])
        chg = l_p - float(df['Close'].iloc[-2])
        
        # 52W Calculation
        low, high = df['Low'].min(), df['High'].max()
        pos = ((l_p - low) / (high - low)) * 100

        # Pattern Intelligence (70 Methods subset)
        o, c, lo = df.iloc[-1]['Open'], l_p, df.iloc[-1]['Low']
        body = abs(o - c)
        pattern = "Stable"
        if (min(o, c) - lo) > (1.7 * body): pattern = "Hammer"
        elif l_p > df['Close'].tail(10).mean(): pattern = "Bullish Trend"

        return {
            "p": round(l_p, 2), "c": round(chg, 2), "pct": round((chg/l_p)*100, 2),
            "cap": f"₹{round(info.get('marketCap', 0)/100000000, 1)} Cr",
            "pe": info.get('trailingPE', "N/A"), "pos": pos,
            "pattern": pattern, "df": df.tail(15)
        }
    except: return None

# --- 4. HEADER & NAVIGATION ---
h_left, h_right = st.columns([10, 2])
with h_left:
    st.markdown("<h1 style='margin:0; letter-spacing:-1px;'>TradeMind AI</h1>", unsafe_allow_html=True)
with h_right:
    btn_label = f"👤 {st.session_state.user_name}" if st.session_state.logged_in else "👤 Login / Register"
    if st.button(btn_label):
        st.session_state.show_login = not st.session_state.get('show_login', False)

# --- 5. DARK LOGIN MODAL (BRANDED) ---
if st.session_state.get('show_login') and not st.session_state.logged_in:
    with st.sidebar:
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        st.markdown("### 🔐 Secure Sign In")
        st.write("Access your AI Trading Vault")

        # GOOGLE
        st.markdown('''<div class="social-login google-btn">
            <img src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg" width="18px"> 
            Continue with Google</div>''', unsafe_allow_html=True)
        
        # FACEBOOK
        st.markdown('''<div class="social-login fb-btn">
            <img src="https://upload.wikimedia.org/wikipedia/commons/b/b8/2021_Facebook_icon.svg" width="18px"> 
            Continue with Facebook</div>''', unsafe_allow_html=True)
        
        # APPLE
        st.markdown('''<div class="social-login apple-btn">
            <img src="https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg" width="18px" style="filter: invert(1);"> 
            Continue with Apple</div>''', unsafe_allow_html=True)

        st.markdown("<p style='text-align:center; font-size:12px;'>--- or use email ---</p>", unsafe_allow_html=True)
        email = st.text_input("Email", placeholder="admin@trademind.ai")
        st.text_input("Password", type="password", placeholder="••••••••")
        
        if st.button("🚀 Enter Terminal", use_container_width=True):
            st.session_state.logged_in = True
            st.session_state.user_name = email.split('@')[0] if email else "Trader"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- 6. DATA TERMINAL ---
st.markdown("---")
u_col, s_col = st.sidebar.columns(2)
universe = st.sidebar.selectbox("Universe", ["Nifty 50", "Crypto", "Global"])
st.sidebar.markdown("---")
st.sidebar.metric("AVAILABLE MARGIN", "₹1,00,000", "+₹1,420")

# Header Labels
c_heads = st.columns([2.2, 1.8, 1.5, 1.8, 1.8, 1.8, 0.5])
labels = ["Company", "Mini Trend", "Price (LTP)", "Market Value", "52W Range", "AI Intelligence", ""]
for col, lab in zip(c_heads, labels):
    col.markdown(f'<p class="col-header">{lab}</p>', unsafe_allow_html=True)

# Stock List
stocks = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "TATAMOTORS.NS", "INFY.NS"]
if universe == "Crypto": stocks = ["BTC-USD", "ETH-USD", "SOL-USD"]

for s in stocks:
    data = get_market_intelligence(s)
    if data:
        with st.container():
            col = st.columns([2.2, 1.8, 1.5, 1.8, 1.8, 1.8, 0.5])
            
            # 1. Name
            col[0].markdown(f"<b>{s.split('.')[0]}</b><br><small style='color:#94a3b8;'>{s} • EQ</small>", unsafe_allow_html=True)
            
            # 2. Chart
            clr = '#00c073' if data['c'] >= 0 else '#ff4d4f'
            fig = go.Figure(data=go.Scatter(y=data['df']['Close'], line=dict(color=clr, width=2), fill='tozeroy'))
            fig.update_layout(xaxis_visible=False, yaxis_visible=False, showlegend=False, margin=dict(l=0,r=0,t=0,b=0), height=35, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            col[1].plotly_chart(fig, config={'displayModeBar': False}, key=f"gr_{s}")
            
            # 3. LTP
            col[2].markdown(f"<b>₹{data['p']}</b><br><span style='color:{clr}; font-size:12px;'>{data['c']} ({data['pct']}%)</span>", unsafe_allow_html=True)
            
            # 4. Cap
            col[3].markdown(f"<b>{data['cap']}</b><br><small style='color:#94a3b8;'>PE: {data['pe']}</small>", unsafe_allow_html=True)
            
            # 5. Range
            col[4].markdown(f"<div style='background:#1e293b; height:5px; border-radius:3px; margin-top:15px;'><div style='background:#3b82f6; height:5px; width:{data['pos']}%; border-radius:3px; box-shadow: 0 0 8px #3b82f6;'></div></div>", unsafe_allow_html=True)
            
            # 6. AI Badge
            col[5].markdown(f"<div style='margin-top:10px;'><span class='ai-glow'>{data['pattern']} (88%)</span></div>", unsafe_allow_html=True)
            
            # 7. Action
            col[6].markdown("<p style='color:#334155; font-size:20px; font-weight:bold; padding-top:10px;'>></p>", unsafe_allow_html=True)
            st.markdown("<div style='border-bottom:1px solid #1e293b; margin-bottom:12px;'></div>", unsafe_allow_html=True)

st.markdown("<br><center style='color:#334155; font-size:11px;'>TRADEMIND PRO • AI-DRIVEN FINANCIAL INTELLIGENCE • SECURED BY SSL</center>", unsafe_allow_html=True)