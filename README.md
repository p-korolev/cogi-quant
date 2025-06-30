# cogi-quant 📈 (_under development_)

## **Overview**

Python toolkit aimed to ease quantitative market analysis. Ditch manually downloading financial data and importing 5+ quantitative libraries for analysis, and leverage `cogi-quant` to fetch price history for financial instruments, company financials, S&P500 data, and build time series visuals.

---

## **Installation**

Install via Python pip:
```bash
pip install cogi-quant
```
Install for local development:
```bash
git clone https://github.com/p-korolev/cogi-quant.git
cd cogi-quant
pip install -e .
```
---

## **Features**

- 🔎 **Fetch Historical Market Data**  
  Load open, close, high, low, and volume series for any publically traded ticker over any period.
```bash
from cogi_quant.instrument.stock import Stock
from cogi_quant.processing import price_history

AAPL = Stock("AAPL")
price_history.get_price_open_series(stock=AAPL, period='1d', interval='1h')
```

- 🧠 **View Qualitative Company Information**  
  Access **qualitative company profiles** like company summaries, employees, industry, chair of directors, etc.
```bash
from cogi_quant.dataload import company_profile as profile
from cogi_quant.instrument import stock

ABNB_profile = profile.CompanyProfile("Airbnb")
ABNB_profile.summary()
ABNB_profile.get_chair()
```
  
- 🧠 **Stock Stats Quick-View**  
  Access **quantitative company stock stats** like PE ratios, volume, beta, risk, etc.

- 🗂️ **S&P 500 & Index Membership**  
  Easily pull S&P 500 constituents for index-level or sector-level analysis.
```bash
from cogi_quant.dataload import snp

health_care_securities = snp.get_securities_by_sector(sector="Health Care")
```

- 🧮 **Statistical & Technical Analysis**  
  Built-in tools for basic stats, rolling operations, market indicators, and more.

- 📊 **Plotting & Visualization** *(under development)*  
  - Time series plotting for historical and live stock prices with technical indicators as overlay options
  - Time series plotting for historical company financials with projections
  - Volumetric plotting for metric correlation

- 🔮 **Future Modules** *(under development)*  
  - Balance sheets, income statements, cash flow views  
  - Real-world non-market data (weather, rates, inflation)  
  - Trading simulation (returns visualization, run buy/sell order simulations on historical markets)
  - Machine learning models for price projections

## **Example Usage**

```bash
from cogi_quant.instrument import stock
from cogi_quant.processing import price_history
from cogi_quant.mat import technicals
from cogi_quant.mat import stats
import matplotlib.pyplot as plt

# Initialize instrument (Apple stock used as example)
AAPL = stock.Stock("AAPL")

# Fetch 1-month open price history
hist = price_history.get_price_open_series(stock=AAPL, period='1mo')

# Construct respective market indicators for plotting
ma_fast = technicals.simple_moving_average(hist, window=2)
ma_slow = technicals.simple_moving_average(hist, window=5)
rsi = technicals.rsi(hist, period=5)

# Get statistical indicators for plotting
min, max = stats.sup(hist), stats.inf(hist)

# Plot visual
plt.plot(hist, label='Open Price'))
plt.plot(ma_fast, label='Fast Moving Avg')
plt.plot(ma_slow, label='Slow Moving Avg')
plt.plot(rsi, label='Relative Strength Index', linestyle='--')
plt.axhline(y=min, label='Range-Low')
plt.axhline(y=max, label='Range-High')
plt.show()
```





