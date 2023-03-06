
# vs code find: \[(.)\]
# replace __$1__

def scaled_results_v1(problem, theme):
  x = f"""A math word problem is a coherent story that provides the student with good clues to the cor- rect mathematical operations between the numerical quantities described therein. However, the particular theme of a problem, whether it be about collecting apples or traveling distances through space, can vary significantly so long as the correlation between the story and underlying equation is maintained.


Here are some examples:
------------------------
Original Problem: 
Jim walked ___A___ of a mile from school to David’s house and ___B___ of a mile from David’s house to his own house. How many miles did Jim walk in all?

New theme - Star Wars:
==Very Good==
Uncle Owen walked ___A___ of a mile from his hangar to Luke Skywalker’s room and ___B___ of a mile from Luke Sky- walker’s room to his own room. How many miles did Uncle Owen walk in all?
==Very Good==
Darth Vader flew ___A___ of a mile from his planet to Senator Palpatine’s base and ___B___ of a mile from Senator Palpatine’s base to his own. How many miles did Darth Vader fly in all?
==Good==
Uncle Owen walked ___A___ miles from his hangar to Luke Skywalker’s room and ___B___ miles from Luke Sky- walker’s room to his own room. How many miles did Uncle Owen walk in all?
==Bad==
Darth Vader flew ___A___ of a mile from his planet to Senator Palpatine’s base and ___B___ of a mile from Senator Palpatine’s base to his own. Then he flew ___C___ more miles to fight Anakin. How many miles did Darth Vader fly in all?


New Theme - Western: 
==Very Good==
Duane strolled ___A___ of a mile from his barn to Madeline’s camp and ___B___ of a mile from Madeline’s camp to his own camp. How many miles did Duane stroll in all?
==Very Good==
Cowboy Chris rode ___A___ of a mile from his ranch to Sheriff Steve’s town and ___B___ of a mile from Sherrif Steve’s town to his own. How many miles did Cowboy Chris stroll in all?
==Good==
Duane strolled ___A___ miles from his barn to Madeline’s camp and ___B___ miles from Madeline’s camp to his own camp. How many miles did Duane stroll in all?
==Bad==
Cowboy Chris rode ___A___ of a mile from his ranch to Sheriff Steve’s town and ___B___ of a mile from Sherrif Steve’s town to his own. He then rode ___C___ more miles to wrangle some sheep. How many miles did Cowboy Chris stroll in all?
------------------------
Original Problem:
{problem}

New Theme - {theme}: 
==Very Good==
"""
  return x








