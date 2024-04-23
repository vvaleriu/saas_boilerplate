#!/usr/bin/env python3
import os
import subprocess
import sys
import pathlib
import random
import string
import re

# Define default values
# DEFAULT_HOST_PORT = 8000
DEFAULT_WEB_FOLDER = "web"
SUPABASE_DEFAULT_PROJECT_NAME = "saas"
DEFAULT_DOCKER_NETWORK_NAME = "saas"
DEFAULT_POSTGRES_PASSWORD = "postgres123"
DEFAULT_POSTGRES_HOST = "db"
DEFAULT_POSTGRES_DB = "postgres"
DEFAULT_POSTGRES_PORT = 5432
DEFAULT_DISABLE_SIGNUP = 'true'
DEFAULT_DASHBOARD_USERNAME = 'supabase'
DEFAULT_DASHBOARD_PASSWORD = 'supabase123'
DEFAULT_ADMINER_HOST_PORT = 14519
DEFAULT_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ewogICJyb2xlIjogImFub24iLAogICJpc3MiOiAic3VwYWJhc2UiLAogICJpYXQiOiAxNzA0NDA5MjAwLAogICJleHAiOiAxODYyMjYyMDAwCn0.-f1yFYT-yKZBO7wIuch8WjZ-JOCTVmW9blD1gzLbh7A"
DEFAULT_SERVICE_ROLE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ewogICJyb2xlIjogInNlcnZpY2Vfcm9sZSIsCiAgImlzcyI6ICJzdXBhYmFzZSIsCiAgImlhdCI6IDE3MDQ0MDkyMDAsCiAgImV4cCI6IDE4NjIyNjIwMDAKfQ.yzJYfNC1JNgc6mTuP0bRjY4--BWwu2WfmURsrP6iFT0"

# Define a list of variables with their expected type and default value
ENV = {
    "WEB_FOLDER": {"name": "WEB_FOLDER", "type": str, "value": DEFAULT_WEB_FOLDER},
    "STUDIO_DEFAULT_PROJECT": {"name": "STUDIO_DEFAULT_PROJECT", "type": str, "value": SUPABASE_DEFAULT_PROJECT_NAME},
    "DOCKER_NETWORK_NAME": {"name": "DOCKER_NETWORK_NAME", "type": str, "value": DEFAULT_DOCKER_NETWORK_NAME},
    "POSTGRES_HOST": {"name": "POSTGRES_HOST", "type": str, "value": DEFAULT_POSTGRES_HOST},
    "POSTGRES_PORT": {"name": "POSTGRES_PORT", "type": int, "value": DEFAULT_POSTGRES_PORT},
    "POSTGRES_DB": {"name": "POSTGRES_DB", "type": str, "value": DEFAULT_POSTGRES_DB},
    "POSTGRES_PASSWORD": {"name": "POSTGRES_PASSWORD", "type": str, "value": DEFAULT_POSTGRES_PASSWORD},
    "DISABLE_SIGNUP": {"name": "DISABLE_SIGNUP", "type": str, "value": DEFAULT_DISABLE_SIGNUP},
    "DASHBOARD_USERNAME": {"name": "DASHBOARD_USERNAME", "type": str, "value": DEFAULT_DASHBOARD_USERNAME},
    "DASHBOARD_PASSWORD": {"name": "DASHBOARD_PASSWORD", "type": str, "value": DEFAULT_DASHBOARD_PASSWORD},
    "ADMINER_HOST_PORT": {"name": "ADMINER_HOST_PORT", "type": int, "value": DEFAULT_ADMINER_HOST_PORT},
    "PUBLIC_SUPABASE_URL": {"name": "PUBLIC_SUPABASE_URL", "type": str, "value": "http://localhost:8000"},
    "PUBLIC_SUPABASE_ANON_KEY": {"name": "PUBLIC_SUPABASE_ANON_KEY", "type": str, "value": DEFAULT_ANON_KEY},
    "PRIVATE_SUPABASE_SERVICE_ROLE": {"name": "PRIVATE_SUPABASE_SERVICE_ROLE", "type": str, "value": DEFAULT_SERVICE_ROLE_KEY},
}

