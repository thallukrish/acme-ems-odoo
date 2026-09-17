from .hooks import post_init_hook as _base_post_init_hook
from .scenario_extension import extend_demo_scenario


def post_init_hook(env):
    _base_post_init_hook(env)
    extend_demo_scenario(env)
