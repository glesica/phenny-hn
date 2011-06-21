###### Phenny-HN

This is a Phenny IRC bot module for sharing the most popular link on the Hacker News front page in a channel.

##### Setup

Install the module, hn.py, in your Phenny instance. It will do the rest. There are some configuration constants near the top of the file you can set.

`REFRESH_SECONDS` - Minimum number of seconds the bot will sleep for between links.

`MAX_HISTORY_SIZE` - The number of previous links the bot will remember, and thus not share again.

##### Commands

If you tell the bot to "repeat hn" it will re-share the last link.
