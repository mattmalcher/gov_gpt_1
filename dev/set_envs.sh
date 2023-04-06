# store API key in secrets-tool
# https://manpages.ubuntu.com/manpages/bionic/man1/secret-tool.1.html
export OPENAI_API_KEY=$(secret-tool lookup api openai)