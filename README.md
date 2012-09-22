**Dependencies:**  
* Python http://www.python.org/  
* python-irclib-0.4.8 http://python-irclib.sourceforge.net/  

**Usage:**  
This is intended for movie nights that are hosted via any chat room. Every
user obtains their own copy of the movie then once everyone is in the chat
channel this bot starts a timer. Then users sync where they are in the movie
with this timer. This timer is used to sync up all the copies
of the movie playing simultaneously on the different user's computers.
This syncronization makes live discussion of the movie far more enjoyable.


**Instructions:**  
Download python-irclib-0.4.8 and run "python setup.py install" to install the 
irclib needed.
Run "python MovieNight_IrcBot.py irc.us.baconbits.org:6667 #movienight MovieBot"
which will have the bot join #movienight under the name MovieBot. It will 
also leave #lounge, since all public chat that MovieBot does it sent to all 
channels it is in.


To use commands you just send a PM to MovieBot with nothing but the command in it.  
**Commands:**  
* welcome - Sends "The way this will work is everyone pauses at 0:00 before we 
start. Then I will countdown from 10 and we all hit play together. So go and 
pause those players now!" to the channel, recommended to be played before sending 
start.
* announce - Says the name of everyone in the channel to give their IRC client a
 ping, recommended to get users in before you start.
start - Immediately begins a countdown from 10 to 0 at which point all the 
users press play.
* time - Sends a private message with the current timestamp to the user, for 
those that join late or get off sync.
* stop - Stops keeping track of time, to be used only after the movie is over.
* backup - WIP! Currently not working well at all but the idea is that if a stop
command is sent on accident or to grief you can use the backup command to 
start back where the stop command was sent. Most likely unneeded feature.
* die - Kills the bot.
* disconnect - Bot leaves and rejoins after 60 seconds. Pretty much useless.
* stats - Likely to be removed, came default with the library. Sends some 
channels stats to the user.
* dcc - starts a dcc chat with the user, also likely to be removed.

**TODO:**  
Backup working  
A way for MovieBot to talk to the channel, just for fun.