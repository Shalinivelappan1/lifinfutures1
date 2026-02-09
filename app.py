import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

st.set_page_config(layout="wide")
st.title("Futures Trading & Hedging Lab")

# =====================================================
# HELPER FUNCTIONS
# =====================================================
def payoff_matrix(x, y, label="P&L"):
    df = pd.DataFrame({"Price": x, label: y})
    st.dataframe(df, use_container_width=True)

def hedge_matrix(moves, portfolio, futures, net):
    df = pd.DataFrame({
        "Market Move %": moves*100,
        "Portfolio": portfolio,
        "Futures": futures,
        "Net": net
    })
    st.dataframe(df, use_container_width=True)

# =====================================================
# SIDEBAR
# =====================================================
topic = st.sidebar.radio(
    "Select Module",
    [
        "1. Why Futures",
        "2. Futures Pricing",
        "3. MTM & Margin Calls",
        "4. Trading P&L",
        "5. Trading Strategy Builder",
        "6. Hedging Strategy Builder",
        "7. Optimal Hedge Ratio",
        "8. Basis & Convergence",
        "9. Basis Risk",
        "10. Rolling Futures",
        "11. Matching System",
        "12. Real-World Cases",
        "13. Advanced Strategies",
        "14. Quiz & Certificate"
    ]
)

# =====================================================
# 1 WHY FUTURES
# =====================================================
if topic == "1. Why Futures":
    st.header("Why Futures Exist")
    st.write("""
Hedgers transfer risk  
Speculators take risk  
Arbitrageurs enforce pricing  
""")

# =====================================================
# 2 PRICING
# =====================================================
elif topic == "2. Futures Pricing":
    st.header("Cost of Carry")
    st.latex("F = S(1+r-c)^T")

    S = st.slider("Spot",100,1000,500)
    r = st.slider("Interest %",0,15,8)/100
    c = st.slider("Dividend %",0,10,2)/100
    T = st.slider("Time",0.1,1.0,0.5)

    F = S*(1+r-c)**T
    st.metric("Futures Price", round(F,2))

# =====================================================
# 3 MTM + MARGIN CALL
# =====================================================
elif topic == "3. MTM & Margin Calls":

    st.header("MTM & Margin Call Simulator")

    entry = st.number_input("Entry price",22000)
    contracts = st.slider("Contracts",1,20,5)
    size = 50

    init_margin = st.number_input("Initial margin",150000)
    maint_margin = st.number_input("Maintenance margin",100000)

    prices = np.linspace(entry-2000, entry+2000, 8)

    balances = []
    status = []

    for p in prices:
        pnl = (p-entry)*contracts*size
        bal = init_margin + pnl
        balances.append(bal)

        if bal < maint_margin:
            status.append("MARGIN CALL")
        else:
            status.append("OK")

    fig, ax = plt.subplots()
    ax.plot(prices, balances)
    ax.axhline(maint_margin, linestyle="--")
    ax.set_title("Margin Balance")
    st.pyplot(fig)

    df = pd.DataFrame({
        "Price": prices,
        "Margin Balance": balances,
        "Status": status
    })
    st.dataframe(df)

# =====================================================
# 4 TRADING PNL
# =====================================================
elif topic == "4. Trading P&L":

    st.header("Long vs Short Payoff")

    entry = st.number_input("Entry",22000)
    contracts = st.slider("Contracts",1,20,5)
    size = 50

    prices = np.linspace(entry-2000, entry+2000, 8)
    long = (prices-entry)*contracts*size
    short = -long

    fig, ax = plt.subplots()
    ax.plot(prices,long,label="Long")
    ax.plot(prices,short,label="Short")
    ax.legend()
    st.pyplot(fig)

    payoff_matrix(prices,long)

# =====================================================
# 5 TRADING BUILDER
# =====================================================
elif topic == "5. Trading Strategy Builder":

    st.header("Directional Strategy Builder")

    entry = st.number_input("Entry price",22000)
    contracts = st.slider("Contracts",1,20,5)
    size = 50

    prices = np.linspace(entry-2000, entry+2000, 8)
    pnl = (prices-entry)*contracts*size

    fig, ax = plt.subplots()
    ax.plot(prices,pnl)
    ax.axhline(0)
    st.pyplot(fig)

    payoff_matrix(prices,pnl)

