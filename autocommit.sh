#!/bin/bash

git add .

read varname

git commit -m '$varname'

git push origin main

git status


