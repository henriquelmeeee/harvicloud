if [ "$EUID" -ne 0 ]
  then echo "Você deve executar este script como root"
  exit
fi
apt-get install python3
apt-get install pip-python3
apt-get install mysql-server
python3 -m pip install mysql-connector-python
python3 -m pip install Flask
python3 -m pip install -U discord.py
python3 -m pip install tcp_latency
python3 -m pip install -U discord-py-slash-command
python3 -m pip install -U discord-py-interactions
python3 -m pip install -U selenium
python3 -m pip install webdriver-manager
sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
apt-get update
apt-get install google-chrome-stable

echo ---------------
echo Finalizado com sucesso!
echo ---------------
