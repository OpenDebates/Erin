.. _configuring_database:

=======================
Configuring a database
=======================

Glia does not come with it's own database. So we need to install and configure one to make sure Glia works properly.
Currently Glia uses MongoDB to store all it's data.

You need to either setup one using Google Cloud like we are in production or set one up yourself on a bare metal server or a VPS.
Either ways, it is outside the scope of this documentation for the most part.

You can read more about setting up a database by following the official MongoDB `documentation <https://docs.mongodb.com/manual/administration/install-community/>`_
Once you've successfully done this, we need to setup an administrator with superuser capabilites. You can read more about setting this up `here <https://docs.mongodb.com/manual/tutorial/enable-authentication/#enable-auth>`_

To do this, first we need to open up the ``mongo`` shell and create our user adjusting the commands below as needed.

::

    use admin
    db.createUser(
      {
        user: "myUserAdmin",
        pwd: "abc123",
        roles: [ { role: "root", db: "admin" } ]
      }
    )

This will create a superuser role giving Glia complete control over the database. Take these credentials down as will you need to use them in the config file.


For Developers
==============

Read the :ref:`handbook_index` to start contributing.
