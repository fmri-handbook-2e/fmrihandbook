"""
config setup for fmri-handbook
"""

import os
import git
import yaml
from box import Box
from pathlib import Path


def get_config(nbfile=None, configfile=None, basedir=None, required_dirs=None):
    """
    load config for project from yaml file

    Arguments:
    nbfile: name of notebook file (i.e. __file__), used to extract module name
    configfile: specify location for configuration file (defaults to config.yaml in basedir)
    basedir: specify location for basedir (defaults to repo base)
    required_dirs: required directories to check for

    Returns:
    config: a Box instance
    """

    repo = git.Repo(os.path.dirname(__file__),
                    search_parent_directories=True)
    repo_path = repo.git.rev_parse("--show-toplevel")

    if configfile is None:
        configfile = os.path.join(repo_path, "config.yaml")

    with open(configfile, "r") as ymlfile:
        config = Box(yaml.safe_load(ymlfile), 
                     default_box=True, default_box_attr=None)

    # check for existence of required directories
    if required_dirs is None:
        required_dirs = ['orig_figuredir', 'figure_basedir', 'data_basedir']

    for dir in required_dirs:
        if config[dir] is None:
            raise Exception(
                f'{dir} must be specified in the config file')
        # if not absolute, use repo base
        if not Path(config[dir]).is_absolute():
            config[dir] = os.path.join(
                repo_path, config[dir])
        if not os.path.exists(config[dir]):
            try:
                os.mkdir(config[dir])
                print('Created', config[dir])
            except FileNotFoundError:
                raise Exception(
                    f'{dir} does not exist - please create it')
    config['figure_dir'] = None
    if nbfile is not None:
        config['module'] = Path(nbfile).stem
        config['figure_dir'] = os.path.join(
            config['figure_basedir'], config['module'])
        config['data_dir'] = os.path.join(
            config['data_basedir'], config['module'])
    return(config)
