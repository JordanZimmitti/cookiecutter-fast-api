#!/bin/sh

git init
git add .
git branch -M main
sh scripts/setup.sh
git add .
git commit -m "Initial commit"
