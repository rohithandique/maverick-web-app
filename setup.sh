mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"rohit.handique.rh@gmail.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
[theme]\n\
base="light"\n\
primaryColor="\#3371f6"\n\
\n\
" > ~/.streamlit/config.toml