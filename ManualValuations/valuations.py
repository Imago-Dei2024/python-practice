from rich.console import Console 
from rich.table import Table 
from rich.text import Text 
from rich.panel import Panel 
from rich.align import Align 


# COMPANY OVERVIEW Unformatted
companyName = str(input("Enter the Name of the Company: "))
shares = 13140000
shareprice = 163.68

marketcap = (shares * shareprice)

freeCash = int(input("Enter the TTM Free Cash Flow: "))

dcRate = .10

dayLow = 104.00 
dayHigh = 106.99 

yearlyLow = 81.74
yearlyHigh = 113.84

bidPrice = 104.95
bidQuantity = 400

askPrice = 106.00
askQuantity = 900

volume = 66,988
averageVolume = 22,800

intraMktCap = "1.38B" 

beta = 0.22
peRatio = 10.01

eps = 10.49
eMonth = "Aug"
eDay = 6
eYear = 2025

fwdDivYield = 3
xMonth = "May"
xDay = 20
xYear = 2025

oneYearTarget = "--"

# Company Overview - Formatted
sharesOutstanding = f"{shares:,}"
sharePriceFormatted = f"${shareprice:,.2f}"
marketCap = f"${marketcap:,.2f}"
freeCashFlow = f"${freeCash:,.2f}"
discountRate = f"{dcRate:.0%}"
fwdDividendYield = f"{fwdDivYield:.0%}"


# --- PERPETUITY MODEL (Rate / Free Cash Flow) Unformatted Numbers -----
perpModel = freeCash / dcRate
rawPerpModelPrice = (perpModel / shares)
rawPerpModelROI = (rawPerpModelPrice - shareprice) / shareprice
# Perpetuity Model Results
perpModelValuation = f"${perpModel:,.2f}"
perpModelPrice = f"${rawPerpModelPrice:,.2f}"
perpModelROI = f"{rawPerpModelROI:.0%}"


# --- GORDON GROWTH MODEL (CF1 / (R - g)) ---
#Calculate Cash Flow 1 (Free Cash Flow * (1 + g))
freeCash
terminalGrowth = .02
cashF1 = (freeCash * (1 + terminalGrowth))
# Gordon Growth Valuation
gordonGrowth = cashF1 / (dcRate - terminalGrowth)
rawGGPrice = (gordonGrowth / shares)
rawGGROI = (rawGGPrice - shareprice) / shareprice

# Formatted Valuation
cashFlow1 = f"${cashF1:,.2f}"
gordonGrowthValuation = f"${gordonGrowth:,.2f}"
gordonGrowthPrice = f"${rawGGPrice:,.2f}"
gordonGrowthROI = f"{rawGGROI:.0%}"