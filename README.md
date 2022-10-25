# Project presentation

# Download

    git clone https://github.com/PnEcrins/Istsos-import.git

# Instalation

### Install system requirements:

    apt install python3-pip redis libpq-dev

### Create a python virtualenv and install dependencies

    cd Istsos-import
    sudo pip3 install virtualenv
    virtualenv -p /usr/bin/python3 venv
    source venv/bin/activate
    pip install .

### Config file

Copy and edit the config file

    cp config.toml.example config.toml
    nano config.toml

### Install database

Do not do this command if you already have a istosos-import instance for an other service

    cd src/istsosimport
    flask db upgrade

### Prod deployment

##### Create a systemd service

    sudo cp istsosimport.service /etc/systemd/system
    # Replace <APP_DIRECTORY> by the directory where the app is located (/opt/istsos-import for exemple) and $USER by your current linux user
    sudo mkdir /var/log/istsosimport
    sudo chown $USER: /var/log/istsosimport/
    sudo systemctl daemon-reload
    sudo systemctl enable istsosimports
    sudo systemctl start istsosimport

##### Make a apache conf

    sudo cp istsosimport.conf /etc/apache2/sites-available/
    sudo a2enmod proxy
    sudo a2ensite istsosimport.conf
    sudo systemctl reload apache2

# Run in dev

In order to send mail, Flask has to know the "SERVER_NAME". In dev we use IP but we don't have a domain. Add those line in your `/etc/hosts`

::
127.0.0.1 istsosimport.local

In config.toml set the `URL_APPLICATION` like this : `URL_APPLICATION = "http://istsosimport.local:<PORT>/"` where the port is the port on which Flask run

Run flask app and celery app in two separate terminals

    flask run
    celery -A istsosimport.celery_app worker -l INFO

The app is available on `http://istsosimport.local:<PORT>`
