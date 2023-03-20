from main import *
x = """Mike bought some toys. He bought marbles for $9.05, a football for $4.95, and spent $6.52 on a baseball. In total, how much did Mike spend on toys?"""

def one_off(problem, theme, constraints_string, helm_key, include_intro=True):
    print(problem)
    subbed_problem, nums = sub.problem_to_generic(problem)
    print(nums)

    # prompt = prompts.scaled_results_v1(subbed_problem, theme)

    # print(subbed_problem, nums)

    # request = Request(model="openai/text-davinci-003", prompt=prompt, echo_prompt=False)
    # request_result: RequestResult = service.make_request(auth, request)
    # result = request_result.completions[0].text
    # result =
    rewritten, critique, revision, intro, combined = rewrite_and_revise(subbed_problem, theme, helm_key, include_intro=include_intro)
    # print(rewritten, critique, revision, intro, combined)

    # num_dict = constraints.parse_constraints(constraints_string, split_char='|')
    rewritten = sub.generic_to_problem(rewritten, nums)
    if revision:
      revision = sub.generic_to_problem(revision, nums)
    # if combined:
    #   combined = sub.generic_to_problem(combined, nums)
    print(rewritten)
    return rewritten, critique, revision, intro, combined, '', subbed_problem

probs = x.split('\n')

res = []

for problem in probs:
  res_2 = {}
  for theme in "sports,nature,science,fantasy,indiana jones".split(','):
    rewritten, critique, revision, intro, combined, answer, subbed_problem = one_off(problem, theme, "", helm_key)
    res_2[theme] = (revision if revision else rewritten, critique)
  res.append(res_2)
  print(res_2)

import json
print(json.dumps(res, indent=2))

