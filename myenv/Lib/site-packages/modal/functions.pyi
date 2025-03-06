import google.protobuf.message
import modal._utils.async_utils
import modal._utils.function_utils
import modal.app
import modal.call_graph
import modal.client
import modal.cloud_bucket_mount
import modal.cls
import modal.gpu
import modal.image
import modal.mount
import modal.network_file_system
import modal.object
import modal.parallel_map
import modal.partial_function
import modal.proxy
import modal.retries
import modal.schedule
import modal.scheduler_placement
import modal.secret
import modal.volume
import modal_proto.api_pb2
import modal_proto.modal_api_grpc
import pathlib
import typing
import typing_extensions

class _Invocation:
    stub: modal_proto.modal_api_grpc.ModalClientModal

    def __init__(
        self, stub: modal_proto.modal_api_grpc.ModalClientModal, function_call_id: str, client: modal.client._Client
    ): ...
    @staticmethod
    async def create(
        function: _Function, args, kwargs, *, client: modal.client._Client, function_call_invocation_type: int
    ) -> _Invocation: ...
    async def pop_function_call_outputs(
        self, timeout: typing.Optional[float], clear_on_success: bool
    ) -> modal_proto.api_pb2.FunctionGetOutputsResponse: ...
    async def run_function(self) -> typing.Any: ...
    async def poll_function(self, timeout: typing.Optional[float] = None): ...
    def run_generator(self): ...

class FunctionStats:
    backlog: int
    num_total_runners: int

    def __getattr__(self, name): ...
    def __init__(self, backlog: int, num_total_runners: int) -> None: ...
    def __repr__(self): ...
    def __eq__(self, other): ...
    def __setattr__(self, name, value): ...
    def __delattr__(self, name): ...
    def __hash__(self): ...

def _parse_retries(
    retries: typing.Union[int, modal.retries.Retries, None], source: str = ""
) -> typing.Optional[modal_proto.api_pb2.FunctionRetryPolicy]: ...

class _FunctionSpec:
    image: typing.Optional[modal.image._Image]
    mounts: typing.Sequence[modal.mount._Mount]
    secrets: typing.Sequence[modal.secret._Secret]
    network_file_systems: typing.Dict[
        typing.Union[str, pathlib.PurePosixPath], modal.network_file_system._NetworkFileSystem
    ]
    volumes: typing.Dict[
        typing.Union[str, pathlib.PurePosixPath],
        typing.Union[modal.volume._Volume, modal.cloud_bucket_mount._CloudBucketMount],
    ]
    gpus: typing.Union[
        None, bool, str, modal.gpu._GPUConfig, typing.List[typing.Union[None, bool, str, modal.gpu._GPUConfig]]
    ]
    cloud: typing.Optional[str]
    cpu: typing.Optional[float]
    memory: typing.Union[int, typing.Tuple[int, int], None]
    ephemeral_disk: typing.Optional[int]
    scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement]

    def __init__(
        self,
        image: typing.Optional[modal.image._Image],
        mounts: typing.Sequence[modal.mount._Mount],
        secrets: typing.Sequence[modal.secret._Secret],
        network_file_systems: typing.Dict[
            typing.Union[str, pathlib.PurePosixPath], modal.network_file_system._NetworkFileSystem
        ],
        volumes: typing.Dict[
            typing.Union[str, pathlib.PurePosixPath],
            typing.Union[modal.volume._Volume, modal.cloud_bucket_mount._CloudBucketMount],
        ],
        gpus: typing.Union[
            None, bool, str, modal.gpu._GPUConfig, typing.List[typing.Union[None, bool, str, modal.gpu._GPUConfig]]
        ],
        cloud: typing.Optional[str],
        cpu: typing.Optional[float],
        memory: typing.Union[int, typing.Tuple[int, int], None],
        ephemeral_disk: typing.Optional[int],
        scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement],
    ) -> None: ...
    def __repr__(self): ...
    def __eq__(self, other): ...

P = typing_extensions.ParamSpec("P")

ReturnType = typing.TypeVar("ReturnType", covariant=True)

OriginalReturnType = typing.TypeVar("OriginalReturnType", covariant=True)

