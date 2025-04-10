@echo off
REM Simple script to run the RSS generator on Windows

REM Ensure virtual environment if it doesn't exist
if not exist venv (
  echo Creating virtual environment...
  python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Run the script
echo Running RSS generator...
python firstwordpharma_rss_scraper.py

echo Done!
pause