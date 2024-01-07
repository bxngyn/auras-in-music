Auras in Music
===================
A flask web application that utilizes user input to randomly output song from Spotify databases. <br>
Live Website: https://bxngyn.pythonanywhere.com/


Usage
-----
Upon arriving at the website, the user will have two options: login or register. With registering, there is currently no requirement implemented on the amount or type of characters a username or password needs. However, the code does restrict multiple duplicate usernames between users of the website and does check if a user tries to register without a valid username / password / confirmation password. In case a user accidentally clicks on login but doesn't have an account yet, there is a button below the form to go directly to the register page instead. This is also the same vice versa. After registering, the user will be brought to the main home screen, which contains three buttons: "aura", "history", and "log out".

"Aura" is the page which contains the main function and purpose of the website. Clicking "aura" will lead the user to a new page which asks them how they are doing, and then presents 4 buttons shortly after: "happy", "sad", "nostalgic", and "just ok". The database which a song is drawn from differs depending on what button the user clicks on. If the user clicks on "happy," the SQL query will draw from the "happyvibe.db" database, which contains 123 songs. If the user clicks on "sad," the SQL query will draw from the "sadhour.db" database, which contains 210 songs. If the user clicks on "nostalgic," the SQL query will draw from the "nostalgicsongs.db" database, which contains 584 songs that were in the top 10 Spotify playlist in each year from 2010-2019. However, the SQL query will only select songs from 2010-2012. If the user clicks on "just ok," the SQL query will draw from the "indiesongs.db" database, which contains 100 songs. After clicking on an emotion button, the website presents a song title and the artist's name, as well as two buttons: "Search on YouTube" and "Go to homepage." If the user clicks "Search on YouTube", a new tab will open that has automatically searched whatever song the website gave out in YouTube. "Go to homepage" will simply lead the user back to the main homepage.

"History" displays a table containing the emotion the user picked, the song that was given to them, the artist, and on what day and time.

"Log out" will log the user out and bring them back to the beginning welcome page.


