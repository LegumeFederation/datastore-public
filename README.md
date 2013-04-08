sra README
==================

Environment Configuration (CentOS 5)
-----------------------

### Python
    yum install python26 python26-devel

### Setuptools
    cd /tmp
    curl -O https://pypi.python.org/packages/2.6/s/setuptools/setuptools-0.6c11-py2.6.egg
    chmod 775 setuptools-0.6c11-py2.6.egg
    sh setuptools-0.6c11-py2.6.egg

### Pip
    curl -O https://pypi.python.org/packages/source/p/pip/pip-1.2.1.tar.gz
    tar zxvf pip-1.2.1.tar.gz 
    cd pip-1.2.1
    python26 setup.py install

### Virtualenv
Make sure to create your virtualenv as a non-root user

    pip-2.6 install virtualenv
    mkdir ~/env
    cd ~/env
    virtualenv-2.6 --no-site-packages sra
    . sra/bin/activate

Environment Configuration (Ubuntu 12.04)
---------------------------

### Packages
    sudo apt-get install python-dev python-pip python-virtualenv

### Virtualenv
    mkdir ~/env
    cd ~/env
    virtualenv --no-site-packages sra
    . sra/bin/activate

Installation
------------

### pycommands
    pip install git+git://github.com/cjlarose/pycommands.git

### SRA
Clone as a non-root user

    cd ~
    git clone git@github.com:cjlarose/sra.git
    sudo mv sra /opt
    cd /opt/sra
    python setup.py develop

### Fire it up
    sudo ~/env/sra/bin/pserve production.ini --log-file=sra.log --daemon
