import json

import openai

from helm.common.authentication import Authentication
from helm.common.request import Request, RequestResult
from helm.proxy.services.remote_service import RemoteService

import problems
import prompts
import sub
import constraints

# An example of how to use the request API.
helm_key = open('apikeys.txt').readlines()[0].strip()
open_api_key = open('apikeys.txt').readlines()[1].strip()

openai.api_key = open_api_key
auth = Authentication(api_key=helm_key)
service = RemoteService("https://crfm-models.stanford.edu")

problems = json.load(open('problems.json'))
themes = ["sports", "cats", "unicorns", "art"]

def rewrite_and_revise(original_problem, theme, token_fn = prompts.token_v1, prompt_fn = prompts.scaled_results_v1, revise_yes_no_fn = prompts.yes_no_critique_v1, revise_fn = prompts.revision_critique_v1 , **kwargs):
  rewrite_prompt = prompt_fn(original_problem, theme, token=token_fn)
  request = Request(model="openai/text-davinci-003", prompt=rewrite_prompt, echo_prompt=False, temperature=.3)
  request_result: RequestResult = service.make_request(auth, request)
  result = request_result.completions[0].text
  rewritten_problem = result[:result.find("==")]

  critique_prompt = revise_yes_no_fn(original_problem, rewritten_problem, theme, token=token_fn)
  request = Request(model="openai/text-davinci-003", prompt=critique_prompt, echo_prompt=False)
  request_result: RequestResult = service.make_request(auth, request)
  result = request_result.completions[0].text
  critique = result[:result.find("==")]

  if not critique.lower().startswith('y'):
    print('no critique', critique)
    return rewritten_problem
  print('got critique!', rewritten_problem, critique)
  revise_prompt = revise_fn(original_problem, rewritten_problem, theme, critique, token=token_fn)
  request = Request(model="openai/text-davinci-003", prompt=revise_prompt, echo_prompt=False)
  request_result: RequestResult = service.make_request(auth, request)
  result = request_result.completions[0].text
  revision = result[:min(result.find("END"), result.find('----'))]
  return revision


def one_off(problem, theme):
  subbed_problem, nums = sub.problem_to_generic(problem)
  # prompt = prompts.scaled_results_v1(subbed_problem, theme)

  # print(subbed_problem, nums)

  # request = Request(model="openai/text-davinci-003", prompt=prompt, echo_prompt=False)
  # request_result: RequestResult = service.make_request(auth, request)
  # result = request_result.completions[0].text
  # result = 
  
  result = rewrite_and_revise(subbed_problem, theme)
  print(sub.generic_to_problem(result, nums))
  return result

def demo():
  question = {
    "question": "There were 28 bales of hay in the barn. Tim stacked more bales in the barn today. There are now 54 bales of hay in the barn. How many bales did he store in the barn ?",
    "generic": "There were ___A___ bales of hay in the barn. Tim stacked more bales in the barn today. There are now ___B___ bales of hay in the barn. How many bales did he store in the barn ?",
    "numbers": [
      28,
      54
    ],
    "constraints": "A=randint(20,40)\nB=randint(40,50)\nanswer= B - A",
    "lEquations": [
      "28+x=54"
    ],
    "lSolutions": [
      26.0
    ],
    "grammarCheck": 0,
    "templateNumber": 0,
    "sQuestion": "There were 28 bales of hay in the barn. Tim stacked more bales in the barn today. There are now 54 bales of hay in the barn. How many bales did he store in the barn ?",
    "iIndex": 1
  }

  print('original question:', question['question'])
  print('generic question', question['generic'])
  print('constraints:', question['constraints'])

  for theme in themes:
    print('\nNew theme:', theme)
    nums = constraints.parse_constraints(question['constraints'])
    print('Evaluated constraints:', nums)
    request = Request(model="openai/text-davinci-003", prompt=prompts.scaled_results_v1(question['generic'], theme), echo_prompt=False)
    request_result: RequestResult = service.make_request(auth, request)
    result = request_result.completions[0].text
    result = result[:result.find("==")]
    print('Rewritten problem:', sub.generic_to_problem(result, list(nums.values())))


def batch(question_file, k, themes):
  with open(question_file) as f:
    questions = json.load(f)
    for key, problem in list(questions.items())[:k]:
        
        print('original problem', '\n')
        print(problem['question'])
        for theme in themes:
          print(f'===== {key} - {theme} =======')
          prompt = prompts.scaled_results_v1(problem['generic'], theme)

          # response = openai.Completion.create(model="text-davinci-003", prompt="Say this is a test", temperature=0, max_tokens=7)
          # print(response)

          request = Request(model="openai/text-davinci-003", prompt=prompt, echo_prompt=False)
          request_result: RequestResult = service.make_request(auth, request)
          result = request_result.completions[0].text
          result = result[:result.find("==")]

          print('rewritten for theme: ', theme, '\n')
          print(sub.generic_to_problem(result, problem['numbers']))
  
if __name__ == '__main__':
  # batch('questions_with_generics_50.json', 5, themes)
  # demo()
  for theme in themes + ['baseball']:
    # problem = "Sam went to 14 football games this year. He went to 29 games  last year. How many football games did Sam go to in all?"
    problem= """The table below show the points Janet scored on a video game each time she played.
Game # | Points Scored
1 | 155
2 | 150
3 | 180
After the first 3 games, she took a break and came back the next day and scored 2 times as many points as she had during all the previous games combined. How many more points did she score after her break?
"""
    x = one_off(problem, theme)
    
    # intro_prompt = prompts.write_intro_v1(x)
    intro_prompt = prompts.write_intro_v2(x)
    request = Request(model="openai/text-davinci-003", prompt=intro_prompt, echo_prompt=False)
    request_result: RequestResult = service.make_request(auth, request)
    intro = request_result.completions[0].text
    intro = intro[:intro.find('\n')]
    print(problem)    
    print(intro)
    print(x)