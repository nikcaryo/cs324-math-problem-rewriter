import re
import json

numeric_const_pattern = '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
rx = re.compile(numeric_const_pattern, re.VERBOSE)

TOKEN_DELIM = "--" # default prompts.token_v1
token_pattern = fr'{TOKEN_DELIM}.*{TOKEN_DELIM}'
rx2 = re.compile(token_pattern, re.VERBOSE)


def get_floats(str_val):
  return rx.findall(str_val)

def problem_to_generic(s):
  count = 0
  lines = []
  nums = []
  
  for line in s.split('\n'):
    result = []
    for word in line.split():
      floats = get_floats("".join(filter(lambda x: x != ',', word)))
      if floats:
        assert(len(floats) == 1)
        result.append(rx.sub(f"{TOKEN_DELIM}{chr(ord('A') + count)}{TOKEN_DELIM}", word))
        try:
          nums.append(int(floats[0]))
        except:
          nums.append(float(floats[0]))
        count += 1
      else:
        result.append(word)
    lines.append(" ".join(result))
  return "\n".join(lines), nums

def generic_to_problem(s, args):
  count = 0
  lines = []
  for line in s.split('\n'):
    result = []
    for word in line.split():
      if rx2.findall(word):
        result.append(rx2.sub(str(args[count]), word))
        count += 1
      else:
        result.append(word)
    lines.append(" ".join(result))

  return "\n".join(lines)


if __name__ == "__main__":
  new_questions = {}
  with open('TACL2015/questions.json') as f:
    questions = json.load(f)
    for question in questions:
      generic, numbers = problem_to_generic(question['sQuestion'])
      new_questions[question['iIndex']] = {
        'question': question['sQuestion'],
        'generic': generic,
        'numbers': numbers,
        **question
      }
  with open('questions_with_generics.json', 'w') as f:
    json.dump(new_questions, f, indent=2)

  # all numbers replaced with generics
  for k, question in new_questions.items():
    assert(len("".join(filter(lambda x: x.isdigit(), question['generic']))) == 0)
      
