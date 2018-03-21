.. _installing_bot:

==================
Installing the bot
==================

For Users
=========

.. todo::

    Add instructions for Docker, Kubernetes and pip wheel releases.

Follow the developer instructions for now and verify you have a working installation with this command.

::

    $ enigma -V    # This should show the current version.
    enigma 0.1.0.dev0

For Developers
==============

Installing from source
----------------------

Enigma is very easy to install from source. First clone the latest development version from the master branch.

::

    git clone https://github.com/UnethicalDiscord/Enigma.git


Since Enigma has a lot of dependencies, it is wise to install a virtualenv first. Please do not use `pipenv <https://docs.pipenv.org/>`_ however.
It's incompatible with Enigma's dependencies and may cause more problems in the future. If you wish to submit a pull request to fix this problem please read more `here <https://github.com/pypa/pipenv/issues/1578>`_

First let's make a virtualenv. So we have to install it first.

::

    pip install virtualenv

Then create a new virtualenv within the repository. If you name it ``venv`` it won't get checked in.

::

    cd Enigma/
    virtualenv venv

Now let's activate the virtual environment.

::

    source venv/bin/activate

You should now see your terminal change to show your are you now using a virtual environment.
Let's install the package dependencies now. This may take a while depending on your machine.


::

    pip install -r requirements.txt

Now let's install it locally as an editable installation to make sure our changes get picked up.

::

    pip install -e .

Additionally, if you need to write tests run this command.

::

    pip install -e .[TESTS]
