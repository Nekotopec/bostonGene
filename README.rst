Task
****
.. image:: https://github.com/Nekotopec/bostonGene/raw/master/image/task.jpg


How to install?
***************

1 Install docker and docker compose. If you're using ubuntu:

.. code-block:: bash

   sudo apt install docker.io docker-compose

2 Clone this repository.

.. code-block:: bash
   
   git clone https://github.com/Nekotopec/bostonGene.git

3 Go to project directory.

.. code-block:: bash
   
   cd bostonGene/

4 Create a container.

.. code-block:: bash

   docker-compose build

5 Run.

.. code-block:: bash

   docker-compose up
   
It will give you a server on address localhost:8000

To see running containers use:

.. code-block:: bash

   docker-compose ps

To stop it use:

.. code-block:: bash

   docker-compose stop
