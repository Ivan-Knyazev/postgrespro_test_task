import os
import sys
from fabric import Connection
from invoke import UnexpectedExit
from dotenv import load_dotenv


def get_env() -> dict[str]:
    """Get ENVs from .env file."""
    load_dotenv()

    key_path = os.getenv("PRIVATE_KEY_PATH")
    try:
        ssh_port = int(os.getenv("SSH_PORT"))
    except ValueError:
        print("Error! SSH_PORT must be an int")
        sys.exit(1)
    postgres_user = os.getenv("POSTGRES_USER")
    postgres_pwd = os.getenv("POSTGRES_PASSWORD")

    envs = {
        "path": key_path,
        "port": ssh_port,
        "user": postgres_user,
        "pwd": postgres_pwd,
    }

    return envs


def get_server_load(server_ip: str, envs: dict[str]) -> float | None:
    """Get load of server."""
    try:
        conn = Connection(
            host=server_ip,
            user="root",
            port=envs["port"],
            connect_kwargs={"key_filename": envs["path"]},
        )

        load_avg = conn.run("cat /proc/loadavg | awk '{print $1}'", hide=True)
        load_avg = float(load_avg.stdout.strip())

        nproc = conn.run("nproc", hide=True)
        nproc = int(nproc.stdout.strip())

        normalized_load = load_avg / nproc

        return normalized_load

    except Exception as e:
        print(f"Error when connecting to server {server_ip}: {e}")
        return None


def get_target_server(servers: list[str], envs: dict[str]) -> str | None:
    """Calculate target server (with min load)."""
    loads = {
        server: get_server_load(server_ip=server, envs=envs)
        for server in servers
        if get_server_load(server_ip=server, envs=envs) is not None
    }

    if not loads:
        print("Couldn't get download from any of the servers.")
        sys.exit(1)

    target_server = min(loads, key=lambda host: loads[host])
    print("[DEBUG] Get loads and target_server", loads, target_server)
    return target_server


def detect_os(server_ip: str, conn: Connection) -> str | None:
    """Detect server OS (Debian vs Almalinux)."""
    try:
        result = conn.run("cat /etc/os-release", hide=True)
        output = result.stdout.lower()
        if "debian" in output or "ubuntu" in output:
            print(f"[INFO] In target server {server_ip} detected DEBIAN")
            return "debian"
        elif "almalinux" in output or "centos" in output:
            print(f"[INFO] In target server {server_ip} detected ALMALINUX")
            return "almalinux"
        else:
            print("[ERROR] Unsupported OS detected in", server_ip)
            return None
    except Exception as e:
        print(f"Error execute command or connect to server {server_ip}: {e}")
        return None


def get_config_files(conn: Connection, os_family: str) -> dict[str, str] | None:
    """Get full paths for postgres config files (postgresql.conf, pg_hba.conf)."""
    try:
        result_conf = conn.run(
            "sudo -u postgres psql -t -P format=unaligned -c 'show config_file;'",
            hide=True,
        )
        conf_file = result_conf.stdout.strip()

        result_hba = conn.run(
            "sudo -u postgres psql -t -P format=unaligned -c 'show hba_file;'",
            hide=True,
        )
        hba_file = result_hba.stdout.strip()

        if not conf_file or not hba_file:
            raise ValueError("Could not retrieve config file paths from PostgreSQL.")

        print("[DEBUG] Found postgresql.conf:", conf_file)
        print("[DEBUG] Found pg_hba.conf:", hba_file)
        return {"config_file": conf_file, "hba_file": hba_file}
    except ValueError:
        if os_family == "debian":
            try:
                version_dir = (
                    conn.run("ls /etc/postgresql/", hide=True).stdout.strip().split()[0]
                )
                conf_file = f"/etc/postgresql/{version_dir}/main/postgresql.conf"
                hba_file = f"/etc/postgresql/{version_dir}/main/pg_hba.conf"
                print("[DEBUG] Found postgresql.conf:", conf_file)
                print("[DEBUG] Found pg_hba.conf:", hba_file)
                return {"config_file": conf_file, "hba_file": hba_file}
            except Exception as e:
                print("[ERROR] Not found conf files: ", e)
                return None
        elif os_family == "almalinux":
            data_dir = "/var/lib/pgsql/data"
            if conn.run(f"sudo test -d {data_dir}", warn=True).ok:
                conf_file = f"{data_dir}/postgresql.conf"
                hba_file = f"{data_dir}/pg_hba.conf"
                print("[DEBUG] Found postgresql.conf:", conf_file)
                print("[DEBUG] Found pg_hba.conf:", hba_file)
                return {"config_file": conf_file, "hba_file": hba_file}
            else:
                print("[ERROR] Not found conf files: ", e)
                return None
        else:
            return None
    except Exception as e:
        print("[ERROR] Not found conf files: ", e)
        return None


