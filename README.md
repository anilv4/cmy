# cmy: c-mee

cmy (clear mind YAML) pronounced as c-mee is a simple daily log keeper, powered by python. Logs are stored in YAML format. 

# Background
I was looking for a simple daily log keeper + simple todo that can record a small text with minimal steps. I.e. I should be able to record a small text with just one step with minimal interruption to my work. The tool has to store all the associated metadata automatically like time, date, & type so that I can quickly identify the context. 

# How to install?
For efficient use cmy needs some alias to be created. Unfortunately the aliases are not working as expectd when adding entries. I was able to workaround the problem using wraparound shell scripts. But it looks dirty. Those scripts do not work on zsh also. Thanks to Riyas (https://twitter.com/riyaas) for finding the bug.

I am in the process of re-writing some parts of the code, to correct this problem.
