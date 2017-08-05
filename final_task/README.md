VK Uniq Group finder
=============================
This script allows to find out uniq user group.
Sctips waits initial parametrs from command line. Results are written in outGroups.json(by default).
Command line arguments:
  -h, --help    show this help message and exit
  -i I          Vk user id
  -u U          Vk user name
  -o OUT_FILE   File to write results(Default: outGroups.json)
  -a AUTH_DATA  Vk AuthToken. If not filled then default token is used.
You should enter "user id" or "user name" to start examination.
You able to ommit -o and -a argumends defaults values would be used.
Results are stored in OUT_FILE in json format.