def install_postgresql(server_ip: str, envs: dict[str], second_server_ip: str) -> bool:
    """Install PostgreSQL to target server and configure it."""
    try:
        conn = Connection(
            host=server_ip,
            user="root",
            port=envs["port"],
            connect_kwargs={"key_filename": envs["path"]},
        )
        os_family = detect_os(server_ip=server_ip, conn=conn)
        if os_family is None:
            return False

        commands_for_install = [
            (
                "apt update && apt install -y postgresql postgresql-contrib"
                if os_family == "debian"
                else "dnf update && dnf install -y postgresql-server postgresql-contrib"
            ),
            (
                "systemctl status postgresql.service"
                if os_family == "debian"
                else "postgresql-setup --initdb"
            ),
            "systemctl start postgresql.service",
            "systemctl enable postgresql.service",
        ]
        for command in commands_for_install:
            print("[INFO] Executed command:", command)
            result = conn.run(command)  # hide=True - for delete output to console
            if len(result.stderr.strip()) != 0:
                print("[WARNING/ERROR]", result.stderr)
            # print(result.stdout.strip())
            print("=" * 100)

        config_files = get_config_files(conn=conn, os_family=os_family)
        if config_files is None:
            return False

        commands_for_configure = [
            f"sudo -i -u postgres psql -c \"CREATE USER {envs['user']} WITH PASSWORD '{envs['pwd']}';\"",
            f"sudo -i -u postgres psql -c \"GRANT CONNECT ON DATABASE postgres TO {envs['user']};\"",
            f"echo \"listen_addresses = '*'\" >> {config_files['config_file']}",
            f"echo \"host all {envs['user']} {second_server_ip}/32 md5\" >> {config_files['hba_file']}",
            "systemctl restart postgresql.service",
            "systemctl status postgresql.service",
            "sudo -i -u postgres psql -c 'SELECT 1;'",
        ]

        for command in commands_for_configure:
            print("[INFO] Executed command:", command)
            result = conn.run(command)  # hide=True - for delete output to console
            if len(result.stderr.strip()) != 0:
                print("[WARNING/ERROR]", result.stderr)

            if "SELECT" in command:
                if (
                    "1 row" in result.stdout
                    or "1 строка" in result.stdout
                    or result.stdout.strip() == "1"
                ):
                    print(
                        "[INFO] PostgreSQL local verification successful (SELECT 1 returned successfully)"
                    )
                    if os_family == "almalinux":
                        firewall_commands = [
                            "systemctl status firewalld.service",
                            "systemctl start firewalld.service",
                            "firewall-cmd --zone=public --add-port=5432/tcp --permanent",
                            "firewall-cmd --zone=public --add-service=ssh --permanent",
                            "firewall-cmd --reload",
                            "firewall-cmd --list-ports",
                        ]
                        print("[INFO] Execute commands to configure firewall:")
                        for command in firewall_commands:
                            print("[INFO] Executed command:", command)
                            result = conn.run(
                                command
                            )  # hide=True - for delete output to console
                            if len(result.stderr.strip()) != 0:
                                print("[WARNING/ERROR]", result.stderr)
                            print("=" * 100)
                else:
                    print(
                        f"[INFO] PostgreSQL local verification command ran, but output unexpected: {result.stdout}"
                    )
                    return False
            print("=" * 100)

        conn2 = Connection(
            host=second_server_ip,
            user="root",
            port=envs["port"],
            connect_kwargs={"key_filename": envs["path"]},
        )
        os_family = detect_os(server_ip=second_server_ip, conn=conn2)

        check_connection(
            second_server=second_server_ip,
            target_server=server_ip,
            envs=envs,
            os_family=os_family,
        )
        return True

    except UnexpectedExit as e:
        print(f"Command execution error on {server_ip}:", e)
        return False


