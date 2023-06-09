import importlib
import pip
import os
from utils import GenerateTemplate, TEMPLATE_LOC
import numpy as np

import toml  # type: ignore
import gymnasium


def test_run_env():
    with GenerateTemplate():
        environment_loc = TEMPLATE_LOC.joinpath("pyproject.toml")
        env_vars = toml.load(environment_loc)
        env_name = env_vars.get("project").get("name")

        os.chdir(TEMPLATE_LOC)
        pip.main(["uninstall", env_name, "-y"])
        pip.main(["install", "-e", "."])
        importlib.import_module(env_name)  # , package=None)
        from gymnasium.wrappers import FlattenObservation

        env = gymnasium.make(f"{env_name}/GridWorld-v0")
        wrapped_env = FlattenObservation(env)
        out1, out2 = wrapped_env.reset(seed=42)
        np.testing.assert_array_equal(out1, [0, 3, 3, 2])
        assert out2 == {"distance": 4.0}
        pip.main(["uninstall", env_name, "-y"])
