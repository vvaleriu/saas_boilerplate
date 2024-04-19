#!/usr/bin/env python3
import os
import subprocess
import sys
import pathlib
import random
import string

# Define default values
# DEFAULT_HOST_PORT = 8000
DEFAULT_WEB_FOLDER = "web"
SUPABASE_DEFAULT_PROJECT_NAME = "saas"
DEFAULT_POSTGRES_PASSWORD = "your-super-secret-and-long-postgres-password"
DEFAULT_POSTGRES_HOST = "db"
DEFAULT_POSTGRES_DB = "postgres"
DEFAULT_POSTGRES_PORT = 5432
DEFAULT_DISABLE_SIGNUP = 'true'
DEFAULT_DASHBOARD_USERNAME = 'supabase'
DEFAULT_DASHBOARD_PASSWORD = 'supabase123'
DEFAULT_ADMINER_HOST_PORT = 14519

# Define a list of variables with their expected type and default value
ENV = {
    "WEB_FOLDER": {"name": "WEB_FOLDER", "type": str, "value": DEFAULT_WEB_FOLDER},
    "STUDIO_DEFAULT_PROJECT": {"name": "STUDIO_DEFAULT_PROJECT", "type": str, "value": SUPABASE_DEFAULT_PROJECT_NAME},
    "POSTGRES_HOST": {"name": "POSTGRES_HOST", "type": str, "value": DEFAULT_POSTGRES_HOST},
    "POSTGRES_PORT": {"name": "POSTGRES_PORT", "type": int, "value": DEFAULT_POSTGRES_PORT},
    "POSTGRES_DB": {"name": "POSTGRES_DB", "type": str, "value": DEFAULT_POSTGRES_DB},
    "POSTGRES_PASSWORD": {"name": "POSTGRES_PASSWORD", "type": str, "value": DEFAULT_POSTGRES_PASSWORD},
    "DISABLE_SIGNUP": {"name": "DISABLE_SIGNUP", "type": str, "value": DEFAULT_DISABLE_SIGNUP},
    "DASHBOARD_USERNAME": {"name": "DASHBOARD_USERNAME", "type": str, "value": DEFAULT_DASHBOARD_USERNAME},
    "DASHBOARD_PASSWORD": {"name": "DASHBOARD_PASSWORD", "type": str, "value": DEFAULT_DASHBOARD_PASSWORD},
    "ADMINER_HOST_PORT": {"name": "ADMINER_HOST_PORT", "type": int, "value": DEFAULT_ADMINER_HOST_PORT},
}

# Create a dictionary to store the user input values
# supabase_user_input_values = {
#     'STUDIO_DEFAULT_PROJECT': '',
#     # 'HOST_PORT': DEFAULT_HOST_PORT,
#     'POSTGRES_PASSWORD': DEFAULT_POSTGRES_PASSWORD,
#     'POSTGRES_HOST': DEFAULT_POSTGRES_HOST,
#     'POSTGRES_DB': DEFAULT_POSTGRES_DB,
#     'POSTGRES_PORT': DEFAULT_POSTGRES_PORT,
#     'DISABLE_SIGNUP': DEFAULT_DISABLE_SIGNUP,
#     'DASHBOARD_USERNAME': DEFAULT_DASHBOARD_USERNAME,
#     'DASHBOARD_PASSWORD': DEFAULT_DASHBOARD_PASSWORD,
#     'ADMINER_HOST_PORT': DEFAULT_ADMINER_HOST_PORT,
# }

OVERRIDE_DEFAULT = False
SUPABASE_PATH = pathlib.Path(__file__).parent.resolve()

## Manage supabase variables values

# ###########################
# FRONT
# ###########################

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)

