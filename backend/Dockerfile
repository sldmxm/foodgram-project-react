FROM python:3.7-slim
WORKDIR /backend
COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .

# при разворачивании локально, можно раскаментить, шрифт поставится автоматом
#COPY ./static/RobotoMono-Regular.ttf ./
#RUN mkdir -p /usr/share/fonts/truetype/
#RUN install -m644 RobotoMono-Regular.ttf /usr/share/fonts/truetype/
#RUN rm ./RobotoMono-Regular.ttf