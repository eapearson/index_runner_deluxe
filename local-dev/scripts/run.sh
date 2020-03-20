cd ..
echo "Token is ${TOKEN}"
echo "Workspace admin? ${WS_ADMIN:=no}"
echo "Skip relation engine? ${SKIP_RELENG:=yes}"
echo "Skip features? ${SKIP_FEATURES:=yes}"
echo "Max object size is ${MAX_OBJECT_SIZE:=100000000}"
echo "Host is ${HOST:=ci.kbase.us}"
echo "Host IP is ${HOST_IP:=128.3.56.133}"
if [ -n "${ALLOW_INDICES}" ]
then
    echo "Allowing only indices ${ALLOW_INDICES}"
else
    echo "Allowing all indices"
fi
# This ensures that even if we have local mapping of ci.kbase.us to a local proxy, the
# docker container can still talk to CI.
# Cannot get the following to work -- since /app/config is volume mounted
# via docker, it may be that the python url api is tripping up over that. There
# are statements from the Python core dev team (may be moot now) that file access
# within Docker is not fully supported.
# --env GLOBAL_CONFIG_URL=file://localhost/app/config/confg.yaml \
docker run --rm \
    --net kbase-dev \
    --add-host ${HOST}:${HOST_IP} \
    --mount type=bind,source="$(pwd)"/../index_runner_spec,target=/app/config \
    --env SKIP_RELENG=${SKIP_RELENG} \
    --env SKIP_FEATURES=${SKIP_FEATURES} \
    --env ALLOW_INDICES=${ALLOW_INDICES} \
    --env ELASTICSEARCH_HOST=elasticsearch \
    --env ELASTICSEARCH_PORT=9200 \
    --env KAFKA_SERVER=kafka \
    --env KAFKA_CLIENTGROUP=search_indexer \
    --env KBASE_ENDPOINT=https://${HOST}/services \
    --env WORKSPACE_TOKEN="${TOKEN}" \
    --env WS_ADMIN="${WS_ADMIN}" \
    --env MAX_OBJECT_SIZE="${MAX_OBJECT_SIZE}" \
    --name indexrunner \
    indexrunner:dev
cd local-dev
