block
*****

- Change to normal views...

- Settings - Image Library

  - Icon for delete.
  - Edit icon for changing title, category

- Upload an image

  - Category drop down.  Defined in settings.  No tags!
  - Tick box... add to library.  Default is ticked.
  - Title as alt tag.  Yes... no change to the UI.

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
