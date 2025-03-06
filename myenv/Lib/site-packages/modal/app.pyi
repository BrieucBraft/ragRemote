import modal._utils.function_utils
import modal.client
import modal.cloud_bucket_mount
import modal.cls
import modal.functions
import modal.gpu
import modal.image
import modal.mount
import modal.network_file_system
import modal.object
import modal.partial_function
import modal.proxy
import modal.retries
import modal.running_app
import modal.sandbox
import modal.schedule
import modal.scheduler_placement
import modal.secret
import modal.volume
import modal_proto.api_pb2
import pathlib
import synchronicity.combined_types
import typing
import typing_extensions

class _LocalEntrypoint:
    _info: modal._utils.function_utils.FunctionInfo
    _app: _App

    def __init__(self, info: modal._utils.function_utils.FunctionInfo, app: _App) -> None: ...
    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any: ...
    @property
    def info(self) -> modal._utils.function_utils.FunctionInfo: ...
    @property
    def app(self) -> _App: ...
    @property
    def stub(self) -> _App: ...

class LocalEntrypoint:
    _info: modal._utils.function_utils.FunctionInfo
    _app: App

    def __init__(self, info: modal._utils.function_utils.FunctionInfo, app: App) -> None: ...
    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any: ...
    @property
    def info(self) -> modal._utils.function_utils.FunctionInfo: ...
    @property
    def app(self) -> App: ...
    @property
    def stub(self) -> App: ...

def check_sequence(items: typing.Sequence[typing.Any], item_type: typing.Type[typing.Any], error_msg: str) -> None: ...

CLS_T = typing.TypeVar("CLS_T", bound="typing.Type[typing.Any]")

P = typing_extensions.ParamSpec("P")

ReturnType = typing.TypeVar("ReturnType")

OriginalReturnType = typing.TypeVar("OriginalReturnType")

class _FunctionDecoratorType:
    @typing.overload
    def __call__(
        self, func: modal.partial_function.PartialFunction[P, ReturnType, OriginalReturnType]
    ) -> modal.functions.Function[P, ReturnType, OriginalReturnType]: ...
    @typing.overload
    def __call__(
        self, func: typing.Callable[P, typing.Coroutine[typing.Any, typing.Any, ReturnType]]
    ) -> modal.functions.Function[P, ReturnType, typing.Coroutine[typing.Any, typing.Any, ReturnType]]: ...
    @typing.overload
    def __call__(self, func: typing.Callable[P, ReturnType]) -> modal.functions.Function[P, ReturnType, ReturnType]: ...