# =====================================================
# 6 HEDGING BUILDER
# =====================================================
elif topic == "6. Hedging Strategy Builder":

    st.header("Portfolio Hedge Simulator")

    V = st.number_input("Portfolio value",5_000_000)
    beta = st.slider("Beta",0.5,1.5,1.0)
    contracts = st.slider("Contracts",0,100,20)
    F = st.number_input("Futures price",22000)

    moves = np.linspace(-0.1,0.1,8)

    portfolio = V*beta*moves
    futures = -contracts*50*F*moves
    net = portfolio+futures

    fig, ax = plt.subplots()
    ax.plot(moves*100,portfolio,label="Portfolio")
    ax.plot(moves*100,net,label="Hedged")
    ax.legend()
    st.pyplot(fig)

    hedge_matrix(moves,portfolio,futures,net)

# =====================================================
# 7 OPTIMAL HEDGE
# =====================================================
elif topic == "7. Optimal Hedge Ratio":

    st.header("Optimal Hedge Ratio")

    V = st.number_input("Portfolio",5_000_000)
    beta = st.slider("Beta",0.5,1.5,1.0)
    F = st.number_input("Futures",22000)

    N = (beta*V)/(F*50)
    st.metric("Contracts", round(N,2))

# =====================================================
# 8 BASIS
# =====================================================
elif topic == "8. Basis & Convergence":

    st.header("Basis")

    spot = st.number_input("Spot",22000)
    futures = st.number_input("Futures",22100)

    basis = spot-futures
    st.metric("Basis",basis)

# =====================================================
# 9 BASIS RISK
# =====================================================
elif topic == "9. Basis Risk":

    st.header("Basis Risk")

    corr = st.slider("Correlation",0.0,1.0,0.8)
    st.metric("Hedge effectiveness",corr*100)

# =====================================================
# 10 ROLLING
# =====================================================
elif topic == "10. Rolling Futures":

    st.header("Roll Over")

    near = st.number_input("Near",22000)
    far = st.number_input("Next",22150)

    st.metric("Roll cost",far-near)

# =====================================================
# 11 MATCHING
# =====================================================
elif topic == "11. Matching System":

    st.header("Exchange Matching")

    buyers = st.slider("Buy orders",0,100,60)
    sellers = st.slider("Sell orders",0,100,50)

    st.metric("Trades executed",min(buyers,sellers))

# =====================================================
# 12 REAL WORLD CASES
# =====================================================
elif topic == "12. Real-World Cases":

    st.header("Equity Portfolio Hedge Case")

    V = 5_000_000
    F = 22000
    size = 50

    N = V/(F*size)
    st.metric("Contracts to short", round(N,1))

    moves = np.linspace(-0.1,0.1,8)
    portfolio = V*moves
    futures = -N*50*F*moves
    net = portfolio+futures

    hedge_matrix(moves,portfolio,futures,net)

# =====================================================
# 13 ADVANCED STRATEGIES
# =====================================================
elif topic == "13. Advanced Strategies":

    st.header("Advanced Strategies")

    strat = st.selectbox(
        "Strategy",
        [
            "Directional Trade",
            "Calendar Spread",
            "Cash-and-Carry Arbitrage",
            "Basis Trade",
            "Partial Hedge"
        ]
    )

    if strat == "Directional Trade":

        entry = st.number_input("Entry",22000)
        prices = np.linspace(entry-2000,entry+2000,8)
        pnl = prices-entry

        fig, ax = plt.subplots()
        ax.plot(prices,pnl)
        st.pyplot(fig)

        payoff_matrix(prices,pnl)
    # =====================================================
    # CALENDAR SPREAD
    # =====================================================
    elif strat == "Calendar Spread":

        near = st.number_input("Near contract",22000)
        far = st.number_input("Far contract",22200)

        spread = far-near
        st.metric("Spread",spread)

        prices = np.linspace(near-1000,near+1000,8)
        pnl = (far-near) - (prices-near)

        fig, ax = plt.subplots()
        ax.plot(prices,pnl)
        ax.axhline(0)
        st.pyplot(fig)

        payoff_matrix(prices,pnl,"Spread P&L")

    # =====================================================
    # CASH & CARRY
    # =====================================================
    elif strat == "Cash-and-Carry Arbitrage":

        spot = st.number_input("Spot",1000)
        futures = st.number_input("Futures",1050)
        r = st.slider("Interest %",0,15,8)/100

        fair = spot*(1+r)
        st.metric("Fair futures",round(fair,2))

        prices = np.linspace(spot-200,spot+200,8)
        pnl = futures-prices

        fig, ax = plt.subplots()
        ax.plot(prices,pnl)
        ax.axhline(0)
        st.pyplot(fig)

        payoff_matrix(prices,pnl,"Arbitrage P&L")

    # =====================================================
    # BASIS TRADE
    # =====================================================
    elif strat == "Basis Trade":

        spot = st.number_input("Spot",22000)
        futures = st.number_input("Futures",22100)

        basis = spot-futures
        st.metric("Basis",basis)

        prices = np.linspace(spot-1000,spot+1000,8)
        pnl = prices-futures

        fig, ax = plt.subplots()
        ax.plot(prices,pnl)
        ax.axhline(0)
        st.pyplot(fig)

        payoff_matrix(prices,pnl,"Basis Trade P&L")

    # =====================================================
    # PARTIAL HEDGE
    # =====================================================
    elif strat == "Partial Hedge":

        V = st.number_input("Portfolio",5_000_000)
        hedge_pct = st.slider("Hedge %",0,100,50)/100

        moves = np.linspace(-0.1,0.1,8)
        unhedged = V*moves
        hedged = unhedged*(1-hedge_pct)

        fig, ax = plt.subplots()
        ax.plot(moves*100,unhedged,label="Unhedged")
        ax.plot(moves*100,hedged,label="Hedged")
        ax.legend()
        st.pyplot(fig)

        df = pd.DataFrame({
            "Market Move %":moves*100,
            "Unhedged":unhedged,
            "Hedged":hedged
        })
        st.dataframe(df)

