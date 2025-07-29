import valuations

from rich.console import Console 
from rich.table import Table 
from rich.text import Text 
from rich.panel import Panel 
from rich.align import Align 
from rich.box import ROUNDED 



overview_table = Table(
    show_header=False,
    border_style = "yellow",  # No box, we'll use lines between rows
    padding=(0, 2), # Padding top/bottom, left/right
    title=f"\n[bold cyan]{valuations.companyName}[/bold cyan]",
    title_justify="center"
)

# ==== Add 4 Columns to Table ==== # 
overview_table.add_column(style="bold white") 
overview_table.add_column(style="bold white") 
overview_table.add_column(style="bold white") 
overview_table.add_column(style="bold white") 

#Populate Table Rows 
overview_table.add_row ( 
    Text(f"Previous Close.            {valuations.sharePriceFormatted}", justify="left"),
    Text(f"Day's Range                {valuations.dayLow} x {valuations.dayHigh}", justify="left"), 
    Text(f"Market Cap (intraday)      {valuations.intraMktCap}", justify="left"), 
    Text(f"Earnings Date              {valuations.eMonth} {valuations.eDay}, {valuations.eYear}", justify="left")
) 

#Row 2 
overview_table.add_row ( 
    Text(f"Open                       {valuations.sharePriceFormatted}", justify="left"), 
    Text(f"52 Week Range              {valuations.yearlyLow} - {valuations.yearlyHigh}", justify="left"), 
    Text(f"Beta (5Y Monthly)          {valuations.beta}", justify="left"),  
    Text(f"Forward Dividend & Yield   {valuations.fwdDividendYield}", justify="left"), 
) 

#Row 3 
overview_table.add_row ( 
    Text(f"Bid                        {valuations.bidPrice}x{valuations.bidQuantity}", justify="left"), 
    Text(f"Volume                     {valuations.volume}", justify="left"), 
    Text(f"PE Ratio (TTM)             {valuations.peRatio}", justify="left"), 
    Text(f"Ex-Dividend Date           {valuations.xMonth} {valuations.xDay}, {valuations.xYear}", justify="left"), 
) 

#Row 4 
overview_table.add_row ( 
    Text(f"Ask                        {valuations.askPrice}x{valuations.askQuantity}", justify="left"), 
    Text(f"Avg. Volume                {valuations.averageVolume}", justify="left"), 
    Text(f"EPS (TTM)                  {valuations.eps}", justify="left"), 
    Text(f"1y Target Est              {valuations.oneYearTarget}", justify="left"), 
)  

# --- Create Company Overview Table --- 

# --- Create Valuation Tables ---
def create_valuation_panel(title, valuation, price, roi):
    grid = Table.grid(expand=True)
    grid.add_column(justify="left", ratio=1)
    grid.add_column(justify="right", ratio=1)
    grid.add_row("Intrinsic Valuation:", f"[bold green]{valuation}")
    grid.add_row("Implied Share Price:", f"[bold green]{price}")
    grid.add_row("Potential ROI:", f"[bold green]{roi}")
    return Panel(
        grid,
        title=f"[bold yellow]{title}",
        border_style="yellow",
        padding=(1, 2)
    ) 

perp_panel = create_valuation_panel(
    "Perpetuity Model",
    valuations.perpModelValuation,
    valuations.perpModelPrice,
    valuations.perpModelROI
)

gg_panel = create_valuation_panel(
    "Gordon Growth Model",
    valuations.gordonGrowthValuation,
    valuations.gordonGrowthPrice,
    valuations.gordonGrowthROI
)

# --- Print everything to the console ---
console = Console() 
console.print(overview_table)
console.print(Align.center(perp_panel))
console.print(Align.center(gg_panel))





