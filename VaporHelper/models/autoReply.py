from peewee import TextField
from VaporHelper.sql import BaseModel


@BaseModel.register
class AutoReply(BaseModel):
    word = TextField()
    reply = TextField()

    def check_string(self, content):
        return self.word.lower() in content.lower() # pylint: disable=E1101
    
    @property
    def searchable(self):
        return '{} {}'.format(self.word, self.reply)
