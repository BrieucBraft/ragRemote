import google.protobuf.message
import modal.cloud_bucket_mount
import modal.functions
import modal.gpu
import modal.mount
import modal.network_file_system
import modal.object
import modal.secret
import modal.volume
import modal_proto.api_pb2
import pathlib
import typing
import typing_extensions

ImageBuilderVersion = typing.Literal["2023.12", "2024.04", "2024.10"]

def _validate_python_version(
    python_version: typing.Optional[str],
    builder_version: typing.Literal["2023.12", "2024.04", "2024.10"],
    allow_micro_granularity: bool = True,
) -> str: ...
def _dockerhub_python_version(
    builder_version: typing.Literal["2023.12", "2024.04", "2024.10"], python_version: typing.Optional[str] = None
) -> str: ...
def _base_image_config(group: str, builder_version: typing.Literal["2023.12", "2024.04", "2024.10"]) -> typing.Any: ...
def _get_modal_requirements_path(
    builder_version: typing.Literal["2023.12", "2024.04", "2024.10"], python_version: typing.Optional[str] = None
) -> str: ...
def _get_modal_requirements_command(version: typing.Literal["2023.12", "2024.04", "2024.10"]) -> str: ...
def _flatten_str_args(
    function_name: str, arg_name: str, args: typing.Tuple[typing.Union[str, typing.List[str]], ...]
) -> typing.List[str]: ...
def _validate_packages(packages: typing.List[str]) -> bool: ...
def _warn_invalid_packages(old_command: str) -> None: ...
def _make_pip_install_args(
    find_links: typing.Optional[str] = None,
    index_url: typing.Optional[str] = None,
    extra_index_url: typing.Optional[str] = None,
    pre: bool = False,
    extra_options: str = "",
) -> str: ...
def _get_image_builder_version(
    server_version: typing.Literal["2023.12", "2024.04", "2024.10"],
) -> typing.Literal["2023.12", "2024.04", "2024.10"]: ...

class _ImageRegistryConfig:
    def __init__(self, registry_auth_type: int = 0, secret: typing.Optional[modal.secret._Secret] = None): ...
    def get_proto(self) -> modal_proto.api_pb2.ImageRegistryConfig: ...

class DockerfileSpec:
    commands: typing.List[str]
    context_files: typing.Dict[str, str]

    def __init__(self, commands: typing.List[str], context_files: typing.Dict[str, str]) -> None: ...
    def __repr__(self): ...
    def __eq__(self, other): ...

