:: Start Funds Service
cd Backend
start cmd.exe /k "python funds.py"

:: Start Funds Stocks Service
cd Backend
start cmd.exe /k "python funds_stocks.py"

:: Start Users Stocks Service
cd Backend
start cmd.exe /k "python users_stocks.py"

:: Start Stocks Service
cd Backend
start cmd.exe /k "python stocks.py"

:: Start Transaction Service
cd Backend
start cmd.exe /k "python transactions.py"

:: Start Users Service
cd Backend
start cmd.exe /k "python users.py"

:: Start Users Funds Service
cd Backend
start cmd.exe /k "python users_funds.py"

:: Start Marketplace Stocks Service
cd Backend
start cmd.exe /k "python marketplace_stocks.py"

:: Start Marketplace Service
cd Backend
start cmd.exe /k "python marketplace.py"

:: Start Place Market Order Service
cd Backend
start cmd.exe /k "python place_market_order.py"