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

:: Start Users Funds Service
cd Backend
start cmd.exe /k "python users_funds.py"
