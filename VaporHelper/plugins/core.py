from disco.bot import Plugin

class CorePlugin(Plugin):

    @Plugin.command('ping', level=30)
    def ping(self, event):
        event.msg.reply('pong')