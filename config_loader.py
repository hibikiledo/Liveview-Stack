'''
    Configuration Loader

    This module provide a convenient method for reading configuration file.
    It returns dictionary as a result of the reading.
'''


def load(filename):

    config_dict = {}
    config_file = open(filename)

    while True:
        # read a single line
        line = config_file.readline()
        # if length of line is 0, then EOF has reached
        if len(line) == 0:
            break
        if len(line) == 1:
            continue
        # split at = sign
        tokens = line.split("=")
        tokens_cleaned = [ token.replace("\n", "") for token in tokens ]
        # update value into config dict
        config_dict[tokens_cleaned[0]] = tokens_cleaned[1]

    return config_dict
