import pythoncom
from win32comext.propsys import propsys
from win32comext.shell import shellcon
import os


def format_api_args(bef_url: str, **kwargs):
    res = bef_url
    for key, val in kwargs.items():
        res += f"{key}={val}&"
    return res.replace(" ", "%20")


class FileTag:
    def __init__(self, file_path: str) -> None:
        self.file_path = os.path.realpath(file_path)
        self.property_key = propsys.PSGetPropertyKeyFromName("System.Keywords")
        self.property_store = propsys.SHGetPropertyStoreFromParsingName(
            self.file_path, None, shellcon.GPS_READWRITE, propsys.IID_IPropertyStore)
        current_value = self.property_store.GetValue(
            self.property_key).GetValue()
        self.tags = list(current_value) if current_value else []

    def clear(self):
        self.tags = []

    def add_tags(self, *tags):
        self.tags.extend(tags)

    def remove_tags(self, *tags):
        for tag in tags:
            self.tags.remove(tag)

    def save(self):
        self.property_store.SetValue(self.property_key, propsys.PROPVARIANTType(
            self.tags, pythoncom.VT_VECTOR | pythoncom.VT_BSTR))
        self.property_store.Commit()
