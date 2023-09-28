import os, sys
sys.path.insert(0, os.path.dirname(os.getcwd()))
import streamlit as st
import pandas as pd
import pandas_ta as ta
import plotly.express as px
from bcb import sgs
from streamlit.components.v1 import html
from datetime import datetime, timedelta


st.set_page_config(
    page_title="Markets Analysis",
    page_icon="📈",
    layout="wide",
)

us10y = """
<iframe src="https://tvc-invdn-com.investing.com/web/1.12.34/index60-prod.html?carrier=6df1bdd7805b9098ba8ad4a1d9a38b0e&amp;time=1695697170&amp;domain_ID=1&amp;lang_ID=1&amp;timezone_ID=8&amp;version=1.12.34&amp;locale=en&amp;timezone=America/New_York&amp;pair_ID=23705&amp;interval=D&amp;session=24x7&amp;prefix=www&amp;suffix=&amp;client=1&amp;user=203421857&amp;family_prefix=tvc4&amp;init_page=instrument&amp;sock_srv=https://streaming.forexpros.com&amp;m_pids=&amp;watchlist=&amp;geoc=BR&amp;site=https://www.investing.com" frameborder="0" scrolling="no" seamless="seamless" style="width: 100%; height:400px;" class="abs"></iframe>
"""
brent="""
<iframe src="https://tvc-invdn-com.investing.com/web/1.12.34/index60-prod.html?carrier=afe1ae15749c71cb53a6f548c202d228&amp;time=1695698198&amp;domain_ID=1&amp;lang_ID=1&amp;timezone_ID=8&amp;version=1.12.34&amp;locale=en&amp;timezone=America/New_York&amp;pair_ID=8833&amp;interval=D&amp;session=24x7&amp;prefix=www&amp;suffix=&amp;client=1&amp;user=203421857&amp;family_prefix=tvc4&amp;init_page=instrument&amp;sock_srv=https://streaming.forexpros.com&amp;m_pids=&amp;watchlist=&amp;geoc=BR&amp;site=https://www.investing.com" frameborder="0" scrolling="no" seamless="seamless" style="width: 100%; height:400px;" class="abs"></iframe>
"""
ibovfut="""
<iframe src="https://tvc-invdn-com.investing.com/web/1.12.34/index60-prod.html?carrier=cc6e38a779ed2416cc78ec17b6080804&amp;time=1695698354&amp;domain_ID=1&amp;lang_ID=1&amp;timezone_ID=8&amp;version=1.12.34&amp;locale=en&amp;timezone=America/New_York&amp;pair_ID=941612&amp;interval=D&amp;session=24x7&amp;prefix=www&amp;suffix=&amp;client=1&amp;user=203421857&amp;family_prefix=tvc4&amp;init_page=instrument&amp;sock_srv=https://streaming.forexpros.com&amp;m_pids=&amp;watchlist=&amp;geoc=BR&amp;site=https://www.investing.com" frameborder="0" scrolling="no" seamless="seamless" style="width: 100%; height:400px;" class="abs"></iframe>
"""
nasdaqfut="""
<iframe src="https://tvc-invdn-com.investing.com/web/1.12.34/index60-prod.html?carrier=3725f99e38394cce51a9e38b871392bc&amp;time=1695698571&amp;domain_ID=1&amp;lang_ID=1&amp;timezone_ID=8&amp;version=1.12.34&amp;locale=en&amp;timezone=America/New_York&amp;pair_ID=8874&amp;interval=D&amp;session=24x7&amp;prefix=www&amp;suffix=&amp;client=1&amp;user=203421857&amp;family_prefix=tvc4&amp;init_page=instrument&amp;sock_srv=https://streaming.forexpros.com&amp;m_pids=&amp;watchlist=&amp;geoc=BR&amp;site=https://www.investing.com" frameborder="0" scrolling="no" seamless="seamless" style="width: 100%; height:400px;" class="abs"></iframe>
"""
usdbrl="""
<iframe src="https://tvc-invdn-com.investing.com/web/1.12.34/index60-prod.html?carrier=8c606fc0811c049a3603e7bc4a49a011&amp;time=1695698706&amp;domain_ID=1&amp;lang_ID=1&amp;timezone_ID=8&amp;version=1.12.34&amp;locale=en&amp;timezone=America/New_York&amp;pair_ID=2103&amp;interval=D&amp;session=24x7&amp;prefix=www&amp;suffix=&amp;client=1&amp;user=203421857&amp;family_prefix=tvc4&amp;init_page=instrument&amp;sock_srv=https://streaming.forexpros.com&amp;m_pids=&amp;watchlist=&amp;geoc=BR&amp;site=https://www.investing.com" frameborder="0" scrolling="no" seamless="seamless" style="width: 100%; height:400px;" class="abs"></iframe>
"""
br10y="""
<iframe src="https://tvc-invdn-com.investing.com/web/1.12.34/index60-prod.html?carrier=cfd2aab50d462f27e956102ca5fe2868&amp;time=1695726550&amp;domain_ID=1&amp;lang_ID=1&amp;timezone_ID=8&amp;version=1.12.34&amp;locale=en&amp;timezone=America/New_York&amp;pair_ID=24029&amp;interval=D&amp;session=session&amp;prefix=www&amp;suffix=&amp;client=1&amp;user=203421857&amp;family_prefix=tvc6&amp;init_page=instrument&amp;sock_srv=https://streaming.forexpros.com&amp;m_pids=&amp;watchlist=&amp;geoc=BR&amp;site=https://www.investing.com" frameborder="0" scrolling="no" seamless="seamless" style="width: 100%; height:400px;" class="abs"></iframe>
"""
sp500="""
<iframe src="https://tvc-invdn-com.investing.com/web/1.12.34/index60-prod.html?carrier=537ab64a2484e3f665bb7d3bd0f5050d&amp;time=1695726810&amp;domain_ID=1&amp;lang_ID=1&amp;timezone_ID=8&amp;version=1.12.34&amp;locale=en&amp;timezone=America/New_York&amp;pair_ID=166&amp;interval=D&amp;session=24x7&amp;prefix=www&amp;suffix=&amp;client=1&amp;user=203421857&amp;family_prefix=tvc6&amp;init_page=instrument&amp;sock_srv=https://streaming.forexpros.com&amp;m_pids=&amp;watchlist=&amp;geoc=BR&amp;site=https://www.investing.com" frameborder="0" scrolling="no" seamless="seamless" style="width: 100%; height:400px;" class="abs"></iframe>
"""
vix="""
<iframe src="https://tvc-invdn-com.investing.com/web/1.12.34/index60-prod.html?carrier=1dcafeb3bde2fa752ac1b6e516ef0f0e&amp;time=1695728975&amp;domain_ID=1&amp;lang_ID=1&amp;timezone_ID=8&amp;version=1.12.34&amp;locale=en&amp;timezone=America/New_York&amp;pair_ID=44336&amp;interval=D&amp;session=24x7&amp;prefix=www&amp;suffix=&amp;client=1&amp;user=203421857&amp;family_prefix=tvc6&amp;init_page=instrument&amp;sock_srv=https://streaming.forexpros.com&amp;m_pids=&amp;watchlist=&amp;geoc=BR&amp;site=https://www.investing.com" frameborder="0" scrolling="no" seamless="seamless" style="width: 100%; height:400px;" class="abs"></iframe>
"""


