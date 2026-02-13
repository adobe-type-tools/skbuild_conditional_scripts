"""
Generic dynamic script metadata provider for scikit-build-core.

This provider merges base scripts with conditional scripts based on
environment variable checks. All script definitions are configured in
pyproject.toml [tool.scikit-build.metadata.scripts].

Configuration in pyproject.toml:
    [tool.scikit-build.metadata.scripts]
    provider = "afdko_build_scripts"
    provider-path = "_build_helpers"

    # Always installed scripts
    scripts = {
        "command1" = "package.module:function1",
        "command2" = "package.module:function2",
    }

    # Conditionally installed scripts
    conditional-scripts = {
        "command3" = "package.module:function3",
    }

    # Condition for installing conditional-scripts
    condition-env-var = "SOME_ENV_VAR"
    condition-env-value = "ON"  # Install conditional-scripts if var equals this
"""

import os


def dynamic_metadata(field, settings, metadata):
    """
    Generic provider that merges base scripts with conditional scripts.

    Args:
        field: The metadata field being requested (should be "scripts")
        settings: Configuration from [tool.scikit-build.metadata.scripts]
                  Expected keys:
                  - scripts: dict of always-installed entry points
                  - conditional-scripts: dict of conditionally-installed entry points
                  - condition-env-var: environment variable name to check
                  - condition-env-value: value that triggers conditional install
        metadata: DynamicPyProject mapping with access to [project] section

    Returns:
        Dictionary mapping script names to entry points

    Example:
        If AFDKO_COMMAND_USE_WRAPPER=ON, both base and conditional scripts
        are installed. Otherwise, only base scripts are installed.
    """
    assert field == "scripts", f"Expected 'scripts' field, got '{field}'"

    # Start with base scripts (always installed)
    scripts = dict(settings.get("scripts", {}))

    # Check if we should include conditional scripts
    env_var = settings.get("condition-env-var")
    if env_var:
        expected_value = settings.get("condition-env-value", "ON")
        actual_value = os.environ.get(env_var)

        if actual_value == expected_value:
            # Add conditional scripts
            conditional = settings.get("conditional-scripts", {})
            scripts.update(conditional)

    return scripts
