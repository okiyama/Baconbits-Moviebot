#! /usr/bin/env python
#
# Example program using ircbot.py.
#
# Joel Rosdahl <joel@rosdahl.net>

"""A simple example bot.

This is an example bot that uses the SingleServerIRCBot class from
ircbot.py.  The bot enters a channel and listens for commands in
private messages and channel traffic.  Commands in channel messages
are given by prefixing the text by the bot name followed by a colon.
It also responds to DCC CHAT invitations and echos data sent in such
sessions.

The known commands are:

    stats -- Prints some channel information.

    disconnect -- Disconnect the bot.  The bot will try to reconnect
                  after 60 seconds.

    die -- Let the bot cease to exist.

    dcc -- Let the bot invite you to a DCC CHAT connection.
"""

"""Here's Julian's stuff now
"""
import time
from datetime import datetime

from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower, ip_numstr_to_quad, ip_quad_to_numstr

class TestBot(SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)
        c.part("#lounge", "fuck da polees")
    def on_privmsg(self, c, e):
        self.do_command(e, e.arguments()[0])

    def on_pubmsg(self, c, e):
        a = e.arguments()[0].split(":", 1)
        if len(a) > 1 and irc_lower(a[0]) == irc_lower(self.connection.get_nickname()):
            self.do_command(e, a[1].strip())
        return

    def on_dccmsg(self, c, e):
        for chname, chobj in self.channels.items():
            c.privmsg(e.arguments()[0])

    def on_dccchat(self, c, e):
        if len(e.arguments()) != 2:
            return
        args = e.arguments()[1].split()
        if len(args) == 4:
            try:
                address = ip_numstr_to_quad(args[2])
                port = int(args[3])
            except ValueError:
                return
            self.dcc_connect(address, port)
    

    def do_command(self, e, cmd):
        nick = nm_to_n(e.source())
        c = self.connection

        if cmd == "disconnect":
            self.disconnect()
        elif cmd == "die":
            self.die()
        elif cmd == "stats":
            for chname, chobj in self.channels.items():
                c.notice(nick, "--- Channel statistics ---")
                c.notice(nick, "Channel: " + chname)
                users = chobj.users()
                users.sort()
                c.notice(nick, "Users: " + ", ".join(users))
                opers = chobj.opers()
                opers.sort()
                c.notice(nick, "Opers: " + ", ".join(opers))
                voiced = chobj.voiced()
                voiced.sort()
                c.notice(nick, "Voiced: " + ", ".join(voiced))
        elif cmd == "dcc":
            dcc = self.dcc_listen()
            c.ctcp("DCC", nick, "CHAT chat %s %d" % (
                ip_quad_to_numstr(dcc.localaddress),
                dcc.localport))
        elif cmd == "start":
            for chname, chobj in self.channels.items():
                for i in range(10, 0 , -1):
                    c.privmsg(chname, i)
                    time.sleep(1)
                i = 10
                t = datetime.now()
                c.privmsg(chname, "Press play now! To get the current time send me a PM that says time")
        elif cmd == "time":
            try:
                global t
                c.privmsg(nick, (datetime.now() - t))
            except TypeError:
                c.privmsg(nick, "We aren't watching anything right now")
            except NameError:
                c.privmsg(nick, "We aren't watching anything right now")
        elif cmd == "stop":
            try:
                for chname, chobj in self.channels.items():
                    c.privmsg(chname, "Stopping now, hope everyone enjoyed the movie!")
                    backup = datetime.now() #if there is a mistake you can restore from backup
            except TypeError:
                c.privmsg(nick, "We haven't started, why even try to stop? Idiot.")
        elif cmd == "backup": #not working!
            for chname, chobj in self.channels.items():
                c.privmsg(nick, "Restoring backup, telling channel")
                c.privmsg(chname, "Oops, didn't mean to stop there, let's keep going from where we stopped!")
                global backup
                t = backup
                c.privmsg(chname, (datetime.now() - t))
        elif cmd == "welcome":
            for chname, chobj in self.channels.items():
                c.privmsg(chname, "The way this will work is everyone pauses at 0:00 before we start. Then I will countdown from 10 and we all hit play together. So go and pause those players now!")
        elif cmd == "announce":
            for chname, chobj in self.channels.items():
                c.privmsg(chname, "Pinging everyone because we're starting soon!")
                users = chobj.users()
                users.sort()
                c.notice(chname, ", ".join(users))
        else:
            c.notice(nick, "Not understood: " + cmd)

def main():
    import sys
    if len(sys.argv) != 4:
        print "Usage: testbot <server[:port]> <channel> <nickname>"
        sys.exit(1)

    s = sys.argv[1].split(":", 1)
    server = s[0]
    if len(s) == 2:
        try:
            port = int(s[1])
        except ValueError:
            print "Error: Erroneous port."
            sys.exit(1)
    else:
        port = 6667
    channel = sys.argv[2]
    nickname = sys.argv[3]

    bot = TestBot(channel, nickname, server, port)
    bot.start()

if __name__ == "__main__":
    main()