class _Function(typing.Generic[P, ReturnType, OriginalReturnType], modal.object._Object):
    _info: typing.Optional[modal._utils.function_utils.FunctionInfo]
    _serve_mounts: typing.FrozenSet[modal.mount._Mount]
    _app: typing.Optional[modal.app._App]
    _obj: typing.Optional[modal.cls._Obj]
    _web_url: typing.Optional[str]
    _function_name: typing.Optional[str]
    _is_method: bool
    _spec: typing.Optional[_FunctionSpec]
    _tag: str
    _raw_f: typing.Callable[..., typing.Any]
    _build_args: dict
    _can_use_base_function: bool
    _is_generator: typing.Optional[bool]
    _cluster_size: typing.Optional[int]
    _use_function_id: str
    _use_method_name: str
    _parent: typing.Optional[_Function]
    _class_parameter_info: typing.Optional[modal_proto.api_pb2.ClassParameterInfo]
    _method_handle_metadata: typing.Optional[typing.Dict[str, modal_proto.api_pb2.FunctionHandleMetadata]]

    def _bind_method(self, user_cls, method_name: str, partial_function: modal.partial_function._PartialFunction): ...
    def _bind_method_old(
        self, user_cls, method_name: str, partial_function: modal.partial_function._PartialFunction
    ): ...
    def _bind_instance_method(self, class_bound_method: _Function): ...
    @staticmethod
    def from_args(
        info: modal._utils.function_utils.FunctionInfo,
        app,
        image: modal.image._Image,
        secrets: typing.Sequence[modal.secret._Secret] = (),
        schedule: typing.Optional[modal.schedule.Schedule] = None,
        is_generator=False,
        gpu: typing.Union[
            None, bool, str, modal.gpu._GPUConfig, typing.List[typing.Union[None, bool, str, modal.gpu._GPUConfig]]
        ] = None,
        mounts: typing.Collection[modal.mount._Mount] = (),
        network_file_systems: typing.Dict[
            typing.Union[str, pathlib.PurePosixPath], modal.network_file_system._NetworkFileSystem
        ] = {},
        allow_cross_region_volumes: bool = False,
        volumes: typing.Dict[
            typing.Union[str, pathlib.PurePosixPath],
            typing.Union[modal.volume._Volume, modal.cloud_bucket_mount._CloudBucketMount],
        ] = {},
        webhook_config: typing.Optional[modal_proto.api_pb2.WebhookConfig] = None,
        memory: typing.Union[int, typing.Tuple[int, int], None] = None,
        proxy: typing.Optional[modal.proxy._Proxy] = None,
        retries: typing.Union[int, modal.retries.Retries, None] = None,
        timeout: typing.Optional[int] = None,
        concurrency_limit: typing.Optional[int] = None,
        allow_concurrent_inputs: typing.Optional[int] = None,
        batch_max_size: typing.Optional[int] = None,
        batch_wait_ms: typing.Optional[int] = None,
        container_idle_timeout: typing.Optional[int] = None,
        cpu: typing.Optional[float] = None,
        keep_warm: typing.Optional[int] = None,
        cloud: typing.Optional[str] = None,
        scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement] = None,
        is_builder_function: bool = False,
        is_auto_snapshot: bool = False,
        enable_memory_snapshot: bool = False,
        block_network: bool = False,
        i6pn_enabled: bool = False,
        cluster_size: typing.Optional[int] = None,
        max_inputs: typing.Optional[int] = None,
        ephemeral_disk: typing.Optional[int] = None,
        _experimental_buffer_containers: typing.Optional[int] = None,
        _experimental_proxy_ip: typing.Optional[str] = None,
        _experimental_custom_scaling_factor: typing.Optional[float] = None,
    ) -> None: ...
    def _bind_parameters(
        self,
        obj: modal.cls._Obj,
        from_other_workspace: bool,
        options: typing.Optional[modal_proto.api_pb2.FunctionOptions],
        args: typing.Sized,
        kwargs: typing.Dict[str, typing.Any],
    ) -> _Function: ...
    async def keep_warm(self, warm_pool_size: int) -> None: ...
    @classmethod
    def from_name(
        cls: typing.Type[_Function], app_name: str, tag: str, namespace=1, environment_name: typing.Optional[str] = None
    ) -> _Function: ...
    @staticmethod
    async def lookup(
        app_name: str,
        tag: str,
        namespace=1,
        client: typing.Optional[modal.client._Client] = None,
        environment_name: typing.Optional[str] = None,
    ) -> _Function: ...
    @property
    def tag(self) -> str: ...
    @property
    def app(self) -> modal.app._App: ...
    @property
    def stub(self) -> modal.app._App: ...
    @property
    def info(self) -> modal._utils.function_utils.FunctionInfo: ...
    @property
    def spec(self) -> _FunctionSpec: ...
    def get_build_def(self) -> str: ...
    def _initialize_from_empty(self): ...
    def _hydrate_metadata(self, metadata: typing.Optional[google.protobuf.message.Message]): ...
    def _invocation_function_id(self) -> str: ...
    def _get_metadata(self): ...
    def _check_no_web_url(self, fn_name: str): ...
    @property
    def web_url(self) -> str: ...
    @property
    def is_generator(self) -> bool: ...
    @property
    def cluster_size(self) -> int: ...
    def _map(
        self, input_queue: modal.parallel_map._SynchronizedQueue, order_outputs: bool, return_exceptions: bool
    ) -> typing.AsyncGenerator[typing.Any, None]: ...
    async def _call_function(self, args, kwargs) -> ReturnType: ...
    async def _call_function_nowait(self, args, kwargs, function_call_invocation_type: int) -> _Invocation: ...
    def _call_generator(self, args, kwargs): ...
    async def _call_generator_nowait(self, args, kwargs): ...
    async def remote(self, *args: P.args, **kwargs: P.kwargs) -> ReturnType: ...
    def remote_gen(self, *args, **kwargs) -> typing.AsyncGenerator[typing.Any, None]: ...
    def _get_info(self) -> modal._utils.function_utils.FunctionInfo: ...
    def _get_obj(self) -> typing.Optional[modal.cls._Obj]: ...
    def local(self, *args: P.args, **kwargs: P.kwargs) -> OriginalReturnType: ...
    async def _experimental_spawn(self, *args: P.args, **kwargs: P.kwargs) -> _FunctionCall[ReturnType]: ...
    async def spawn(self, *args: P.args, **kwargs: P.kwargs) -> _FunctionCall[ReturnType]: ...
    def get_raw_f(self) -> typing.Callable[..., typing.Any]: ...
    async def get_current_stats(self) -> FunctionStats: ...

    class __map_spec(typing_extensions.Protocol):
        def __call__(
            self, *input_iterators, kwargs={}, order_outputs: bool = True, return_exceptions: bool = False
        ) -> modal._utils.async_utils.AsyncOrSyncIterable: ...
        def aio(
            self,
            *input_iterators: typing.Union[typing.Iterable[typing.Any], typing.AsyncIterable[typing.Any]],
            kwargs={},
            order_outputs: bool = True,
            return_exceptions: bool = False,
        ) -> typing.AsyncGenerator[typing.Any, None]: ...

    map: __map_spec

    class __starmap_spec(typing_extensions.Protocol):
        def __call__(
            self,
            input_iterator: typing.Iterable[typing.Sequence[typing.Any]],
            kwargs={},
            order_outputs: bool = True,
            return_exceptions: bool = False,
        ) -> modal._utils.async_utils.AsyncOrSyncIterable: ...
        def aio(
            self,
            input_iterator: typing.Union[
                typing.Iterable[typing.Sequence[typing.Any]], typing.AsyncIterable[typing.Sequence[typing.Any]]
            ],
            kwargs={},
            order_outputs: bool = True,
            return_exceptions: bool = False,
        ) -> typing.AsyncIterable[typing.Any]: ...

    starmap: __starmap_spec

    class __for_each_spec(typing_extensions.Protocol):
        def __call__(self, *input_iterators, kwargs={}, ignore_exceptions: bool = False): ...
        async def aio(self, *input_iterators, kwargs={}, ignore_exceptions: bool = False): ...

    for_each: __for_each_spec

