projman
=======

This is my first python script. It's not finished and is probably ass backards.

It's a dirty little project management framework for linux web developers. 
It's based almost entirely on a script by Anthony Cargile(.com) that 
clones and configures webservers from git repos. This script is an attempt 
to modularize this functionality so we can build out a more complete solution. 

notes
=====

little shell script using inotify to run my script on folder modification,
this, tmux and vim is a decent IDE.

while true; do   
    change=$(inotifywait -e close_write,moved_to,create .)
    changes=${change#./ * }  
    if [ "$change" = "newproj" ]; clear && then python ./newproj WebPageTest; fi 
done 

