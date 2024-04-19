#!/usr/bin/env python3
import os
import subprocess
import sys
import pathlib
import random
import string



# Define default values
# DEFAULT_HOST_PORT = 8000
DEFAULT_POSTGRES_PASSWORD = "your-super-secret-and-long-postgres-password"
DEFAULT_POSTGRES_HOST = "db"
DEFAULT_POSTGRES_DB = "postgres"
DEFAULT_POSTGRES_PORT = 5432
DEFAULT_DISABLE_SIGNUP = True
DEFAULT_DASHBOARD_USERNAME = 'supabase'
DEFAULT_DASHBOARD_PASSWORD = 'supabase123'
DEFAULT_ADMINER_HOST_PORT = 14519

# Define a list of variables with their expected type and default value
variables = [
    # ("HOST_PORT", int, DEFAULT_HOST_PORT),
    ("POSTGRES_PASSWORD", str, DEFAULT_POSTGRES_PASSWORD),
    ("POSTGRES_HOST", str, DEFAULT_POSTGRES_HOST),
    ("POSTGRES_DB", str, DEFAULT_POSTGRES_DB),
    ("POSTGRES_PORT", int, DEFAULT_POSTGRES_PORT),
    ("DISABLE_SIGNUP", bool, DEFAULT_DISABLE_SIGNUP),
    ("DASHBOARD_USERNAME", str, DEFAULT_DASHBOARD_USERNAME),
    ("DASHBOARD_PASSWORD", str, DEFAULT_DASHBOARD_PASSWORD),
    ("ADMINER_HOST_PORT", int, DEFAULT_ADMINER_HOST_PORT)
]

# Create a dictionary to store the user input values
user_input_values = {
    'STUDIO_DEFAULT_PROJECT': '',
    # 'HOST_PORT': DEFAULT_HOST_PORT,
    'POSTGRES_PASSWORD': DEFAULT_POSTGRES_PASSWORD,
    'POSTGRES_HOST': DEFAULT_POSTGRES_HOST,
    'POSTGRES_DB': DEFAULT_POSTGRES_DB,
    'POSTGRES_PORT': DEFAULT_POSTGRES_PORT,
    'DISABLE_SIGNUP': DEFAULT_DISABLE_SIGNUP,
    'DASHBOARD_USERNAME': DEFAULT_DASHBOARD_USERNAME,
    'DASHBOARD_PASSWORD': DEFAULT_DASHBOARD_PASSWORD,
    'ADMINER_HOST_PORT': DEFAULT_ADMINER_HOST_PORT,
}

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

# Ask user for input in a loop
def ask_supabase_variable_value():
    for var_name, var_type, default_value in variables:
        while True:
            user_input = input(f"Do you want to override the default value for {var_name} ({var_type.__name__})? Current default is {default_value}: ")
            if user_input == "":
                user_input_values[var_name] = default_value
                break
            try:
                # Convert input to expected type
                if var_type == bool:
                    user_input = user_input.lower() in ["true", "t", "yes", "y", "1"]
                else:
                    user_input = var_type(user_input)
                user_input_values[var_name] = user_input
                break
            except ValueError:
                print(f"Invalid input. Please enter a value of type {var_type.__name__}.")

    # Print the final values
    print("\nSupabase instance values:")
    user_input_values['DISABLE_SIGNUP'] = 'true' if user_input_values['DISABLE_SIGNUP'] in [True, 'y', 'yes', 'true', '1', 1] else 'false'
    for var_name in user_input_values:
        print(f"{var_name} = {user_input_values[var_name]}")

## Choosing project installation path 
def create_folder(path):
    if os.path.exists(path):
        print(f"this path already exists. Retry. Exiting")
        sys.exit()
    try:
        os.makedirs(path)
        print(f"Folder created at {path}")
    except OSError as e:
        print(f"Error creating folder: {e}")

# ###########################
# SUPABASE RELATIVE SCRIPTS
# ###########################

def setup_repos():
    """
    Parameters:
    directory (str): directory the repo will be cloned in
    url (str): repo url to be cloned as a subtree
    """
    os.chdir(pathlib.Path(__file__).parent.resolve())
    print(f'Repo as "CMSaasStarter.git" a subtree')
    subprocess.run(["git", "subtree", "add", f"--prefix=web", "--squash", 'https://github.com/CriticalMoments/CMSaasStarter.git', 'extension/internationalization'])
    print(f'Cloning supabase.git as ')
    subprocess.run(["git", "clone", "--depth", "1", 'https://github.com/supabase/supabase.git'])

def setup_env_file(path, input_values):
    os.chdir(os.path.join(path, "supabase/docker"))
    subprocess.run(["cp", ".env.example", ".env"])
    
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
                if variable in input_values:
                    # Replace the value with the one from the dictionary
                    line = f'{variable}={input_values[variable]}\n'
            
            # Write the line back to the file
            file.write(line)
        file.close()

    # ADD ADMINER (postgres admin panl) ENV VALUES
    with open('.env', 'a') as file:
        file.write('\n####### Personnal ENV variables')
        file.write(f"\nADMINER_HOST_PORT={user_input_values['ADMINER_HOST_PORT']}\n")
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

    setup_repos()
    sys.exit()
    # defining project name
    while user_input_values['STUDIO_DEFAULT_PROJECT'] == '':
        user_input_values['STUDIO_DEFAULT_PROJECT'] = input(f"Enter a project name: ")
    
    # Handling supabase variable values
    OVERRIDE_DEFAULT = input(f"Override default supabase values ? [y/N]")
    if OVERRIDE_DEFAULT in ['y', 'Y']:
        ask_supabase_variable_value()

    ##### Supabase

    # Creating installation path and handling installation
    PROJECT_PATH = input("Enter a path full on the system where to install the supabase files. (The final installation will be \"/your/path/supabase\"): ")
    # PROJECT_PATH = "/home/vincent/Projets/cocobongo"
    create_folder(PROJECT_PATH)
    setup_repos(PROJECT_PATH)

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