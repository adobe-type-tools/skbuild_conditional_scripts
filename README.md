# skbuild-conditional-scripts

Generic dynamic script metadata provider for scikit-build-core projects.

This micro-package provides a reusable metadata provider that can conditionally
install entry point scripts based on environment variables. Originally developed
for AFDKO to choose between installing a C++ binary or Python wrapper, it can be
used by any scikit-build-core project that needs conditional entry point generation.

## Features

- **Data-driven**: All script definitions live in `pyproject.toml`, not code
- **Conditional installation**: Install different scripts based on environment variables
- **Generic**: Can be reused by other projects with similar needs

## Usage

1. Install this package (or include via `provider-path`)
2. Configure in your `pyproject.toml`:

```toml
[tool.scikit-build.metadata.scripts]
provider = "skbuild_conditional_scripts"
provider-path = "_build_helpers"  # if using local copy

scripts = {
    "always-installed" = "package:function",
}

conditional-scripts = {
    "maybe-installed" = "package:other_function",
}

condition-env-var = "MY_ENV_VAR"
condition-env-value = "ON"
```

3. At build time, if `MY_ENV_VAR=ON`, both script sets are installed.
   Otherwise, only base scripts are installed.
