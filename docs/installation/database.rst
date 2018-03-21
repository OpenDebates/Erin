.. _configuring_database:

=======================
Configuring a database
=======================

Enigma does not come with it's own database. So we need to install and configure one to make sure Enigma works properly.
Currently Enigma uses PostgreSQL to store all it's data into a table.

You need to either setup one using Google Cloud like we are in production or set one up yourself on a bare metal server or a VPS.
Either ways, it is outside the scope of this documentation for the most part.

You can read more about setting up a database by following one of these tutorials.

- `Ubuntu 16.04 <https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04>`_
- `Fedora 23 <https://www.liquidweb.com/kb/how-to-install-and-connect-to-postgresql-on-fedora-23/>`_
- `Google Cloud <https://cloud.google.com/community/tutorials/setting-up-postgres>`_

Once you've successfully done this, we need to open up ``psql`` an create the database and roles.

::

    sudo su postgres -c psql

Then run this sql query either in the shell or using your preferred database management solution.

.. code-block:: sql

    CREATE USER my_user WITH LOGIN PASSWORD 'my_password'; -- Where my_user and my_password are your desired credentials.
    CREATE DATABASE my_database OWNER my_user; -- Where my_database is your desired database name.

Congratulations! You now have a working installation of Enigma.
If all went well, you can proceed to reading the :ref:`manual_index`.


For Developers
==============

Read the :ref:`handbook_index` to start contributing.