def get_user_input(env):
    """
    Function to get user input for each environment variable and validate the data type.

    :param env: list of dictionaries representing the environment variables
    :return: updated list with user inputs or the original list if no updates were made
    """

    for key, val in env.items():
        # name = val["name"]
        current_value = val["value"]
        data_type = val["type"]

        new_value = input(f"Enter value for {key} [default: {current_value}]: ")

        if data_type == str:
            try:
                new_value = eval(new_value)
                raise TypeError()
            except (SyntaxError, NameError, TypeError):
                pass  # Valid input as a string
            else:
                print(f"Invalid input for {key}. Current value '{current_value}' will be used.")
                continue
            
        elif data_type == int:
            try:
                new_value = int(new_value)
            except ValueError:
                print(f"Invalid input for {key}. Current value '{current_value}' will be used.")
                continue

        if new_value:
            val["value"] = new_value

    for key, val in env.items():
        print(f"{key}: {val['value']} ({val['type']})")
    return env

def setup_repos(env):
    """
    Parameters:
    directory (str): directory the repo will be cloned in
    url (str): repo url to be cloned as a subtree
    """
    os.chdir(pathlib.Path(__file__).parent.resolve())
    print(f'Repo as "CMSaasStarter.git" a subtree')
    subprocess.run(["git", "subtree", "add", f"--prefix={env['WEB_FOLDER']['value']}", "--squash", 'https://github.com/CriticalMoments/CMSaasStarter.git', 'extension/internationalization'])
    print(f'SUPABASE')
    subprocess.run(["git", "clone", "--depth", "1", 'https://github.com/supabase/supabase.git'])

# ###########################
# SUPABASE RELATIVE SCRIPTS
# ###########################


def setup_supabase(env):
    os.chdir(os.path.join(pathlib.Path(__file__).parent.resolve(), "supabase/docker"))
    subprocess.run(["cp", ".env.example", ".env"])

    env_names = (o['name'] for o in env)
    
    # CHANGE SUPABASE VALUES
    with open('.env', 'r+') as file:
        # Read the content of the file
        content = file.readlines()
    
        # Go to the beginning of the file to overwrite it later
        file.seek(0)
        
        # Loop through each line in the file
        for line in content:
            # Split the line into the variable name and its value
            if '=' in line:
                variable, value = line.strip().split('=')
                
                # Check if the variable is in the input_values dictionary
                if variable in env.keys():
                    # Replace the value with the one from the dictionary
                    line = f"{variable}={env[variable]['value']}\n"
            
            # Write the line back to the file
            file.write(line)
        file.close()

    # ADD ADMINER (postgres admin panl) ENV VALUES
    with open('.env', 'a') as file:
        file.write('\n############')
        file.write('\n# Personnal ENV variables')
        file.write('\n############')
        file.write(f"\nADMINER_HOST_PORT={env['ADMINER_HOST_PORT']['value']}\n")
        file.close()
    print('Copie et modification du fichier supabase/docker/.env')

def setup_docker_file(path):
    os.chdir(os.path.join(path, "supabase/docker"))
    with open('docker-compose.yml', 'r') as file:
        lines = file.readlines()

    # Open the file in write mode
    with open('docker-compose.yml', 'w') as file:
        for line in lines:
            if "services:" in line:
                file.write('''
services:
  # Manually added to manage postgresql db
  adminer:
    image: adminer
    restart: always
    ports:
      - ${ADMINER_HOST_PORT}:8080\n
                ''')
            else:
                file.write(line)
    file.close()
    print('Modification du supabase/docker/docker-compose.yml pour ajouter adminer (interface admin postgres)')

def main():
    global ENV

    OVERRIDE_DEFAULT = input(f"Override default supabase values ? [y/N]")
    if OVERRIDE_DEFAULT in ['y', 'Y']:
        ENV = get_user_input(ENV)

    setup_repos(ENV)
    setup_supabase(ENV)
    sys.exit()
    setup_env_file(PROJECT_PATH)
    setup_docker_file(PROJECT_PATH)
    print(f'''
Le projet est maintenant prêt à être lancé.
Voir "https://supabase.com/docs/guides/self-hosting/docker" pour plus d'information.
Pour lancer le projet :
cd {PROJECT_PATH}

# Pull the latest images
docker compose pull

# Start the services (in detached mode)
docker compose up -d
          ''')

if __name__ == "__main__":
    main()