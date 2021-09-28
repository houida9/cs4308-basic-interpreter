10 REM compute the sum of even numbers from 2 to 20 with GOTO loop

20 TEXT : HOME : PR#0

30 LET N=2

40 LET S = S + N

50 PRINT N,S

60 LET N = N + 2

70 IF N <= 20 THEN GOTO 40

80 PRINT : REM print empty line

90 PRINT "Final sum:";S

100 END