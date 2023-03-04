# -*- coding: utf-8 -*-
"""Hw03.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bROlBrQXsL_QZLuHs7RTyhOsgYzoJ9DU

Algorithm to implement local alignment (Smith-Waterman algorithm) and produce the local alignment
"""

from tabulate import tabulate
def buildSWTable(X, Y, match= 1, mismatch= -1, gap=-1):
  print('sequence 1: ', X)
  print('sequence 2: ', Y)
  m = len(X)
  n = len(Y)
  table = []
  for i in range(m +1):
    sub = []
    for j in range(n +1):
      sub.append(0)
    table.append(sub)
  for j in range(1,n+1):
    table[0][j] = table[0][j-1]
  for i in range(1,m+1):
    table[i][0]= table[i-1][0]
  print('\n',"The initial alignment table is: ", '\n')
  print(tabulate(table))
  for i in range(1,len(X)+1):
    for j in range(1,len(Y)+1):
      if X[i-1] == Y[j-1]:
        case1 = table[i-1][j-1]+ match
      else:
        if table[i-1][j-1] > 0:
          case1 = table[i-1][j-1]+ mismatch
        else:
          case1 = 0          
      case2 = table[i-1][j]+ gap
      case3 = table[i][j-1]+ gap
      table[i][j] = max([case1, case2, case3])
  print('\n',"The final alignment table is: ", '\n')
  return table

X = 'AGATCAGAAATG'
Y = 'ATAGAAT'
buildSWTable(X,Y)



def SWTraceBack(X, Y, match=1, mismatch=-1, gap=-1):
  first = ''        # alignment for X
  second = ''       # alignment for Y
  score = 0  
  print('sequence 1: ', X)
  print('sequence 2: ', Y, '\n')
  table = []
  max_index = []
  for i in range(len(X) +1):
    sub = []
    for j in range(len(Y) +1):
      sub.append(0)
    table.append(sub)
  for j in range(1,len(Y)+1):
    table[0][j] = table[0][j-1]
  for i in range(1,len(X)+1):
    table[i][0]= table[i-1][0]

  for i in range(1,len(X)+1):
    for j in range(1,len(Y)+1):
      if X[i-1] == Y[j-1]:
        case1 = table[i-1][j-1]+ match
      else:
        if table[i-1][j-1] > 0:
          case1 = table[i-1][j-1]+ mismatch
        else:
          case1 = 0          
      case2 = table[i-1][j]+ gap
      if case2 <0:
        case2 = 0
      case3 = table[i][j-1]+ gap
      if case2 <0:
        case2 = 0
      table[i][j] = max([case1, case2, case3])
      max_score = max([case1, case2, case3])
      if max_score >= score:
        max_index.clear()
        score = max_score
        max_index.append(i)
        max_index.append(j)
  print("The final alignment table is: ", '\n')
  print(tabulate(table))
  print("The optimal alignment  score is: ", score, '\n')
  index_col = max_index[1]
  index_row = max_index[0]
  while score>0:
    if X[index_row-1] == Y[index_col-1]:
      case1 = table[index_row-1][index_col-1]+ match
    else:
      case1 = table[index_row-1][index_col-1]+ mismatch         
    case2 = table[index_row-1][index_col]+ gap
    case3 = table[index_row][index_col-1]+ gap
  
    if case1 == table[index_row][index_col]:  
      first += X[index_row-1]
      second += Y[index_col-1]
      score = table[index_row-1][index_col-1]
      index_row -=1
      index_col -=1

    elif case2 == table[index_row][index_col]:
      first += X[index_row-1]
      second += '-'
      score = table[index_row-1][index_col]
      index_row -=1
    elif case3 == table[index_row][index_col]:
      first += '-'
      second += Y[index_col-1]
      score = table[index_row][index_col-1]
      index_col -=1
    
  first = first[::-1]
  second = second[::-1]
  return first,second

X = 'AGATCAGAAATG'
Y = 'ATAGAAT'
seq1,seq2 = SWTraceBack(X,Y)
print('The best alignment is: ')
print(*seq1)
print(*seq2)

"""Multiple Sequence Alignment"""

