
import sub

# by default, align with whatever sub.py uses
def token_v1(s, token_delim=sub.TOKEN_DELIM):
  return f"{token_delim}{s}{token_delim}"

def scaled_results_v1(problem, theme, token = token_v1):
  x = f"""A math word problem is a coherent story that provides the student with good clues to the cor- rect mathematical operations between the numerical quantities described therein. However, the particular theme of a problem, whether it be about collecting apples or traveling distances through space, can vary significantly so long as the correlation between the story and underlying equation is maintained.

Here are some examples:
------------------------
Original Problem: 
Jim walked {token('A')} of a mile from school to David’s house and {token('B')} of a mile from David’s house to his own house. How many miles did Jim walk in all?

New theme - Star Wars:
==Very Good==
Uncle Owen walked {token('A')} of a mile from his hangar to Luke Skywalker’s room and {token('B')} of a mile from Luke Sky- walker’s room to his own room. How many miles did Uncle Owen walk in all?
==Very Good==
Darth Vader flew {token('A')} of a mile from his planet to Senator Palpatine’s base and {token('B')} of a mile from Senator Palpatine’s base to his own. How many miles did Darth Vader fly in all?
==Good==
Uncle Owen walked {token('A')} miles from his hangar to Luke Skywalker’s room and {token('B')} miles from Luke Sky- walker’s room to his own room. How many miles did Uncle Owen walk in all?
==Bad==
Darth Vader flew {token('A')} of a mile from his planet to Senator Palpatine’s base and {token('B')} of a mile from Senator Palpatine’s base to his own. Then he flew {token('C')} more miles to fight Anakin. How many miles did Darth Vader fly in all?

New Theme - Western: 
==Very Good==
Duane strolled {token('A')} of a mile from his barn to Madeline’s camp and {token('B')} of a mile from Madeline’s camp to his own camp. How many miles did Duane stroll in all?
==Very Good==
Cowboy Chris rode {token('A')} of a mile from his ranch to Sheriff Steve’s town and {token('B')} of a mile from Sherrif Steve’s town to his own. How many miles did Cowboy Chris stroll in all?
==Good==
Duane strolled {token('A')} miles from his barn to Madeline’s camp and {token('B')} miles from Madeline’s camp to his own camp. How many miles did Duane stroll in all?
==Bad==
Cowboy Chris rode {token('A')} of a mile from his ranch to Sheriff Steve’s town and {token('B')} of a mile from Sherrif Steve’s town to his own. He then rode {token('C')} more miles to wrangle some sheep. How many miles did Cowboy Chris stroll in all?
------------------------
Original Problem:
{problem}

New Theme - {theme}: 
==Very Good==
"""
  return x


def yes_no_critique_v1(original_problem, rewritten_problem, theme, token = token_v1):
  x = f"""Human: Can you rewrite this math problem with a western theme?
Duane strolled {token('A')} of a mile from his barn to Madeline’s camp and {token('B')} of a mile from Madeline’s camp to his own camp. How many miles did Duane stroll in all?

Assistant:
Yes, here is the rewritten problem

Traveler Alex journeyed {token('A')} of a mile from their homestead to Sheriff Jamie's town and {token('B')} of a mile from Sheriff Jamie's town to their own homestead. How many miles did Traveler Alex journey in all?

Critique Request:
Evaluate the problem for it’s inclusiveness towards all genders and types of people, and any use of harmful language. If major critiques are found, reply "Yes" followed by the critique. If no major critiques are found, reply "None found":

Critique:
Yes. The problem is not inclusive towards all genders and types of people as it assumes that cowboys are only male. The problem could be made more inclusive by using gender-neutral language such as "rider" instead of "cowboy" or by using a different profession that is not gender-specific. Additionally, the problem could benefit from including a more diverse cast of characters to better represent a range of people.
---------
Human: Can you rewrite this math problem with a unicorn theme?
Joan found {token('A')} seashells on the beach. she gave Sam some of her seashells. She has {token('B')} seashell left. How many seashells did she give to Sam ?

Assistant:
Yes, here is the rewritten problem

Max found {token('A')} magical horns on the meadow. He gave Bethany some of his horns. He has {token('B')} horns left. How many horns did he give to Bethany?

Critique Request:
Evaluate the problem for it’s inclusiveness towards all genders and types of people, and any use of harmful language. If major critiques are found, reply "Yes" followed by the critique. If no major critiques are found, reply "No major critiques":

Critique:
No major critiques.
---------
Human: Can you rewrite this math problem with a {theme} theme?
{original_problem}

Assistant:
Yes, here is the rewritten problem

{rewritten_problem}

Critique Request:
Evaluate the problem for it’s inclusiveness towards all genders and types of people, and any use of harmful language. If major critiques are found, reply "Yes" followed by the critique. If no major critiques are found, reply "No major critiques":

Critique:
"""
  return x

