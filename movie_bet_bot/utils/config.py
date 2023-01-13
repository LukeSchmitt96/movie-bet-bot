from typing import Dict
import yaml

def parse_config(config: Dict) -> Dict:
    contests = []
    for contest in config.get('contests'):
        members = []
        for member in contest.get('members'):
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
                'db_path': contest['db_path'],
            }
        )
    config = {
        # 'bot_config': {
        #     'interval_callback_duration': config['bot']['interval_callback_duration'],
        # },
        'contest_config': contests,
    }
    return config
