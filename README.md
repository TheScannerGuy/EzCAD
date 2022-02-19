# EzCAD
EzCAD is in Alpha stage of development and is not nearly finished.

EzCAD is a CAD/MDT intended for FiveM RP style servers.
It is meant to be a largely customizable web
application that can be easily deployed.

---

# Developer Quick Start

_Prerequisties:_
 - [Git](https://git-scm.com/downloads)
 - [Python](https://www.python.org/downloads/)
 - [Angular CLI](https://angular.io/cli/)

In terminal (GitBash for Windows users):
1. `git clone https://github.com/TheScannerGuy/EzCAD.git`
2. `cd EzCAD/ezcad-ui`
3. `npm install`
4. `ng build`
5. `cd ~/EzCAD`
6. `pip install -r requirements.txt`
7. Now create a file called `.env` in the EzCAD directory
8. Enter keys for `SECRET_KEY` and `DISCORD_CLIENT_SECRET`

Your `EzCAD/.env` file should look like this
```
# Flask Secret Key
SECRET_KEY = "bits representing secret key"

# Discord Secret Key
DISCORD_CLIENT_SECRET = "discord oauth secret"

# Discord ID of Admin
ADMIN_DISCORD_ID = 123456789101112131415
```

Get your DISCORD_CLIENT_SECRET from https://discord.com/developers/applications

8. After that you can start the server by using
`python run.py` in the EzCAD directory
