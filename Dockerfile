FROM python:3.10-slim
ENV PYTHONBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]