# TwitAPI
A twitter api tool capable of pulling a specific users data, storing it as a json making it easily parseable!
The tool also has a image scraper for a users tweets 

![TwitAPIgui](https://user-images.githubusercontent.com/60188000/192237127-3e3e10a0-278b-496f-9c7d-f1d71647d05a.png)

## Features

- Capable of pulling and storing any number of affiliated users tweets
- Uses pagination to allow pulls bigger than 100 up to the api limits of 3200
- A simple data display capable of sorting and displaying a specific users tweets and their data
- Data storage in json makes parsing and storing multiple datapoints easy


## Installation

- clone the repo or download the zip
- apply for twitter api dev to get access to bearer token
- unpack/run the script
## Roadmap

- Better threading
- Long run scripts for periodic fetching
- Replacing json with databases
- more dataframe display and sorting options
## Lessons Learned

This project, as long and arduous as it was taught me a lot about both basic and advanced things related to python

- pyqt is a nice way to do a GUI if you HAVE to make one using python, but i wouldnt recommend it
    - programming the gui line by line, and using its threading functions is difficult in comparison to my experience with c#
    - if i were to re do the project i wouldnt make a GUI at all, and would rather make it run in commandline

- I learned the indepth details of how jsons are actually formatted, and having to deal with multiple fields of nested arrays and datapoints taught me the importance of having to format my own jsons in the future better

- Learned more about how i should file format my own programs, dividing parts into multiple files that have specific functionalities
## Feedback

If you have any feedback, you can reach out to me at snutri.dev@gmail.com

