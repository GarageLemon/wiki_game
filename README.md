Wiki Parser Game
===
Implementation of 6 transitions game in Wiki, using async methods
---
To start the program you need to type in your terminal in the same directory as project:

`python3.11 main.py`

You can also define number of link chunks that going to be parsed in one cycle by typing number after 'main.py'.
For example:

`python3.11 main.py 100`

If number is not passed, then default value is going to be 50.

Then you need to type start url/article and end url/article of Wiki page.
Program going to parse through start article, find all links in it, and parse them recursively for next group of links.

If program not find end article in 6 attempts, then it goint to finish without results.

However, if it find the end article, program going to print a tree-like structure that covers the whole path to end article.