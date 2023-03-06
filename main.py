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


def one_off(problem, theme):
  subbed_problem, nums = sub.problem_to_generic(problem)
  prompt = prompts.scaled_results_v1(subbed_problem, theme)

  print(subbed_problem, nums)

  request = Request(model="openai/text-davinci-003", prompt=prompt, echo_prompt=False)
  request_result: RequestResult = service.make_request(auth, request)
  result = request_result.completions[0].text
  result = result[:result.find("==")]
  print(sub.generic_to_problem(result, nums))
  return re

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
  demo()