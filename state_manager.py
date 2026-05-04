import json
import os

class StateManager:
    def __init__(self, state_file='seen_items.json'):
        self.state_file = state_file
        self.seen_items = self._load_state()

    def _load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return set(json.load(f))
            except (json.JSONDecodeError, TypeError):
                return set()
        return set()

    def save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump(list(self.seen_items), f)

    def is_new(self, item_id):
        return item_id not in self.seen_items

    def add_item(self, item_id):
        self.seen_items.add(item_id)
