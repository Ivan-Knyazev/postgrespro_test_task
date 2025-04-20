## Результаты работы скрипта

- Для удаления `PostgreSQL` и различных зависимостей, созданных во время автоматического развёртывания, и, таким образом, приведения ОС к "чистому виду" были написаные небольшие `bash`-скрипты: `remove_postgres_alma.sh` `remove_postgres_debian.sh`. Это было сделано для проведения корректного тестирования во время отладки.

У меня тестирование происходило посредством запуска написанного скрипта из WSL, установленной на OS Windows 11. На VirtualBox также были установлены VM с Debian и AlmaLinux. Виртуальная машина с `Debian` имела `IP`-адрес `192.168.1.41`. Виртуальная машина с `AlmaLinux` имела `IP`-адрес `192.168.1.43`.


**Тестирование** написанного скрипта было проведено в 2 этапа:

1) **Установка `PosgreSQL` на удалённый хост с `Debian`.** Для этого на другой машине с `AlmaLinux` была временно запущена команда `yes > /dev/null` для полной загрузки одного ядра процессора. Это было сделано для того, чтобы скрипт точно выбрал в качестве целевого сервера машину с `Debian`.
   
   Для подтверждения проведённого тестирования вывод из консоли после выполнения срипта представлен ниже. Всё было **успешно установлено и протестировано** посредством запуска `python`-скрипта для подключения к только что установленному `Postgres` с другого сервера пользователем `student`, что и требует Техническое Задание.
   
    ```
    (venv) ivan@Ivan-Lenovo:~/internships/postgrespro-devops$ python3 deploy_postgres.py 192.168.1.41,192.168.1.43
    [DEBUG] Get loads and target_server {'192.168.1.41': 0.115, '192.168.1.43': 0.2275} 192.168.1.41
    [INFO] Target server: 192.168.1.41
    [INFO] In target server 192.168.1.41 detected DEBIAN
    [INFO] Executed command: apt update && apt install -y postgresql postgresql-contrib

    WARNING: apt does not have a stable CLI interface. Use with caution in scripts.

    Hit:1 http://deb.debian.org/debian bookworm InRelease
    Hit:2 http://security.debian.org/debian-security bookworm-security InRelease
    Hit:3 http://deb.debian.org/debian bookworm-updates InRelease
    Reading package lists...
    Building dependency tree...
    Reading state information...
    18 packages can be upgraded. Run 'apt list --upgradable' to see them.

    WARNING: apt does not have a stable CLI interface. Use with caution in scripts.

    Reading package lists...
    Building dependency tree...
    Reading state information...
    The following additional packages will be installed:
    libcommon-sense-perl libjson-perl libjson-xs-perl libllvm14 libpq5
    libtypes-serialiser-perl postgresql-15 postgresql-client-15
    postgresql-client-common postgresql-common sysstat
    Suggested packages:
    postgresql-doc postgresql-doc-15 isag
    The following NEW packages will be installed:
    libcommon-sense-perl libjson-perl libjson-xs-perl libllvm14 libpq5
    libtypes-serialiser-perl postgresql postgresql-15 postgresql-client-15
    postgresql-client-common postgresql-common postgresql-contrib sysstat
    0 upgraded, 13 newly installed, 0 to remove and 18 not upgraded.
    Need to get 41.6 MB of archives.
    After this operation, 177 MB of additional disk space will be used.
    Get:1 http://deb.debian.org/debian bookworm/main amd64 libjson-perl all 4.10000-1 [87.5 kB]
    Get:2 http://deb.debian.org/debian bookworm/main amd64 postgresql-client-common all 248 [35.1 kB]
    Get:3 http://deb.debian.org/debian bookworm/main amd64 postgresql-common all 248 [179 kB]
    Get:4 http://deb.debian.org/debian bookworm/main amd64 libcommon-sense-perl amd64 3.75-3 [23.0 kB]
    Get:5 http://deb.debian.org/debian bookworm/main amd64 libtypes-serialiser-perl all 1.01-1 [12.2 kB]
    Get:6 http://deb.debian.org/debian bookworm/main amd64 libjson-xs-perl amd64 4.030-2+b1 [92.1 kB]
    Get:7 http://deb.debian.org/debian bookworm/main amd64 libllvm14 amd64 1:14.0.6-12 [21.8 MB]
    Get:8 http://deb.debian.org/debian bookworm/main amd64 libpq5 amd64 15.12-0+deb12u2 [192 kB]
    Get:9 http://deb.debian.org/debian bookworm/main amd64 postgresql-client-15 amd64 15.12-0+deb12u2 [1,724 kB]
    Get:10 http://deb.debian.org/debian bookworm/main amd64 postgresql-15 amd64 15.12-0+deb12u2 [16.8 MB]
    Get:11 http://deb.debian.org/debian bookworm/main amd64 postgresql all 15+248 [10.1 kB]
    Get:12 http://deb.debian.org/debian bookworm/main amd64 postgresql-contrib all 15+248 [10.1 kB]
    Get:13 http://deb.debian.org/debian bookworm/main amd64 sysstat amd64 12.6.1-1 [596 kB]
    debconf: unable to initialize frontend: Dialog
    debconf: (TERM is not set, so the dialog frontend is not usable.)
    debconf: falling back to frontend: Readline
    debconf: unable to initialize frontend: Readline
    debconf: (This frontend requires a controlling tty.)
    debconf: falling back to frontend: Teletype
    dpkg-preconfigure: unable to re-open stdin: 
    Fetched 41.6 MB in 10s (3,975 kB/s)
    Selecting previously unselected package libjson-perl.
    (Reading database ... 166956 files and directories currently installed.)
    Preparing to unpack .../00-libjson-perl_4.10000-1_all.deb ...
    Unpacking libjson-perl (4.10000-1) ...
    Selecting previously unselected package postgresql-client-common.
    Preparing to unpack .../01-postgresql-client-common_248_all.deb ...
    Unpacking postgresql-client-common (248) ...
    Selecting previously unselected package postgresql-common.
    Preparing to unpack .../02-postgresql-common_248_all.deb ...
    Adding 'diversion of /usr/bin/pg_config to /usr/bin/pg_config.libpq-dev by postgresql-common'
    Unpacking postgresql-common (248) ...
    Selecting previously unselected package libcommon-sense-perl:amd64.
    Preparing to unpack .../03-libcommon-sense-perl_3.75-3_amd64.deb ...
    Unpacking libcommon-sense-perl:amd64 (3.75-3) ...
    Selecting previously unselected package libtypes-serialiser-perl.
    Preparing to unpack .../04-libtypes-serialiser-perl_1.01-1_all.deb ...
    Unpacking libtypes-serialiser-perl (1.01-1) ...
    Selecting previously unselected package libjson-xs-perl.
    Preparing to unpack .../05-libjson-xs-perl_4.030-2+b1_amd64.deb ...
    Unpacking libjson-xs-perl (4.030-2+b1) ...
    Selecting previously unselected package libllvm14:amd64.
    Preparing to unpack .../06-libllvm14_1%3a14.0.6-12_amd64.deb ...
    Unpacking libllvm14:amd64 (1:14.0.6-12) ...
    Selecting previously unselected package libpq5:amd64.
    Preparing to unpack .../07-libpq5_15.12-0+deb12u2_amd64.deb ...
    Unpacking libpq5:amd64 (15.12-0+deb12u2) ...
    Selecting previously unselected package postgresql-client-15.
    Preparing to unpack .../08-postgresql-client-15_15.12-0+deb12u2_amd64.deb ...
    Unpacking postgresql-client-15 (15.12-0+deb12u2) ...
    Selecting previously unselected package postgresql-15.
    Preparing to unpack .../09-postgresql-15_15.12-0+deb12u2_amd64.deb ...
    Unpacking postgresql-15 (15.12-0+deb12u2) ...
    Selecting previously unselected package postgresql.
    Preparing to unpack .../10-postgresql_15+248_all.deb ...
    Unpacking postgresql (15+248) ...
    Selecting previously unselected package postgresql-contrib.
    Preparing to unpack .../11-postgresql-contrib_15+248_all.deb ...
    Unpacking postgresql-contrib (15+248) ...
    Selecting previously unselected package sysstat.
    Preparing to unpack .../12-sysstat_12.6.1-1_amd64.deb ...
    Unpacking sysstat (12.6.1-1) ...
    Setting up postgresql-client-common (248) ...
    Setting up libpq5:amd64 (15.12-0+deb12u2) ...
    Setting up libcommon-sense-perl:amd64 (3.75-3) ...
    Setting up postgresql-client-15 (15.12-0+deb12u2) ...
    update-alternatives: using /usr/share/postgresql/15/man/man1/psql.1.gz to provide /usr/share/man/man1/psql.1.gz (psql.1.gz) in auto mode
    Setting up libllvm14:amd64 (1:14.0.6-12) ...
    Setting up libtypes-serialiser-perl (1.01-1) ...
    Setting up libjson-perl (4.10000-1) ...
    Setting up sysstat (12.6.1-1) ...
    debconf: unable to initialize frontend: Dialog
    debconf: (TERM is not set, so the dialog frontend is not usable.)
    debconf: falling back to frontend: Readline
    debconf: unable to initialize frontend: Readline
    debconf: (This frontend requires a controlling tty.)
    debconf: falling back to frontend: Teletype
    update-alternatives: using /usr/bin/sar.sysstat to provide /usr/bin/sar (sar) in auto mode
    Setting up libjson-xs-perl (4.030-2+b1) ...
    Setting up postgresql-common (248) ...
    debconf: unable to initialize frontend: Dialog
    debconf: (TERM is not set, so the dialog frontend is not usable.)
    debconf: falling back to frontend: Readline
    debconf: unable to initialize frontend: Readline
    debconf: (This frontend requires a controlling tty.)
    debconf: falling back to frontend: Teletype

    Creating config file /etc/postgresql-common/createcluster.conf with new version
    Building PostgreSQL dictionaries from installed myspell/hunspell packages...
    en_us
    Removing obsolete dictionary files:
    Created symlink /etc/systemd/system/multi-user.target.wants/postgresql.service → /lib/systemd/system/postgresql.service.
    Setting up postgresql-15 (15.12-0+deb12u2) ...
    debconf: unable to initialize frontend: Dialog
    debconf: (TERM is not set, so the dialog frontend is not usable.)
    debconf: falling back to frontend: Readline
    debconf: unable to initialize frontend: Readline
    debconf: (This frontend requires a controlling tty.)
    debconf: falling back to frontend: Teletype
    Creating new PostgreSQL cluster 15/main ...
    /usr/lib/postgresql/15/bin/initdb -D /var/lib/postgresql/15/main --auth-local peer --auth-host scram-sha-256 --no-instructions
    The files belonging to this database system will be owned by user "postgres".
    This user must also own the server process.

    The database cluster will be initialized with locale "en_US.UTF-8".
    The default database encoding has accordingly been set to "UTF8".
    The default text search configuration will be set to "english".

    Data page checksums are disabled.

    fixing permissions on existing directory /var/lib/postgresql/15/main ... ok
    creating subdirectories ... ok
    selecting dynamic shared memory implementation ... posix
    selecting default max_connections ... 100
    selecting default shared_buffers ... 128MB
    selecting default time zone ... Europe/Moscow
    creating configuration files ... ok
    running bootstrap script ... ok
    performing post-bootstrap initialization ... ok
    syncing data to disk ... ok
    update-alternatives: using /usr/share/postgresql/15/man/man1/postmaster.1.gz to provide /usr/share/man/man1/postmaster.1.gz (postmaster.1.gz) in auto mode
    Setting up postgresql-contrib (15+248) ...
    Setting up postgresql (15+248) ...
    Processing triggers for man-db (2.11.2-2) ...
    Processing triggers for libc-bin (2.36-9+deb12u10) ...
    [WARNING/ERROR] 
    WARNING: apt does not have a stable CLI interface. Use with caution in scripts.


    WARNING: apt does not have a stable CLI interface. Use with caution in scripts.

    debconf: unable to initialize frontend: Dialog
    debconf: (TERM is not set, so the dialog frontend is not usable.)
    debconf: falling back to frontend: Readline
    debconf: unable to initialize frontend: Readline
    debconf: (This frontend requires a controlling tty.)
    debconf: falling back to frontend: Teletype
    dpkg-preconfigure: unable to re-open stdin: 

    ====================================================================================================
    [INFO] Executed command: systemctl status postgresql.service
    ● postgresql.service - PostgreSQL RDBMS
        Loaded: loaded (/lib/systemd/system/postgresql.service; enabled; preset: enabled)
        Active: active (exited) since Sun 2025-04-20 23:30:56 MSK; 9s ago
    Main PID: 6690 (code=exited, status=0/SUCCESS)
            CPU: 2ms

    Apr 20 23:30:56 vbox systemd[1]: Starting postgresql.service - PostgreSQL RDBMS...
    Apr 20 23:30:56 vbox systemd[1]: Finished postgresql.service - PostgreSQL RDBMS.
    ====================================================================================================
    [INFO] Executed command: systemctl start postgresql.service
    ====================================================================================================
    [INFO] Executed command: systemctl enable postgresql.service
    Synchronizing state of postgresql.service with SysV service script with /lib/systemd/systemd-sysv-install.
    Executing: /lib/systemd/systemd-sysv-install enable postgresql
    [WARNING/ERROR] Synchronizing state of postgresql.service with SysV service script with /lib/systemd/systemd-sysv-install.
    Executing: /lib/systemd/systemd-sysv-install enable postgresql

    ====================================================================================================
    [DEBUG] Found postgresql.conf: /etc/postgresql/15/main/postgresql.conf
    [DEBUG] Found pg_hba.conf: /etc/postgresql/15/main/pg_hba.conf
    [INFO] Executed command: sudo -i -u postgres psql -c "CREATE USER student WITH PASSWORD 'password';"
    CREATE ROLE
    ====================================================================================================
    [INFO] Executed command: sudo -i -u postgres psql -c "GRANT CONNECT ON DATABASE postgres TO student;"
    GRANT
    ====================================================================================================
    [INFO] Executed command: echo "listen_addresses = '*'" >> /etc/postgresql/15/main/postgresql.conf
    ====================================================================================================
    [INFO] Executed command: echo "host all student 192.168.1.43/32 md5" >> /etc/postgresql/15/main/pg_hba.conf
    ====================================================================================================
    [INFO] Executed command: systemctl restart postgresql.service
    ====================================================================================================
    [INFO] Executed command: systemctl status postgresql.service
    ● postgresql.service - PostgreSQL RDBMS
        Loaded: loaded (/lib/systemd/system/postgresql.service; enabled; preset: enabled)
        Active: active (exited) since Sun 2025-04-20 23:31:10 MSK; 68ms ago
        Process: 7079 ExecStart=/bin/true (code=exited, status=0/SUCCESS)
    Main PID: 7079 (code=exited, status=0/SUCCESS)
            CPU: 3ms

    Apr 20 23:31:10 vbox systemd[1]: Starting postgresql.service - PostgreSQL RDBMS...
    Apr 20 23:31:10 vbox systemd[1]: Finished postgresql.service - PostgreSQL RDBMS.
    ====================================================================================================
    [INFO] Executed command: sudo -i -u postgres psql -c 'SELECT 1;'
    ?column? 
    ----------
            1
    (1 row)

    [INFO] PostgreSQL local verification successful (SELECT 1 returned successfully)
    ====================================================================================================
    [INFO] In target server 192.168.1.43 detected ALMALINUX
    [INFO] Testing connection to target_server 192.168.1.41 with Postgres from 192.168.1.43
    [INFO] Upload test check_postgres.py script and .env to 192.168.1.43...
    [INFO] Running check_postgres.py in 192.168.1.43...
    [INFO] Executed command in 192.168.1.43: dnf check-update && dnf install -y python3 python3-pip
    Последняя проверка окончания срока действия метаданных: 0:28:03 назад, Вс 20 апр 2025 23:03:09.
    Последняя проверка окончания срока действия метаданных: 0:28:05 назад, Вс 20 апр 2025 23:03:09.
    Пакет python3-3.9.21-1.el9_5.x86_64 уже установлен.
    Пакет python3-pip-21.3.1-1.el9.noarch уже установлен.
    Зависимости разрешены.
    Отсутствуют действия для выполнения.
    Выполнено!
    ====================================================================================================
    [INFO] Executed command in 192.168.1.43: mkdir -p /tmp/check_postgres && cd /tmp/check_postgres
    ====================================================================================================
    [INFO] Executed command in 192.168.1.43: mv /tmp/check_postgres.py /tmp/check_postgres/check_postgres.py && mv /tmp/.env /tmp/check_postgres/.env
    ====================================================================================================
    [INFO] Executed command in 192.168.1.43: cd /tmp/check_postgres && python3 -m venv venv
    ====================================================================================================
    [INFO] Executed command in 192.168.1.43: cd /tmp/check_postgres && source ./venv/bin/activate && pip3 install psycopg2-binary dotenv
    Collecting psycopg2-binary
    Using cached psycopg2_binary-2.9.10-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (3.0 MB)
    Collecting dotenv
    Using cached dotenv-0.9.9-py2.py3-none-any.whl (1.9 kB)
    Collecting python-dotenv
    Using cached python_dotenv-1.1.0-py3-none-any.whl (20 kB)
    Installing collected packages: python-dotenv, psycopg2-binary, dotenv
    Successfully installed dotenv-0.9.9 psycopg2-binary-2.9.10 python-dotenv-1.1.0
    WARNING: You are using pip version 21.3.1; however, version 25.0.1 is available.
    You should consider upgrading via the '/tmp/check_postgres/venv/bin/python3 -m pip install --upgrade pip' command.
    [WARNING/ERROR] WARNING: You are using pip version 21.3.1; however, version 25.0.1 is available.
    You should consider upgrading via the '/tmp/check_postgres/venv/bin/python3 -m pip install --upgrade pip' command.

    ====================================================================================================
    [INFO] Executed command in 192.168.1.43: cd /tmp/check_postgres && source ./venv/bin/activate && python3 check_postgres.py 192.168.1.41
    Connection successful!
    Result of query 'SELECT 1': 1
    [INFO] ===== Successful test connection to Postgres =====
    ====================================================================================================
    [INFO] ===== Successful installation and configuration Postgres =====
    ```


