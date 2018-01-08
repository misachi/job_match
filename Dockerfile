 FROM python:3
 ENV PYTHONUNBUFFERED 1
 ENV APP_HOME=/home/matcher/
 RUN groupadd -g 1000 jobmatch && \
    useradd -r -u 1000 -g jobmatch jobmatch
 RUN mkdir $APP_HOME
 WORKDIR $APP_HOME
 COPY requirements.txt $APP_HOME
 RUN pip install -r requirements.txt
 COPY . $APP_HOME
 RUN chown -R jobmatch:jobmatch $APP_HOME
 
 USER jobmatch