ReturnType_INNER = typing.TypeVar("ReturnType_INNER", covariant=True)

P_INNER = typing_extensions.ParamSpec("P_INNER")

class Function(typing.Generic[P, ReturnType, OriginalReturnType], modal.object.Object):
    _info: typing.Optional[modal._utils.function_utils.FunctionInfo]
    _serve_mounts: typing.FrozenSet[modal.mount.Mount]
    _app: typing.Optional[modal.app.App]
    _obj: typing.Optional[modal.cls.Obj]
    _web_url: typing.Optional[str]
    _function_name: typing.Optional[str]
    _is_method: bool
    _spec: typing.Optional[_FunctionSpec]
    _tag: str
    _raw_f: typing.Callable[..., typing.Any]
    _build_args: dict
    _can_use_base_function: bool
    _is_generator: typing.Optional[bool]
    _cluster_size: typing.Optional[int]
    _use_function_id: str
    _use_method_name: str
    _parent: typing.Optional[Function]
    _class_parameter_info: typing.Optional[modal_proto.api_pb2.ClassParameterInfo]
    _method_handle_metadata: typing.Optional[typing.Dict[str, modal_proto.api_pb2.FunctionHandleMetadata]]

    def __init__(self, *args, **kwargs): ...
    def _bind_method(self, user_cls, method_name: str, partial_function: modal.partial_function.PartialFunction): ...
    def _bind_method_old(
        self, user_cls, method_name: str, partial_function: modal.partial_function.PartialFunction
    ): ...
    def _bind_instance_method(self, class_bound_method: Function): ...
    @staticmethod
    def from_args(
        info: modal._utils.function_utils.FunctionInfo,
        app,
        image: modal.image.Image,
        secrets: typing.Sequence[modal.secret.Secret] = (),
        schedule: typing.Optional[modal.schedule.Schedule] = None,
        is_generator=False,
        gpu: typing.Union[
            None, bool, str, modal.gpu._GPUConfig, typing.List[typing.Union[None, bool, str, modal.gpu._GPUConfig]]
        ] = None,
        mounts: typing.Collection[modal.mount.Mount] = (),
        network_file_systems: typing.Dict[
            typing.Union[str, pathlib.PurePosixPath], modal.network_file_system.NetworkFileSystem
        ] = {},
        allow_cross_region_volumes: bool = False,
        volumes: typing.Dict[
            typing.Union[str, pathlib.PurePosixPath],
            typing.Union[modal.volume.Volume, modal.cloud_bucket_mount.CloudBucketMount],
        ] = {},
        webhook_config: typing.Optional[modal_proto.api_pb2.WebhookConfig] = None,
        memory: typing.Union[int, typing.Tuple[int, int], None] = None,
        proxy: typing.Optional[modal.proxy.Proxy] = None,
        retries: typing.Union[int, modal.retries.Retries, None] = None,
        timeout: typing.Optional[int] = None,
        concurrency_limit: typing.Optional[int] = None,
        allow_concurrent_inputs: typing.Optional[int] = None,
        batch_max_size: typing.Optional[int] = None,
        batch_wait_ms: typing.Optional[int] = None,
        container_idle_timeout: typing.Optional[int] = None,
        cpu: typing.Optional[float] = None,
        keep_warm: typing.Optional[int] = None,
        cloud: typing.Optional[str] = None,
        scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement] = None,
        is_builder_function: bool = False,
        is_auto_snapshot: bool = False,
        enable_memory_snapshot: bool = False,
        block_network: bool = False,
        i6pn_enabled: bool = False,
        cluster_size: typing.Optional[int] = None,
        max_inputs: typing.Optional[int] = None,
        ephemeral_disk: typing.Optional[int] = None,
        _experimental_buffer_containers: typing.Optional[int] = None,
        _experimental_proxy_ip: typing.Optional[str] = None,
        _experimental_custom_scaling_factor: typing.Optional[float] = None,
    ) -> None: ...
    def _bind_parameters(
        self,
        obj: modal.cls.Obj,
        from_other_workspace: bool,
        options: typing.Optional[modal_proto.api_pb2.FunctionOptions],
        args: typing.Sized,
        kwargs: typing.Dict[str, typing.Any],
    ) -> Function: ...

    class __keep_warm_spec(typing_extensions.Protocol):
        def __call__(self, warm_pool_size: int) -> None: ...
        async def aio(self, warm_pool_size: int) -> None: ...

    keep_warm: __keep_warm_spec

    @classmethod
    def from_name(
        cls: typing.Type[Function], app_name: str, tag: str, namespace=1, environment_name: typing.Optional[str] = None
    ) -> Function: ...

    class __lookup_spec(typing_extensions.Protocol):
        def __call__(
            self,
            app_name: str,
            tag: str,
            namespace=1,
            client: typing.Optional[modal.client.Client] = None,
            environment_name: typing.Optional[str] = None,
        ) -> Function: ...
        async def aio(
            self,
            app_name: str,
            tag: str,
            namespace=1,
            client: typing.Optional[modal.client.Client] = None,
            environment_name: typing.Optional[str] = None,
        ) -> Function: ...

    lookup: __lookup_spec

    @property
    def tag(self) -> str: ...
    @property
    def app(self) -> modal.app.App: ...
    @property
    def stub(self) -> modal.app.App: ...
    @property
    def info(self) -> modal._utils.function_utils.FunctionInfo: ...
    @property
    def spec(self) -> _FunctionSpec: ...
    def get_build_def(self) -> str: ...
    def _initialize_from_empty(self): ...
    def _hydrate_metadata(self, metadata: typing.Optional[google.protobuf.message.Message]): ...
    def _invocation_function_id(self) -> str: ...
    def _get_metadata(self): ...
    def _check_no_web_url(self, fn_name: str): ...
    @property
    def web_url(self) -> str: ...
    @property
    def is_generator(self) -> bool: ...
    @property
    def cluster_size(self) -> int: ...

    class ___map_spec(typing_extensions.Protocol):
        def __call__(
            self, input_queue: modal.parallel_map.SynchronizedQueue, order_outputs: bool, return_exceptions: bool
        ) -> typing.Generator[typing.Any, None, None]: ...
        def aio(
            self, input_queue: modal.parallel_map.SynchronizedQueue, order_outputs: bool, return_exceptions: bool
        ) -> typing.AsyncGenerator[typing.Any, None]: ...

    _map: ___map_spec

    class ___call_function_spec(typing_extensions.Protocol[ReturnType_INNER]):
        def __call__(self, args, kwargs) -> ReturnType_INNER: ...
        async def aio(self, args, kwargs) -> ReturnType_INNER: ...

    _call_function: ___call_function_spec[ReturnType]

    class ___call_function_nowait_spec(typing_extensions.Protocol):
        def __call__(self, args, kwargs, function_call_invocation_type: int) -> _Invocation: ...
        async def aio(self, args, kwargs, function_call_invocation_type: int) -> _Invocation: ...

    _call_function_nowait: ___call_function_nowait_spec

    def _call_generator(self, args, kwargs): ...

    class ___call_generator_nowait_spec(typing_extensions.Protocol):
        def __call__(self, args, kwargs): ...
        async def aio(self, args, kwargs): ...

    _call_generator_nowait: ___call_generator_nowait_spec

    class __remote_spec(typing_extensions.Protocol[ReturnType_INNER, P_INNER]):
        def __call__(self, *args: P_INNER.args, **kwargs: P_INNER.kwargs) -> ReturnType_INNER: ...
        async def aio(self, *args: P_INNER.args, **kwargs: P_INNER.kwargs) -> ReturnType_INNER: ...

    remote: __remote_spec[ReturnType, P]

    class __remote_gen_spec(typing_extensions.Protocol):
        def __call__(self, *args, **kwargs) -> typing.Generator[typing.Any, None, None]: ...
        def aio(self, *args, **kwargs) -> typing.AsyncGenerator[typing.Any, None]: ...

    remote_gen: __remote_gen_spec

    def _get_info(self) -> modal._utils.function_utils.FunctionInfo: ...
    def _get_obj(self) -> typing.Optional[modal.cls.Obj]: ...
    def local(self, *args: P.args, **kwargs: P.kwargs) -> OriginalReturnType: ...

    class ___experimental_spawn_spec(typing_extensions.Protocol[ReturnType_INNER, P_INNER]):
        def __call__(self, *args: P_INNER.args, **kwargs: P_INNER.kwargs) -> FunctionCall[ReturnType_INNER]: ...
        async def aio(self, *args: P_INNER.args, **kwargs: P_INNER.kwargs) -> FunctionCall[ReturnType_INNER]: ...

    _experimental_spawn: ___experimental_spawn_spec[ReturnType, P]

    class __spawn_spec(typing_extensions.Protocol[ReturnType_INNER, P_INNER]):
        def __call__(self, *args: P_INNER.args, **kwargs: P_INNER.kwargs) -> FunctionCall[ReturnType_INNER]: ...
        async def aio(self, *args: P_INNER.args, **kwargs: P_INNER.kwargs) -> FunctionCall[ReturnType_INNER]: ...

    spawn: __spawn_spec[ReturnType, P]

    def get_raw_f(self) -> typing.Callable[..., typing.Any]: ...

    class __get_current_stats_spec(typing_extensions.Protocol):
        def __call__(self) -> FunctionStats: ...
        async def aio(self) -> FunctionStats: ...

    get_current_stats: __get_current_stats_spec

    class __map_spec(typing_extensions.Protocol):
        def __call__(
            self, *input_iterators, kwargs={}, order_outputs: bool = True, return_exceptions: bool = False
        ) -> modal._utils.async_utils.AsyncOrSyncIterable: ...
        def aio(
            self,
            *input_iterators: typing.Union[typing.Iterable[typing.Any], typing.AsyncIterable[typing.Any]],
            kwargs={},
            order_outputs: bool = True,
            return_exceptions: bool = False,
        ) -> typing.AsyncGenerator[typing.Any, None]: ...

    map: __map_spec

    class __starmap_spec(typing_extensions.Protocol):
        def __call__(
            self,
            input_iterator: typing.Iterable[typing.Sequence[typing.Any]],
            kwargs={},
            order_outputs: bool = True,
            return_exceptions: bool = False,
        ) -> modal._utils.async_utils.AsyncOrSyncIterable: ...
        def aio(
            self,
            input_iterator: typing.Union[
                typing.Iterable[typing.Sequence[typing.Any]], typing.AsyncIterable[typing.Sequence[typing.Any]]
            ],
            kwargs={},
            order_outputs: bool = True,
            return_exceptions: bool = False,
        ) -> typing.AsyncIterable[typing.Any]: ...

    starmap: __starmap_spec

    class __for_each_spec(typing_extensions.Protocol):
        def __call__(self, *input_iterators, kwargs={}, ignore_exceptions: bool = False): ...
        async def aio(self, *input_iterators, kwargs={}, ignore_exceptions: bool = False): ...

    for_each: __for_each_spec

