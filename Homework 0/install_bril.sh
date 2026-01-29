#!/bin/bash

# TODO: Add the commands to install the Bril environment tools.
# Make sure your script installs Deno, Flit, and the Bril tools.
# Ensure the script works on any machine and sets up the PATH correctly.

curl -fsSL https://deno.land/install.sh | sh

#python3 -m venv .venv

export PATH="$PATH:$HOME/.deno/bin"

deno install bril/brili.ts

deno install --allow-env --allow-read bril/ts2bril.ts

deno install --allow-env --allow-read bril/brilck.ts

#source .venv/bin/activate

pip install --user flit

cd bril/bril-txt

flit install --symlink --user

cd ../..

pip install --user turnt

#deactivate