2) **Установка `PosgreSQL` на удалённый хост с `AlmaLinux`.** Для этого на другой машине с `Debian` аналогичного была временно запущена команда `yes > /dev/null` для полной загрузки одного ядра процессора. Это было сделано для того, чтобы скрипт точно выбрал в качестве целевого сервера машину с `AlmaLinux`. Вывод из консоли после выполнения срипта представлен ниже.
   
   Для подтверждения проведённого тестирования вывод из консоли после выполнения срипта представлен ниже. Всё было снова **успешно установлено и протестировано** посредством запуска `python`-скрипта для подключения к только что установленному `Postgres` с другого сервера пользователем `student`, что и требует Техническое Задание.
   
    ```
    (venv) ivan@Ivan-Lenovo:~/internships/postgrespro-devops$ python3 deploy_postgres.py 192.168.1.41,192.168.1.43
    [DEBUG] Get loads and target_server {'192.168.1.41': 0.3425, '192.168.1.43': 0.0925} 192.168.1.43
    [INFO] Target server: 192.168.1.43
    [INFO] In target server 192.168.1.43 detected ALMALINUX
    [INFO] Executed command: dnf update && dnf install -y postgresql-server postgresql-contrib
    AlmaLinux 9 - AppStream                         472 kB/s |  16 MB     00:33    
    AlmaLinux 9 - BaseOS                            381 kB/s |  18 MB     00:48    
    AlmaLinux 9 - Extras                             23 kB/s |  13 kB     00:00    
    Extra Packages for Enterprise Linux 9 - x86_64  5.7 MB/s |  23 MB     00:04    
    Extra Packages for Enterprise Linux 9 openh264  1.4 kB/s | 2.5 kB     00:01    
    Зависимости разрешены.
    Отсутствуют действия для выполнения.
    Выполнено!
    Последняя проверка окончания срока действия метаданных: 0:00:07 назад, Вс 20 апр 2025 23:03:09.
    Зависимости разрешены.
    ================================================================================
    Пакет                       Архитектура
                                            Версия              Репозиторий   Размер
    ================================================================================
    Установка:
    postgresql-contrib          x86_64     13.20-1.el9_5       appstream     816 k
    postgresql-server           x86_64     13.20-1.el9_5       appstream     5.7 M
    Установка зависимостей:
    postgresql                  x86_64     13.20-1.el9_5       appstream     1.5 M
    postgresql-private-libs     x86_64     13.20-1.el9_5       appstream     137 k
    uuid                        x86_64     1.6.2-55.el9        appstream      56 k

    Результат транзакции
    ================================================================================
    Установка  5 Пакетов

    Объем загрузки: 8.3 M
    Объем изменений: 32 M
    Загрузка пакетов:
    (1/5): postgresql-private-libs-13.20-1.el9_5.x8 1.6 MB/s | 137 kB     00:00    
    (2/5): postgresql-contrib-13.20-1.el9_5.x86_64. 2.4 MB/s | 816 kB     00:00    
    (3/5): uuid-1.6.2-55.el9.x86_64.rpm             1.8 MB/s |  56 kB     00:00    
    (4/5): postgresql-13.20-1.el9_5.x86_64.rpm      3.1 MB/s | 1.5 MB     00:00    
    (5/5): postgresql-server-13.20-1.el9_5.x86_64.r 1.9 MB/s | 5.7 MB     00:03    
    --------------------------------------------------------------------------------
    Общий размер                                    2.3 MB/s | 8.3 MB     00:03     
    Проверка транзакции
    Проверка транзакции успешно завершена.
    Идет проверка транзакции
    Тест транзакции проведен успешно.
    Выполнение транзакции
    Подготовка       :                                                        1/1 
    Установка        : postgresql-private-libs-13.20-1.el9_5.x86_64           1/5 
    Установка        : postgresql-13.20-1.el9_5.x86_64                        2/5 
    Установка        : uuid-1.6.2-55.el9.x86_64                               3/5 
    Установка        : postgresql-contrib-13.20-1.el9_5.x86_64                4/5 
    Запуск скриптлета: postgresql-server-13.20-1.el9_5.x86_64                 5/5 
    Установка        : postgresql-server-13.20-1.el9_5.x86_64                 5/5 
    Запуск скриптлета: postgresql-server-13.20-1.el9_5.x86_64                 5/5 
    Проверка         : postgresql-13.20-1.el9_5.x86_64                        1/5 
    Проверка         : postgresql-contrib-13.20-1.el9_5.x86_64                2/5 
    Проверка         : postgresql-private-libs-13.20-1.el9_5.x86_64           3/5 
    Проверка         : postgresql-server-13.20-1.el9_5.x86_64                 4/5 
    Проверка         : uuid-1.6.2-55.el9.x86_64                               5/5 

    Установлен:
    postgresql-13.20-1.el9_5.x86_64                                               
    postgresql-contrib-13.20-1.el9_5.x86_64                                       
    postgresql-private-libs-13.20-1.el9_5.x86_64                                  
    postgresql-server-13.20-1.el9_5.x86_64                                        
    uuid-1.6.2-55.el9.x86_64                                                      

    Выполнено!
    ====================================================================================================
    [INFO] Executed command: postgresql-setup --initdb
    * Initializing database in '/var/lib/pgsql/data'
    * Initialized, logs are in /var/lib/pgsql/initdb_postgresql.log
    [WARNING/ERROR]  * Initializing database in '/var/lib/pgsql/data'
    * Initialized, logs are in /var/lib/pgsql/initdb_postgresql.log

    ====================================================================================================
    [INFO] Executed command: systemctl start postgresql.service
    ====================================================================================================
    [INFO] Executed command: systemctl enable postgresql.service
    Created symlink /etc/systemd/system/multi-user.target.wants/postgresql.service → /usr/lib/systemd/system/postgresql.service.
    [WARNING/ERROR] Created symlink /etc/systemd/system/multi-user.target.wants/postgresql.service → /usr/lib/systemd/system/postgresql.service.

    ====================================================================================================
    [DEBUG] Found postgresql.conf: /var/lib/pgsql/data/postgresql.conf
    [DEBUG] Found pg_hba.conf: /var/lib/pgsql/data/pg_hba.conf
    [INFO] Executed command: sudo -i -u postgres psql -c "CREATE USER student WITH PASSWORD 'password';"
    CREATE ROLE
    ====================================================================================================
    [INFO] Executed command: sudo -i -u postgres psql -c "GRANT CONNECT ON DATABASE postgres TO student;"
    GRANT
    ====================================================================================================
    [INFO] Executed command: echo "listen_addresses = '*'" >> /var/lib/pgsql/data/postgresql.conf
    ====================================================================================================
    [INFO] Executed command: echo "host all student 192.168.1.41/32 md5" >> /var/lib/pgsql/data/pg_hba.conf
    ====================================================================================================
    [INFO] Executed command: systemctl restart postgresql.service
    ====================================================================================================
    [INFO] Executed command: systemctl status postgresql.service
    ● postgresql.service - PostgreSQL database server
        Loaded: loaded (/usr/lib/systemd/system/postgresql.service; enabled; preset: disabled)
        Active: active (running) since Sun 2025-04-20 23:03:35 MSK; 160ms ago
        Process: 11182 ExecStartPre=/usr/libexec/postgresql-check-db-dir postgresql (code=exited, status=0/SUCCESS)
    Main PID: 11185 (postmaster)
        Tasks: 8 (limit: 10946)
        Memory: 16.5M
            CPU: 95ms
        CGroup: /system.slice/postgresql.service
                ├─11185 /usr/bin/postmaster -D /var/lib/pgsql/data
                ├─11186 "postgres: logger "
                ├─11188 "postgres: checkpointer "
                ├─11189 "postgres: background writer "
                ├─11190 "postgres: walwriter "
                ├─11191 "postgres: autovacuum launcher "
                ├─11192 "postgres: stats collector "
                └─11193 "postgres: logical replication launcher "

    апр 20 23:03:35 localhost.localdomain systemd[1]: Starting PostgreSQL database server...
    апр 20 23:03:35 localhost.localdomain postmaster[11185]: 2025-04-20 23:03:35.287 MSK [11185] СООБЩЕНИЕ:  передача вывода в протокол процессу сбора протоколов
    апр 20 23:03:35 localhost.localdomain postmaster[11185]: 2025-04-20 23:03:35.287 MSK [11185] ПОДСКАЗКА:  В дальнейшем протоколы будут выводиться в каталог "log".
    апр 20 23:03:35 localhost.localdomain systemd[1]: Started PostgreSQL database server.
    ====================================================================================================
    [INFO] Executed command: sudo -i -u postgres psql -c 'SELECT 1;'
    ?column? 
    ----------
            1
    (1 строка)

    [INFO] PostgreSQL local verification successful (SELECT 1 returned successfully)
    [INFO] Execute commands to configure firewall:
    [INFO] Executed command: systemctl status firewalld.service
    ● firewalld.service - firewalld - dynamic firewall daemon
        Loaded: loaded (/usr/lib/systemd/system/firewalld.service; enabled; preset: enabled)
        Active: active (running) since Sun 2025-04-20 22:53:14 MSK; 10min ago
        Docs: man:firewalld(1)
    Main PID: 7963 (firewalld)
        Tasks: 4 (limit: 10946)
        Memory: 22.4M
            CPU: 3.611s
        CGroup: /system.slice/firewalld.service
                └─7963 /usr/bin/python3 -s /usr/sbin/firewalld --nofork --nopid

    апр 20 22:53:14 localhost.localdomain systemd[1]: Starting firewalld - dynamic firewall daemon...
    апр 20 22:53:14 localhost.localdomain systemd[1]: Started firewalld - dynamic firewall daemon.
    апр 20 22:53:17 localhost.localdomain firewalld[7963]: ERROR: INVALID_RULE: no element, no action
    ====================================================================================================
    [INFO] Executed command: systemctl start firewalld.service
    ====================================================================================================
    [INFO] Executed command: firewall-cmd --zone=public --add-port=5432/tcp --permanent
    success
    ====================================================================================================
    [INFO] Executed command: firewall-cmd --zone=public --add-service=ssh --permanent
    Warning: ALREADY_ENABLED: ssh
    success
    [WARNING/ERROR] Warning: ALREADY_ENABLED: ssh

    ====================================================================================================
    [INFO] Executed command: firewall-cmd --reload
    success
    ====================================================================================================
    [INFO] Executed command: firewall-cmd --list-ports
    5432/tcp
    ====================================================================================================
    ====================================================================================================
    [INFO] In target server 192.168.1.41 detected DEBIAN
    [INFO] Testing connection to target_server 192.168.1.43 with Postgres from 192.168.1.41
    [INFO] Upload test check_postgres.py script and .env to 192.168.1.41...
    [INFO] Running check_postgres.py in 192.168.1.41...
    [INFO] Executed command in 192.168.1.41: apt update && apt install -y python3-full python3-venv python3-pip

    WARNING: apt does not have a stable CLI interface. Use with caution in scripts.

    Hit:1 http://security.debian.org/debian-security bookworm-security InRelease
    Hit:2 http://deb.debian.org/debian bookworm InRelease
    Hit:3 http://deb.debian.org/debian bookworm-updates InRelease
    Reading package lists...
    Building dependency tree...
    Reading state information...
    18 packages can be upgraded. Run 'apt list --upgradable' to see them.

    WARNING: apt does not have a stable CLI interface. Use with caution in scripts.

    Reading package lists...
    Building dependency tree...
    Reading state information...
    python3-full is already the newest version (3.11.2-1+b1).
    python3-venv is already the newest version (3.11.2-1+b1).
    python3-pip is already the newest version (23.0.1+dfsg-1).
    0 upgraded, 0 newly installed, 0 to remove and 18 not upgraded.
    [WARNING/ERROR] 
    WARNING: apt does not have a stable CLI interface. Use with caution in scripts.


    WARNING: apt does not have a stable CLI interface. Use with caution in scripts.


    ====================================================================================================
    [INFO] Executed command in 192.168.1.41: mkdir -p /tmp/check_postgres && cd /tmp/check_postgres
    ====================================================================================================
    [INFO] Executed command in 192.168.1.41: mv /tmp/check_postgres.py /tmp/check_postgres/check_postgres.py && mv /tmp/.env /tmp/check_postgres/.env
    ====================================================================================================
    [INFO] Executed command in 192.168.1.41: cd /tmp/check_postgres && python3 -m venv venv
    ====================================================================================================
    [INFO] Executed command in 192.168.1.41: cd /tmp/check_postgres && source ./venv/bin/activate && pip3 install psycopg2-binary dotenv
    Collecting psycopg2-binary
    Using cached psycopg2_binary-2.9.10-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (3.0 MB)
    Collecting dotenv
    Using cached dotenv-0.9.9-py2.py3-none-any.whl (1.9 kB)
    Collecting python-dotenv
    Using cached python_dotenv-1.1.0-py3-none-any.whl (20 kB)
    Installing collected packages: python-dotenv, psycopg2-binary, dotenv
    Successfully installed dotenv-0.9.9 psycopg2-binary-2.9.10 python-dotenv-1.1.0
    ====================================================================================================
    [INFO] Executed command in 192.168.1.41: cd /tmp/check_postgres && source ./venv/bin/activate && python3 check_postgres.py 192.168.1.43
    Connection successful!
    Result of query 'SELECT 1': 1
    [INFO] ===== Successful test connection to Postgres =====
    ====================================================================================================
    [INFO] ===== Successful installation and configuration Postgres =====
    ```
