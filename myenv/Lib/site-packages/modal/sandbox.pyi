import google.protobuf.message
import modal._tunnel
import modal.app
import modal.client
import modal.cloud_bucket_mount
import modal.container_process
import modal.gpu
import modal.image
import modal.io_streams
import modal.mount
import modal.network_file_system
import modal.object
import modal.scheduler_placement
import modal.secret
import modal.stream_type
import modal.volume
import modal_proto.api_pb2
import os
import typing
import typing_extensions

class _Sandbox(modal.object._Object):
    _result: typing.Optional[modal_proto.api_pb2.GenericResult]
    _stdout: modal.io_streams._StreamReader[str]
    _stderr: modal.io_streams._StreamReader[str]
    _stdin: modal.io_streams._StreamWriter
    _task_id: typing.Optional[str]
    _tunnels: typing.Optional[typing.Dict[int, modal._tunnel.Tunnel]]

    @staticmethod
    def _new(
        entrypoint_args: typing.Sequence[str],
        image: modal.image._Image,
        mounts: typing.Sequence[modal.mount._Mount],
        secrets: typing.Sequence[modal.secret._Secret],
        timeout: typing.Optional[int] = None,
        workdir: typing.Optional[str] = None,
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
        cloud: typing.Optional[str] = None,
        region: typing.Union[str, typing.Sequence[str], None] = None,
        cpu: typing.Optional[float] = None,
        memory: typing.Union[int, typing.Tuple[int, int], None] = None,
        network_file_systems: typing.Dict[
            typing.Union[str, os.PathLike], modal.network_file_system._NetworkFileSystem
        ] = {},
        block_network: bool = False,
        cidr_allowlist: typing.Optional[typing.Sequence[str]] = None,
        volumes: typing.Dict[
            typing.Union[str, os.PathLike],
            typing.Union[modal.volume._Volume, modal.cloud_bucket_mount._CloudBucketMount],
        ] = {},
        pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
        encrypted_ports: typing.Sequence[int] = [],
        unencrypted_ports: typing.Sequence[int] = [],
        _experimental_scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement] = None,
    ) -> _Sandbox: ...
    @staticmethod
    async def create(
        *entrypoint_args: str,
        app: typing.Optional[modal.app._App] = None,
        environment_name: typing.Optional[str] = None,
        image: typing.Optional[modal.image._Image] = None,
        mounts: typing.Sequence[modal.mount._Mount] = (),
        secrets: typing.Sequence[modal.secret._Secret] = (),
        network_file_systems: typing.Dict[
            typing.Union[str, os.PathLike], modal.network_file_system._NetworkFileSystem
        ] = {},
        timeout: typing.Optional[int] = None,
        workdir: typing.Optional[str] = None,
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
        cloud: typing.Optional[str] = None,
        region: typing.Union[str, typing.Sequence[str], None] = None,
        cpu: typing.Optional[float] = None,
        memory: typing.Union[int, typing.Tuple[int, int], None] = None,
        block_network: bool = False,
        cidr_allowlist: typing.Optional[typing.Sequence[str]] = None,
        volumes: typing.Dict[
            typing.Union[str, os.PathLike],
            typing.Union[modal.volume._Volume, modal.cloud_bucket_mount._CloudBucketMount],
        ] = {},
        pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
        encrypted_ports: typing.Sequence[int] = [],
        unencrypted_ports: typing.Sequence[int] = [],
        _experimental_scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement] = None,
        client: typing.Optional[modal.client._Client] = None,
    ) -> _Sandbox: ...
    def _hydrate_metadata(self, handle_metadata: typing.Optional[google.protobuf.message.Message]): ...
    @staticmethod
    async def from_id(sandbox_id: str, client: typing.Optional[modal.client._Client] = None) -> _Sandbox: ...
    async def set_tags(self, tags: typing.Dict[str, str], *, client: typing.Optional[modal.client._Client] = None): ...
    async def wait(self, raise_on_termination: bool = True): ...
    async def tunnels(self, timeout: int = 50) -> typing.Dict[int, modal._tunnel.Tunnel]: ...
    async def terminate(self): ...
    async def poll(self) -> typing.Optional[int]: ...
    async def _get_task_id(self): ...
    @typing.overload
    async def exec(
        self,
        *cmds: str,
        pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
        stdout: modal.stream_type.StreamType = modal.stream_type.StreamType.PIPE,
        stderr: modal.stream_type.StreamType = modal.stream_type.StreamType.PIPE,
        timeout: typing.Optional[int] = None,
        workdir: typing.Optional[str] = None,
        secrets: typing.Sequence[modal.secret._Secret] = (),
        text: typing.Literal[True] = True,
        bufsize: typing.Literal[-1, 1] = -1,
        _pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
    ) -> modal.container_process._ContainerProcess[str]: ...
    @typing.overload
    async def exec(
        self,
        *cmds: str,
        pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
        stdout: modal.stream_type.StreamType = modal.stream_type.StreamType.PIPE,
        stderr: modal.stream_type.StreamType = modal.stream_type.StreamType.PIPE,
        timeout: typing.Optional[int] = None,
        workdir: typing.Optional[str] = None,
        secrets: typing.Sequence[modal.secret._Secret] = (),
        text: typing.Literal[False] = False,
        bufsize: typing.Literal[-1, 1] = -1,
        _pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
    ) -> modal.container_process._ContainerProcess[bytes]: ...
    @property
    def stdout(self) -> modal.io_streams._StreamReader[str]: ...
    @property
    def stderr(self) -> modal.io_streams._StreamReader[str]: ...
    @property
    def stdin(self) -> modal.io_streams._StreamWriter: ...
    @property
    def returncode(self) -> typing.Optional[int]: ...
    @staticmethod
    def list(
        *,
        app_id: typing.Optional[str] = None,
        tags: typing.Optional[typing.Dict[str, str]] = None,
        client: typing.Optional[modal.client._Client] = None,
    ) -> typing.AsyncGenerator[_Sandbox, None]: ...

