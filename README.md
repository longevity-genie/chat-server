# chat-server
Example hugging-chat UI + litellm proxy deployment
By default chat uses Open-AI through a caching proxy

## Cloning the repo
Clone the project:
```commandline
git clone https://github.com/longevity-genie/chat-server.git
```
## Deploying the docker environment
Install latest docker and docker-compose from respective sites. 
Optionally, if needed, you may use or refer to the provided script 
```commandline
install_docker_ubuntu.sh
```

Create environment variable file and populate chat model settings. 
```commandline
cp env.local.template .env.local
nano .env.local
```
To insert your agentic chain, set model baseURL in chat env to your endpoint, set baseurl for your agent to proxy address from docker-compose.
For containerized endpoints use `chat-server` network
NB!! For endpoints that are outside containers use docker gateway IP 
`"baseURL": "http://172.17.0.1:60777/custom/v1"`,
And vice-versa, to point local endpoints to proxy in the container use localhost and external 14000 (changeable in `docker-compose.yaml`) port mapping: 
`OPENAI_API_BASE=http://127.0.0.1:14000/v1`

Create environment variable file for proxy and populate the OPENAI_API_KEY, GROQ_API_KEY and other keys you're going to use with respective valid keys
Inspect and correct `proxy.yaml` as desirable
```commandline
cp env.proxy.template .env.proxy
nano .env.proxy
nano proxy.yaml
```

docker-compose fetches latest pre-built longevity-genie/chat-ui 
Alternatively, you may want to re-build the chat-ui from source using the submodule [longevity-genie/chat-ui](https://github.com/longevity-genie/chat-ui): 
```commandline
git submodule update --init --recursive
git pull --recurse-submodules
docker-compose up --build
```