revsion_request_string = "Please rewrite the the problem to address the critique, without changing the underlying math word problem."

def revision_critique_v1(original_problem, rewritten_problem, theme, critique, token = token_v1):
  x = f"""Human: Can you rewrite this math problem with a western theme?
Duane strolled {token('A')} of a mile from his barn to Madeline’s camp and {token('B')} of a mile from Madeline’s camp to his own camp. How many miles did Duane stroll in all?

Assistant:
Yes, here is the rewritten problem

Traveler Alex journeyed {token('A')} of a mile from their homestead to Sheriff Jamie's town and {token('B')} of a mile from Sheriff Jamie's town to their own homestead. How many miles did Traveler Alex journey in all?

Critique Request:
Evaluate the problem for it’s inclusiveness towards all genders and types of people, and any use of harmful language. If major critiques are found, reply "Yes" followed by the critique. If no major critiques are found, reply "None found":

Critique:
Yes. The problem is not inclusive towards all genders and types of people as it assumes that cowboys are only male. The problem could be made more inclusive by using gender-neutral language such as "rider" instead of "cowboy" or by using a different profession that is not gender-specific. Additionally, the problem could benefit from including a more diverse cast of characters to better represent a range of people.

Revision Request:
{revsion_request_string}

Revision:
Traveler Alex journeyed {token('A')} of a mile from their homestead to Sheriff Jamie's town and {token('B')} of a mile from Sheriff Jamie's town to their own homestead. How many miles did Traveler Alex journey in all?
END
---------
Human: Can you rewrite this math problem with a {theme} theme?
{original_problem}

Assistant:
Yes, here is the rewritten problem

{rewritten_problem}

Critique Request:
Evaluate the problem for it’s inclusiveness towards all genders and types of people, and any use of harmful language. If major critiques are found, reply "Yes" followed by the critique. If no major critiques are found, reply "No major critiques":

Critique:
{critique}

Revision Request:
{revsion_request_string}

Revision:
"""
  return x

def scaled_results_v2(problem, theme, gender, token = token_v1):
  x = f"""A math word problem is a coherent story that provides the student with good clues to the cor- rect mathematical operations between the numerical quantities described therein. However, the particular theme of a problem, whether it be about collecting apples or traveling distances through space, can vary significantly so long as the correlation between the story and underlying equation is maintained.


Here are some examples:
------------------------
Original Problem: 
Jim walked {token('A')} of a mile from school to David’s house and {token('B')} of a mile from David’s house to his own house. How many miles did Jim walk in all?

New theme - Star Wars (male):
==Very Good==
Uncle Owen walked {token('A')} of a mile from his hangar to Luke Skywalker’s room and {token('B')} of a mile from Luke Sky- walker’s room to his own room. How many miles did Uncle Owen walk in all?
==Very Good==
Darth Vader flew {token('A')} of a mile from his planet to Senator Palpatine’s base and {token('B')} of a mile from Senator Palpatine’s base to his own. How many miles did Darth Vader fly in all?
==Good==
Uncle Owen walked {token('A')} miles from his hangar to Luke Skywalker’s room and {token('B')} miles from Luke Sky- walker’s room to his own room. How many miles did Uncle Owen walk in all?
==Bad==
Darth Vader flew {token('A')} of a mile from his planet to Senator Palpatine’s base and {token('B')} of a mile from Senator Palpatine’s base to his own. Then he flew {token('C')} more miles to fight Anakin. How many miles did Darth Vader fly in all?

New theme - Star Wars (female):
==Very Good==
Princess Leia walked {token('A')} of a mile from his hangar to Rey’s room and {token('B')} of a mile from Rey’s room to her own room. How many miles did Princess Leia walk in all?
==Very Good==
Ahsoka flew {token('A')} of a mile from her planet to Princess Padme’s base and {token('B')} of a mile from Princess Padme’s base to her own. How many miles did Ahsoka fly in all?
==Good==
Princess Leia walked {token('A')} miles from his hangar to Rey’s room and {token('B')} miles from Rey’s room to her own room. How many miles did Princess Leia walk in all?
==Bad==
Ahsoka flew {token('A')} of a mile from his planet to Princess Padme’s base and {token('B')} of a mile from Princess Padme’s base to her own. Then he flew {token('C')} more miles to fight Anakin. How many miles did Ahsoka fly in all?
------------------------
Original Problem: 
{problem}

New theme - {theme} ({gender}):
==Very Good==
"""
  return x


