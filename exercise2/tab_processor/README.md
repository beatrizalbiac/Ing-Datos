# Exercise 2 - Exercise 2 – Processing of music data
*By Beatriz Albiac*

## Issues to fix:
1. Modify the get_songs in ‘songs.py’ file to use the catalog instead of scrapping again
2. Check the logs for something strange. Try to know where those messages come from. No need to solve it, only get the origin:

The only weird this apparent is the following(e.g):

2025-11-24 22:44:10 INFO     File ./files\songs\l\loquillo\cadillac_solitario.txt already exists. Skipping download.
2025-11-24 22:44:10 INFO     Skipping download for existing file: ./files/songs/l/loquillo/cadillac_solitario.txt

It just says the same thing twice because the "check" of wether a song has already been downloaded is implemented in different places (in scrapper/utils/files.py and on the scrapper.py)

3. The cleaner is getting the catalogs also as inputs. Although it is not a problem for now, we need to avoid it. Implement a solution
4. There is an issue when reading/saving the files as it is creating more directories than needed **NOT IMPLEMENTED**
5. Implement an additional validation rule **NOT IMPLEMENTED**
6. Propose any change to make the code cleaner, clearer and better:

The main thing I can add to what the base code we were given is that it just didn't work for windows. It had problems with the songs and artits's names being in spanish (as it couldn't read "ñ" or "á, é, ect."
It also has issues with reading the directories as the "/" and "\" caused many issues because of windows.

## Funcionalities to add:
1. Add a new Python module called ‘results’ that checks the number of files we have for
each output
2. Add a new python module called ‘lyrics’ that removes all the chords from the
successfully validated files and stores it in the file’s directory *MAINLY WORKS BUT WOULD NEED FURTHER IMPLEMENTATION*
3. Add a new python module called ‘insights’ that merges all OK lyrics into a single text
file for each artist. Count, for each artist, the top 10 words (nouns, verbs, adjectives)
that his lyrics have. Do it also globally, but with the top 20 **NOT IMPLEMENTED**
4. Create a Python file that executes all modules in order. It has to have his own log file,
and make sure that if any of the processes fail, is registered there **NOT IMPLEMENTED**



## Conclusion:
There were many external problems while I was trying to do this project, so there are many things that couldn't be implemented or documented properly, and I apologize for it
