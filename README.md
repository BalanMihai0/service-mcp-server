# OpenRemote MCP Server Service
MCP Server for your OpenRemote instance.



## Quick start guide
This guide assumes you already have an OpenRemote instance running.

1. **Create service user**

   In your OpenRemote instance, create a new service user (`settings > users > SERVICE USERS > ADD USER`) and give it the permissions you want to have.
   The MCP server will auto discover the tools that are available.

   _Note: The service user is required to have the `read:services` & `write:services` role._


2. **Setup docker service**
   Create a docker-compose.yml file and configure the service.
    ```yaml
    services:
      # Other OpenRemote services...
    
      mcp-server:
        image: openremote/mcp-server:latest
        restart: always
        depends_on:
          manager:
            condition: service_healthy
        ports:
          - "8420:8420"
        environment:
          APP_HOMEPAGE_URL: https://<SERVICE_URL>:8420 # Change this to the URL this service is available on
          
          OPENREMOTE_CLIENT_ID: <OPENREMOTE_CLIENT_ID>
          OPENREMOTE_CLIENT_SECRET: <OPENREMOTE_CLIENT_SECRET>
          OPENREMOTE_URL: <OPENREMOTE_URL>
          OPENREMOTE_VERIFY_SSL: 1
    ```

4. **Run the service**

   Finally, you can run the new service by using docker compose.
    ```shell
    docker compose up
    ```
   This will run the additional service, it will auto-register to your OpenRemote instance. and you can view them in the services tab inside your OpenRemote dashboard.


## Development guide
This guide assumes you already have an OpenRemote instance running.

### Prerequisites:
- [Python](https://www.python.org/downloads/) & [UV](https://docs.astral.sh/uv/#installation) installed
- Running an instance of [OpenRemote](https://docs.openremote.io/docs/quick-start)

1. **Create service user**

   In your OpenRemote instance, create a new service user (`settings > users > SERVICE USERS > ADD USER`) and give it the permissions you want to have.
   The MCP server will auto discover the tools that are available.

   _Note: The service user is required to have the `read:services` & `write:services` role._


2. **Sync dependencies**
    ```shell
    uv sync
    ```

3. **Setup environment variables**

   Create a new file `.env` in the root of the project directory. and fill in the following variables replacing the brackets with your own values.
    ```dotenv
    OPENREMOTE_CLIENT_ID=<OPENREMOTE_CLIENT_ID>
    OPENREMOTE_CLIENT_SECRET=<OPENREMOTE_CLIENT_SECRET>
    OPENREMOTE_URL=<OPENREMOTE_URL>
    OPENREMOTE_VERIFY_SSL=0
    ```

4. **Run service**
    ```shell
    uv run uvicorn app:app --reload --port=8420
    ```

## Production guide

### Prerequisites:
- [Docker](https://docs.docker.com/engine/install/) installed

1. **Build docker image**

    Build the docker image
    ```shell
    docker build . --tag=openremote/mcp-server:latest 
    ```