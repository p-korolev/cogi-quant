# cogi-quant 📈 (_under development_)

## **Overview**

`cogi-quant` is a modular Python library designed to make **quantitative finance workflows** easier, faster, and more intuitive. Whether you're an algorithmic trader, a data analyst, or a researcher, this toolkit offers **data fetching**, **time series visualization**, **statistical computation**, and **custom financial structures** to support rapid market experimentation.

---

## **Installation**

Install via Python pip:
```bash
pip install cogi-quant
```
Alternatively, install for local development:
```bash
git clone https://github.com/yourusername/cogi-quant.git
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

# initialize stock (Apple used as example)
AAPL = Stock("AAPL")

# fetch 1-month open price history
price_history.get_price_open_series(stock=AAPL, period='1mo')

# fetch past day hourly price history
price_history.get_price_open_series(stock=AAPL, period='1d', interval='1h')
```

- 🧠 **View Qualitative Company Information**  
  Access **qualitative company profiles** like company summaries, employees, industry, chair of directors, etc.
```bash
from cogi_quant.dataload import company_profile as profile
from cogi_quant.instrument import stock
  
# Method 1: initialize profile object using string
ABNB_profile = profile.CompanyProfile("Airbnb")

#Method 2: initialize profile object using Stock object
ABNB = stock.Stock("ABNB")
ABNB_profile = profile.CompanyProfile(ABNB)

# get a company summary
ABNB_profile.summary()

# get company chair of directors
ABNB_profile.get_chair()
```
  
- 🧠 **Stock Stats Quick-View**  
  Access **quantitative company stock stats** like PE ratios, volume, beta, risk, etc.
```bash
from cogi_quant.dataload import quoting

# initalizing quoting
GOOGL_q = quoting.Quote("GOOGL")

# access GOOGL stock PE ratios
GOOGL_q.get_PE_trailing()
GOOGL_q.get_PE_forward()

# other stats
risk = GOOGL_q.overall_risk()
beta = GOOGL_q.get_beta()
day_volume = GOOGL_q.get_current_day_volume()
```

- 🗂️ **S&P 500 & Index Membership**  
  Easily pull S&P 500 constituents for index-level or sector-level analysis.
```bash
from cogi_quant.dataload import snp

# view securities by industry/sector
health_care_securities = snp.get_securities_by_sector(sector="Health Care")
```

- 🧮 **Statistical & Technical Analysis**  
  Built-in tools for basic stats, rolling operations, market indicators, and more.
```bash
from cogi_quant.instrument import stock
from cogi_quant.processing import price_history as history
from cogi_quant.mat import technicals

#initialize stock
AMZN = stock.Stock("AMZN")

# get 1-minute stock price quotes for last day
day_prices_by_minute = history.get_price_open(AMZN, period='1d', interval='1m')

# load technicals like moving averages, rsi, moving average conv/div as series
moving_average = technicals.simple_moving_average(day_prices_by_minute, window=3)
relative_strength_index = technicals.rsi(day_prices_by_minute, period=14)
macd = macd(day_prices_by_minute) 
```

- 📊 **Plotting & Visualization** *(under development)*  
  - Time series plotting for historical and live stock prices with technical indicators as overlay options
  - Time series plotting for historical company financials with projections
  - Volumetric plotting for metric correlation

- 🔮 **Future Modules** *(under development)*  
  - Balance sheets, income statements, cash flow views  
  - Real-world non-market data (weather, rates, inflation)  
  - Trading simulation (returns visualization, run buy/sell order simulations on historical markets)
  - Machine learning models for price projections





