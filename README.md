# parrot-app

I have a very annoying parrot which screams almost all day and drives my family crazy. That’s why I decided to develop this app with the hope to  make him be more quiet :)

If he screams continuously a curtain will drop and it will cover the parrot’s cage and a calming music will be played on my mobile phone. After several minutes the curtain will rise up and everything will be back to normal.

A showcase of the result:</br>
![Screenshot](/showcase-pics/curtain-down.gif)            ![Screenshot](/showcase-pics/curtain-up.gif) 


This project consists of several components:
* Raspberry PI zero with Python service for classification of audio sounds
* Step motor
* Mobile Phone which sends the realtime recorded audio to the PI zero and plays calming sounds if the bird is screaming
* Curtain mechanism
- - - -
More detailed and visual  representation of the project:

![Screenshot](/showcase-pics/parrot-app-architecture.png)