class _FunctionCall(typing.Generic[ReturnType], modal.object._Object):
    _is_generator: bool

    def _invocation(self): ...
    async def get(self, timeout: typing.Optional[float] = None) -> ReturnType: ...
    def get_gen(self) -> typing.AsyncGenerator[typing.Any, None]: ...
    async def get_call_graph(self) -> typing.List[modal.call_graph.InputInfo]: ...
    async def cancel(self, terminate_containers: bool = False): ...
    @staticmethod
    async def from_id(
        function_call_id: str, client: typing.Optional[modal.client._Client] = None, is_generator: bool = False
    ) -> _FunctionCall: ...

class FunctionCall(typing.Generic[ReturnType], modal.object.Object):
    _is_generator: bool

    def __init__(self, *args, **kwargs): ...
    def _invocation(self): ...

    class __get_spec(typing_extensions.Protocol[ReturnType_INNER]):
        def __call__(self, timeout: typing.Optional[float] = None) -> ReturnType_INNER: ...
        async def aio(self, timeout: typing.Optional[float] = None) -> ReturnType_INNER: ...

    get: __get_spec[ReturnType]

    class __get_gen_spec(typing_extensions.Protocol):
        def __call__(self) -> typing.Generator[typing.Any, None, None]: ...
        def aio(self) -> typing.AsyncGenerator[typing.Any, None]: ...

    get_gen: __get_gen_spec

    class __get_call_graph_spec(typing_extensions.Protocol):
        def __call__(self) -> typing.List[modal.call_graph.InputInfo]: ...
        async def aio(self) -> typing.List[modal.call_graph.InputInfo]: ...

    get_call_graph: __get_call_graph_spec

    class __cancel_spec(typing_extensions.Protocol):
        def __call__(self, terminate_containers: bool = False): ...
        async def aio(self, terminate_containers: bool = False): ...

    cancel: __cancel_spec

    class __from_id_spec(typing_extensions.Protocol):
        def __call__(
            self, function_call_id: str, client: typing.Optional[modal.client.Client] = None, is_generator: bool = False
        ) -> FunctionCall: ...
        async def aio(
            self, function_call_id: str, client: typing.Optional[modal.client.Client] = None, is_generator: bool = False
        ) -> FunctionCall: ...

    from_id: __from_id_spec

async def _gather(*function_calls: _FunctionCall[ReturnType]) -> typing.Sequence[ReturnType]: ...

class __gather_spec(typing_extensions.Protocol):
    def __call__(self, *function_calls: FunctionCall[ReturnType]) -> typing.Sequence[ReturnType]: ...
    async def aio(self, *function_calls: FunctionCall[ReturnType]) -> typing.Sequence[ReturnType]: ...

gather: __gather_spec
