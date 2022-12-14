FROM ubuntu:18.04

# RUN locale-gen en_US.UTF-8

WORKDIR /usr/app

RUN apt-get update
RUN apt-get -y install curl gnupg
RUN curl -sL https://deb.nodesource.com/setup_16.x  | bash -
RUN apt-get -y install nodejs

RUN apt-get install --yes python3
RUN apt-get install --yes python3-dev libmysqlclient-dev
RUN apt update && apt install --yes python3-pip
RUN pip3 install mysql-connector-python sqlalchemy pandas ciscoconfparse mysql
# RUN pip3 install mysql
RUN pip3 install sklearn scikit-learn

RUN apt-get install -y locales
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en

COPY ./package.json ./
RUN npm install

COPY ./ ./

RUN npm run build:prod

CMD  ["npm" ,"start"]
# CMD  ["npm" ,"start"]
# RUN npm i -g pm2
# CMD ["pm2","start","pm2.json"]
# CMD ["npm", "run" ,"dev"]
