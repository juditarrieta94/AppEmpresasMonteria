mkdir -p ~/.streamlit/
echo "
[theme]
primaryColor="#22366B"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#AFB3BD"
textColor="#000000"
font="sans serif"
[server]
headless = true
enableCORS=false
enableXsrfProtection=false
port = $PORT
" > ~/.streamlit/config.toml