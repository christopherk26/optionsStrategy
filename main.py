import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Option and stock strategy visualized",
    page_icon=" ",
    layout="wide",
    initial_sidebar_state="expanded")


# Custom CSS to inject into Streamlit
st.markdown("""
<style>
/* */
.metric-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 6px; /* Adjust the padding to control height */
    width: auto; /* Auto width for responsiveness, or set a fixed width if necessary */
    margin: 0 auto; /* Center the container */
}
</style>
""", unsafe_allow_html=True)

def buyCall (x, strike, contractCost): 
    if x < strike:
        return -contractCost
    else:
        return x - contractCost - strike

vBuyCall = np.vectorize(buyCall, otypes=[float])



def buyPut (x, strike, contractCost): 
    if x > strike:
        return -contractCost
    else:
        return -x - contractCost + strike


vBuyPut = np.vectorize(buyPut)




def sellCall (x, strike, contractCost): 
    if x < strike:
        return contractCost
    else:
        return -x + contractCost + strike


vSellCall = np.vectorize(sellCall, otypes=[float])



def sellPut (x, strike, contractCost): 
    if x > strike:
        return contractCost
    else:
        return x + contractCost - strike



vSellPut = np.vectorize(sellPut)



def buyShares (x): 
    return - sharePrice + x

vBuyShares = np.vectorize(buyShares, otypes=[float])

def shortShares (x): 
    return sharePrice - x

vShortShares = np.vectorize(shortShares, otypes=[float])

sharePrice = 100
numberOfShares = 1
numberOfShortShares = 0

strikeBuyCall = 110
contractCostBuyCall = 5
numberOfBuyCall = 0

strikeBuyPut = 110
contractCostBuyPut = 5
numberOfBuyPut = 0

strikeSellCall = 110
contractCostSellCall = 5
numberOfSellCall = 0

strikeSellPut = 110
contractCostSellPut = 5
numberOfSellPut = 0

with st.sidebar:
    st.title("Options and Share Parameters")
    st.write("Shares")
    sharePrice = st.number_input("Share Price", value=100.0, step=0.1)
    numberOfShares = st.number_input("Number Of Shares", value=1, step=1)
    numberOfShortShares = st.number_input("Number Of Short Shares", value=0, step=1)

    st.markdown("---")
    st.write("Bought Calls")
    strikeBuyCall = st.number_input("Strike Price Of Bought Call", value=110.0, step=0.1)
    contractCostBuyCall = st.number_input("Contract Cost Of Bought Call", value=5.0, step=0.1)
    numberOfBuyCall = st.number_input("Number Of Bought Call Contracts", value=0, step=1)

    st.markdown("---")
    st.write("Bought Puts")
    strikeBuyPut = st.number_input("Strike Price Of Bought Put", value=110.0, step=0.1)
    contractCostBuyPut = st.number_input("Contract Cost Of Bought Put", value=5.0, step=0.1)
    numberOfBuyPut = st.number_input("Number Of Bought Put Contracts", value=0, step=1)

    st.markdown("---")
    st.write("Sold Calls")
    strikeSellCall = st.number_input("Strike Price Of Sold Call", value=110.0, step=0.1)
    contractCostSellCall = st.number_input("Contract Cost Of Sold Call", value=5.0, step=0.1)
    numberOfSellCall = st.number_input("Number Of Sold Call Contracts", value=0, step=1)

    st.markdown("---")
    st.write("Sold Puts")
    strikeSellPut = st.number_input("Strike Price Of Sold Put", value=110.0, step=0.1)
    contractCostSellPut = st.number_input("Contract Cost Of Sold Put", value=5.0, step=0.1)
    numberOfSellPut = st.number_input("Number Of Sold Put Contracts", value=0, step=1)

    st.markdown("---")
    st.title("Graph Bounds")
    percentOff = st.number_input('Percent From Share Price', min_value=0.1, value=0.4, step=0.05)
    

x = np.linspace(sharePrice * (1 - percentOff), sharePrice * (1 + percentOff), num=int(500))
# number must be equal to the delta share price plotted plus one

y = vSellPut(x, strikeSellPut, contractCostSellPut) * numberOfSellPut + vSellCall(x, strikeSellCall, contractCostSellCall) * numberOfSellCall
y = y + (vBuyCall(x, strikeBuyCall, contractCostBuyCall) * numberOfBuyCall) + (vBuyPut(x, strikeBuyPut, contractCostBuyPut) * numberOfBuyPut)
y = y + (vBuyShares(x)) * numberOfShares + (vShortShares(x)) * numberOfShortShares

plt.style.use('dark_background')
horizontal = plt.axhline(y = 0, color = 'gray', linestyle = '-') 




plt.fill_between(x, y, where = (y >= 0), color = 'green', alpha = 0.3)

plt.fill_between(x, y, where = (y <= 0), color = 'red', alpha = 0.3)

plt.xlabel('Share Price')
plt.ylabel('Profit / Loss')
plt.title('Options and Stock Strategy Chart')
plt.plot(x, y, color = 'white', linestyle = '-')

st.title("Strategy for options and stocks:")
st.write("""See your strategy play out by adjusting the data on the left column.""")

st.markdown("")

col1, col2 = st.columns([1,1], gap="small")

with col1:
    st.pyplot(plt, use_container_width=True)