def check_connection(
    second_server: str, target_server: str, envs: dict[str], os_family: str
):
    """Check connection to target_server from second_server."""
    try:
        print(
            f"[INFO] Testing connection to target_server {target_server} with Postgres from {second_server}"
        )
        conn = Connection(
            host=second_server,
            user="root",
            port=envs["port"],
            connect_kwargs={"key_filename": envs["path"]},
        )

        # Upload files
        local_script_path = "check_postgres.py"
        remote_script_path = "/tmp/check_postgres.py"
        print(
            f"[INFO] Upload test check_postgres.py script and .env to {second_server}..."
        )
        conn.put(local_script_path, remote_script_path)
        conn.put(".env", "/tmp/.env")

        print(f"[INFO] Running check_postgres.py in {second_server}...")
        commands = [
            (
                "apt update && apt install -y python3-full python3-venv python3-pip"
                if "debian" == os_family
                else "dnf check-update && dnf install -y python3 python3-pip"
            ),
            "mkdir -p /tmp/check_postgres && cd /tmp/check_postgres",
            "mv /tmp/check_postgres.py /tmp/check_postgres/check_postgres.py && mv /tmp/.env /tmp/check_postgres/.env",
            "cd /tmp/check_postgres && python3 -m venv venv",
            "cd /tmp/check_postgres && source ./venv/bin/activate && pip3 install psycopg2-binary dotenv",
            f"cd /tmp/check_postgres && source ./venv/bin/activate && python3 check_postgres.py {target_server}",
        ]

        for command in commands:
            print(f"[INFO] Executed command in {second_server}:", command)
            result = conn.run(command)  # hide=True - for delete output to console
            if len(result.stderr.strip()) != 0:
                print("[WARNING/ERROR]", result.stderr)
            # print(result.stdout.strip())
            print("=" * 100)

        # Delete files
        conn.run("rm -rf /tmp/check_postgres")

    except Exception as e:
        print(f"Error in check connection on {second_server}:", e)


def main():
    """Main function for step-by-step complete all tasks."""
    if len(sys.argv) != 2:
        print("Incorrect usage!")
        print("Usage: python deploy_postgres.py <server1_ip,server2_ip>")
        sys.exit(1)

    servers = sys.argv[1].split(",")
    envs = get_env()
    target_server = get_target_server(servers=servers, envs=envs)
    second_server = [server for server in servers if server != target_server][0]
    print(f"[INFO] Target server: {target_server}")

    status = install_postgresql(
        server_ip=target_server, envs=envs, second_server_ip=second_server
    )
    if status:
        print("[INFO] ===== Successful installation and configuration Postgres =====")
    else:
        print(
            "[ERRROR] ===== Error when installation and configuration Postgres! ====="
        )


if __name__ == "__main__":
    main()

    ## For testing connection from remote host
    # envs = get_env()
    # print("[INFO] Target server: 192.168.1.41")
    # check_connection(
    #     second_server="192.168.1.41",
    #     target_server="192.168.1.43",
    #     envs=envs,
    #     os_family="debian",
    # )