from tabulate import tabulate
def construct_MSA(Sequence, match=1, mismatch=-1, gap=-2):
  table = []
  for i in range(len(Sequence)):
    sub = []
    for j in range(len(Sequence)):
      sub.append(0)
    table.append(sub)
  for i in Sequence:
    a= Sequence.index(i)
    for j in Sequence:
      b= Sequence.index(j)
      Seq1 = len(i)
      Seq2 = len(j)
      if Seq1 > Seq2:
        gap_fill = Seq1 -Seq2
        j = j + gap_fill * ' '
      elif Seq2 > Seq1:
        gap_fill = Seq2 - Seq1
        i = i + gap_fill * ' '
      
      Score = 0
      for k in range(len(i)):
        if i[k] == j[k]:
          Score += match
        elif i[k] != j[k] and i[k] != ' ' and j[k] != ' ':
          Score += mismatch
        else:
          Score += gap
      table[a][b] = Score
      if i == j:
        table[a][b]= 0
  print('Standard Alignment Score Matrix: ')
  print(tabulate(table))
#summing the rows to select the sequence with best score
  Row_sum = []
  for i in table:
    Row_sum.append(sum(i))
  best_seq = Sequence[Row_sum.index(max(Row_sum))]
  #print(best_seq)
  seq_copy = Sequence.copy()       
  seq_copy.remove(best_seq)
  g_align = []
  for i in seq_copy:
    g_align.append(NWTraceBack(best_seq,i))               # using Traceback function from previous home work

  #print(tabulate(g_align))

  bestSeq_len = []
  for i in range(len(g_align)):
    bestSeq_len.append(len(g_align[i][0]))

  Maxlength_index = bestSeq_len.index(max(bestSeq_len))

  Maxlength_seq = g_align[Maxlength_index][0]

  MSA = []
  MSA.append(Maxlength_seq)


  temp = []
  final_align = 0
  for i in range(len(g_align)):
    for j in range(len(Maxlength_seq)):
      if final_align == len(g_align[i][0]):
        temp.append('-')
      elif Maxlength_seq[j] != g_align[i][0][final_align]:
        temp.append('-')
      elif Maxlength_seq[j] == g_align[i][0][final_align]:
        if final_align < len(g_align[i][0]):
          temp.append(g_align[i][1][final_align])
          final_align += 1

    MSA.append(temp)
    final_align = 0
    temp =[]

  print('Optimal Multiple Sequence Alignment:')
  print(tabulate(MSA))
  
  return best_seq

Sequence = ['CATTT','ATTTA','ATTG','GCATA']
construct_MSA(Sequence)
#print(out)

def NWTraceBack(X, Y, match=1, mismatch=-1, gap=-1):
  first = []        # alignment for X
  second = []       # alignment for Y
  score = 0
  m = len(X)
  n = len(Y)
  table = []
  for i in range(m +1):
    sub = []
    for j in range(n +1):
      sub.append(0)
    table.append(sub)
  for j in range(n+1):
    table[0][j] = table[0][j]+ mismatch * j
  for i in range(m+1):
    table[i][0]= table[i][0] +mismatch * i
  for i in range(1,len(X)+1):
    for j in range(1,len(Y)+1):
      if X[i-1] == Y[j-1]:
        case1 = table[i-1][j-1]+ match
      else:
        case1 = table[i-1][j-1]+ mismatch
      case2 = table[i-1][j]+ gap
      case3 = table[i][j-1]+ gap
      table[i][j] = max([case1, case2, case3])
  
  col_start = len(Y)
  row_start = len(X)
  while col_start>0 or row_start>0:
    if X[row_start-1] == Y[col_start-1]:
      case1 = table[row_start-1][col_start-1]+ match
    else:
      case1 = table[row_start-1][col_start-1]+ mismatch
    case2 = table[row_start-1][col_start]+ gap
    case3 = table[row_start][col_start-1]+ gap
    if case1 == table[row_start][col_start]:
      first.insert(0,X[row_start-1])
      second.insert(0,Y[col_start-1])
      row_start -=1
      col_start -=1

    elif case2 == table[row_start][col_start]:
      first.insert(0,X[row_start-1])
      second.insert(0,'-')
      row_start -=1
    elif case3 == table[row_start][col_start]:
      first.insert(0,'-')
      second.insert(0,Y[col_start-1])
      col_start -=1
  #first = first[::-1]
  #second = second[::-1]
  for i in range(len(first)):
    if first[i] == second[i]:
      score += match
    elif first[i] != second[i]:
      score += mismatch
    elif first[i] == '-' or second[i] == '-':
      score += gap
  
  return [first,second]


#sequences = ['CATTT','CATT','CTTT','CATT']

#X = 'CGTA'
#Y = 'GTA'
#seq1,seq2 = NWTraceBack(X,Y)
#print('The best alignment is: ')
#print(seq1)
#print(seq2)