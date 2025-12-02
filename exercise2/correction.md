
### Fundamentals of Data Engineering – Exercise 2 Correction
# Student: Beatriz Albiac

---

## Correction Notes

### Issues to solve:

#### (scrapper) Modify get_songs to use catalog (2 points)
- [ ] Points awarded: 2
- [ ] Comments:

#### (scrapper) Check logs for strange messages (0.5 points)
- [ ] Points awarded: 0.4
- [ ] Comments: Good job, there is a 'duplicate' line your log file. But you did not issued the 'Warning' on the logs when loading the catalog.

#### (cleaner) Avoid processing catalogs (0.5 points)
- [ ] Points awarded: 0.5
- [ ] Comments:

#### (Validator) Fix directory creation issue (0.5 points)
- [ ] Points awarded: 0.5
- [ ] Comments:

#### (Validator) Additional validation rule (0.5 points)
- [ ] Points awarded: 0
- [ ] Comments: Not implemented.

#### Code improvements (0.5 points)
- [ ] Points awarded: 0
- [ ] Comments: Though it had problems on his own, it is not a code improvement that makes the code cleaner and better. You should re-state as this: 'The code should handle the directories agnostically os it has no dependence on the infrastructure it is running on'.

### Functionalities to add:

#### 'results' module (0.5 points)
- [ ] Points awarded: 0.1
- [ ] Comments: You provided a python file, but it should have its own directory so we can make dependencies and utilities for it: that is what defines a module, as the other in this exercise do. Also:
- - Your code only prints the results. You are not storing anywhere those results. What if it was a pipeline that needs to be executed daily and you need to track these results to monitor them?
- - You are not logging anything from this module. You could use a log file to both log the execution and the results to keep track.

#### 'lyrics' module (2 points)
- [ ] Points awarded: 1
- [ ] Comments: The lyrics are not being extracted correctly. 
```
algun_dia_moriremos_lyrics.txt 


  unos durmiendo, otros en coche

  unos amando, otros soñando

SIm             MI            (LA / FA#m) x 2
  algún día moriremos de nocheeeeee...eh

```
Anyway, you are storing the files correctly in his own folder. But:
- - You are not logging anything from this module.
- - You should have considered using the variables in tab_cleaner/utils/chords.py.
- - You did not modularized your code. For example 'remove_brackets' function could be placed on an utility file like 'utils/strings.py' as we are doing in other modules.

#### 'insights' module (2 points)
- [ ] Points awarded: 0
- [ ] Comments:

#### Main execution file (1 point)
- [ ] Points awarded: 0
- [ ] Comments:

---

## Total Score: 4.5 / 10 points

## General Comments:
The parts implemented are mainly ok, with lot of room for improvement, but works. You should have worked a bit more on that, the not implemented parts were very eassy and straightfordward. Also the problems with the windows environment were difficult, but you managed to run some of the processes. I think I gave you lot of time to do this exercise and worked on it in class. I think you could have a much better mark if you have worked the parts you didn't.
