import copy
import os
import signal
import subprocess

import click
import gevent


class BotSupervisor(object):
    def __init__(self, env={}):
        self.proc = None
        self.env = env
        self.bind_signals()
        self.start()

    def bind_signals(self):
        signal.signal(signal.SIGUSR1, self.handle_sigusr1)

    def handle_sigusr1(self, signum, frame):
        print 'SIGUSR1 - RESTARTING'
        gevent.spawn(self.restart)

    def start(self):
        env = copy.deepcopy(os.environ)
        env.update(self.env)
        self.proc = subprocess.Popen(['python', '-m', 'disco.cli', '--token', os.getenv('VAPORHELPER_DISCORD_BOT_TOKEN'), '--config', 'config.yaml'], env=env)

    def stop(self):
        self.proc.terminate()

    def restart(self):
        try:
            self.stop()
        except:
            pass

        self.start()

    def run_forever(self):
        while True:
            self.proc.wait()
            gevent.sleep(5)

@click.group()
def cli():
    pass

@cli.command()
@click.option('--env', '-e', default='local')
def bot(env):
    supervisor = BotSupervisor(env={
        'ENV': env
    })
    supervisor.run_forever()

if __name__ == '__main__':
    cli()
