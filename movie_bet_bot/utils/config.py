from dataclasses import dataclass
from typing import List, Set
from yaml import Node

def parse_config(config: Node):
    contests = []
    for contest in config['contests']:
        members = []
        for member in contest['members']:
            members.append(
                {
                    'name': member['name'],
                    'profile_url': member['profile_url'],
                    'contest_url': member['contest_url'],
                }
            )
        contests.append(
            {
                'name': contest['name'],
                'members': members,
            }
        )
    return {
        'bot_config': {
            'interval_callback_duration': config['bot']['interval_callback_duration']
        },
        'contest_config': contests,
    }
