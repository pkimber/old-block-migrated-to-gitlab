block
*****

To Do

- Link wizard

  - Link to another site
  - Page on this site
  - Upload a document and link to it
  - Use an existing document
  - Remove link

- Other tickets (to minimise migrations)
  - SEO

Django application

Install
=======

Virtual Environment
-------------------

::

  pyvenv-3.4 --without-pip venv-block
  source venv-block/bin/activate
  wget https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py
  python get-pip.py

  pip install -r requirements/local.txt

Testing
=======

::

  find . -name '*.pyc' -delete
  py.test -x

Usage
=====

::

  ./init_dev.sh

Release
=======

https://www.pkimber.net/open/
