from disco.bot import Plugin
from disco.bot.command import CommandLevels
from disco.types.message import MessageTable

from VaporHelper.models.autoReply import AutoReply
from VaporHelper.sql import init_db


class AutoReplyPlugin(Plugin):
    """Auto replies to certain tokens"""

    def load(self, ctx):
        init_db()

    @Plugin.listen('MessageCreate')
    def on_message_create(self, event):
        if event.message.author.bot:
            return
        if event.message.author.id == 479967319695687681:
            return
        if event.message.content.startswith(self.bot.config.commands_prefix):
            return
        replies = []
        for reply in AutoReply.select():
            if reply.check_string(event.message.content):
                replies.append(reply.reply)
        
        if len(replies) >= 1:
            event.message.reply('\n'.join(replies))
    
    @Plugin.command('all', group='reply', level=CommandLevels.MOD)
    def all_replies(self, event):
        foundReplies = AutoReply.select()
        if not len(foundReplies) >= 1:
            event.msg.reply('No auto replies found')
            return
        tbl = MessageTable(codeblock=False)
        tbl.set_header('word', 'reply')
        for reply in foundReplies:
            tbl.add(reply.word, reply.reply)
        
        result = tbl.compile()
        if len(result) > 1900:
            return event.msg.reply('Result is too big. Take a TXT file!',
                        attachments=[('result.txt', result)])
        return event.msg.reply('```' + result + '```')

    
    @Plugin.command('find', '<term:str>', group='reply', level=30)
    def find_reply(self, event, term):
        foundReplies = AutoReply.select().where(
            (AutoReply.word.contains(term)) |
            (AutoReply.reply.contains(term))
        )
        if not len(foundReplies) >= 1:
            event.msg.reply('No auto replies found')
            return
        tbl = MessageTable(codeblock=False)
        tbl.set_header('word', 'reply')
        for reply in foundReplies:
            tbl.add(reply.word, reply.reply)
        
        result = tbl.compile()
        if len(result) > 1900:
            return event.msg.reply('Result is too big. Take a TXT file!',
                        attachments=[('result.txt', result)])
        return event.msg.reply('```' + result + '```')
    
    @Plugin.command('edit', '<word:str>, <reply:str...>', group='reply', level=CommandLevels.MOD)
    def edit_reply(self, event, word, reply):
        try:
            gReply = AutoReply.select().where(AutoReply.word==word).get()
        except AutoReply.DoesNotExist:
            event.msg.reply('This auto reply does not exist. Create it using `reply add`')
        else:
            gReply.reply = reply
            gReply.save()
            event.msg.reply('Updated reply!')

    @Plugin.command('add', '<word:str>, <reply:str...>', group='reply', level=CommandLevels.MOD)
    def add_reply(self, event, word, reply):
        AutoReply.create(word=word, reply=reply)
        event.msg.reply('Created reply `{}` for `{}`'.format(reply, word))
    
    @Plugin.command('delete', '<word:str>', group='reply', level=CommandLevels.MOD)
    def remove_reply(self, event, word, reply):
        try:
            gReply = AutoReply.select().where(AutoReply.word==word).get()
        except AutoReply.DoesNotExist:
            event.msg.reply('This auto reply does not exist. Unable to delete it')
        else:
            gReply.delete_instance()
            event.msg.reply('Deleted reply for {}'.format(word))
