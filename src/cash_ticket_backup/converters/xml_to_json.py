import json
from typing import Tuple, Union

import xmltodict


def convert_to_json(xml_data: str) -> Tuple[bool, Union[str, dict]]:
    try:
        dict_data = xmltodict.parse(xml_data)
        json_data = json.dumps(dict_data)

        return True, json_data
    except Exception as e:
        # Conversion failed, use xml
        return False, xml_data
