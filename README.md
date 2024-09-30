# chat-server
Example hugging-chat UI + litellm proxy deployment
By default chat uses Open-AI through a caching proxy

## Cloning the repo
Clone the project:
```commandline
git clone https://github.com/longevity-genie/chat-server.git
```
## Preparing the docker environment
Install the latest Docker and Docker-Compose from their respective websites.
Optionally, if needed, you may use or refer to the provided script:
```commandline
install_docker_ubuntu.sh
```

## Populate the environment with your API keys
Create an environment variable file from template and populate the chat model settings:
```commandline
cp .env.local.template .env.local
nano .env.local
```
To insert your agentic chain, set the model `baseURL` in the chat environment to your endpoint. Set the baseURL for your agent to the proxy address from `docker-compose.yaml`.
For containerized endpoints use `chat-server` network
NB!! For endpoints that are outside containers use docker gateway IP 
`"baseURL": "http://172.17.0.1:60777/custom/v1"`,
And vice-versa, to point local endpoints to proxy in the container use localhost and external 14000 (changeable in `docker-compose.yaml`) port mapping: 
`OPENAI_API_BASE=http://127.0.0.1:14000/v1`

Create an environment variable file for the proxy and populate `OPENAI_API_KEY`, `GROQ_API_KEY` and other keys with their respective valid values.
Inspect and correct `proxy.yaml` as needed, currently it is configured for commonly used OpenAI and GroQ models.
Specify passwords in 
```commandline
cp .env.proxy.template .env.proxy
nano .env.proxy
nano proxy.yaml
nano .env.db
```
## Building chat-ui from source as submodule
`docker-compose` fetches latest pre-built `longevity-genie/chat-ui` 
Alternatively, you may want to re-build the chat-ui from source using the submodule [longevity-genie/chat-ui](https://github.com/longevity-genie/chat-ui): 
```commandline
git submodule update --init --recursive
git pull --recurse-submodules
docker-compose up --build
```

