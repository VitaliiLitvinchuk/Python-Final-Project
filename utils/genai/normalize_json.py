import json
import re


def normalize_json(json_string: str) -> dict[str, str]:
    result_text = json_string.strip()
    result_text = re.sub(r"^```json", "", result_text)
    result_text = re.sub(r"```$", "", result_text)
    result_text = result_text.strip()

    try:
        parsed_json = json.loads(result_text)
    except Exception as e:
        raise Exception(f"Error parsing JSON: {str(e)}")

    return parsed_json
