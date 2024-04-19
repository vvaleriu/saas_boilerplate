# saas_template

This will install and setup a template for a small Saas with this stack:
Backend: supabase
Front: Sveltekit, TailwindCss, DaisyUI

'https://github.com/CriticalMoments/CMSaasStarter' on branch extension/internationalization is a subtree of this repository. It's been added this way:

> git subtree add --prefix=web --squash https://github.com/CriticalMoments/CMSaasStarter.git extension/internationalization

Command python3 and git must be on the system.

# Installation

Execute install.py and follow instructions.

> chmod +x install.py
> ./install.py

Default values:
```
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
```

# Start

## Launch supabase
> cd /project/path/supabase/docker
> docker compose up

go to `url: http://localhost:8000/`


Supabase default credentials with this project are:
> login: supabase
> pass: supabase123

On first launch, do not forget to copy and execute sql from
`web/app/database_migration.sql` into `http://localhost:8000/project/default/sql/1`

## Launch web
> cd web
> docker compose up     # Just launch the container without running nodejs
> docker exec -it {DEFAULT_WEB_FOLDER} /bin/bash
> pnpm run dev

go to: `http://localhost:5173/`

For further details, go to:
```https://github.com/CriticalMoments/CMSaasStarter```

And 

```https://supabase.com/docs/guides/self-hosting/docker```