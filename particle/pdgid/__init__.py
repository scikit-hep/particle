# Copyright (c) 2018-2019, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

r"""
The Particle Data Group (PDG) defines the standard particle identification numbering scheme
in the form of a signed 7-digit number +/- N Nr Nl Nq1 Nq2 Nq3 Nj.

PDG IDs with more than 7 digits exist for non-standard particles such as Q-balls.

This module provides the following:

- A pythonic version of the functions defined in HepPID and HepPDT,
  which work with PDG particle identification codes (PDG IDs).
- A handy `PDGID` class.
- A few other functions extending the functionality of the HepXXX code.


Matrix of spin states for mesons
--------------------------------

The table below provides a handy overview of the "links" between PDG IDs
and meson quantum numbers. It is provided here for reference (for lack of a better place!),
as it is not at all easy to find ... not to say impossible.

Useful definitions:

- State: (2S+1)^L_J
- Parity P = (-1)^(L+1)
- Charge conjugation C = (-1)^(L+S), valid only for neutral mesons
- "q q" stands for "nq2 nq3" in the table below

==== === === ======================== ======== ================= ====================== =======================
 J    S   L   State                    J^PC     Name              Mesons                 PDG nL nq1 nq2 nq3 nJ
---- --- --- ------------------------ -------- ----------------- ---------------------- -----------------------
 0    0   0   L=J   , S=0  (1^S_0)     0^-+     pseudo-scalar     pi  eta  eta'  K        00qq1
 0    1   \-  L=J-1 , S=1              \-       \-                \-                      \-
 0    1   \-  L=J   , S=1              \-       \-                \-                      \-
 0    1   1   L=J+1 , S=1  (3^P_0)     0^++     scalar            a_0  f_0  f'_0  K*_0    10qq1
 1    0   1   L=J   , S=0  (1^P_1)     1^+-     pseudo-vector     b_1  h_1  h'_1  K_1     10qq3
 1    1   0   L=J-1 , S=1  (3^S_1)     1^--     vector            rho  omega  phi  K*     00qq3
 1    1   1   L=J   , S=1  (3^P_1)     1^++     axial vector      a_1  f_1  f'_1  K_1     20qq3
 1    1   2   L=J+1 , S=1              1^--     \-                                        30qq3
 2    0   2   L=J   , S=0              2^-+     \-                                        10qq5
 2    1   1   L=J-1 , S=1              2^++     \-                                        00qq5
 2    1   2   L=J   , S=1              2^--     \-                                        20qq5
 2    1   3   L=J+1 , S=1  (3^P_2)     2^++     vector            a_2  f_2  f'_2  K*_2    30qq5
 3    0   3   L=J   , S=0              3^+-     \-                                        10qq7
 3    1   2   L=J-1 , S=1              3^--     \-                                        00qq7
 3    1   3   L=J   , S=1              3^++     \-                                        20qq7
 3    1   4   L=J+1 , S=1              3^--     \-                                        30qq7
 4    0   4   L=J   , S=0              4^-+     \-                                        10qq9
 4    1   3   L=J-1 , S=1              4^++     \-                                        00qq9
 4    1   4   L=J   , S=1              4^--     \-                                        20qq9
 4    1   5   L=J+1 , S=1              4^++     \-                                        30qq9
==== === === ======================== ======== ================= ====================== =======================

References
----------

HepPDT and HepPID versions 3.04.01: http://lcgapp.cern.ch/project/simu/HepPDT/
"""

from __future__ import absolute_import

from .functions import is_valid
from .functions import abspid

from .functions import is_lepton
from .functions import is_hadron
from .functions import is_meson
from .functions import is_baryon
from .functions import is_diquark
from .functions import is_nucleus
from .functions import is_pentaquark
from .functions import is_Rhadron
from .functions import is_Qball
from .functions import is_dyon
from .functions import is_SUSY

from .functions import has_down
from .functions import has_up
from .functions import has_strange
from .functions import has_charm
from .functions import has_bottom
from .functions import has_top
from .functions import has_fundamental_anti

from .functions import charge
from .functions import three_charge
from .functions import j_spin
from .functions import J
from .functions import s_spin
from .functions import S
from .functions import l_spin
from .functions import L
from .functions import P
from .functions import C
from .functions import A
from .functions import Z

from .pdgid import PDGID


__all__ = ('is_valid',
           'abspid',
           #
           'is_lepton',
           'is_hadron',
           'is_meson',
           'is_baryon',
           'is_diquark',
           'is_nucleus',
           'is_pentaquark',
           'is_Rhadron',
           'is_Qball',
           'is_dyon',
           'is_SUSY',
           #
           'has_down',
           'has_up',
           'has_strange',
           'has_charm',
           'has_bottom',
           'has_top',
           'has_fundamental_anti',
           #
           'charge',
           'three_charge',
           'j_spin',
           'J',
           's_spin',
           'S',
           'l_spin',
           'L',
           'A',
           'Z'
           )
