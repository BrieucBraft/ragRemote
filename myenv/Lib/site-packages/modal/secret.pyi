import modal.client
import modal.object
import typing
import typing_extensions

class _Secret(modal.object._Object):
    @staticmethod
    def from_dict(env_dict: typing.Dict[str, typing.Optional[str]] = {}): ...
    @staticmethod
    def from_local_environ(env_keys: typing.List[str]): ...
    @staticmethod
    def from_dotenv(path=None, *, filename=".env"): ...
    @staticmethod
    def from_name(
        label: str, namespace=1, environment_name: typing.Optional[str] = None, required_keys: typing.List[str] = []
    ) -> _Secret: ...
    @staticmethod
    async def lookup(
        label: str,
        namespace=1,
        client: typing.Optional[modal.client._Client] = None,
        environment_name: typing.Optional[str] = None,
        required_keys: typing.List[str] = [],
    ) -> _Secret: ...
    @staticmethod
    async def create_deployed(
        deployment_name: str,
        env_dict: typing.Dict[str, str],
        namespace=1,
        client: typing.Optional[modal.client._Client] = None,
        environment_name: typing.Optional[str] = None,
        overwrite: bool = False,
    ) -> str: ...

class Secret(modal.object.Object):
    def __init__(self, *args, **kwargs): ...
    @staticmethod
    def from_dict(env_dict: typing.Dict[str, typing.Optional[str]] = {}): ...
    @staticmethod
    def from_local_environ(env_keys: typing.List[str]): ...
    @staticmethod
    def from_dotenv(path=None, *, filename=".env"): ...
    @staticmethod
    def from_name(
        label: str, namespace=1, environment_name: typing.Optional[str] = None, required_keys: typing.List[str] = []
    ) -> Secret: ...

    class __lookup_spec(typing_extensions.Protocol):
        def __call__(
            self,
            label: str,
            namespace=1,
            client: typing.Optional[modal.client.Client] = None,
            environment_name: typing.Optional[str] = None,
            required_keys: typing.List[str] = [],
        ) -> Secret: ...
        async def aio(
            self,
            label: str,
            namespace=1,
            client: typing.Optional[modal.client.Client] = None,
            environment_name: typing.Optional[str] = None,
            required_keys: typing.List[str] = [],
        ) -> Secret: ...

    lookup: __lookup_spec

    class __create_deployed_spec(typing_extensions.Protocol):
        def __call__(
            self,
            deployment_name: str,
            env_dict: typing.Dict[str, str],
            namespace=1,
            client: typing.Optional[modal.client.Client] = None,
            environment_name: typing.Optional[str] = None,
            overwrite: bool = False,
        ) -> str: ...
        async def aio(
            self,
            deployment_name: str,
            env_dict: typing.Dict[str, str],
            namespace=1,
            client: typing.Optional[modal.client.Client] = None,
            environment_name: typing.Optional[str] = None,
            overwrite: bool = False,
        ) -> str: ...

    create_deployed: __create_deployed_spec
