import paramiko
import json


private_key = None


def is_directory_exists(ssh, remote_directory):
    command = f"cd {remote_directory} && [ -d .git ] && echo 'Git' || ([ -d .svn ] && echo 'Svn' || echo 'Not git or svn') "
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode().strip()
    return output


def get_git_branch(sftp, git_directory):
    stdin, stdout, stderr = sftp.exec_command(f"cd {git_directory} && git symbolic-ref --short HEAD")
    branch_name = stdout.read().decode().strip()
    return branch_name


def get_git_revision(sftp, git_directory):
    stdin, stdout, stderr = sftp.exec_command(f"cd {git_directory} && git rev-parse HEAD")
    revision = stdout.read().decode().strip()
    return revision


def get_svn_branch(sftp, svn_directory):
    stdin, stdout, stderr = sftp.exec_command(f"cd {svn_directory} && svn info --show-item url")
    url = stdout.read().decode().strip()
    branch_name = url.split("/")[-1]
    return branch_name


def get_svn_revision(sftp, svn_directory):
    stdin, stdout, stderr = sftp.exec_command(f"cd {svn_directory} && svn info --show-item revision")
    revision = stdout.read().decode().strip()
    return revision


def update_json_data(data, repository_info):
    data["branch"] = repository_info.get("branch")
    data["revision"] = repository_info.get("revision")


def establish_ssh_connection(hostname, username, password, key_path=None):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        if key_path:
            ssh.connect(hostname, username=username, password=password, key_filename=key_path)
            print("SSH connection established using SSH key!")
        else:
            ssh.connect(hostname, username=username, password=password)
            print("SSH connection established using username and password!")

        return ssh

    except paramiko.AuthenticationException:
        print("Authentication failed. Please check the username and password.")
    except paramiko.SSHException as e:
        print("SSH connection failed:", str(e))

    return None


def retrieve_repository_info(ssh, remote_directory):
    repository = is_directory_exists(ssh, remote_directory)

    # Собираем информацию о рабочей копии, а именно:
    # Для git узнаём за какой веткой следит данная рабочая копия и на какой ревизии она находится.
    # Для subversion узнаём какая ветка находится в рабочей копии и на какой ревизии.
    if repository == "Git":
        branch = get_git_branch(ssh, remote_directory)
        revision = get_git_revision(ssh, remote_directory)
        repository_info = {"branch": branch, "revision": revision}
    elif repository == "Svn":
        branch = get_svn_branch(ssh, remote_directory)
        revision = get_svn_revision(ssh, remote_directory)
        repository_info = {"branch": branch, "revision": revision}
    else:
        repository_info = None

    return repository_info


def login():
    with open("data.json") as f:
        data = json.load(f)

    # Проходим по всем пользователям из JSON
    for cluster in data["hosts"].values():
        user = cluster["user"]
        host = cluster["host"]

        #  Авторизация на ssh host может происходить либо по ssh ключу, либо по password, который равен user,
        # то есть для пользователя user1, пароль user1, если у пользователя нет ключа.
        if private_key is not None:
            ssh = establish_ssh_connection(hostname=host, username=user, password=user, key_path=private_key)
        else:
            ssh = establish_ssh_connection(hostname=host, username=user, password=user)

        if ssh is not None:
            # У каждого пользователя user в директории ~/bw/ может быть рабочая копия git или subversion.
            remote_directory = "~/bw"
            repository_info = retrieve_repository_info(ssh, remote_directory)
            ssh.close()

            for key, value in repository_info.items():
                cluster[key] = value

    # Добавляем в изначальный JSON собранную информацию из папок на сервере
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)


login()
