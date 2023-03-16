
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
==Good==
Uncle Owen walked {token('A')} of a mile from his hangar to Luke Skywalker’s room and {token('B')} of a mile from Luke Sky- walker’s room to his own room. How many miles did Uncle Owen walk in all?
==Good==
Darth Vader flew {token('A')} of a mile from his planet to Senator Palpatine’s base and {token('B')} of a mile from Senator Palpatine’s base to his own. How many miles did Darth Vader fly in all?
==Bad==
Darth Vader flew {token('A')} of a mile from his planet to Senator Palpatine’s base and {token('B')} of a mile from Senator Palpatine’s base to his own. Then he flew {token('C')} more miles to fight Anakin. How many miles did Darth Vader fly in all?

New Theme - Western: 
==Good==
Duane strolled {token('A')} of a mile from his barn to Madeline’s camp and {token('B')} of a mile from Madeline’s camp to his own camp. How many miles did Duane stroll in all?
==Good==
Cowboy Chris rode {token('A')} of a mile from his ranch to Sheriff Sarah’s town and {token('B')} of a mile from Sherrif Sarah’s town to his own. How many miles did Cowboy Chris stroll in all?
==Bad==
Cowboy Chris rode {token('A')} of a mile from his ranch to Sheriff Sarah’s town and {token('B')} of a mile from Sherrif Sarah’s town to his own. He then rode {token('C')} more miles to wrangle some sheep. How many miles did Cowboy Chris stroll in all?
------------------------
Original Problem:
{problem}

New Theme - {theme}: 
==Good==
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
  x = f"""Write a creative and interesting introduction to each math problem. Do not include any numbers or math concepts in the intro (e.g. ').
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
The three best friends, Alyssa, Sandy, and Sally, were planning a surprise birthday party for their other best friend, Bella. They wanted to make sure the decorations were perfect, especially the balloons.  They were all so excited to blow them up and decorate the room with them. However, before they could start decorating, they had to figure out how many blue balloons they had in total.

Intro (bad):
The three best friends, Alyssa, Sandy, and Sally, were planning a surprise birthday party for their other best friend, Bella. They wanted to make sure the decorations were perfect, especially the balloons.  They were all so excited to blow them up and decorate the room with them. However, before they could start decorating, they had to figure out how many blue balloons they had in total. Alyssa brought {token('A')} blue balloons, Sandy brought {token('B')} blue balloons, and Sally brought {token('C')} blue balloons.
_____
Problem:
{problem}

Intro (good):
"""
  return x  

import re
from sub import TOKEN_DELIM
token_pattern = fr'{TOKEN_DELIM}.*{TOKEN_DELIM}'
rx2 = re.compile(token_pattern, re.VERBOSE)

def intro_check_for_numbers_v1(intro):
  results = rx2.findall(intro)
  if not results:
    return None
  
  tokens = []
  for word in intro.split():
    if rx2.findall(word):
      tokens.append(rx2.findall(word)[0])

  x = f"""Please rewrite the following intro to not include the following symbols:  --A--, --G--
Intro:
John loved playing various video games and one of his favorites was unicorn racing. He was determined to get better and better each time he played. As he improved, his score climbed higher and higher. After the first --G-- games, he decided to take a break. Little did he know that, when he came back the next day, his score would skyrocket by --A-- points!
Rewritten:
John enjoys playing video games, particularly unicorn racing, and he wants to improve his performance every time he plays. After playing some games, he decided to take a break. When he resumed playing the next day, his score significantly increased.
----
Please rewrite the following intro to not include the following symbols:  --A--, --B--, --C--
Intro:
Sandy, Benny, and Tim were all avid cat lovers, and their homes were full of furry friends. Sandy had --A-- cats, Benny had --B-- cats, and Tim had --C-- cats. They all wanted to figure out how many cats they had together, so they decided to add up the numbers.
Rewritten:
Sandy, Benny, and Tim were all avid cat lovers, and their homes were full of furry friends. They all wanted to figure out how many cats they had together, so they decided to add up the numbers.

Please rewrite the following intro to not include the following symbols: {", ".join(set(tokens))}

Intro:
{intro}

Rewritten:
"""
  return x

z = """
Duane was a cowboy who lived on a sprawling ranch in the heart of the Wild West. One day, he decided to visit his friend Madeline, who had set up camp --A-- of a mile away. As he walked, he couldn't help but admire the beauty of the open range and the majestic mountains looming in the distance.

"""

def combine_intro_and_prompt(intro, problem, token=token_v1):
  x = f"""Combine the intro and problem so that the two flow together nicely. Make as little changes as possible.

Intro:
John, Sarah, and Steve were all running for office in the same district. As politicians, they knew it was their job to represent their constituents to the best of their abilities. So, they each went out and campaigned rigorously to spread their message. In the end, they all won their respective seats. Now, they wanted to figure out how many constituents they had in total.
Problem:
John, Sarah, and Stever are all politicians. John has {token('A')} constituents, Sarah has {token('B')} constituents, and Steve has {token('C')} constituents. How many constituents do they have together?
Combined:
John, Sarah, and Steve were all running for office in the same district. As politicians, they knew it was their job to represent their constituents to the best of their abilities. So, they each went out and campaigned rigorously to spread their message. In the end, they all won their respective seats. Now, they wanted to figure out how many constituents they had in total. John has 10 constituents, Sarah has 20 constituents, and Steve has 34 constituents. How many constituents do they have together?
---
Intro:
{intro}
Problem:
{problem}
Combined:
"""
  return x

# print(intro_check_for_numbers_v1(z)) # Duane was a cowboy who lived on a sprawling ranch in the heart of the Wild West. One day, he decided to visit his friend Madeline, who had set up camp a certain distance away. As he walked, he couldn't help but admire the beauty of the open range and the majestic mountains looming in the distance.
# Intro (good):
# John loved playing various video games and one of his favorites was unicorn racing. He was determined to get better and better each time he played. As he improved, his score climbed higher and higher. After the first ___G___ games, he decided to take a break. Little did he know that, when he came back the next day, his score would skyrocket! Can you help him figure out how many more points he scored after his break?

# Please rewrite that to not include ___G___.