: this sets the working dir as the dir this file is located in
SET mypath=%~dp0
cd %mypath:~0,-1%

python selfmoji.py