def write_intro_v1(problem, token=token_v1):
  x = f"""Write a creative and interesting introduction to each math problem.
-----
Problem:
Duane strolled {token('A')} of a mile from his barn to Madeline’s camp and {token('B')} of a mile from Madeline’s camp to his own camp. How many miles did Duane stroll in all?

Intro:
Duane was a cowboy who lived on a sprawling ranch in the heart of the Wild West. One day, he decided to visit his friend Madeline, who had set up camp a short distance away. As he walked, he couldn't help but admire the beauty of the open range and the majestic mountains looming in the distance.
-----
Problem:
Alyssa has {token('A')} blue balloons, Sandy has {token('B')} blue balloons, and Sally has {token('C')} blue balloons. How many blue balloons do they have in all ?

Intro:
The three best friends, Alyssa, Sandy, and Sally, were planning a surprise birthday party for their other best friend, Bella. They wanted to make sure the decorations were perfect, especially the balloons.  They were all so excited to blow them up and decorate the room with them. However, before they could start decorating, they had to figure out how many blue balloons they had in total. Can you help them figure it out?

_____
Problem:
John went to 14 baseball games this year. He went to 29 games last year. How many baseball games did John go to in all?

-----
Problem:
{problem}

Intro:
"""
  return x  

def write_intro_v2(problem, token=token_v1):
  x = f"""Write a creative and interesting introduction to each math problem. Do not include any numbers or math concepts in the intro.
-----
Problem:
Duane strolled {token('A')} of a mile from his barn to Madeline’s camp and {token('B')} of a mile from Madeline’s camp to his own camp. How many miles did Duane stroll in all?

Intro (good):
Duane was a cowboy who lived on a sprawling ranch in the heart of the Wild West. One day, he decided to visit his friend Madeline, who had set up camp a short distance away. As he walked, he couldn't help but admire the beauty of the open range and the majestic mountains looming in the distance.

Intro (bad):
Duane was a cowboy who lived on a sprawling ranch in the heart of the Wild West. One day, he decided to visit his friend Madeline, who had set up camp {token('A')} of a mile away. As he walked, he couldn't help but admire the beauty of the open range and the majestic mountains looming in the distance.
-----
Problem:
Alyssa has {token('A')} blue balloons, Sandy has {token('B')} blue balloons, and Sally has {token('C')} blue balloons. How many blue balloons do they have in all ?

Intro (good):
The three best friends, Alyssa, Sandy, and Sally, were planning a surprise birthday party for their other best friend, Bella. They wanted to make sure the decorations were perfect, especially the balloons.  They were all so excited to blow them up and decorate the room with them. However, before they could start decorating, they had to figure out how many blue balloons they had in total. Can you help them figure it out?

Intro (bad):
The three best friends, Alyssa, Sandy, and Sally, were planning a surprise birthday party for their other best friend, Bella. They wanted to make sure the decorations were perfect, especially the balloons.  They were all so excited to blow them up and decorate the room with them. However, before they could start decorating, they had to figure out how many blue balloons they had in total. Alyssa brought {token('A')} blue balloons, Sandy brought {token('B')} blue balloons, and Sally brought {token('C')} blue balloons. Can you help them figure it out?
_____
Problem:
{problem}

Intro (good):
"""
  return x  