class Sandbox(modal.object.Object):
    _result: typing.Optional[modal_proto.api_pb2.GenericResult]
    _stdout: modal.io_streams.StreamReader[str]
    _stderr: modal.io_streams.StreamReader[str]
    _stdin: modal.io_streams.StreamWriter
    _task_id: typing.Optional[str]
    _tunnels: typing.Optional[typing.Dict[int, modal._tunnel.Tunnel]]

    def __init__(self, *args, **kwargs): ...
    @staticmethod
    def _new(
        entrypoint_args: typing.Sequence[str],
        image: modal.image.Image,
        mounts: typing.Sequence[modal.mount.Mount],
        secrets: typing.Sequence[modal.secret.Secret],
        timeout: typing.Optional[int] = None,
        workdir: typing.Optional[str] = None,
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
        cloud: typing.Optional[str] = None,
        region: typing.Union[str, typing.Sequence[str], None] = None,
        cpu: typing.Optional[float] = None,
        memory: typing.Union[int, typing.Tuple[int, int], None] = None,
        network_file_systems: typing.Dict[
            typing.Union[str, os.PathLike], modal.network_file_system.NetworkFileSystem
        ] = {},
        block_network: bool = False,
        cidr_allowlist: typing.Optional[typing.Sequence[str]] = None,
        volumes: typing.Dict[
            typing.Union[str, os.PathLike], typing.Union[modal.volume.Volume, modal.cloud_bucket_mount.CloudBucketMount]
        ] = {},
        pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
        encrypted_ports: typing.Sequence[int] = [],
        unencrypted_ports: typing.Sequence[int] = [],
        _experimental_scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement] = None,
    ) -> Sandbox: ...

    class __create_spec(typing_extensions.Protocol):
        def __call__(
            self,
            *entrypoint_args: str,
            app: typing.Optional[modal.app.App] = None,
            environment_name: typing.Optional[str] = None,
            image: typing.Optional[modal.image.Image] = None,
            mounts: typing.Sequence[modal.mount.Mount] = (),
            secrets: typing.Sequence[modal.secret.Secret] = (),
            network_file_systems: typing.Dict[
                typing.Union[str, os.PathLike], modal.network_file_system.NetworkFileSystem
            ] = {},
            timeout: typing.Optional[int] = None,
            workdir: typing.Optional[str] = None,
            gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
            cloud: typing.Optional[str] = None,
            region: typing.Union[str, typing.Sequence[str], None] = None,
            cpu: typing.Optional[float] = None,
            memory: typing.Union[int, typing.Tuple[int, int], None] = None,
            block_network: bool = False,
            cidr_allowlist: typing.Optional[typing.Sequence[str]] = None,
            volumes: typing.Dict[
                typing.Union[str, os.PathLike],
                typing.Union[modal.volume.Volume, modal.cloud_bucket_mount.CloudBucketMount],
            ] = {},
            pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
            encrypted_ports: typing.Sequence[int] = [],
            unencrypted_ports: typing.Sequence[int] = [],
            _experimental_scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement] = None,
            client: typing.Optional[modal.client.Client] = None,
        ) -> Sandbox: ...
        async def aio(
            self,
            *entrypoint_args: str,
            app: typing.Optional[modal.app.App] = None,
            environment_name: typing.Optional[str] = None,
            image: typing.Optional[modal.image.Image] = None,
            mounts: typing.Sequence[modal.mount.Mount] = (),
            secrets: typing.Sequence[modal.secret.Secret] = (),
            network_file_systems: typing.Dict[
                typing.Union[str, os.PathLike], modal.network_file_system.NetworkFileSystem
            ] = {},
            timeout: typing.Optional[int] = None,
            workdir: typing.Optional[str] = None,
            gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
            cloud: typing.Optional[str] = None,
            region: typing.Union[str, typing.Sequence[str], None] = None,
            cpu: typing.Optional[float] = None,
            memory: typing.Union[int, typing.Tuple[int, int], None] = None,
            block_network: bool = False,
            cidr_allowlist: typing.Optional[typing.Sequence[str]] = None,
            volumes: typing.Dict[
                typing.Union[str, os.PathLike],
                typing.Union[modal.volume.Volume, modal.cloud_bucket_mount.CloudBucketMount],
            ] = {},
            pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
            encrypted_ports: typing.Sequence[int] = [],
            unencrypted_ports: typing.Sequence[int] = [],
            _experimental_scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement] = None,
            client: typing.Optional[modal.client.Client] = None,
        ) -> Sandbox: ...

    create: __create_spec

    def _hydrate_metadata(self, handle_metadata: typing.Optional[google.protobuf.message.Message]): ...

    class __from_id_spec(typing_extensions.Protocol):
        def __call__(self, sandbox_id: str, client: typing.Optional[modal.client.Client] = None) -> Sandbox: ...
        async def aio(self, sandbox_id: str, client: typing.Optional[modal.client.Client] = None) -> Sandbox: ...

    from_id: __from_id_spec

    class __set_tags_spec(typing_extensions.Protocol):
        def __call__(self, tags: typing.Dict[str, str], *, client: typing.Optional[modal.client.Client] = None): ...
        async def aio(self, tags: typing.Dict[str, str], *, client: typing.Optional[modal.client.Client] = None): ...

    set_tags: __set_tags_spec

    class __wait_spec(typing_extensions.Protocol):
        def __call__(self, raise_on_termination: bool = True): ...
        async def aio(self, raise_on_termination: bool = True): ...

    wait: __wait_spec

    class __tunnels_spec(typing_extensions.Protocol):
        def __call__(self, timeout: int = 50) -> typing.Dict[int, modal._tunnel.Tunnel]: ...
        async def aio(self, timeout: int = 50) -> typing.Dict[int, modal._tunnel.Tunnel]: ...

    tunnels: __tunnels_spec

    class __terminate_spec(typing_extensions.Protocol):
        def __call__(self): ...
        async def aio(self): ...

    terminate: __terminate_spec

    class __poll_spec(typing_extensions.Protocol):
        def __call__(self) -> typing.Optional[int]: ...
        async def aio(self) -> typing.Optional[int]: ...

    poll: __poll_spec

    class ___get_task_id_spec(typing_extensions.Protocol):
        def __call__(self): ...
        async def aio(self): ...

    _get_task_id: ___get_task_id_spec

    class __exec_spec(typing_extensions.Protocol):
        @typing.overload
        def __call__(
            self,
            *cmds: str,
            pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
            stdout: modal.stream_type.StreamType = modal.stream_type.StreamType.PIPE,
            stderr: modal.stream_type.StreamType = modal.stream_type.StreamType.PIPE,
            timeout: typing.Optional[int] = None,
            workdir: typing.Optional[str] = None,
            secrets: typing.Sequence[modal.secret.Secret] = (),
            text: typing.Literal[True] = True,
            bufsize: typing.Literal[-1, 1] = -1,
            _pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
        ) -> modal.container_process.ContainerProcess[str]: ...
        @typing.overload
        def __call__(
            self,
            *cmds: str,
            pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
            stdout: modal.stream_type.StreamType = modal.stream_type.StreamType.PIPE,
            stderr: modal.stream_type.StreamType = modal.stream_type.StreamType.PIPE,
            timeout: typing.Optional[int] = None,
            workdir: typing.Optional[str] = None,
            secrets: typing.Sequence[modal.secret.Secret] = (),
            text: typing.Literal[False] = False,
            bufsize: typing.Literal[-1, 1] = -1,
            _pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
        ) -> modal.container_process.ContainerProcess[bytes]: ...
        @typing.overload
        async def aio(
            self,
            *cmds: str,
            pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
            stdout: modal.stream_type.StreamType = modal.stream_type.StreamType.PIPE,
            stderr: modal.stream_type.StreamType = modal.stream_type.StreamType.PIPE,
            timeout: typing.Optional[int] = None,
            workdir: typing.Optional[str] = None,
            secrets: typing.Sequence[modal.secret.Secret] = (),
            text: typing.Literal[True] = True,
            bufsize: typing.Literal[-1, 1] = -1,
            _pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
        ) -> modal.container_process.ContainerProcess[str]: ...
        @typing.overload
        async def aio(
            self,
            *cmds: str,
            pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
            stdout: modal.stream_type.StreamType = modal.stream_type.StreamType.PIPE,
            stderr: modal.stream_type.StreamType = modal.stream_type.StreamType.PIPE,
            timeout: typing.Optional[int] = None,
            workdir: typing.Optional[str] = None,
            secrets: typing.Sequence[modal.secret.Secret] = (),
            text: typing.Literal[False] = False,
            bufsize: typing.Literal[-1, 1] = -1,
            _pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
        ) -> modal.container_process.ContainerProcess[bytes]: ...

    exec: __exec_spec

    @property
    def stdout(self) -> modal.io_streams.StreamReader[str]: ...
    @property
    def stderr(self) -> modal.io_streams.StreamReader[str]: ...
    @property
    def stdin(self) -> modal.io_streams.StreamWriter: ...
    @property
    def returncode(self) -> typing.Optional[int]: ...

    class __list_spec(typing_extensions.Protocol):
        def __call__(
            self,
            *,
            app_id: typing.Optional[str] = None,
            tags: typing.Optional[typing.Dict[str, str]] = None,
            client: typing.Optional[modal.client.Client] = None,
        ) -> typing.Generator[Sandbox, None, None]: ...
        def aio(
            self,
            *,
            app_id: typing.Optional[str] = None,
            tags: typing.Optional[typing.Dict[str, str]] = None,
            client: typing.Optional[modal.client.Client] = None,
        ) -> typing.AsyncGenerator[Sandbox, None]: ...

    list: __list_spec

def __getattr__(name): ...

_default_image: modal.image._Image
