from typing import Optional, Dict, Union, Any, Mapping, Iterable, Tuple, IO, List

from scaleway_core.api import APILogger

from scaleway.instance.v1 import InstanceV1API, ServerAction, ServerActionResponse
import requests
import json

from scaleway_core.bridge import (
    Zone,
)

from scaleway_core.utils import (
    validate_path_param,
)

from scaleway.instance.v1.types import (
    ServerActionRequestVolumeBackupTemplate,
    ServerActionRequest,
    BootType,
    VolumeServerTemplate,
    SecurityGroupTemplate,
    PrivateNIC,
    UpdateServerResponse,
)
from scaleway.instance.v1.marshalling import (
    marshal_ServerActionRequest,
    unmarshal_ServerActionResponse,
    marshal__UpdateServerRequest,
    unmarshal_UpdateServerResponse,
)

from scaleway.instance.v1.types_private import (
    _UpdateServerRequest,
)

Body = Union[
    str, bytes, Mapping[str, Any], Iterable[Tuple[str, Optional[str]]], IO[Any]
]

Params = Mapping[str, Any]


def fixed_request(
    api: InstanceV1API,
    method: str,
    path: str,
    params: Params = {},
    headers: Dict[str, str] = {},
    body: Optional[Body] = None,
) -> requests.Response:
    additional_headers: Dict[str, str] = {}

    method = method.upper()
    if method == "POST" or method == "PUT" or method == "PATCH":
        additional_headers["Content-Type"] = "application/json; charset=utf-8"

        if body is None:
            body = {}
        empty_keys = [k for k, v in body.items() if not v]  # type: ignore
        for k in empty_keys:
            del body[k]  # type: ignore
    raw_body = json.dumps(body) if body is not None else None

    params = {k: str(v) for k, v in params.items() if v is not None}

    headers = {
        "accept": "application/json",
        "x-auth-token": api.client.secret_key or "",
        "user-agent": api.client.user_agent,
        **additional_headers,
        **headers,
    }

    url = f"{api.client.api_url}{path}"

    logger = APILogger(api._log, api.client._increment_request_count())

    logger.log_request(
        method=method,
        url=url,
        params=params,
        headers=headers,
        body=raw_body,
    )

    response = requests.request(
        method=method,
        url=url,
        params=params,
        headers=headers,
        data=raw_body,
        verify=not api.client.api_allow_insecure,
    )

    logger.log_response(
        response=response,
    )

    return response


def server_action(
    api: InstanceV1API,
    *,
    server_id: str,
    action: ServerAction,
    zone: Optional[Zone] = None,
    name: Optional[str] = None,
    volumes: Optional[Dict[str, ServerActionRequestVolumeBackupTemplate]] = None,
) -> ServerActionResponse:
    """
    Perform power related actions on a server. Be wary that when terminating a server, all the attached volumes (local *and* block storage) are deleted. So, if you want to keep your local volumes, you must use the `archive` action instead of `terminate`. And if you want to keep block-storage volumes, **you must** detach it beforehand you issue the `terminate` call.  For more information, read the [Volumes](#volumes-7e8a39) documentation.
    :param zone: Zone to target. If none is passed will use default zone from the config
    :param server_id: UUID of the server
    :param action: The action to perform on the server
    :param name: The name of the backup you want to create.
    This field should only be specified when performing a backup action.

    :param volumes: For each volume UUID, the snapshot parameters of the volume.
    This field should only be specified when performing a backup action.

    :return: :class:`ServerActionResponse <ServerActionResponse>`

    Usage:
    ::

        result = await api.server_action(
            server_id="example",
            action=poweron,
        )
    """

    param_zone = validate_path_param("zone", zone or api.client.default_zone)
    param_server_id = validate_path_param("server_id", server_id)

    res = fixed_request(
        api,
        "POST",
        f"/instance/v1/zones/{param_zone}/servers/{param_server_id}/action",
        body=marshal_ServerActionRequest(
            ServerActionRequest(
                server_id=server_id,
                action=action,
                zone=zone,
                name=name,
                volumes=volumes,
            ),
            api.client,
        ),
    )

    api._throw_on_error(res)
    return unmarshal_ServerActionResponse(res.json())


def update_server(
    api: InstanceV1API,
    *,
    server_id: str,
    zone: Optional[Zone] = None,
    name: Optional[str] = None,
    boot_type: Optional[BootType] = None,
    tags: Optional[List[str]] = None,
    volumes: Optional[Dict[str, VolumeServerTemplate]] = None,
    bootscript: Optional[str] = None,
    dynamic_ip_required: Optional[bool] = None,
    enable_ipv6: Optional[bool] = None,
    protected: Optional[bool] = None,
    security_group: Optional[SecurityGroupTemplate] = None,
    placement_group: Optional[str] = None,
    private_nics: Optional[List[PrivateNIC]] = None,
) -> UpdateServerResponse:
    """
    Update a server
    :param zone: Zone to target. If none is passed will use default zone from the config
    :param server_id: UUID of the server
    :param name: Name of the server
    :param boot_type:
    :param tags: Tags of the server
    :param volumes:
    :param bootscript:
    :param dynamic_ip_required:
    :param enable_ipv6:
    :param protected:
    :param security_group:
    :param placement_group: Placement group ID if server must be part of a placement group
    :param private_nics: The server private NICs
    :return: :class:`UpdateServerResponse <UpdateServerResponse>`

    Usage:
    ::

        result = await api._update_server(server_id="example")
    """

    param_zone = validate_path_param("zone", zone or api.client.default_zone)
    param_server_id = validate_path_param("server_id", server_id)

    res = fixed_request(
        api,
        "PATCH",
        f"/instance/v1/zones/{param_zone}/servers/{param_server_id}",
        body=marshal__UpdateServerRequest(
            _UpdateServerRequest(
                server_id=server_id,
                zone=zone,
                name=name,
                boot_type=boot_type,
                tags=tags,
                volumes=volumes,
                bootscript=bootscript,
                dynamic_ip_required=dynamic_ip_required,
                enable_ipv6=enable_ipv6,
                protected=protected,
                security_group=security_group,
                placement_group=placement_group,
                private_nics=private_nics,
            ),
            api.client,
        ),
    )

    api._throw_on_error(res)
    return unmarshal_UpdateServerResponse(res.json())
