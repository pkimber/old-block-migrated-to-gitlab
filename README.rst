block
*****

Image Categories

- Only allow delete if un-used
- Don't allow the user to select a deleted category for an image.

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
