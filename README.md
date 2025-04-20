# Установка Postgres на удалённые сервера (Тестовое задание в PostgresPro, направление DevOps)

## Тестирвоание работоспособности решения

Для тестирования решения на локальном ПК необходимо иметь гипервизор второго типа, на котором будут запущены необходимые виртуальные машины. Затем нужно удостовериться в доступности данных хостов, создать ssh-ключи, их открытую часть перебросить на виртуальные машины. После чего можно будет запускать скрипт.

## Start system

```bash
python3 deploy_postgres.py <ip_server_1>,<ip_server_2>
```

## Testing

Info about testing in [result.md](./result.md)

<hr>

У меня тестирование локальное происходило посредством запуска написанного скрипта из WSL, установленной на OS Windows 11. На VirtualBox были установлены VM с Debian и AlmaLinux.

```bash
python3 deploy_postgres.py 192.168.1.41,192.168.1.43
```


## Some Commands for testing
```
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

ssh-copy-id -i ~/.ssh/id_rsa.pub root@server1_ip
ssh-copy-id -i ~/.ssh/id_rsa.pub root@server2_ip

# To connect
ssh root@server1_ip
ssh root@server2_ip
```
