from statsbombpy import sb

import json

def get_competitions() -> str:
    return json.dumps(
        sb.competitions().to_dict(orient='records')
    )