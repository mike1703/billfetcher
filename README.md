## Installation:

### On Debian based systems:
```
sudo aptitude install python-dev virtualenvwrapper libxml2-dev libxslt-dev libff1-dev
```

### Create a virtual environment
```
mkvirtualenv scrapy
workon scrapy
pip install -r requirements.txt
```

### Configure the billfetcher
```
vim billfetcher/settings.py
# enter username/password/path to archive
```

## Usage:
```
workon scrapy
scrapy crawl deutschlandsim
```
