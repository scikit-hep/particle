import re

getname = re.compile(r'''
^                                           # Beginning of string
      (?P<name>       \w+?        )         # One or more characters, non-greedy
(?:\( (?P<family>    [udsctb][\w]*) \) )?   # Optional family like (s)
(?:\( (?P<state>      \d+         ) \)      # Optional state in ()
      (?=             \*? \(      )  )?     #   - lookahead for mass
      (?P<star>       \*          )?        # Optional star
(?:\( (?P<mass>       \d+         ) \) )?   # Optional mass in ()
      (?P<bar>        (bar|~)     )?        # Optional bar
      (?P<charge>     [0\+\-][+-]?)         # Required 0, -, --, or +, ++
$                                           # End of string
''', re.VERBOSE)

getdec = re.compile(r'''
^                                           # Beginning of string
      (?P<bar>        (anti-)     )?        # Optional anti-
      (?P<name>       [a-zA-Z]+?  )         # One or more characters, non-greedy
      (?P<prime>      '*          )         # Optional prime(s)
(?: _ (?P<state>      \d+         )    )?   # Optional state in ()
(?:   (?P<family>     _[udsctb][\w]*)  )?   # Optional family like (s)
(?:\( (?P<mass>       \d+         ) \) )?   # Optional mass in ()
      (?P<star>       \*?         )         # Optional star
      (?P<charge>     [0\+\-][+-]?)         # Required 0, -, --, or +, ++
$                                           # End of string
''', re.VERBOSE)