class _Image(modal.object._Object):
    force_build: bool
    inside_exceptions: typing.List[Exception]
    _serve_mounts: typing.FrozenSet[modal.mount._Mount]
    _deferred_mounts: typing.Sequence[modal.mount._Mount]
    _metadata: typing.Optional[modal_proto.api_pb2.ImageMetadata]

    def _initialize_from_empty(self): ...
    def _initialize_from_other(self, other: _Image): ...
    def _hydrate_metadata(self, message: typing.Optional[google.protobuf.message.Message]): ...
    def _add_mount_layer_or_copy(self, mount: modal.mount._Mount, copy: bool = False): ...
    @property
    def _mount_layers(self) -> typing.Tuple[modal.mount._Mount]: ...
    def _assert_no_mount_layers(self): ...
    @staticmethod
    def _from_args(
        *,
        base_images: typing.Optional[typing.Dict[str, _Image]] = None,
        dockerfile_function: typing.Optional[
            typing.Callable[[typing.Literal["2023.12", "2024.04", "2024.10"]], DockerfileSpec]
        ] = None,
        secrets: typing.Optional[typing.Sequence[modal.secret._Secret]] = None,
        gpu_config: typing.Optional[modal_proto.api_pb2.GPUConfig] = None,
        build_function: typing.Optional[modal.functions._Function] = None,
        build_function_input: typing.Optional[modal_proto.api_pb2.FunctionInput] = None,
        image_registry_config: typing.Optional[_ImageRegistryConfig] = None,
        context_mount: typing.Optional[modal.mount._Mount] = None,
        force_build: bool = False,
        _namespace: int = 1,
        _do_assert_no_mount_layers: bool = True,
    ): ...
    def extend(
        self,
        *,
        secrets: typing.Optional[typing.Sequence[modal.secret._Secret]] = None,
        gpu_config: typing.Optional[modal_proto.api_pb2.GPUConfig] = None,
        build_function: typing.Optional[modal.functions._Function] = None,
        build_function_input: typing.Optional[modal_proto.api_pb2.FunctionInput] = None,
        image_registry_config: typing.Optional[_ImageRegistryConfig] = None,
        context_mount: typing.Optional[modal.mount._Mount] = None,
        force_build: bool = False,
        _namespace: int = 1,
        _do_assert_no_mount_layers: bool = True,
    ) -> _Image: ...
    def copy_mount(self, mount: modal.mount._Mount, remote_path: typing.Union[str, pathlib.Path] = ".") -> _Image: ...
    def add_local_file(
        self, local_path: typing.Union[str, pathlib.Path], remote_path: str, *, copy: bool = False
    ) -> _Image: ...
    def add_local_dir(
        self, local_path: typing.Union[str, pathlib.Path], remote_path: str, *, copy: bool = False
    ) -> _Image: ...
    def copy_local_file(
        self, local_path: typing.Union[str, pathlib.Path], remote_path: typing.Union[str, pathlib.Path] = "./"
    ) -> _Image: ...
    def _add_local_python_packages(self, *module_names, copy: bool = False) -> _Image: ...
    def copy_local_dir(
        self, local_path: typing.Union[str, pathlib.Path], remote_path: typing.Union[str, pathlib.Path] = "."
    ) -> _Image: ...
    def pip_install(
        self,
        *packages: typing.Union[str, typing.List[str]],
        find_links: typing.Optional[str] = None,
        index_url: typing.Optional[str] = None,
        extra_index_url: typing.Optional[str] = None,
        pre: bool = False,
        extra_options: str = "",
        force_build: bool = False,
        secrets: typing.Sequence[modal.secret._Secret] = [],
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
    ) -> _Image: ...
    def pip_install_private_repos(
        self,
        *repositories: str,
        git_user: str,
        find_links: typing.Optional[str] = None,
        index_url: typing.Optional[str] = None,
        extra_index_url: typing.Optional[str] = None,
        pre: bool = False,
        extra_options: str = "",
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
        secrets: typing.Sequence[modal.secret._Secret] = [],
        force_build: bool = False,
    ) -> _Image: ...
    def pip_install_from_requirements(
        self,
        requirements_txt: str,
        find_links: typing.Optional[str] = None,
        *,
        index_url: typing.Optional[str] = None,
        extra_index_url: typing.Optional[str] = None,
        pre: bool = False,
        extra_options: str = "",
        force_build: bool = False,
        secrets: typing.Sequence[modal.secret._Secret] = [],
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
    ) -> _Image: ...
    def pip_install_from_pyproject(
        self,
        pyproject_toml: str,
        optional_dependencies: typing.List[str] = [],
        *,
        find_links: typing.Optional[str] = None,
        index_url: typing.Optional[str] = None,
        extra_index_url: typing.Optional[str] = None,
        pre: bool = False,
        extra_options: str = "",
        force_build: bool = False,
        secrets: typing.Sequence[modal.secret._Secret] = [],
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
    ) -> _Image: ...
    def poetry_install_from_file(
        self,
        poetry_pyproject_toml: str,
        poetry_lockfile: typing.Optional[str] = None,
        ignore_lockfile: bool = False,
        old_installer: bool = False,
        force_build: bool = False,
        with_: typing.List[str] = [],
        without: typing.List[str] = [],
        only: typing.List[str] = [],
        *,
        secrets: typing.Sequence[modal.secret._Secret] = [],
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
    ) -> _Image: ...
    def dockerfile_commands(
        self,
        *dockerfile_commands: typing.Union[str, typing.List[str]],
        context_files: typing.Dict[str, str] = {},
        secrets: typing.Sequence[modal.secret._Secret] = [],
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
        context_mount: typing.Optional[modal.mount._Mount] = None,
        force_build: bool = False,
    ) -> _Image: ...
    def entrypoint(self, entrypoint_commands: typing.List[str]) -> _Image: ...
    def shell(self, shell_commands: typing.List[str]) -> _Image: ...
    def run_commands(
        self,
        *commands: typing.Union[str, typing.List[str]],
        secrets: typing.Sequence[modal.secret._Secret] = [],
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
        force_build: bool = False,
    ) -> _Image: ...
    @staticmethod
    def conda(python_version: typing.Optional[str] = None, force_build: bool = False): ...
    def conda_install(
        self,
        *packages: typing.Union[str, typing.List[str]],
        channels: typing.List[str] = [],
        force_build: bool = False,
        secrets: typing.Sequence[modal.secret._Secret] = [],
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
    ): ...
    def conda_update_from_environment(
        self,
        environment_yml: str,
        force_build: bool = False,
        *,
        secrets: typing.Sequence[modal.secret._Secret] = [],
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
    ): ...
    @staticmethod
    def micromamba(python_version: typing.Optional[str] = None, force_build: bool = False) -> _Image: ...
    def micromamba_install(
        self,
        *packages: typing.Union[str, typing.List[str]],
        spec_file: typing.Optional[str] = None,
        channels: typing.List[str] = [],
        force_build: bool = False,
        secrets: typing.Sequence[modal.secret._Secret] = [],
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
    ) -> _Image: ...
    @staticmethod
    def _registry_setup_commands(
        tag: str,
        builder_version: typing.Literal["2023.12", "2024.04", "2024.10"],
        setup_commands: typing.List[str],
        add_python: typing.Optional[str] = None,
    ) -> typing.List[str]: ...
    @staticmethod
    def from_registry(
        tag: str,
        *,
        secret: typing.Optional[modal.secret._Secret] = None,
        setup_dockerfile_commands: typing.List[str] = [],
        force_build: bool = False,
        add_python: typing.Optional[str] = None,
        **kwargs,
    ) -> _Image: ...
    @staticmethod
    def from_gcp_artifact_registry(
        tag: str,
        secret: typing.Optional[modal.secret._Secret] = None,
        *,
        setup_dockerfile_commands: typing.List[str] = [],
        force_build: bool = False,
        add_python: typing.Optional[str] = None,
        **kwargs,
    ) -> _Image: ...
    @staticmethod
    def from_aws_ecr(
        tag: str,
        secret: typing.Optional[modal.secret._Secret] = None,
        *,
        setup_dockerfile_commands: typing.List[str] = [],
        force_build: bool = False,
        add_python: typing.Optional[str] = None,
        **kwargs,
    ) -> _Image: ...
    @staticmethod
    def from_dockerfile(
        path: typing.Union[str, pathlib.Path],
        context_mount: typing.Optional[modal.mount._Mount] = None,
        force_build: bool = False,
        *,
        secrets: typing.Sequence[modal.secret._Secret] = [],
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
        add_python: typing.Optional[str] = None,
    ) -> _Image: ...
    @staticmethod
    def debian_slim(python_version: typing.Optional[str] = None, force_build: bool = False) -> _Image: ...
    def apt_install(
        self,
        *packages: typing.Union[str, typing.List[str]],
        force_build: bool = False,
        secrets: typing.Sequence[modal.secret._Secret] = [],
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
    ) -> _Image: ...
    def run_function(
        self,
        raw_f: typing.Callable[..., typing.Any],
        secrets: typing.Sequence[modal.secret._Secret] = (),
        gpu: typing.Union[
            None, bool, str, modal.gpu._GPUConfig, typing.List[typing.Union[None, bool, str, modal.gpu._GPUConfig]]
        ] = None,
        mounts: typing.Sequence[modal.mount._Mount] = (),
        volumes: typing.Dict[
            typing.Union[str, pathlib.PurePosixPath],
            typing.Union[modal.volume._Volume, modal.cloud_bucket_mount._CloudBucketMount],
        ] = {},
        network_file_systems: typing.Dict[
            typing.Union[str, pathlib.PurePosixPath], modal.network_file_system._NetworkFileSystem
        ] = {},
        cpu: typing.Optional[float] = None,
        memory: typing.Optional[int] = None,
        timeout: typing.Optional[int] = 3600,
        force_build: bool = False,
        cloud: typing.Optional[str] = None,
        region: typing.Union[str, typing.Sequence[str], None] = None,
        args: typing.Sequence[typing.Any] = (),
        kwargs: typing.Dict[str, typing.Any] = {},
    ) -> _Image: ...
    def env(self, vars: typing.Dict[str, str]) -> _Image: ...
    def workdir(self, path: typing.Union[str, pathlib.PurePosixPath]) -> _Image: ...
    def imports(self): ...
    def _logs(self) -> typing.AsyncGenerator[str, None]: ...

