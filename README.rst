block
*****

To Do

- Link wizard

  - Can you delete a document, a link... or both?

- Other tickets (to minimise migrations)

  - SEO

Django application

Install
=======

Virtual Environment
-------------------

::

  virtualenv --python=python3 venv-block
  source venv-block/bin/activate

  pip install -r requirements/local.txt

Testing
=======

::

  find . -name '*.pyc' -delete
  py.test -x

Development
===========

::

  ./init_dev.sh

Release
=======

https://www.kbsoftware.co.uk/docs/
