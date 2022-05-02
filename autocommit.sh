#!/bin/bash

git add .

read txtcommt

git commit -m $txtcommt

git push origin main

git status

read txtcommttt
