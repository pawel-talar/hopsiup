# HopSiup

Low quality version of HopSiup site. To test, run:

    ./init_db.sh

and (after adding some data to db under hopsiup/hopsiup.db)

    python hopsiup.py


## Docker

You can also test it using docker, executing from main directory (that with
Dockerfile):

    docker build -t hopsiup .
    docker run -d -P 5000:5000 hopsiup

and opening in browser:

    http://localhost:5000/
