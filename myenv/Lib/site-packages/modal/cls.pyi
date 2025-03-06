import google.protobuf.message
import inspect
import modal.app
import modal.client
import modal.functions
import modal.gpu
import modal.object
import modal.partial_function
import modal.retries
import modal.secret
import modal.volume
import modal_proto.api_pb2
import os
import typing
import typing_extensions

T = typing.TypeVar("T")

def _use_annotation_parameters(user_cls) -> bool: ...
def _get_class_constructor_signature(user_cls: type) -> inspect.Signature: ...

class _Obj:
    _functions: typing.Dict[str, modal.functions._Function]
    _entered: bool
    _user_cls_instance: typing.Optional[typing.Any]
    _construction_args: typing.Tuple[tuple, typing.Dict[str, typing.Any]]
    _instance_service_function: typing.Optional[modal.functions._Function]

    def _uses_common_service_function(self): ...
    def __init__(
        self,
        user_cls: type,
        class_service_function: typing.Optional[modal.functions._Function],
        classbound_methods: typing.Dict[str, modal.functions._Function],
        from_other_workspace: bool,
        options: typing.Optional[modal_proto.api_pb2.FunctionOptions],
        args,
        kwargs,
    ): ...
    def _user_cls_instance_constr(self): ...
    async def keep_warm(self, warm_pool_size: int) -> None: ...
    def _get_user_cls_instance(self): ...
    def enter(self): ...
    @property
    def entered(self): ...
    @entered.setter
    def entered(self, val): ...
    async def aenter(self): ...
    def __getattr__(self, k): ...

class Obj:
    _functions: typing.Dict[str, modal.functions.Function]
    _entered: bool
    _user_cls_instance: typing.Optional[typing.Any]
    _construction_args: typing.Tuple[tuple, typing.Dict[str, typing.Any]]
    _instance_service_function: typing.Optional[modal.functions.Function]

    def __init__(
        self,
        user_cls: type,
        class_service_function: typing.Optional[modal.functions.Function],
        classbound_methods: typing.Dict[str, modal.functions.Function],
        from_other_workspace: bool,
        options: typing.Optional[modal_proto.api_pb2.FunctionOptions],
        args,
        kwargs,
    ): ...
    def _uses_common_service_function(self): ...
    def _user_cls_instance_constr(self): ...

    class __keep_warm_spec(typing_extensions.Protocol):
        def __call__(self, warm_pool_size: int) -> None: ...
        async def aio(self, warm_pool_size: int) -> None: ...

    keep_warm: __keep_warm_spec

    def _get_user_cls_instance(self): ...
    def enter(self): ...
    @property
    def entered(self): ...
    @entered.setter
    def entered(self, val): ...
    async def aenter(self): ...
    def __getattr__(self, k): ...

class _Cls(modal.object._Object):
    _user_cls: typing.Optional[type]
    _class_service_function: typing.Optional[modal.functions._Function]
    _method_functions: typing.Dict[str, modal.functions._Function]
    _options: typing.Optional[modal_proto.api_pb2.FunctionOptions]
    _callables: typing.Dict[str, typing.Callable[..., typing.Any]]
    _from_other_workspace: typing.Optional[bool]
    _app: typing.Optional[modal.app._App]

    def _initialize_from_empty(self): ...
    def _initialize_from_other(self, other: _Cls): ...
    def _get_partial_functions(self) -> typing.Dict[str, modal.partial_function._PartialFunction]: ...
    def _hydrate_metadata(self, metadata: google.protobuf.message.Message): ...
    def _get_metadata(self) -> modal_proto.api_pb2.ClassHandleMetadata: ...
    @staticmethod
    def validate_construction_mechanism(user_cls): ...
    @staticmethod
    def from_local(user_cls, app: modal.app._App, class_service_function: modal.functions._Function) -> _Cls: ...
    def _uses_common_service_function(self): ...
    @classmethod
    def from_name(
        cls: typing.Type[_Cls],
        app_name: str,
        tag: str,
        namespace=1,
        environment_name: typing.Optional[str] = None,
        workspace: typing.Optional[str] = None,
    ) -> _Cls: ...
    def with_options(
        self: _Cls,
        cpu: typing.Union[float, typing.Tuple[float, float], None] = None,
        memory: typing.Union[int, typing.Tuple[int, int], None] = None,
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
        secrets: typing.Collection[modal.secret._Secret] = (),
        volumes: typing.Dict[typing.Union[str, os.PathLike], modal.volume._Volume] = {},
        retries: typing.Union[int, modal.retries.Retries, None] = None,
        timeout: typing.Optional[int] = None,
        concurrency_limit: typing.Optional[int] = None,
        allow_concurrent_inputs: typing.Optional[int] = None,
        container_idle_timeout: typing.Optional[int] = None,
    ) -> _Cls: ...
    @staticmethod
    async def lookup(
        app_name: str,
        tag: str,
        namespace=1,
        client: typing.Optional[modal.client._Client] = None,
        environment_name: typing.Optional[str] = None,
        workspace: typing.Optional[str] = None,
    ) -> _Cls: ...
    def __call__(self, *args, **kwargs) -> _Obj: ...
    def __getattr__(self, k): ...

