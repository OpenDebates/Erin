import os
from copy import deepcopy
from random import random

import pytest

from erin.core.exceptions import EnvironmentVariableError
from erin.core.schema import ENV_MAPPINGS, OPTIONAL_ENVS
from erin.core.utils import config_loader


def test_config_env_vars():
    # Delete environment variables
    delete_envs()

    for key, val in ENV_MAPPINGS.items():
        for sub_key, sub_val in val.items():
            # Some random strings
            if sub_val in OPTIONAL_ENVS:
                os.environ[sub_val] = str(random())[2:]
    with pytest.raises(EnvironmentVariableError) as e_info:
        mappings = config_loader(ENV_MAPPINGS, OPTIONAL_ENVS)

    # Check if ENV variables get saved
    saved_maps = deepcopy(ENV_MAPPINGS)
    for key, val in ENV_MAPPINGS.items():
        for sub_key, sub_val in val.items():
            saved_maps[key][sub_key] = str(random())[2:]
            os.environ[sub_val] = saved_maps[key][sub_key]
    mappings = config_loader(ENV_MAPPINGS, OPTIONAL_ENVS)

    assert mappings == saved_maps

    # Teardown
    delete_envs()


def delete_envs():
    for key, val in ENV_MAPPINGS.items():
        for sub_key, sub_val in val.items():
            try:
                # Some random strings
                del os.environ[sub_val]
            except KeyError:
                pass
