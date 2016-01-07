FROM ubuntu:latest

RUN apt-get -y update && apt-get install -y\
    git npm python-virtualenv sqlite3 nodejs
RUN npm update && npm install -g bower coffee-script


expose 5000
CMD ln -s /usr/bin/nodejs /usr/bin/node && git clone https://github.com/PabloRal/hopsiup.git && cd hopsiup && \
    git checkout deploy && virtualenv venv && . venv/bin/activate && pwd && cd hopsiup && \
    pip install -r requirements.txt && bower --allow-root install && python hopsiup.py
