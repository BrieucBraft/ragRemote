import modal.client
import modal.object
import synchronicity.combined_types
import typing
import typing_extensions

class _Queue(modal.object._Object):
    @staticmethod
    def new(): ...
    def __init__(self): ...
    @staticmethod
    def validate_partition_key(partition: typing.Optional[str]) -> bytes: ...
    @classmethod
    def ephemeral(
        cls: typing.Type[_Queue],
        client: typing.Optional[modal.client._Client] = None,
        environment_name: typing.Optional[str] = None,
        _heartbeat_sleep: float = 300,
    ) -> typing.AsyncContextManager[_Queue]: ...
    @staticmethod
    def from_name(
        label: str, namespace=1, environment_name: typing.Optional[str] = None, create_if_missing: bool = False
    ) -> _Queue: ...
    @staticmethod
    async def lookup(
        label: str,
        namespace=1,
        client: typing.Optional[modal.client._Client] = None,
        environment_name: typing.Optional[str] = None,
        create_if_missing: bool = False,
    ) -> _Queue: ...
    @staticmethod
    async def delete(
        label: str,
        *,
        client: typing.Optional[modal.client._Client] = None,
        environment_name: typing.Optional[str] = None,
    ): ...
    async def _get_nonblocking(self, partition: typing.Optional[str], n_values: int) -> typing.List[typing.Any]: ...
    async def _get_blocking(
        self, partition: typing.Optional[str], timeout: typing.Optional[float], n_values: int
    ) -> typing.List[typing.Any]: ...
    async def clear(self, *, partition: typing.Optional[str] = None, all: bool = False) -> None: ...
    async def get(
        self, block: bool = True, timeout: typing.Optional[float] = None, *, partition: typing.Optional[str] = None
    ) -> typing.Optional[typing.Any]: ...
    async def get_many(
        self,
        n_values: int,
        block: bool = True,
        timeout: typing.Optional[float] = None,
        *,
        partition: typing.Optional[str] = None,
    ) -> typing.List[typing.Any]: ...
    async def put(
        self,
        v: typing.Any,
        block: bool = True,
        timeout: typing.Optional[float] = None,
        *,
        partition: typing.Optional[str] = None,
        partition_ttl: int = 86400,
    ) -> None: ...
    async def put_many(
        self,
        vs: typing.List[typing.Any],
        block: bool = True,
        timeout: typing.Optional[float] = None,
        *,
        partition: typing.Optional[str] = None,
        partition_ttl: int = 86400,
    ) -> None: ...
    async def _put_many_blocking(
        self,
        partition: typing.Optional[str],
        partition_ttl: int,
        vs: typing.List[typing.Any],
        timeout: typing.Optional[float] = None,
    ): ...
    async def _put_many_nonblocking(
        self, partition: typing.Optional[str], partition_ttl: int, vs: typing.List[typing.Any]
    ): ...
    async def len(self, *, partition: typing.Optional[str] = None, total: bool = False) -> int: ...
    def iterate(
        self, *, partition: typing.Optional[str] = None, item_poll_timeout: float = 0.0
    ) -> typing.AsyncGenerator[typing.Any, None]: ...

