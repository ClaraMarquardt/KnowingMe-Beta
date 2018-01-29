# Basic Setup
# -------------------
# -------------------
FROM ubuntu:latest  
RUN apt-get update  
RUN apt-get install --no-install-recommends --no-install-suggests -y --reinstall build-essential
RUN apt-get install --no-install-recommends --no-install-suggests -y g++-4.8 git bash python python-setuptools gcc python-pip libc-dev unixodbc-dev python-dev
RUN pip install --upgrade pip

RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN apt-get update && apt-get install -y python-software-properties software-properties-common postgresql-9.3 postgresql-client-9.3 postgresql-contrib-9.3

# Info
# -------------------
# -------------------
MAINTAINER Clara Marquardt "marquardt.clara@gmail.com”
RUN pwd
RUN ls root/


# *Add Local Code
# -------------------
# -------------------

# *Add Env Var
# -------------------
# -------------------
ENV PORT 8000
ENV DEBUG "False"

# Obtain Codebase
# -------------------
# -------------------
RUN mkdir knowingme
COPY . /KnowingMe/
RUN pwd

# Installation
# -------------------
# -------------------

# Installation - Setup
# -------------------
RUN pwd
WORKDIR /KnowingMe/
RUN chmod -R a+rwx .

# Installation - App Settings (app_setting.json)
# -------------------

# Installation 
# -------------------
# [1] Install main Python dependencies (Using 'pip')
RUN pip install --no-binary scipy scikit-learn  
RUN pip --no-cache-dir install -r codebase/setup/dependency.txt           	   # general dependencies (1)
RUN python codebase/setup/dependency.py            			                   # general dependencies (2)
RUN pip install --upgrade google-api-python-client        			           # google api dependency

# [2] NLTK
RUN python codebase/setup/nltk_test.py  

# [3] Spacy
RUN python codebase/setup/spacy_test.py  

USER postgres
RUN    /etc/init.d/postgresql start &&\
    psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'docker';" &&\
    createdb -O docker docker

RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.3/main/pg_hba.conf

# And add ``listen_addresses`` to ``/etc/postgresql/9.3/main/postgresql.conf``
RUN echo "listen_addresses='*'" >> /etc/postgresql/9.3/main/postgresql.conf

# Expose the PostgreSQL port
EXPOSE 5432
# Launch
# -------------------
# -------------------
VOLUME KnowingMe_Data
WORKDIR /KnowingMe/
EXPOSE  $PORT
CMD ["/KnowingMe/test.sh"]
