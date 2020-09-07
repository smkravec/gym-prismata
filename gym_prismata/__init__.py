from gym.envs.registration import register

register(id='PrismataEnv-v0',
    entry_point='gym_prismata.prismata_env_dir:PrismataEnv'
)
