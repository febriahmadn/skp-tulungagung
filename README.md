# SKP Tulungagung

### Pakai Python Python 3.10.6


## Installation

### Create Database

    ```sql
    CREATE DATABASE skp;
    CREATE USER skp_user WITH PASSWORD '5o4wr1515jua8my6xx36';
    ALTER ROLE skp_user SET client_encoding TO 'utf8';
    ALTER ROLE skp_user SET default_transaction_isolation TO 'read committed';
    ALTER ROLE skp_user SET timezone TO 'Asia/Jakarta';
    ALTER ROLE skp_user WITH PASSWORD '5o4wr1515jua8my6xx36';
    GRANT ALL PRIVILEGES ON DATABASE skp TO skp_user;
    ```
