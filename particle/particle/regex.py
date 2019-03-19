# Copyright (c) 2018-2019, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

"""
Collection of regular expression helper utilities for the ``Particle`` class.
"""

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


# Help manipulating .dec DecFile style names
getdec = re.compile(r'''
^                                           # Beginning of string
      (?P<bar>        (anti-)     )?        # Optional anti-
      (?P<name>       [a-zA-Z]+?  )         # One or more characters, non-greedy
      (?P<prime>      '*          )         # Optional prime(s)
(?: _ (?P<state>      \d+         )    )?   # Optional state in ()
(?:   (?P<family>     _[udsctbemna][\w]*) )?# Optional family like (s)
(?:\( (?P<mass>       \d+         ) \) )?   # Optional mass in ()
      (?P<star>       \*?         )         # Optional star
      (?P<charge>     [0\+\-][+-]?)?        # Optional 0, -, --, or +, ++
$                                           # End of string
''', re.VERBOSE)
