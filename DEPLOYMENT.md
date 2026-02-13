# Deployment Options for skbuild-conditional-scripts

This document explains how to deploy the `skbuild-conditional-scripts` provider
for use by AFDKO and other projects.

## The Problem

The provider needs to be available in the **isolated build environment** during
source builds. By default, pip creates an isolated environment with only the
packages listed in `[build-system.requires]`, but our provider is in the local
source tree.

**Important**: End users installing from PyPI wheels don't need the provider -
it's only required at build time. Pre-built wheels contain everything. See
`WHO_NEEDS_THIS.md` for a detailed breakdown of which scenarios need the provider.

## Option 1: Local Development with --no-build-isolation (Current)

### How It Works

Developers manually install the provider first, then use `--no-build-isolation`:

```bash
# One-time setup
pip install ./_build_helpers

# Then build/install AFDKO without isolation
pip install --no-build-isolation .
```

### Pros
- ✅ Simple for development
- ✅ No external dependencies
- ✅ Fast iteration (edit provider, reinstall)

### Cons
- ❌ Requires manual setup step
- ❌ Every contributor needs to know about this
- ❌ Doesn't work for end users (`pip install afdko`)
- ❌ Wheel builds (CI) need special handling

### When to Use
- Local development
- Testing changes to the provider
- Quick iterations

## Option 2: Publish to PyPI (Recommended for Production)

### How It Works

1. Publish `skbuild-conditional-scripts` as a standalone package on PyPI:
   ```bash
   cd _build_helpers
   python -m build
   python -m twine upload dist/*
   ```

2. Update AFDKO's `pyproject.toml`:
   ```toml
   [build-system]
   requires = [
       "scikit-build-core",
       "setuptools-scm",
       "cython",
       "skbuild-conditional-scripts",  # Add this
   ]
   ```

3. Remove the `provider-path`:
   ```toml
   [tool.scikit-build.metadata.scripts]
   provider = "skbuild_conditional_scripts"
   # provider-path = "_build_helpers"  # Remove - package is on PyPI now
   ```

4. Normal pip install works:
   ```bash
   pip install .
   # Or for end users:
   pip install afdko
   ```

### Pros
- ✅ Works everywhere (local dev, CI, end users)
- ✅ Standard Python packaging workflow
- ✅ No special build instructions needed
- ✅ Wheel builds work normally
- ✅ Other projects can reuse it

### Cons
- ❌ Requires PyPI account and publishing workflow
- ❌ Changes to provider require new release
- ❌ Slightly slower development iteration

### When to Use
- Production releases
- CI/CD wheel building
- When others need to install from source
- If other projects want to use the provider

## Option 3: Include in sdist with provider-path (Experimental)

### How It Works

The `provider-path = "_build_helpers"` configuration should theoretically work
because:
1. Source tree (including `_build_helpers/`) is copied to build environment
2. `provider-path` adds that directory to `sys.path`
3. Provider becomes importable

However, this is currently **untested** and may have issues with:
- Path resolution in isolated environments
- Symlinks or temporary directory handling
- Different behavior across pip versions

### Status
⚠️ Not verified to work reliably

## Recommended Approach

### For Now (Development Phase)
**Use Option 1** (--no-build-isolation):
- Add to CONTRIBUTING.md
- Document in developer setup instructions
- Use in CI builds with explicit provider installation step

### For Production (Before Release)
**Switch to Option 2** (PyPI publishing):
- One-time setup to publish provider
- Rarely needs updates (provider is very stable)
- Clean experience for all users
- Standard packaging workflow

## CI/Wheel Building

### Current Setup (Option 1 - --no-build-isolation)

```yaml
# .github/workflows/build_wheels.yml
jobs:
  build_wheels:
    steps:
      - name: Install build provider
        run: pip install ./_build_helpers

      - name: Build wheels
        uses: pypa/cibuildwheel@v2
        env:
          CIBW_BUILD_FRONTEND: "build[uv]"
          # Use --no-build-isolation
          CIBW_BUILD: "*"
          CIBW_BUILD_VERBOSITY: 1
```

### Future Setup (Option 2 - PyPI)

```yaml
# No special steps needed - standard wheel build
jobs:
  build_wheels:
    steps:
      - uses: pypa/cibuildwheel@v2
        # Provider is in build-system.requires, automatically available
```

## Testing the Setup

### Test Local Development
```bash
# Option 1
pip install ./_build_helpers
pip install --no-build-isolation .
afdko --help

# Option 2 (after publishing)
pip install .
afdko --help
```

### Test Conditional Scripts
```bash
# Default: C++ binary
pip install --no-build-isolation .
file $(which afdko)  # Should be ELF/Mach-O binary

# With wrapper
AFDKO_COMMAND_USE_WRAPPER=ON pip install --no-build-isolation .
head -3 $(which afdko)  # Should be Python script
```

### Test Wheel Build
```bash
pip install build
python -m build --wheel
pip install dist/*.whl
afdko --help
```

## Migration Path

1. **Now**: Document Option 1 in developer guide
2. **Before beta release**: Publish provider to PyPI
3. **Update**: Switch to Option 2 in pyproject.toml
4. **Verify**: Test wheel builds work without special steps
5. **Cleanup**: Remove --no-build-isolation from docs

## Publishing to PyPI (When Ready)

```bash
cd _build_helpers

# Install publishing tools
pip install build twine

# Build the package
python -m build

# Upload to Test PyPI first
python -m twine upload --repository testpypi dist/*

# Test install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ skbuild-conditional-scripts

# If all works, upload to real PyPI
python -m twine upload dist/*
```

## Questions?

- **Do we need to version the provider?**
  Yes, but updates should be rare (it's very simple and stable)

- **Can we vendor it instead?**
  Not easily - needs to be importable during isolated build

- **What if someone else publishes this name?**
  Unlikely, but we could use `afdko-skbuild-conditional-scripts` if needed

- **Does this work with editable installs?**
  Yes with Option 1 (--no-build-isolation), automatically with Option 2