class Queue(modal.object.Object):
    def __init__(self): ...
    @staticmethod
    def new(): ...
    @staticmethod
    def validate_partition_key(partition: typing.Optional[str]) -> bytes: ...
    @classmethod
    def ephemeral(
        cls: typing.Type[Queue],
        client: typing.Optional[modal.client.Client] = None,
        environment_name: typing.Optional[str] = None,
        _heartbeat_sleep: float = 300,
    ) -> synchronicity.combined_types.AsyncAndBlockingContextManager[Queue]: ...
    @staticmethod
    def from_name(
        label: str, namespace=1, environment_name: typing.Optional[str] = None, create_if_missing: bool = False
    ) -> Queue: ...

    class __lookup_spec(typing_extensions.Protocol):
        def __call__(
            self,
            label: str,
            namespace=1,
            client: typing.Optional[modal.client.Client] = None,
            environment_name: typing.Optional[str] = None,
            create_if_missing: bool = False,
        ) -> Queue: ...
        async def aio(
            self,
            label: str,
            namespace=1,
            client: typing.Optional[modal.client.Client] = None,
            environment_name: typing.Optional[str] = None,
            create_if_missing: bool = False,
        ) -> Queue: ...

    lookup: __lookup_spec

    class __delete_spec(typing_extensions.Protocol):
        def __call__(
            self,
            label: str,
            *,
            client: typing.Optional[modal.client.Client] = None,
            environment_name: typing.Optional[str] = None,
        ): ...
        async def aio(
            self,
            label: str,
            *,
            client: typing.Optional[modal.client.Client] = None,
            environment_name: typing.Optional[str] = None,
        ): ...

    delete: __delete_spec

    class ___get_nonblocking_spec(typing_extensions.Protocol):
        def __call__(self, partition: typing.Optional[str], n_values: int) -> typing.List[typing.Any]: ...
        async def aio(self, partition: typing.Optional[str], n_values: int) -> typing.List[typing.Any]: ...

    _get_nonblocking: ___get_nonblocking_spec

    class ___get_blocking_spec(typing_extensions.Protocol):
        def __call__(
            self, partition: typing.Optional[str], timeout: typing.Optional[float], n_values: int
        ) -> typing.List[typing.Any]: ...
        async def aio(
            self, partition: typing.Optional[str], timeout: typing.Optional[float], n_values: int
        ) -> typing.List[typing.Any]: ...

    _get_blocking: ___get_blocking_spec

    class __clear_spec(typing_extensions.Protocol):
        def __call__(self, *, partition: typing.Optional[str] = None, all: bool = False) -> None: ...
        async def aio(self, *, partition: typing.Optional[str] = None, all: bool = False) -> None: ...

    clear: __clear_spec

    class __get_spec(typing_extensions.Protocol):
        def __call__(
            self, block: bool = True, timeout: typing.Optional[float] = None, *, partition: typing.Optional[str] = None
        ) -> typing.Optional[typing.Any]: ...
        async def aio(
            self, block: bool = True, timeout: typing.Optional[float] = None, *, partition: typing.Optional[str] = None
        ) -> typing.Optional[typing.Any]: ...

    get: __get_spec

    class __get_many_spec(typing_extensions.Protocol):
        def __call__(
            self,
            n_values: int,
            block: bool = True,
            timeout: typing.Optional[float] = None,
            *,
            partition: typing.Optional[str] = None,
        ) -> typing.List[typing.Any]: ...
        async def aio(
            self,
            n_values: int,
            block: bool = True,
            timeout: typing.Optional[float] = None,
            *,
            partition: typing.Optional[str] = None,
        ) -> typing.List[typing.Any]: ...

    get_many: __get_many_spec

    class __put_spec(typing_extensions.Protocol):
        def __call__(
            self,
            v: typing.Any,
            block: bool = True,
            timeout: typing.Optional[float] = None,
            *,
            partition: typing.Optional[str] = None,
            partition_ttl: int = 86400,
        ) -> None: ...
        async def aio(
            self,
            v: typing.Any,
            block: bool = True,
            timeout: typing.Optional[float] = None,
            *,
            partition: typing.Optional[str] = None,
            partition_ttl: int = 86400,
        ) -> None: ...

    put: __put_spec

    class __put_many_spec(typing_extensions.Protocol):
        def __call__(
            self,
            vs: typing.List[typing.Any],
            block: bool = True,
            timeout: typing.Optional[float] = None,
            *,
            partition: typing.Optional[str] = None,
            partition_ttl: int = 86400,
        ) -> None: ...
        async def aio(
            self,
            vs: typing.List[typing.Any],
            block: bool = True,
            timeout: typing.Optional[float] = None,
            *,
            partition: typing.Optional[str] = None,
            partition_ttl: int = 86400,
        ) -> None: ...

    put_many: __put_many_spec

    class ___put_many_blocking_spec(typing_extensions.Protocol):
        def __call__(
            self,
            partition: typing.Optional[str],
            partition_ttl: int,
            vs: typing.List[typing.Any],
            timeout: typing.Optional[float] = None,
        ): ...
        async def aio(
            self,
            partition: typing.Optional[str],
            partition_ttl: int,
            vs: typing.List[typing.Any],
            timeout: typing.Optional[float] = None,
        ): ...

    _put_many_blocking: ___put_many_blocking_spec

    class ___put_many_nonblocking_spec(typing_extensions.Protocol):
        def __call__(self, partition: typing.Optional[str], partition_ttl: int, vs: typing.List[typing.Any]): ...
        async def aio(self, partition: typing.Optional[str], partition_ttl: int, vs: typing.List[typing.Any]): ...

    _put_many_nonblocking: ___put_many_nonblocking_spec

    class __len_spec(typing_extensions.Protocol):
        def __call__(self, *, partition: typing.Optional[str] = None, total: bool = False) -> int: ...
        async def aio(self, *, partition: typing.Optional[str] = None, total: bool = False) -> int: ...

    len: __len_spec

    class __iterate_spec(typing_extensions.Protocol):
        def __call__(
            self, *, partition: typing.Optional[str] = None, item_poll_timeout: float = 0.0
        ) -> typing.Generator[typing.Any, None, None]: ...
        def aio(
            self, *, partition: typing.Optional[str] = None, item_poll_timeout: float = 0.0
        ) -> typing.AsyncGenerator[typing.Any, None]: ...

    iterate: __iterate_spec
