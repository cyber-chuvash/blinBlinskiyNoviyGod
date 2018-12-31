import json


class Database:
    def __init__(self):
        self.db = None
        self.load()

    def load(self):
        try:
            with open('db.json', 'r') as f:
                text = f.read()
        except FileNotFoundError:
            open('db.json', 'w').close()
            text = None

        if text:
            self.db = json.loads(text)
        else:
            self.db = {
                'chats': [],
            }

    def save(self):
        with open('db.json', 'w') as f:
            f.write(json.dumps(self.db))

    @property
    def chats(self):
        self.load()
        return self.db['chats']

    def add_chat(self, chat):
        if chat not in self.chats:
            self.db['chats'].append(int(chat))
            self.save()

    def remove_chat(self, chat):
        if chat in self.chats:
            self.db['chats'].remove(int(chat))
            self.save()
