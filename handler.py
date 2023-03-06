from scaleway_async import Client
from scaleway_async.instance.v1 import InstanceV1API
from scaleway_async.instance.v1.types import ServerAction

client = Client.from_config_file_and_env()


async def stopSchedule(event, context):
    instance_api = InstanceV1API(client)
    servers = await instance_api.list_servers_all()
    for server in servers:
        if "on-schedule" in server.tags:
            # Set the tag "scheduled-off" to the server and stop the instance
            result = await instance_api.server_action(
                server_id=server.id, action=ServerAction.POWEROFF
            )
            print(result)
            result = await instance_api._update_server(
                server_id=server.id, tags=server.tags + ["scheduled-off"]
            )
            print(result)
    return {
        "body": "Done",
        "headers": {
            "Content-Type": ["text/plain"],
        },
    }


async def startSchedule(event, context):
    instance_api = InstanceV1API(client)
    servers = await instance_api.list_servers_all()
    for server in servers:
        if "scheduled-off" in server.tags:
            # Start the server and remove the scheduled-off tag
            result = await instance_api.server_action(
                server_id=server.id, action=ServerAction.POWERON
            )
            print(result)
            tags = server.tags
            tags.remove("scheduled-off")
            result = await instance_api._update_server(server_id=server.id, tags=tags)
            print(result)
    return {
        "body": "Done",
        "headers": {
            "Content-Type": ["text/plain"],
        },
    }


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    print(loop.run_until_complete(stopSchedule(None, None)))