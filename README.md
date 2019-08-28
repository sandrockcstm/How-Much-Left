# How Much Left

## What is it?
HML is a program that helps you keep track of tasks and quotas.  Need to apply to jobs x number of times in a day? HML can help you to keep track of how many times you've applied.  Need to keep track of how many times you've sat down to write code this week?  HML is suited for that too.  HML can even be used as a simple checklist, if you'd like.

You tell HML what your quota is called, how many times you've done it, and how many times it needs to be done, and then as you complete your task you let HML know to increment your current count.

When you change your current count for your quota, a progress bar will fill up similar to an xp bar in a video game.  This is a visual motivator for you to keep going!  When your current count equals your quota goal, a message will display congratulating you on your accomplishment.  It will then ask if you would like to delete the quota.  You may choose whether or not to keep it, as well as whether or not to reset the count to 0.

HML is currently command-line-only.  A GUI may be built at a later date.

## Setup
Once you have downloaded HML, navigate to the folder you've downloaded it to and type `python3 HML.py new`.  If this is your first time running it, it will ask to initialize the quota database.  Type "yes" to do that.  Afterwards it will take you through the process of setting up your quota by asking for the name of the quota, how many times you've done it already, and how many times it still needs to be done.

You will need to keep the quota.db file in the same folder as HML.py.

You have now added your first quota!

## Usage
The format for using HML is `python3 HML.py [action]`.  An example of this would be `python3 HML.py add`.

The following are valid actions in HML:

`add`.  Increments a quota's current count by 1.

`sub`.  Decrements a quota's current count by 1.

`set`.  Allows you to manually set the current count and the quota count for a quota.

`new`.  Create a new quota.

`del`.  Delete a quota (requires the id of the quota for safety, which can be obtained with the show or show_all command).

`show`. Returns information about a specific quota by name.

`show_all`.  Shows information on all quotas in the database.

You may find a list of valid commands from within the command line by typing `python3 HML.py -h`.

## Technical information
HML is written in Python 3.7.3, and uses sqlite for the database.  It uses the argparse library to handle command inputs from the command line, and Progress to render the progress bar.

## Acknowledgements
Thanks to Noëlle Anthony and Ema Socks for their assistance with this project!

## License
How Much Left uses the Cooperative Software License.  If you are an individual seeking to use or modify this software for personal reasons, you are welcome to do so!  If you are part of a worker-owned business or collective, you are also welcome to use or modify this software.

If you are attempting to use or modify this software for commercial purposes and are not part of a worker-owned cooperative, you may not do so and must contact me to establish an appropriate licensing agreement.