spheatmap = '''
 <!-- TradingView Widget BEGIN -->
<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank"><span class="blue-text"></span></a></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-stock-heatmap.js" async>
  {
  "exchanges": [],
  "dataSource": "SPX500",
  "grouping": "sector",
  "blockSize": "market_cap_basic",
  "blockColor": "change",
  "locale": "en",
  "symbolUrl": "",
  "colorTheme": "dark",
  "hasTopBar": false,
  "isDataSetEnabled": false,
  "isZoomEnabled": true,
  "hasSymbolTooltip": true,
  "width": "100%",
  "height": "500"
}
  </script>
</div>
<!-- TradingView Widget END -->
'''

ibovespaheatmap = '''
 <!-- TradingView Widget BEGIN -->
<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank"><span class="blue-text"></span></a></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-stock-heatmap.js" async>
  {
  "exchanges": [],
  "dataSource": "IBOV",
  "grouping": "sector",
  "blockSize": "market_cap_basic",
  "blockColor": "change",
  "locale": "en",
  "symbolUrl": "",
  "colorTheme": "dark",
  "hasTopBar": false,
  "isDataSetEnabled": false,
  "isZoomEnabled": true,
  "hasSymbolTooltip": true,
  "width": "100%",
  "height": "500"
}
  </script>
</div>
<!-- TradingView Widget END -->
'''

screener = '''
<!-- TradingView Widget BEGIN -->
<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank"><span class="blue-text"></span></a></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
  {
  "symbols": [
    {
      "proName": "FOREXCOM:SPXUSD",
      "title": "S&P 500"
    },
    {
      "proName": "FOREXCOM:NSXUSD",
      "title": "US 100"
    },
    {
      "proName": "FX_IDC:EURUSD",
      "title": "EUR to USD"
    },
    {
      "proName": "BITSTAMP:BTCUSD",
      "title": "Bitcoin"
    },
    {
      "proName": "BITSTAMP:ETHUSD",
      "title": "Ethereum"
    }
  ],
  "showSymbolLogo": true,
  "colorTheme": "dark",
  "isTransparent": false,
  "displayMode": "adaptive",
  "locale": "en"
}
  </script>
</div>
<!-- TradingView Widget END -->
'''

html(screener, width=1000, height=80)

col1, col2 = st.columns(2)
with col1:
    st.markdown(sp500, unsafe_allow_html=True) 
    st.markdown(us10y, unsafe_allow_html=True)
    st.markdown(usdbrl, unsafe_allow_html=True)
    st.markdown(br10y, unsafe_allow_html=True)   
with col2:
    st.markdown(nasdaqfut, unsafe_allow_html=True) 
    st.markdown(vix, unsafe_allow_html=True) 
    st.markdown(ibovfut, unsafe_allow_html=True) 
    st.markdown(brent, unsafe_allow_html=True)

st.markdown('### SP500 Heatmap')
html(spheatmap, width=1000, height=510)
st.markdown('### IBOVESPA Heatmap')
html(ibovespaheatmap, width=1000, height=550)