class _App:
    _all_apps: typing.ClassVar[typing.Dict[typing.Optional[str], typing.List[_App]]]
    _container_app: typing.ClassVar[typing.Optional[modal.running_app.RunningApp]]
    _name: typing.Optional[str]
    _description: typing.Optional[str]
    _indexed_objects: typing.Dict[str, modal.object._Object]
    _image: typing.Optional[modal.image._Image]
    _mounts: typing.Sequence[modal.mount._Mount]
    _secrets: typing.Sequence[modal.secret._Secret]
    _volumes: typing.Dict[typing.Union[str, pathlib.PurePosixPath], modal.volume._Volume]
    _web_endpoints: typing.List[str]
    _local_entrypoints: typing.Dict[str, _LocalEntrypoint]
    _app_id: typing.Optional[str]
    _running_app: typing.Optional[modal.running_app.RunningApp]
    _client: typing.Optional[modal.client._Client]

    def __init__(
        self,
        name: typing.Optional[str] = None,
        *,
        image: typing.Optional[modal.image._Image] = None,
        mounts: typing.Sequence[modal.mount._Mount] = [],
        secrets: typing.Sequence[modal.secret._Secret] = [],
        volumes: typing.Dict[typing.Union[str, pathlib.PurePosixPath], modal.volume._Volume] = {},
    ) -> None: ...
    @property
    def name(self) -> typing.Optional[str]: ...
    @property
    def is_interactive(self) -> bool: ...
    @property
    def app_id(self) -> typing.Optional[str]: ...
    @property
    def description(self) -> typing.Optional[str]: ...
    @staticmethod
    async def lookup(
        label: str,
        client: typing.Optional[modal.client._Client] = None,
        environment_name: typing.Optional[str] = None,
        create_if_missing: bool = False,
    ) -> _App: ...
    def set_description(self, description: str): ...
    def _validate_blueprint_value(self, key: str, value: typing.Any): ...
    def _add_object(self, tag, obj): ...
    def __getitem__(self, tag: str): ...
    def __setitem__(self, tag: str, obj: modal.object._Object): ...
    def __getattr__(self, tag: str): ...
    def __setattr__(self, tag: str, obj: modal.object._Object): ...
    @property
    def image(self) -> modal.image._Image: ...
    @image.setter
    def image(self, value): ...
    def _uncreate_all_objects(self): ...
    def _set_local_app(
        self, client: modal.client._Client, running_app: modal.running_app.RunningApp
    ) -> typing.AsyncContextManager[None]: ...
    def run(
        self,
        client: typing.Optional[modal.client._Client] = None,
        show_progress: typing.Optional[bool] = None,
        detach: bool = False,
        interactive: bool = False,
    ) -> typing.AsyncContextManager[_App]: ...
    def _get_default_image(self): ...
    def _get_watch_mounts(self): ...
    def _add_function(self, function: modal.functions._Function, is_web_endpoint: bool): ...
    def _init_container(self, client: modal.client._Client, running_app: modal.running_app.RunningApp): ...
    @property
    def registered_functions(self) -> typing.Dict[str, modal.functions._Function]: ...
    @property
    def registered_classes(self) -> typing.Dict[str, modal.functions._Function]: ...
    @property
    def registered_entrypoints(self) -> typing.Dict[str, _LocalEntrypoint]: ...
    @property
    def indexed_objects(self) -> typing.Dict[str, modal.object._Object]: ...
    @property
    def registered_web_endpoints(self) -> typing.List[str]: ...
    def local_entrypoint(
        self, _warn_parentheses_missing: typing.Any = None, *, name: typing.Optional[str] = None
    ) -> typing.Callable[[typing.Callable[..., typing.Any]], _LocalEntrypoint]: ...
    def function(
        self,
        _warn_parentheses_missing: typing.Any = None,
        *,
        image: typing.Optional[modal.image._Image] = None,
        schedule: typing.Optional[modal.schedule.Schedule] = None,
        secrets: typing.Sequence[modal.secret._Secret] = (),
        gpu: typing.Union[
            None, bool, str, modal.gpu._GPUConfig, typing.List[typing.Union[None, bool, str, modal.gpu._GPUConfig]]
        ] = None,
        serialized: bool = False,
        mounts: typing.Sequence[modal.mount._Mount] = (),
        network_file_systems: typing.Dict[
            typing.Union[str, pathlib.PurePosixPath], modal.network_file_system._NetworkFileSystem
        ] = {},
        volumes: typing.Dict[
            typing.Union[str, pathlib.PurePosixPath],
            typing.Union[modal.volume._Volume, modal.cloud_bucket_mount._CloudBucketMount],
        ] = {},
        allow_cross_region_volumes: bool = False,
        cpu: typing.Union[float, typing.Tuple[float, float], None] = None,
        memory: typing.Union[int, typing.Tuple[int, int], None] = None,
        ephemeral_disk: typing.Optional[int] = None,
        proxy: typing.Optional[modal.proxy._Proxy] = None,
        retries: typing.Union[int, modal.retries.Retries, None] = None,
        concurrency_limit: typing.Optional[int] = None,
        allow_concurrent_inputs: typing.Optional[int] = None,
        container_idle_timeout: typing.Optional[int] = None,
        timeout: typing.Optional[int] = None,
        keep_warm: typing.Optional[int] = None,
        name: typing.Optional[str] = None,
        is_generator: typing.Optional[bool] = None,
        cloud: typing.Optional[str] = None,
        region: typing.Union[str, typing.Sequence[str], None] = None,
        enable_memory_snapshot: bool = False,
        block_network: bool = False,
        max_inputs: typing.Optional[int] = None,
        i6pn: typing.Optional[bool] = None,
        _experimental_scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement] = None,
        _experimental_buffer_containers: typing.Optional[int] = None,
        _experimental_proxy_ip: typing.Optional[str] = None,
        _experimental_custom_scaling_factor: typing.Optional[float] = None,
    ) -> _FunctionDecoratorType: ...
    @typing_extensions.dataclass_transform(
        field_specifiers=(modal.cls.parameter,),
        kw_only_default=True,
    )
    def cls(
        self,
        _warn_parentheses_missing: typing.Optional[bool] = None,
        *,
        image: typing.Optional[modal.image._Image] = None,
        secrets: typing.Sequence[modal.secret._Secret] = (),
        gpu: typing.Union[
            None, bool, str, modal.gpu._GPUConfig, typing.List[typing.Union[None, bool, str, modal.gpu._GPUConfig]]
        ] = None,
        serialized: bool = False,
        mounts: typing.Sequence[modal.mount._Mount] = (),
        network_file_systems: typing.Dict[
            typing.Union[str, pathlib.PurePosixPath], modal.network_file_system._NetworkFileSystem
        ] = {},
        volumes: typing.Dict[
            typing.Union[str, pathlib.PurePosixPath],
            typing.Union[modal.volume._Volume, modal.cloud_bucket_mount._CloudBucketMount],
        ] = {},
        allow_cross_region_volumes: bool = False,
        cpu: typing.Union[float, typing.Tuple[float, float], None] = None,
        memory: typing.Union[int, typing.Tuple[int, int], None] = None,
        ephemeral_disk: typing.Optional[int] = None,
        proxy: typing.Optional[modal.proxy._Proxy] = None,
        retries: typing.Union[int, modal.retries.Retries, None] = None,
        concurrency_limit: typing.Optional[int] = None,
        allow_concurrent_inputs: typing.Optional[int] = None,
        container_idle_timeout: typing.Optional[int] = None,
        timeout: typing.Optional[int] = None,
        keep_warm: typing.Optional[int] = None,
        cloud: typing.Optional[str] = None,
        region: typing.Union[str, typing.Sequence[str], None] = None,
        enable_memory_snapshot: bool = False,
        block_network: bool = False,
        max_inputs: typing.Optional[int] = None,
        _experimental_scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement] = None,
        _experimental_buffer_containers: typing.Optional[int] = None,
        _experimental_proxy_ip: typing.Optional[str] = None,
        _experimental_custom_scaling_factor: typing.Optional[float] = None,
    ) -> typing.Callable[[CLS_T], CLS_T]: ...
    async def spawn_sandbox(
        self,
        *entrypoint_args: str,
        image: typing.Optional[modal.image._Image] = None,
        mounts: typing.Sequence[modal.mount._Mount] = (),
        secrets: typing.Sequence[modal.secret._Secret] = (),
        network_file_systems: typing.Dict[
            typing.Union[str, pathlib.PurePosixPath], modal.network_file_system._NetworkFileSystem
        ] = {},
        timeout: typing.Optional[int] = None,
        workdir: typing.Optional[str] = None,
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
        cloud: typing.Optional[str] = None,
        region: typing.Union[str, typing.Sequence[str], None] = None,
        cpu: typing.Union[float, typing.Tuple[float, float], None] = None,
        memory: typing.Union[int, typing.Tuple[int, int], None] = None,
        block_network: bool = False,
        volumes: typing.Dict[
            typing.Union[str, pathlib.PurePosixPath],
            typing.Union[modal.volume._Volume, modal.cloud_bucket_mount._CloudBucketMount],
        ] = {},
        pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
        _experimental_scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement] = None,
    ) -> modal.sandbox._Sandbox: ...
    def include(self, /, other_app: _App): ...
    def _logs(self, client: typing.Optional[modal.client._Client] = None) -> typing.AsyncGenerator[str, None]: ...
    @classmethod
    def _reset_container_app(cls): ...

