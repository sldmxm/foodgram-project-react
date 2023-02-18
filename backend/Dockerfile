FROM python:3.7-slim
WORKDIR /backend
COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .

RUN wget https://github.com/google/fonts/archive/master.tar.gz -O gf.tar.gz
RUN tar -xf gf.tar.gz
RUN mkdir -p /usr/share/fonts/truetype/google-fonts
RUN find $PWD/fonts-master/ -name "*.ttf" -exec install -m644 {} /usr/share/fonts/truetype/google-fonts/ \; || return 1
RUN rm -f gf.tar.gz
RUN fc-cache -f && rm -rf /var/cache/*
# при разворачивании локально, можно раскаментить, шрифт поставится автоматом
#COPY ./static/RobotoMono-Regular.ttf ./
#RUN mkdir -p /usr/share/fonts/truetype/
#RUN install -m644 RobotoMono-Regular.ttf /usr/share/fonts/truetype/
#RUN rm ./RobotoMono-Regular.ttf