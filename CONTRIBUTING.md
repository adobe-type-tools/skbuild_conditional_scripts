# Contributing to skbuild-conditional-scripts

This is a small, focused package that provides conditional script installation
for scikit-build-core projects. Changes should be rare and carefully considered.

## Philosophy

**Keep it simple.** This provider does exactly one thing: merge base scripts with
conditional scripts based on environment variable checks. Any feature requests
should be evaluated against this core purpose.

## Development Setup

```bash
# Clone the repository
git clone https://github.com/adobe-type-tools/afdko.git
cd afdko/_build_helpers

# Install in development mode
pip install -e .

# Run tests (if any are added)
pytest
```

## Making Changes

### Code Changes

The provider is **intentionally minimal** (~70 lines including docs). Consider:

1. **Is this change necessary?** Can it be handled in the project's config instead?
2. **Does it maintain backward compatibility?** Existing users shouldn't break.
3. **Is it generic?** Don't add project-specific logic.

### Documentation Changes

Update the following files:
- `README.md` - User-facing documentation
- `__init__.py` - Docstrings and examples
- `DEPLOYMENT.md` - If deployment process changes

## Testing

### Manual Testing

Test with a real scikit-build-core project (like AFDKO):

```bash
# Test default behavior
cd ../../  # Back to AFDKO root
pip install --no-build-isolation .
# Verify scripts installed correctly

# Test conditional behavior
AFDKO_COMMAND_USE_WRAPPER=ON pip install --no-build-isolation --force-reinstall .
# Verify conditional scripts installed
```

### Future: Automated Tests

Consider adding:
- Unit tests for `dynamic_metadata()` function
- Integration tests with a minimal scikit-build-core project
- Tests for edge cases (missing config, invalid env vars, etc.)

## Versioning

Use semantic versioning:
- **1.x.x** - Current stable version
- **Patch** (1.0.x) - Bug fixes, documentation
- **Minor** (1.x.0) - Backward-compatible features
- **Major** (x.0.0) - Breaking changes (rare)

## Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md` (if we create one)
3. Commit: `git commit -m "Release vX.Y.Z"`
4. Tag: `git tag -a vX.Y.Z -m "Version X.Y.Z"`
5. Build: `python -m build`
6. Test: Install from wheel and verify
7. Publish: `python -m twine upload dist/*`
8. Push: `git push && git push --tags`

## Code Style

- Follow PEP 8
- Maximum line length: 88 characters (Black default)
- Use type hints for function signatures
- Keep functions small and focused
- Document with clear docstrings

## Potential Features (Discuss First)

Ideas that might be worth discussing:

- **Multiple conditions**: AND/OR logic for env vars
- **Platform conditionals**: Different scripts per OS
- **Config file support**: Read conditions from a file
- **Logging**: Debug output for troubleshooting
- **Validation**: Check that entry points are valid format

All of these should be **opt-in** and maintain backward compatibility.

## Support

This package is maintained as part of AFDKO. For questions or issues:
- Open an issue on the AFDKO repository
- Include "skbuild-conditional-scripts" in the title
- Provide minimal reproduction case

## License

Apache License 2.0 - same as AFDKO