class Image(modal.object.Object):
    force_build: bool
    inside_exceptions: typing.List[Exception]
    _serve_mounts: typing.FrozenSet[modal.mount.Mount]
    _deferred_mounts: typing.Sequence[modal.mount.Mount]
    _metadata: typing.Optional[modal_proto.api_pb2.ImageMetadata]

    def __init__(self, *args, **kwargs): ...
    def _initialize_from_empty(self): ...
    def _initialize_from_other(self, other: Image): ...
    def _hydrate_metadata(self, message: typing.Optional[google.protobuf.message.Message]): ...
    def _add_mount_layer_or_copy(self, mount: modal.mount.Mount, copy: bool = False): ...
    @property
    def _mount_layers(self) -> typing.Tuple[modal.mount.Mount]: ...
    def _assert_no_mount_layers(self): ...
    @staticmethod
    def _from_args(
        *,
        base_images: typing.Optional[typing.Dict[str, Image]] = None,
        dockerfile_function: typing.Optional[
            typing.Callable[[typing.Literal["2023.12", "2024.04", "2024.10"]], DockerfileSpec]
        ] = None,
        secrets: typing.Optional[typing.Sequence[modal.secret.Secret]] = None,
        gpu_config: typing.Optional[modal_proto.api_pb2.GPUConfig] = None,
        build_function: typing.Optional[modal.functions.Function] = None,
        build_function_input: typing.Optional[modal_proto.api_pb2.FunctionInput] = None,
        image_registry_config: typing.Optional[_ImageRegistryConfig] = None,
        context_mount: typing.Optional[modal.mount.Mount] = None,
        force_build: bool = False,
        _namespace: int = 1,
        _do_assert_no_mount_layers: bool = True,
    ): ...
    def extend(
        self,
        *,
        secrets: typing.Optional[typing.Sequence[modal.secret.Secret]] = None,
        gpu_config: typing.Optional[modal_proto.api_pb2.GPUConfig] = None,
        build_function: typing.Optional[modal.functions.Function] = None,
        build_function_input: typing.Optional[modal_proto.api_pb2.FunctionInput] = None,
        image_registry_config: typing.Optional[_ImageRegistryConfig] = None,
        context_mount: typing.Optional[modal.mount.Mount] = None,
        force_build: bool = False,
        _namespace: int = 1,
        _do_assert_no_mount_layers: bool = True,
    ) -> Image: ...
    def copy_mount(self, mount: modal.mount.Mount, remote_path: typing.Union[str, pathlib.Path] = ".") -> Image: ...
    def add_local_file(
        self, local_path: typing.Union[str, pathlib.Path], remote_path: str, *, copy: bool = False
    ) -> Image: ...
    def add_local_dir(
        self, local_path: typing.Union[str, pathlib.Path], remote_path: str, *, copy: bool = False
    ) -> Image: ...
    def copy_local_file(
        self, local_path: typing.Union[str, pathlib.Path], remote_path: typing.Union[str, pathlib.Path] = "./"
    ) -> Image: ...
    def _add_local_python_packages(self, *module_names, copy: bool = False) -> Image: ...
    def copy_local_dir(
        self, local_path: typing.Union[str, pathlib.Path], remote_path: typing.Union[str, pathlib.Path] = "."
    ) -> Image: ...
    def pip_install(
        self,
        *packages: typing.Union[str, typing.List[str]],
        find_links: typing.Optional[str] = None,
        index_url: typing.Optional[str] = None,
        extra_index_url: typing.Optional[str] = None,
        pre: bool = False,
        extra_options: str = "",
        force_build: bool = False,
        secrets: typing.Sequence[modal.secret.Secret] = [],
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
    ) -> Image: ...
    def pip_install_private_repos(
        self,
        *repositories: str,
        git_user: str,
        find_links: typing.Optional[str] = None,
        index_url: typing.Optional[str] = None,
        extra_index_url: typing.Optional[str] = None,
        pre: bool = False,
        extra_options: str = "",
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
        secrets: typing.Sequence[modal.secret.Secret] = [],
        force_build: bool = False,
    ) -> Image: ...
    def pip_install_from_requirements(
        self,
        requirements_txt: str,
        find_links: typing.Optional[str] = None,
        *,
        index_url: typing.Optional[str] = None,
        extra_index_url: typing.Optional[str] = None,
        pre: bool = False,
        extra_options: str = "",
        force_build: bool = False,
        secrets: typing.Sequence[modal.secret.Secret] = [],
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
    ) -> Image: ...
    def pip_install_from_pyproject(
        self,
        pyproject_toml: str,
        optional_dependencies: typing.List[str] = [],
        *,
        find_links: typing.Optional[str] = None,
        index_url: typing.Optional[str] = None,
        extra_index_url: typing.Optional[str] = None,
        pre: bool = False,
        extra_options: str = "",
        force_build: bool = False,
        secrets: typing.Sequence[modal.secret.Secret] = [],
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
    ) -> Image: ...
    def poetry_install_from_file(
        self,
        poetry_pyproject_toml: str,
        poetry_lockfile: typing.Optional[str] = None,
        ignore_lockfile: bool = False,
        old_installer: bool = False,
        force_build: bool = False,
        with_: typing.List[str] = [],
        without: typing.List[str] = [],
        only: typing.List[str] = [],
        *,
        secrets: typing.Sequence[modal.secret.Secret] = [],
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
    ) -> Image: ...
    def dockerfile_commands(
        self,
        *dockerfile_commands: typing.Union[str, typing.List[str]],
        context_files: typing.Dict[str, str] = {},
        secrets: typing.Sequence[modal.secret.Secret] = [],
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
        context_mount: typing.Optional[modal.mount.Mount] = None,
        force_build: bool = False,
    ) -> Image: ...
    def entrypoint(self, entrypoint_commands: typing.List[str]) -> Image: ...
    def shell(self, shell_commands: typing.List[str]) -> Image: ...
    def run_commands(
        self,
        *commands: typing.Union[str, typing.List[str]],
        secrets: typing.Sequence[modal.secret.Secret] = [],
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
        force_build: bool = False,
    ) -> Image: ...
    @staticmethod
    def conda(python_version: typing.Optional[str] = None, force_build: bool = False): ...
    def conda_install(
        self,
        *packages: typing.Union[str, typing.List[str]],
        channels: typing.List[str] = [],
        force_build: bool = False,
        secrets: typing.Sequence[modal.secret.Secret] = [],
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
    ): ...
    def conda_update_from_environment(
        self,
        environment_yml: str,
        force_build: bool = False,
        *,
        secrets: typing.Sequence[modal.secret.Secret] = [],
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
    ): ...
    @staticmethod
    def micromamba(python_version: typing.Optional[str] = None, force_build: bool = False) -> Image: ...
    def micromamba_install(
        self,
        *packages: typing.Union[str, typing.List[str]],
        spec_file: typing.Optional[str] = None,
        channels: typing.List[str] = [],
        force_build: bool = False,
        secrets: typing.Sequence[modal.secret.Secret] = [],
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
    ) -> Image: ...
    @staticmethod
    def _registry_setup_commands(
        tag: str,
        builder_version: typing.Literal["2023.12", "2024.04", "2024.10"],
        setup_commands: typing.List[str],
        add_python: typing.Optional[str] = None,
    ) -> typing.List[str]: ...
    @staticmethod
    def from_registry(
        tag: str,
        *,
        secret: typing.Optional[modal.secret.Secret] = None,
        setup_dockerfile_commands: typing.List[str] = [],
        force_build: bool = False,
        add_python: typing.Optional[str] = None,
        **kwargs,
    ) -> Image: ...
    @staticmethod
    def from_gcp_artifact_registry(
        tag: str,
        secret: typing.Optional[modal.secret.Secret] = None,
        *,
        setup_dockerfile_commands: typing.List[str] = [],
        force_build: bool = False,
        add_python: typing.Optional[str] = None,
        **kwargs,
    ) -> Image: ...
    @staticmethod
    def from_aws_ecr(
        tag: str,
        secret: typing.Optional[modal.secret.Secret] = None,
        *,
        setup_dockerfile_commands: typing.List[str] = [],
        force_build: bool = False,
        add_python: typing.Optional[str] = None,
        **kwargs,
    ) -> Image: ...
    @staticmethod
    def from_dockerfile(
        path: typing.Union[str, pathlib.Path],
        context_mount: typing.Optional[modal.mount.Mount] = None,
        force_build: bool = False,
        *,
        secrets: typing.Sequence[modal.secret.Secret] = [],
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
        add_python: typing.Optional[str] = None,
    ) -> Image: ...
    @staticmethod
    def debian_slim(python_version: typing.Optional[str] = None, force_build: bool = False) -> Image: ...
    def apt_install(
        self,
        *packages: typing.Union[str, typing.List[str]],
        force_build: bool = False,
        secrets: typing.Sequence[modal.secret.Secret] = [],
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
    ) -> Image: ...
    def run_function(
        self,
        raw_f: typing.Callable[..., typing.Any],
        secrets: typing.Sequence[modal.secret.Secret] = (),
        gpu: typing.Union[
            None, bool, str, modal.gpu._GPUConfig, typing.List[typing.Union[None, bool, str, modal.gpu._GPUConfig]]
        ] = None,
        mounts: typing.Sequence[modal.mount.Mount] = (),
        volumes: typing.Dict[
            typing.Union[str, pathlib.PurePosixPath],
            typing.Union[modal.volume.Volume, modal.cloud_bucket_mount.CloudBucketMount],
        ] = {},
        network_file_systems: typing.Dict[
            typing.Union[str, pathlib.PurePosixPath], modal.network_file_system.NetworkFileSystem
        ] = {},
        cpu: typing.Optional[float] = None,
        memory: typing.Optional[int] = None,
        timeout: typing.Optional[int] = 3600,
        force_build: bool = False,
        cloud: typing.Optional[str] = None,
        region: typing.Union[str, typing.Sequence[str], None] = None,
        args: typing.Sequence[typing.Any] = (),
        kwargs: typing.Dict[str, typing.Any] = {},
    ) -> Image: ...
    def env(self, vars: typing.Dict[str, str]) -> Image: ...
    def workdir(self, path: typing.Union[str, pathlib.PurePosixPath]) -> Image: ...
    def imports(self): ...

    class ___logs_spec(typing_extensions.Protocol):
        def __call__(self) -> typing.Generator[str, None, None]: ...
        def aio(self) -> typing.AsyncGenerator[str, None]: ...

    _logs: ___logs_spec

SUPPORTED_PYTHON_SERIES: typing.Dict[typing.Literal["2023.12", "2024.04", "2024.10"], typing.List[str]]
