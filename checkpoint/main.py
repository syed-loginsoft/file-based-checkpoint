from base64 import b64encode
from json import dump, load
from pathlib import Path
from typing import Any, Dict, List, Optional


class FileCheckpointer:
    def __init__(self, checkpoint_dir: str):
        self._checkpoint_dir = checkpoint_dir

    def encode_key(self, key: str) -> str:
        return b64encode(key.encode()).decode()

    def get_file_path(self, key: str) -> str:
        file_path = Path(self._checkpoint_dir) / self.encode_key(key)
        # breakpoint()
        return str(file_path.absolute())

    def update(self, key: str, state: Any):
        # breakpoint()
        file_name = Path(self.get_file_path(key))
        new_name = f"{file_name.name}_new"
        new_file_name = file_name.parent / new_name
        with open(new_file_name, "w") as fp:
            dump(state, fp)

        file_name.unlink(missing_ok=True)
        new_file_name.rename(file_name)

    def batch_update(self, states: List[Dict[str, Any]]):
        for state in states:
            self.update(state["_key"], state["state"])

    def get(self, key: str) -> Optional[str]:
        # breakpoint()
        file_name = self.get_file_path(key)
        try:
            with open(file_name) as fp:
                return load(fp)
        except (OSError, ValueError):
            return None

    def delete(self, key: str) -> None:
        file_name = Path(self.get_file_path(key))
        file_name.unlink(missing_ok=True)