# =====================================================
# 14 QUIZ & CERTIFICATE
# =====================================================
elif topic == "14. Quiz & Certificate":

    st.header("Futures Lab Quiz")

    # ---------------- QUESTIONS ----------------
    q1 = st.radio("1. Market falls → who gains?",["Long","Short"])
    q2 = st.radio("2. Basis at expiry?",["Zero","Large"])
    q3 = st.number_input("3. Spot=100 r=10% → Futures?")
    q4 = st.number_input("4. Buy 200→210 size50 P&L?")
    q5 = st.number_input("5. Hedge contracts for ₹10L?")
    q6 = st.radio("6. MTM reduces?",["Credit risk","Return"])
    q7 = st.radio("7. Futures>spot?",["Contango","Backwardation"])
    q8 = st.radio("8. Best hedge correlation?",["High","Low"])
    q9 = st.radio("9. Rolling means?",["Close & reopen","Hold"])
    q10 = st.number_input("10. Short 500→520 size10 loss?")

    st.subheader("Student Details")
    student_name = st.text_input("Student Name")
    student_id = st.text_input("Student ID")

    # ---------------- SUBMIT ----------------
    if st.button("Submit Quiz"):

        score = 0
        if q1=="Short": score+=1
        if q2=="Zero": score+=1
        if abs(q3-110)<1: score+=1
        if abs(q4-500)<1: score+=1
        if abs(q5-1)<0.5: score+=1
        if q6=="Credit risk": score+=1
        if q7=="Contango": score+=1
        if q8=="High": score+=1
        if q9=="Close & reopen": score+=1
        if abs(q10-200)<1: score+=1

        st.success(f"Score: {score}/10")

        # ===============================
        # EXCEL DOWNLOAD
        # ===============================
        df = pd.DataFrame({
            "Student Name":[student_name]*10,
            "Student ID":[student_id]*10,
            "Question":[f"Q{i}" for i in range(1,11)],
            "Answer":[q1,q2,q3,q4,q5,q6,q7,q8,q9,q10]
        })

        excel_buffer = io.BytesIO()
        df.to_excel(excel_buffer,index=False)
        excel_buffer.seek(0)

        st.download_button(
            "📥 Download Excel Workings",
            excel_buffer,
            file_name=f"{student_id}_workings.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # ===============================
        # CERTIFICATE
        # ===============================
        if score >= 5 and student_name and student_id:

            buffer = io.BytesIO()
            c = canvas.Canvas(buffer,pagesize=letter)
            width,height = letter

            c.setStrokeColor(HexColor("#C9A227"))
            c.setLineWidth(4)
            c.rect(30,30,width-60,height-60)

            c.setFont("Helvetica-Bold",28)
            c.drawCentredString(width/2,height-140,
                                "Certificate of Completion")

            c.setFont("Helvetica",16)
            c.drawCentredString(width/2,height-180,
                                "Futures Trading & Hedging Lab")

            c.setFont("Helvetica-Bold",22)
            c.drawCentredString(width/2,height-240,student_name)

            c.drawCentredString(width/2,height-270,
                                f"Student ID: {student_id}")

            c.drawCentredString(width/2,height-300,
                                f"Score: {score}/10")

            today = datetime.today().strftime("%d %B %Y")
            c.drawCentredString(width/2,height-340,
                                f"Date: {today}")

            c.drawCentredString(width/2,height-380,
                                "Instructor: Prof. Shalini Velappan")

            c.save()
            buffer.seek(0)

            st.download_button(
                "📄 Download Certificate",
                buffer,
                file_name=f"{student_id}_certificate.pdf",
                mime="application/pdf"
            )