OVERRIDE_DEFAULT = False
SUPABASE_PATH = pathlib.Path(__file__).parent.resolve()
SETUP_SUPBASE = True
RUN_SUPABASE_MIGRATION = True

## Manage supabase variables values

# ###########################
# FRONT
# ###########################

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

def update_config_file(env, file_path):
    '''
    
    '''
    with open('file_path', 'r+') as file:
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
        print(f"Mise à jour des variables d'environnement du fichier : {file_path}")
        file.close()

def setup_supabase(env):
    
    #### Cloning repo
    subprocess.run(["git", "clone", "--depth", "1",'--filter=blob:none', '--sparse', 'https://github.com/supabase/supabase.git'])
    subprocess.run(['git', '-C', 'supabase','sparse-checkout', 'set', 'docker'])

    #### SETUP ENV FILE
    os.chdir(os.path.join(pathlib.Path(__file__).parent.resolve(), "supabase/docker"))
    subprocess.run(["cp", ".env.example", ".env"])
    print(f"Copie de supabase/docker/.env.example -> supabase/docker/.env")
    
    # change supabase env values
    update_config_file(env, '.env')

    ### run migration
    if RUN_SUPABASE_MIGRATION in ['true', 'y', 'yes', 'YES', 'Y', True, 'o', 'oui', 'O', 'OUI']:
        print("implement migration running for supabase")
        # subprocess.run(["cp", "../../web/app/database_migration.sql", "./volumes/db/database_migration.sql"])
        # print(f"Copie de web/app/database_migration.sql -> supabase/docker/volumes/db/database_migration.sql")

def setup_web(env):

    ### Cloning repo as a subtree
    os.chdir(pathlib.Path(__file__).parent.resolve())
    print(f'Repo as "CMSaasStarter.git" a subtree')
    # print(f"{env['WEB_FOLDER']['value']}")
    # os.chdir(os.path.join(pathlib.Path(__file__).parent.resolve(), f"{env['WEB_FOLDER']['value']}"))
    subprocess.run(["git", "subtree", "add", f"--prefix={env['WEB_FOLDER']['value']}/app", "--squash", 'https://github.com/CriticalMoments/CMSaasStarter.git', 'extension/internationalization'])
    # subprocess.run(["git", "subtree", "add", f"--prefix=app", "--squash", 'https://github.com/CriticalMoments/CMSaasStarter.git', 'extension/internationalization'])

    print(f"Copie et remplissage du fichier .env.local")
    os.chdir(os.path.join(pathlib.Path(__file__).parent.resolve(), f"{env['WEB_FOLDER']['value']}", "app"))
    subprocess.run(["cp", "local_env_template", ".env.local"])
    update_config_file(env, '.env.local')

def setup_docker_compose(env):
    os.chdir(pathlib.Path(__file__).parent.resolve())
    update_config_file(env, '.env')

def main():
    global ENV

    # OVERRIDE_DEFAULT = input(f"Override default supabase values ? [y/N]")
    # if OVERRIDE_DEFAULT in ['y', 'Y']:
    #     ENV = get_user_input(ENV)

    # SETUP_SUPBASE = input(f"Install supabase as the backend for the project ? [Y/n] ")
    # if SETUP_SUPBASE in ['', None, 'true', 'y', 'yes', 'YES', 'Y', True, 'o', 'oui', 'O', 'OUI']:
    #     RUN_SUPABASE_MIGRATION = input(f"Run supbase migration ? [Y/n] ")
    #     setup_supabase(ENV)

    setup_web(ENV)
    setup_docker_compose(ENV)
    print('''
Lire le README.md du dépôt pour la suite. Le projet est maintenant quasi prêt à être lancé.
Voir "https://supabase.com/docs/guides/self-hosting/docker" pour plus d'information.
Run project:
cd {PROJECT_PATH}
docker compose up -d
          
## Print sveltekit logs
docker compose logs --follow web       
''')

if __name__ == "__main__":
    main()
