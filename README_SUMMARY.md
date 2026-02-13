# Quick Start Guide

## What is this?

`skbuild-conditional-scripts` is a generic metadata provider that allows
scikit-build-core projects to conditionally install entry point scripts based
on environment variables.

## Do I need this?

**Most people don't need to think about this at all.**

- **End users**: Install from PyPI wheels → no provider needed
- **Contributors**: Need to install provider to build from source
- **CI/CD**: Needs provider to build wheels

See `WHO_NEEDS_THIS.md` for the complete breakdown.

## For AFDKO Contributors

If you're contributing to AFDKO:

```bash
# One-time setup
pip install ./_build_helpers

# Build and install
pip install --no-build-isolation .
```

See `DEPLOYMENT.md` for details.

## For Users of This Provider

If you want to use this provider in your own project:

1. Copy `_build_helpers/` to your project (or install from PyPI when published)

2. Add to your `pyproject.toml`:
   ```toml
   [tool.scikit-build.metadata.scripts]
   provider = "skbuild_conditional_scripts"
   provider-path = "_build_helpers"

   scripts = {
       "always-installed" = "yourpkg:function1",
   }

   conditional-scripts = {
       "maybe-installed" = "yourpkg:function2",
   }

   condition-env-var = "YOUR_ENV_VAR"
   condition-env-value = "ON"
   ```

3. Build your project - conditional scripts will be installed based on env var.

## Documentation

- **`README.md`** - Detailed usage guide for the provider
- **`WHO_NEEDS_THIS.md`** - When is the provider needed? (read this first!)
- **`DEPLOYMENT.md`** - Deployment options and migration path
- **`CONTRIBUTING.md`** - Contributing to the provider itself
- **`../docs/DYNAMIC_SCRIPTS.md`** - AFDKO-specific documentation

## Current Status

**Development Mode (Option 1)**
- Contributors must manually install provider
- Use `--no-build-isolation` for builds
- End users unaffected (install from PyPI wheels)

**Future: Production Mode (Option 2)**
- Publish provider to PyPI
- Remove `--no-build-isolation` requirement
- Everything "just works"

See `DEPLOYMENT.md` for migration plan.

## Support

This package is maintained as part of [AFDKO](https://github.com/adobe-type-tools/afdko).

For issues or questions:
- Check the documentation files above
- Open an issue on the AFDKO repository
- Include "skbuild-conditional-scripts" in the title
