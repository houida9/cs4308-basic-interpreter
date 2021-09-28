05 REM input a number, output its binary representation

10 HOME

20 TEXT : PR#3

30 LET X = 0

40 LET P = 1

50 INPUT "Enter an integer greater or equal than zero: ";A

60 IF (A < 0 OR A<>INT(A)) THEN GOTO 50

70 LET B = A - INT (A/2) * 2

80 REM PRINT B

90 LET X = B * P + X

100 LET P = P * 10

110 LET A = (A - B) / 2

120 IF (A > 0) THEN GOTO 70

130 PRINT "As binary: ";X

140 END