# skbuild-conditional-scripts

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Generic dynamic script metadata provider for scikit-build-core projects.

This micro-package provides a reusable metadata provider that can conditionally
install entry point scripts based on environment variables. Originally developed
for [AFDKO](https://github.com/adobe-type-tools/afdko) to choose between installing
a C++ binary or Python wrapper, it can be used by any scikit-build-core project that
needs conditional entry point generation.

## Features

- **Data-driven**: All script definitions live in `pyproject.toml`, not code
- **Conditional installation**: Install different scripts based on environment variables
- **Generic**: Can be reused by other projects with similar needs
- **Simple**: ~70 lines of code, easy to understand and maintain

## Installation

```bash
pip install skbuild-conditional-scripts
```

Or include in your project locally using `provider-path`.

## Quick Start

Add to your `pyproject.toml`:

```toml
[build-system]
requires = ["scikit-build-core", "skbuild-conditional-scripts"]
build-backend = "scikit_build_core.build"

[tool.scikit-build.metadata.scripts]
provider = "skbuild_conditional_scripts"

# Always installed scripts
scripts = {
    "my-command" = "mypackage:main",
    "my-tool" = "mypackage.tools:cli",
}

# Conditionally installed scripts (only when MY_ENV_VAR=ON)
conditional-scripts = {
    "my-debug-tool" = "mypackage.debug:main",
}

condition-env-var = "MY_ENV_VAR"
condition-env-value = "ON"
```

Then build your project:

```bash
# Normal build - only base scripts installed
pip install .

# With condition - both base and conditional scripts installed
MY_ENV_VAR=ON pip install .
```

## Use Cases

- **Binary vs Python wrapper**: Install C++ binary or Python wrapper based on build configuration
- **Platform-specific commands**: Different entry points for different platforms (via env vars)
- **Debug builds**: Install additional debug tools only when requested
- **Optional features**: Install extra commands when feature flags are enabled

## How It Works

The provider is called during the metadata generation phase (before building). It:

1. Reads configuration from `[tool.scikit-build.metadata.scripts]`
2. Checks the specified environment variable
3. Merges base scripts with conditional scripts if the condition matches
4. Returns the combined dictionary to scikit-build-core

**Note**: This is a build-time tool. End users installing from PyPI wheels don't need it.

## Documentation

- **[WHO_NEEDS_THIS.md](WHO_NEEDS_THIS.md)** - When is this provider needed?
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment options and strategies
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contributing to this project
- **[README_SUMMARY.md](README_SUMMARY.md)** - Quick navigation guide

## Example: AFDKO

AFDKO uses this provider to choose between a C++ binary and Python wrapper:

```toml
[tool.scikit-build.metadata.scripts]
provider = "skbuild_conditional_scripts"

scripts = {
    # 30+ deprecated wrapper scripts always installed
    "tx" = "afdko._deprecated:tx_wrapper",
    "makeotf" = "afdko._deprecated:makeotf_wrapper",
    # ... etc
}

conditional-scripts = {
    # Python wrapper only when requested
    "afdko" = "afdko.invoker:main"
}

condition-env-var = "AFDKO_COMMAND_USE_WRAPPER"
condition-env-value = "ON"
```

Normal builds install the fast C++ binary. When building in environments where the
C++ build fails, setting `AFDKO_COMMAND_USE_WRAPPER=ON` installs the Python wrapper instead.

## Requirements

- Python >= 3.10
- scikit-build-core (as your build backend)

## License

Apache License 2.0 - See [LICENSE](LICENSE) for details.

## Support

This project is maintained by the Adobe Type team.

- **Issues**: [GitHub Issues](https://github.com/adobe-type-tools/skbuild_conditional_scripts/issues)
- **Discussions**: Use issues for questions and discussions
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)

## Related Projects

- [scikit-build-core](https://github.com/scikit-build/scikit-build-core) - Modern Python build backend for CMake
- [AFDKO](https://github.com/adobe-type-tools/afdko) - Adobe Font Development Kit for OpenType
