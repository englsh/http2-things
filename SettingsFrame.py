import warnings

class EmptySettings(Warning): ...
class InvalidSettingName(Exception): ...

class SettingsData:
    # sloppy but eh
    SETTING_INFO = {
        "SETTINGS_HEADER_TABLE_SIZE": 0x01,
        "SETTINGS_ENABLE_PUSH": 0x02,
        "SETTINGS_MAX_CONCURRENT_STREAMS": 0x03,
        "SETTINGS_INITIAL_WINDOW_SIZE": 0x04,
        "SETTINGS_MAX_FRAME_SIZE": 0x05,
        "SETTINGS_MAX_HEADER_LIST_SIZE": 0x06
    }

    def __init__(self, data: dict[str, bytes] = {}):
        '''Class object for generating an HTTP/2 settings frame
        '''
        self.data = data

        if len(self.keys) == 0 or len(self.values) == 0:
            warnings.warn("Invalid settings object, missing keys or values. Using basic setup.", EmptySettings)
            self.data = self.__get_default__()

    def __get_default__(self) -> dict[str, bytes]:
        default_data = {
            "SETTINGS_MAX_CONCURRENT_STREAMS": bytes.fromhex("00000064"),
            "SETTINGS_INITIAL_WINDOW_SIZE": bytes.fromhex("0000ffff")
        }

        return default_data

    def __decode_key_name__(self, key: str) -> bytes:
        value = self.SETTING_INFO.get(key)

        if not value:
            raise InvalidSettingName("Invalid setting name has been provided. To see all valid setting names you can call `SettingsData.get_valid_names()`")

        return int.to_bytes(value, length = 2)

    def to_bytes(self) -> bytes:
        frameType = bytes.fromhex("04") # 04 indicates the SETTINGS frame
        additionalFlags = bytes(1) # no additional flags.
        streamIdentifier = bytes(4) # no stream identifier needed as this request is part of the connection. Use bytes(4) due to this.

        data = b''

        data_keys = self.get_keys()

        for key in data_keys:
            decoded_key = self.__decode_key_name__(key)
            data_value = self.get_value_from_key(key)

            data = data + decoded_key + data_value

        dataLength = int.to_bytes(len(data), length = 3)

        return dataLength + frameType + additionalFlags + streamIdentifier + data
    
    def get_valid_names(self) -> list: return 

    def get_keys(self) -> list: return list(self.data.keys())
    
    def get_values(self) -> list: return list(self.data.values())
        
    def get_value_from_key(self, key: str) -> bytes: return self.data.get(key)