class App:
    _all_apps: typing.ClassVar[typing.Dict[typing.Optional[str], typing.List[App]]]
    _container_app: typing.ClassVar[typing.Optional[modal.running_app.RunningApp]]
    _name: typing.Optional[str]
    _description: typing.Optional[str]
    _indexed_objects: typing.Dict[str, modal.object.Object]
    _image: typing.Optional[modal.image.Image]
    _mounts: typing.Sequence[modal.mount.Mount]
    _secrets: typing.Sequence[modal.secret.Secret]
    _volumes: typing.Dict[typing.Union[str, pathlib.PurePosixPath], modal.volume.Volume]
    _web_endpoints: typing.List[str]
    _local_entrypoints: typing.Dict[str, LocalEntrypoint]
    _app_id: typing.Optional[str]
    _running_app: typing.Optional[modal.running_app.RunningApp]
    _client: typing.Optional[modal.client.Client]

    def __init__(
        self,
        name: typing.Optional[str] = None,
        *,
        image: typing.Optional[modal.image.Image] = None,
        mounts: typing.Sequence[modal.mount.Mount] = [],
        secrets: typing.Sequence[modal.secret.Secret] = [],
        volumes: typing.Dict[typing.Union[str, pathlib.PurePosixPath], modal.volume.Volume] = {},
    ) -> None: ...
    @property
    def name(self) -> typing.Optional[str]: ...
    @property
    def is_interactive(self) -> bool: ...
    @property
    def app_id(self) -> typing.Optional[str]: ...
    @property
    def description(self) -> typing.Optional[str]: ...

    class __lookup_spec(typing_extensions.Protocol):
        def __call__(
            self,
            label: str,
            client: typing.Optional[modal.client.Client] = None,
            environment_name: typing.Optional[str] = None,
            create_if_missing: bool = False,
        ) -> App: ...
        async def aio(
            self,
            label: str,
            client: typing.Optional[modal.client.Client] = None,
            environment_name: typing.Optional[str] = None,
            create_if_missing: bool = False,
        ) -> App: ...

    lookup: __lookup_spec

    def set_description(self, description: str): ...
    def _validate_blueprint_value(self, key: str, value: typing.Any): ...
    def _add_object(self, tag, obj): ...
    def __getitem__(self, tag: str): ...
    def __setitem__(self, tag: str, obj: modal.object.Object): ...
    def __getattr__(self, tag: str): ...
    def __setattr__(self, tag: str, obj: modal.object.Object): ...
    @property
    def image(self) -> modal.image.Image: ...
    @image.setter
    def image(self, value): ...
    def _uncreate_all_objects(self): ...

    class ___set_local_app_spec(typing_extensions.Protocol):
        def __call__(
            self, client: modal.client.Client, running_app: modal.running_app.RunningApp
        ) -> synchronicity.combined_types.AsyncAndBlockingContextManager[None]: ...
        def aio(
            self, client: modal.client.Client, running_app: modal.running_app.RunningApp
        ) -> typing.AsyncContextManager[None]: ...

    _set_local_app: ___set_local_app_spec

    class __run_spec(typing_extensions.Protocol):
        def __call__(
            self,
            client: typing.Optional[modal.client.Client] = None,
            show_progress: typing.Optional[bool] = None,
            detach: bool = False,
            interactive: bool = False,
        ) -> synchronicity.combined_types.AsyncAndBlockingContextManager[App]: ...
        def aio(
            self,
            client: typing.Optional[modal.client.Client] = None,
            show_progress: typing.Optional[bool] = None,
            detach: bool = False,
            interactive: bool = False,
        ) -> typing.AsyncContextManager[App]: ...

    run: __run_spec

    def _get_default_image(self): ...
    def _get_watch_mounts(self): ...
    def _add_function(self, function: modal.functions.Function, is_web_endpoint: bool): ...
    def _init_container(self, client: modal.client.Client, running_app: modal.running_app.RunningApp): ...
    @property
    def registered_functions(self) -> typing.Dict[str, modal.functions.Function]: ...
    @property
    def registered_classes(self) -> typing.Dict[str, modal.functions.Function]: ...
    @property
    def registered_entrypoints(self) -> typing.Dict[str, LocalEntrypoint]: ...
    @property
    def indexed_objects(self) -> typing.Dict[str, modal.object.Object]: ...
    @property
    def registered_web_endpoints(self) -> typing.List[str]: ...
    def local_entrypoint(
        self, _warn_parentheses_missing: typing.Any = None, *, name: typing.Optional[str] = None
    ) -> typing.Callable[[typing.Callable[..., typing.Any]], LocalEntrypoint]: ...
    def function(
        self,
        _warn_parentheses_missing: typing.Any = None,
        *,
        image: typing.Optional[modal.image.Image] = None,
        schedule: typing.Optional[modal.schedule.Schedule] = None,
        secrets: typing.Sequence[modal.secret.Secret] = (),
        gpu: typing.Union[
            None, bool, str, modal.gpu._GPUConfig, typing.List[typing.Union[None, bool, str, modal.gpu._GPUConfig]]
        ] = None,
        serialized: bool = False,
        mounts: typing.Sequence[modal.mount.Mount] = (),
        network_file_systems: typing.Dict[
            typing.Union[str, pathlib.PurePosixPath], modal.network_file_system.NetworkFileSystem
        ] = {},
        volumes: typing.Dict[
            typing.Union[str, pathlib.PurePosixPath],
            typing.Union[modal.volume.Volume, modal.cloud_bucket_mount.CloudBucketMount],
        ] = {},
        allow_cross_region_volumes: bool = False,
        cpu: typing.Union[float, typing.Tuple[float, float], None] = None,
        memory: typing.Union[int, typing.Tuple[int, int], None] = None,
        ephemeral_disk: typing.Optional[int] = None,
        proxy: typing.Optional[modal.proxy.Proxy] = None,
        retries: typing.Union[int, modal.retries.Retries, None] = None,
        concurrency_limit: typing.Optional[int] = None,
        allow_concurrent_inputs: typing.Optional[int] = None,
        container_idle_timeout: typing.Optional[int] = None,
        timeout: typing.Optional[int] = None,
        keep_warm: typing.Optional[int] = None,
        name: typing.Optional[str] = None,
        is_generator: typing.Optional[bool] = None,
        cloud: typing.Optional[str] = None,
        region: typing.Union[str, typing.Sequence[str], None] = None,
        enable_memory_snapshot: bool = False,
        block_network: bool = False,
        max_inputs: typing.Optional[int] = None,
        i6pn: typing.Optional[bool] = None,
        _experimental_scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement] = None,
        _experimental_buffer_containers: typing.Optional[int] = None,
        _experimental_proxy_ip: typing.Optional[str] = None,
        _experimental_custom_scaling_factor: typing.Optional[float] = None,
    ) -> _FunctionDecoratorType: ...
    @typing_extensions.dataclass_transform(
        field_specifiers=(modal.cls.parameter,),
        kw_only_default=True,
    )
    def cls(
        self,
        _warn_parentheses_missing: typing.Optional[bool] = None,
        *,
        image: typing.Optional[modal.image.Image] = None,
        secrets: typing.Sequence[modal.secret.Secret] = (),
        gpu: typing.Union[
            None, bool, str, modal.gpu._GPUConfig, typing.List[typing.Union[None, bool, str, modal.gpu._GPUConfig]]
        ] = None,
        serialized: bool = False,
        mounts: typing.Sequence[modal.mount.Mount] = (),
        network_file_systems: typing.Dict[
            typing.Union[str, pathlib.PurePosixPath], modal.network_file_system.NetworkFileSystem
        ] = {},
        volumes: typing.Dict[
            typing.Union[str, pathlib.PurePosixPath],
            typing.Union[modal.volume.Volume, modal.cloud_bucket_mount.CloudBucketMount],
        ] = {},
        allow_cross_region_volumes: bool = False,
        cpu: typing.Union[float, typing.Tuple[float, float], None] = None,
        memory: typing.Union[int, typing.Tuple[int, int], None] = None,
        ephemeral_disk: typing.Optional[int] = None,
        proxy: typing.Optional[modal.proxy.Proxy] = None,
        retries: typing.Union[int, modal.retries.Retries, None] = None,
        concurrency_limit: typing.Optional[int] = None,
        allow_concurrent_inputs: typing.Optional[int] = None,
        container_idle_timeout: typing.Optional[int] = None,
        timeout: typing.Optional[int] = None,
        keep_warm: typing.Optional[int] = None,
        cloud: typing.Optional[str] = None,
        region: typing.Union[str, typing.Sequence[str], None] = None,
        enable_memory_snapshot: bool = False,
        block_network: bool = False,
        max_inputs: typing.Optional[int] = None,
        _experimental_scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement] = None,
        _experimental_buffer_containers: typing.Optional[int] = None,
        _experimental_proxy_ip: typing.Optional[str] = None,
        _experimental_custom_scaling_factor: typing.Optional[float] = None,
    ) -> typing.Callable[[CLS_T], CLS_T]: ...

    class __spawn_sandbox_spec(typing_extensions.Protocol):
        def __call__(
            self,
            *entrypoint_args: str,
            image: typing.Optional[modal.image.Image] = None,
            mounts: typing.Sequence[modal.mount.Mount] = (),
            secrets: typing.Sequence[modal.secret.Secret] = (),
            network_file_systems: typing.Dict[
                typing.Union[str, pathlib.PurePosixPath], modal.network_file_system.NetworkFileSystem
            ] = {},
            timeout: typing.Optional[int] = None,
            workdir: typing.Optional[str] = None,
            gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
            cloud: typing.Optional[str] = None,
            region: typing.Union[str, typing.Sequence[str], None] = None,
            cpu: typing.Union[float, typing.Tuple[float, float], None] = None,
            memory: typing.Union[int, typing.Tuple[int, int], None] = None,
            block_network: bool = False,
            volumes: typing.Dict[
                typing.Union[str, pathlib.PurePosixPath],
                typing.Union[modal.volume.Volume, modal.cloud_bucket_mount.CloudBucketMount],
            ] = {},
            pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
            _experimental_scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement] = None,
        ) -> modal.sandbox.Sandbox: ...
        async def aio(
            self,
            *entrypoint_args: str,
            image: typing.Optional[modal.image.Image] = None,
            mounts: typing.Sequence[modal.mount.Mount] = (),
            secrets: typing.Sequence[modal.secret.Secret] = (),
            network_file_systems: typing.Dict[
                typing.Union[str, pathlib.PurePosixPath], modal.network_file_system.NetworkFileSystem
            ] = {},
            timeout: typing.Optional[int] = None,
            workdir: typing.Optional[str] = None,
            gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
            cloud: typing.Optional[str] = None,
            region: typing.Union[str, typing.Sequence[str], None] = None,
            cpu: typing.Union[float, typing.Tuple[float, float], None] = None,
            memory: typing.Union[int, typing.Tuple[int, int], None] = None,
            block_network: bool = False,
            volumes: typing.Dict[
                typing.Union[str, pathlib.PurePosixPath],
                typing.Union[modal.volume.Volume, modal.cloud_bucket_mount.CloudBucketMount],
            ] = {},
            pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
            _experimental_scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement] = None,
        ) -> modal.sandbox.Sandbox: ...

    spawn_sandbox: __spawn_sandbox_spec

    def include(self, /, other_app: App): ...

    class ___logs_spec(typing_extensions.Protocol):
        def __call__(
            self, client: typing.Optional[modal.client.Client] = None
        ) -> typing.Generator[str, None, None]: ...
        def aio(self, client: typing.Optional[modal.client.Client] = None) -> typing.AsyncGenerator[str, None]: ...

    _logs: ___logs_spec

    @classmethod
    def _reset_container_app(cls): ...

class _Stub(_App):
    @staticmethod
    def __new__(
        cls,
        name: typing.Optional[str] = None,
        *,
        image: typing.Optional[modal.image._Image] = None,
        mounts: typing.Sequence[modal.mount._Mount] = [],
        secrets: typing.Sequence[modal.secret._Secret] = [],
        volumes: typing.Dict[typing.Union[str, pathlib.PurePosixPath], modal.volume._Volume] = {},
    ): ...

class Stub(App):
    def __init__(
        self,
        name: typing.Optional[str] = None,
        *,
        image: typing.Optional[modal.image.Image] = None,
        mounts: typing.Sequence[modal.mount.Mount] = [],
        secrets: typing.Sequence[modal.secret.Secret] = [],
        volumes: typing.Dict[typing.Union[str, pathlib.PurePosixPath], modal.volume.Volume] = {},
    ) -> None: ...

_default_image: modal.image._Image
