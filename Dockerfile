FROM nikolaik/python-nodejs:latest 

COPY . .
RUN apt update
RUN apt upgrade -y
RUN apt-get install python3-lxml -y

# RUN pip3 install --upgrade
RUN pip3 install -r requirements.txt

CMD forever start -a index.js -p 8000
CMD python3 python_discord.py
# CMD source start_bot.sh