## Abstract
'''''''''''''''**ADD ABSTRACT**'''''''''''''''

##
![GIF](demo.gif)

## Project Structure

- `Development/` # Development environment: data, scraping and training scripts, models
    - `data/` # Sample training data
    - `models/` # Trained model files
    - `src/` # Source code for scraping and training

- `Pipeline/` # Scripts and configs for deployment orchestration (Ansible and Cloud-init setup)

- `Production/` # Web app and production-serving logic (Flask app, Docker setup)
    - `static/` # JS static frontend assets
    - `templates/` # HTML templates for the web interface


## How to deploy

1. **Login to the Client machine**

    ```bash
    ssh -i <PRIVATE KEY> ubuntu@<PRODUCTION-SERVER-IP>
    ```

2. **Install Ansible on the Client machine**

    ```bash
    sudo bash
    ```
    ```bash
    apt-add-repository ppa:ansible/ansible
    ```
    ```bash
    apt update
    ```
    ```bash
    apt install ansible
    ```

3. **Clone the GitHub repository**

    ```bash
    git clone https://github.com/vfe01/DE2-group-13-project.git
    ```

4. **Configure Ansible on the Client machine**
    
    Create a directory to store the cluster ssh keys. You need to be as a *non-root* user.

    ```bash
    mkdir -p /home/ubuntu/cluster-keys
    ```

    Generate the cluster ssh keys.

    ```bash
    ssh-keygen -t rsa
    ```

    When asked, set the file path `/home/ubuntu/cluster-keys/cluster-key`. Do not set the password, simply press Enter twice.

    The keys will be generated and stored at the following location:

    - Private key: `/home/ubuntu/cluster-keys/cluster-key`

    - Public key: `/home/ubuntu/cluster-keys/cluster-key.pub`

    Copy the complete contents of your generated Public key (`cluster-key.pub`) to `ssh_authorized_keys:` section in both `Pipeline/dev-cloud-cfg.txt` and `Pipeline/prod-cloud-cfg.txt`.

5. **Setup OpenStack API environment**

    In order to run the script to launch the VMs, you need to have OpenStack API environment running.

    Download the Runtime Configuration (RC) file (version 3) from the SSC site (Top left frame, Project->API Access->Download OpenStack RC File). Confirm that it has the following variables:

    ```
    export OS_USER_DOMAIN_NAME="snic"
    export OS_IDENTITY_API_VERSION="3"
    export OS_PROJECT_DOMAIN_NAME="snic"
    export OS_PROJECT_NAME="SNIC 2021/18-43"
    ```

    Set the environment variables by sourcing the RC-file.

    ```bash
    source <project_name>_openrc.sh
    ```
    
    *NOTE: You need to enter the API access passward.*

    Install the following packages for API communication:

    ```bash
    sudo apt install python3-openstackclient
    ```
    
    ```bash
    sudo apt install python3-novaclient
    ```

    ```bash
    sudo apt install python3-keystoneclient
    ```

    Check that you have the correct packages available on your Client VM.

    ```
    openstack server list
    ```

    ```
    openstack image list
    ```
    *You should get a list with the existent servers and images, respectively.*

6. **Launch Development and Production machines**

    Run `start_instances.py` script on the Client machine.

    ```bash
    python3 start_instances.py
    ```

    In the output you will see the internal IP addresses of the Development and Production machines. They will be saved to the file `ip_addresses.json`.

    Add these IPs to the Ansible hosts file `/etc/ansible/hosts`.

    ```bash
    sudo vi /etc/ansible/hosts
    ```

    Modify or add these lines in the file.

    ```
    [servers]
    prod_server ansible_host=<production server IP address>
    dev_server ansible_host=<development server IP address>

    [all:vars]
    ansible_python_interpreter=/usr/bin/python3

    [prod_server]
    prod_server ansible_connection=ssh ansible_user=appuser

    [dev_server]
    dev_server ansible_connection=ssh ansible_user=appuser
    ```

    To check the configuration and permissions are correctly set, you can try to access Production and Development servers from the Client machine.

    As a *non-root* user, ssh to the Production VM. You should be able to login.

    ```bash
    ssh -i /home/ubuntu/cluster-keys/cluster-key appuser@<PRODUCTION-SERVER-IP>
    ```

    Exit the Production VM and try the same with the Development one.

    ```bash
    ssh -i /home/ubuntu/cluster-keys/cluster-key appuser@<DEVELOPMENT-SERVER-IP>
    ```

    If both logins have been successful, your Ansible configuration is correctly set.

7. **Run Ansible Playbook**

    Since this is a private repository, only collaborators have access to work with it. Therefore, some configuration is required before running the Ansible Playbook.

    First, set up your GitHub username and email to properly configure commit settings on the development server.

    ```bash
    export GITHUB_USER="<YOUR_GITHUB_USER>"
    ```

    ```bash
    export GITHUB_EMAIL="<YOUR_GITHUB_EMAIL>"
    ```

    You can configure the GitHub connection through SSH or with a Personal Access Token (PAT).

    **Option 1: Using a GitHub Personal Access Token**

    To create a Personal Access Token:

    1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)

    2. Click "Generate new token"

    3. Select scopes: repo (for private repositories)

    4. Copy the token (you won't see it again!)

    *Note: The token should look like: ghp_xxxxxxxxxxxxxxxxxxxx*

    Once the token has been created, we have to set it up as an environment variable in the Client machine.

    ```bash
    export GITHUB_TOKEN="<YOUR_GITHUB_PAT>"
    ```

    ```bash
    export ANSIBLE_HOST_KEY_CHECKING=False
    ```

    When using a Personal Access Token the playbook `configuration_w_token.yml` should be run.

    ```bash
    ansible-playbook Pipeline/configuration_w_token.yml --private-key=/home/ubuntu/cluster-keys/cluster-key
    ```

    The process will take around 10 to 15 minutes to complete. The progress can be seen on the cloud dashboard.

    **Option 2: Using SSH**

    '''''''''''''''**ADD STEPS**'''''''''''''''


    When using the SSH the playbook `configuration_w_ssh.yml` should be run.

    ```bash
    export ANSIBLE_HOST_KEY_CHECKING=False
    ```

    ```bash
    ansible-playbook Pipeline/configuration_w_ssh.yml --private-key=/home/ubuntu/cluster-keys/cluster-key
    ```

    The process will take around 10 to 15 minutes to complete. The progress can be seen on the cloud dashboard.

8. **Access the web-app**

    Once the Production and Development VMs are completely configured, associate a floating IP to the Production machine. Then, you can access the web-app from the client machine.

    `http://<PRODUCTION-SERVER-FLOATING-IP>:5100`

## Development Configuration

For setting up the development environment, see [`Development/README.md`](Development/README.md).
