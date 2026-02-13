# Who Needs the Provider?

Quick reference for understanding when `skbuild-conditional-scripts` is required.

## TL;DR

**End users installing from PyPI don't need this.** Pre-built wheels contain
everything. The provider is only needed at **build time**.

## Scenarios

### ✅ End Users Installing from PyPI

```bash
pip install afdko
```

**Status**: ✅ Works perfectly, no provider needed

**Why**: Pre-built wheels on PyPI already contain:
- All Python code
- All C++ binaries
- All entry point scripts

No building happens, just unpacking the wheel.

---

### ⚠️ Contributors Building from Source (Current - Option 1)

```bash
git clone https://github.com/adobe-type-tools/afdko.git
cd afdko
pip install .
```

**Status**: ❌ Fails - provider not found in isolated build environment

**Solution**:
```bash
pip install ./_build_helpers
pip install --no-build-isolation .
```

**Why**: The provider is in the local tree but not accessible in pip's
isolated build environment.

---

### ✅ Contributors Building from Source (Future - Option 2)

```bash
git clone https://github.com/adobe-type-tools/afdko.git
cd afdko
pip install .
```

**Status**: ✅ Will work after provider is published to PyPI

**Why**: Provider will be in `build-system.requires`, automatically installed
in isolated build environment.

---

### ⚠️ CI/CD Building Wheels (Current - Option 1)

```yaml
- name: Build wheels
  uses: pypa/cibuildwheel@v2
```

**Status**: ❌ Fails - provider not found

**Solution**:
```yaml
- name: Install provider
  run: pip install ./_build_helpers

- name: Build wheels
  uses: pypa/cibuildwheel@v2
  env:
    PIP_NO_BUILD_ISOLATION: "1"
```

**Why**: Same issue as local builds.

---

### ✅ CI/CD Building Wheels (Future - Option 2)

```yaml
- name: Build wheels
  uses: pypa/cibuildwheel@v2
```

**Status**: ✅ Will work after provider is published to PyPI

**Why**: Provider automatically installed from PyPI during build.

---

### ⚠️ Installing from Git URL

```bash
pip install git+https://github.com/adobe-type-tools/afdko.git
```

**Status**: ❌ Fails currently (Option 1)

**Future**: ✅ Will work with Option 2 (provider on PyPI)

**Why**: Git installations trigger source builds in isolated environment.

---

### ✅ Installing from Pre-Built Wheel File

```bash
pip install afdko-5.0.0-cp312-cp312-macosx_14_0_arm64.whl
```

**Status**: ✅ Always works, no provider needed

**Why**: Wheel already built, just unpacking.

---

### 🔄 Building an sdist

```bash
python -m build --sdist
```

**Status**:
- Current (Option 1): ⚠️ Works, but sdist users can't build it
- Future (Option 2): ✅ Works, sdist users can build it

**Why**: The sdist itself builds fine, but anyone building FROM that sdist
needs the provider available.

## Summary Table

| Scenario | Option 1 (Current) | Option 2 (PyPI) | Provider Needed? |
|----------|-------------------|-----------------|------------------|
| `pip install afdko` (PyPI) | ✅ | ✅ | ❌ No (pre-built) |
| `pip install .` (source) | ❌ Needs workaround | ✅ | ✅ Yes (build time) |
| `pip install git+...` | ❌ Fails | ✅ | ✅ Yes (build time) |
| CI wheel building | ❌ Needs workaround | ✅ | ✅ Yes (build time) |
| Install from wheel file | ✅ | ✅ | ❌ No (pre-built) |
| Build sdist | ⚠️ | ✅ | ✅ Yes (for sdist users) |

## Key Insight

**The provider is a build-time dependency, not a runtime dependency.**

Think of it like:
- **cmake/ninja**: Needed to build, not needed to use
- **cython**: Needed to compile .pyx files, not needed to import them
- **skbuild-conditional-scripts**: Needed to generate entry points, not needed to run them

## Recommendations

### For Now (Development Phase)
- Document the `--no-build-isolation` requirement
- Use workaround in CI
- End users unaffected (install from PyPI wheels)

### Before 5.0 Release
- Publish provider to PyPI
- Update `build-system.requires`
- Remove workarounds from CI
- Update contributor documentation

### For 5.0 Release
- Everything "just works"
- Contributors: `pip install .`
- CI: Standard wheel building
- Users: Still `pip install afdko` (unchanged)

## Questions?

**Q: Why not just include the provider in the main package?**

A: Can't import it during build because the package isn't installed yet.
Classic chicken-and-egg problem.

**Q: Why not just use static entry points?**

A: We need conditional logic - sometimes install C++ binary, sometimes Python wrapper.
Static configuration can't express this.

**Q: Will the provider ever need updates?**

A: Very rarely. It's ~70 lines of generic logic that shouldn't change.
All project-specific config is in pyproject.toml.

**Q: What if I want to modify the provider?**

A: For local development, edit `_build_helpers/` and reinstall it.
For production, would need a new provider release.