class Cls(modal.object.Object):
    _user_cls: typing.Optional[type]
    _class_service_function: typing.Optional[modal.functions.Function]
    _method_functions: typing.Dict[str, modal.functions.Function]
    _options: typing.Optional[modal_proto.api_pb2.FunctionOptions]
    _callables: typing.Dict[str, typing.Callable[..., typing.Any]]
    _from_other_workspace: typing.Optional[bool]
    _app: typing.Optional[modal.app.App]

    def __init__(self, *args, **kwargs): ...
    def _initialize_from_empty(self): ...
    def _initialize_from_other(self, other: Cls): ...
    def _get_partial_functions(self) -> typing.Dict[str, modal.partial_function.PartialFunction]: ...
    def _hydrate_metadata(self, metadata: google.protobuf.message.Message): ...
    def _get_metadata(self) -> modal_proto.api_pb2.ClassHandleMetadata: ...
    @staticmethod
    def validate_construction_mechanism(user_cls): ...
    @staticmethod
    def from_local(user_cls, app: modal.app.App, class_service_function: modal.functions.Function) -> Cls: ...
    def _uses_common_service_function(self): ...
    @classmethod
    def from_name(
        cls: typing.Type[Cls],
        app_name: str,
        tag: str,
        namespace=1,
        environment_name: typing.Optional[str] = None,
        workspace: typing.Optional[str] = None,
    ) -> Cls: ...
    def with_options(
        self: Cls,
        cpu: typing.Union[float, typing.Tuple[float, float], None] = None,
        memory: typing.Union[int, typing.Tuple[int, int], None] = None,
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
        secrets: typing.Collection[modal.secret.Secret] = (),
        volumes: typing.Dict[typing.Union[str, os.PathLike], modal.volume.Volume] = {},
        retries: typing.Union[int, modal.retries.Retries, None] = None,
        timeout: typing.Optional[int] = None,
        concurrency_limit: typing.Optional[int] = None,
        allow_concurrent_inputs: typing.Optional[int] = None,
        container_idle_timeout: typing.Optional[int] = None,
    ) -> Cls: ...

    class __lookup_spec(typing_extensions.Protocol):
        def __call__(
            self,
            app_name: str,
            tag: str,
            namespace=1,
            client: typing.Optional[modal.client.Client] = None,
            environment_name: typing.Optional[str] = None,
            workspace: typing.Optional[str] = None,
        ) -> Cls: ...
        async def aio(
            self,
            app_name: str,
            tag: str,
            namespace=1,
            client: typing.Optional[modal.client.Client] = None,
            environment_name: typing.Optional[str] = None,
            workspace: typing.Optional[str] = None,
        ) -> Cls: ...

    lookup: __lookup_spec

    def __call__(self, *args, **kwargs) -> Obj: ...
    def __getattr__(self, k): ...

class _NO_DEFAULT:
    def __repr__(self): ...

_no_default: _NO_DEFAULT

class _Parameter:
    default: typing.Any
    init: bool

    def __init__(self, default: typing.Any, init: bool): ...
    def __get__(self, obj, obj_type=None) -> typing.Any: ...

def is_parameter(p: typing.Any) -> bool: ...
def parameter(*, default: typing.Any = modal.cls._NO_DEFAULT(), init: bool = True) -> typing.Any: ...
