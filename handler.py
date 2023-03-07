from scaleway_lib_fix import server_action, update_server
from scaleway import Client
from scaleway.instance.v1 import InstanceV1API
from scaleway.instance.v1.types import ServerAction

client = Client.from_env()


def stopSchedule(event, context):
    instance_api = InstanceV1API(client)
    servers = instance_api.list_servers_all()
    for server in servers:
        if "on-schedule" in server.tags:
            # Set the tag "scheduled-off" to the server and stop the instance
            result = server_action(
                instance_api, server_id=server.id, action=ServerAction.POWEROFF
            )
            result = update_server(
                instance_api, server_id=server.id, tags=server.tags + ["scheduled-off"]
            )
    return {
        "body": "Done",
        "headers": {
            "Content-Type": ["text/plain"],
        },
    }


def startSchedule(event, context):
    instance_api = InstanceV1API(client)
    servers = instance_api.list_servers_all()
    for server in servers:
        if "scheduled-off" in server.tags:
            # Start the server and remove the scheduled-off tag
            result = server_action(
                instance_api, server_id=server.id, action=ServerAction.POWERON
            )
            tags = server.tags
            tags.remove("scheduled-off")
            result = update_server(instance_api, server_id=server.id, tags=tags)
    return {
        "body": "Done",
        "headers": {
            "Content-Type": ["text/plain"],
        },
    }


if __name__ == "__main__":
    stopSchedule(None, None)
