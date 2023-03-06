import prompts
import sub
from main import *


problem = input("Input a problem:")
themes = input("Input comma separated themes:")

subbed_problem, nums = sub.problem_to_generic(problem)
for theme in themes.split(','):
  print(f'===== {theme} =======')
  prompt = prompts.scaled_results_v1(subbed_problem, theme)

  # response = openai.Completion.create(model="text-davinci-003", prompt="Say this is a test", temperature=0, max_tokens=7)
  # print(response)


  request = Request(model="openai/text-davinci-003", prompt=prompt, echo_prompt=False)
  request_result: RequestResult = service.make_request(auth, request)
  result = request_result.completions[0].text
  result = result[:result.find("==")]


  print('rewritten for theme: ', theme, '\n')
  print(sub.generic_to_problem(result, nums))