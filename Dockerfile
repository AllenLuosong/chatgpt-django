FROM python:3.9.0
RUN mkdir /app
COPY . /app 
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt -i https://pypi.douban.com/simple
RUN python /app/manage.py makemigrations
RUN python manage.py migrate
WORKDIR /app