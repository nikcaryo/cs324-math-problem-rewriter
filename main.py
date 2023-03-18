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
helm_key = open("apikeys.txt").readlines()[0].strip()
open_api_key = open("apikeys.txt").readlines()[1].strip()

openai.api_key = open_api_key
auth = Authentication(api_key=helm_key)
service = RemoteService("https://crfm-models.stanford.edu")

problems = json.load(open("problems.json"))
themes = ["sports", "cats", "unicorns", "art", "spiderman"]


def rewrite_and_revise(
    original_problem,
    theme,
    api_key,
    token_fn=prompts.token_v1,
    prompt_fn=prompts.scaled_results_v1,
    revise_yes_no_fn=prompts.yes_no_critique_v1,
    revise_fn=prompts.revision_critique_v1,
    include_intro=True,
    **kwargs,
):
    auth = Authentication(api_key=api_key)
    service = RemoteService("https://crfm-models.stanford.edu")

    rewrite_prompt = prompt_fn(original_problem, theme, token=token_fn)
    request = Request(
        model="openai/text-davinci-003",
        prompt=rewrite_prompt,
        echo_prompt=False,
        temperature=0.3,
    )
    request_result: RequestResult = service.make_request(auth, request)
    result = request_result.completions[0].text
    rewritten_problem = result[: result.find("==")]

    critique_prompt = revise_yes_no_fn(
        original_problem, rewritten_problem, theme, token=token_fn
    )
    request = Request(
        model="openai/text-davinci-003", prompt=critique_prompt, echo_prompt=False, max_tokens=300
    )
    request_result: RequestResult = service.make_request(auth, request)
    result = request_result.completions[0].text
    critique = result[: result.find("==")]
    revision = None

    if not critique.lower().startswith("y"):
      # print("no critique", critique)
      pass
    else:
      revise_prompt = revise_fn(
          original_problem, rewritten_problem, theme, critique, token=token_fn
      )
      request = Request(
          model="openai/text-davinci-003", prompt=revise_prompt, echo_prompt=False
      )
      request_result: RequestResult = service.make_request(auth, request)
      result = request_result.completions[0].text
      revision = result[: min(result.find("END"), result.find("----"))]

    intro = None
    if include_intro:
      intro_prompt = prompts.write_intro_v2(revision if revision else rewritten_problem, token_fn)

      # high temp, lots of creativity
      request = Request(
        model="openai/text-davinci-003", prompt=intro_prompt, echo_prompt=False, temperature=0.8, max_tokens=300
      )
      request_result: RequestResult = service.make_request(auth, request)
      intro = request_result.completions[0].text.strip()
      
      for _ in range(2):
        remove_numbers_prompt = prompts.intro_check_for_numbers_v1(intro)
        if not remove_numbers_prompt:
          break
        else:
          # low temp, do what we ask
          request = Request(
            model="openai/text-davinci-003", prompt=remove_numbers_prompt, echo_prompt=False, temperature=0.1
          )
          request_result: RequestResult = service.make_request(auth, request)
          new_intro = request_result.completions[0].text.strip()
          intro = new_intro
      
    combined = None
    if intro:
      problem = revision if revision else rewritten_problem
      intro_prompt = prompts.combine_intro_and_problem(problem, intro)
      request = Request(
        model="openai/text-davinci-003", prompt=intro_prompt, echo_prompt=False, temperature=0.1, max_tokens=300
      )
      request_result: RequestResult = service.make_request(auth, request)
      combined = request_result.completions[0].text.strip()


    critique = critique[critique.find('.') + 1:] if critique.lower().startswith("y") else None
    return rewritten_problem, critique, revision, intro, combined


def one_off(problem, theme, constraints_string, helm_key, include_intro=True):
    subbed_problem, nums = sub.problem_to_generic(problem)

    # prompt = prompts.scaled_results_v1(subbed_problem, theme)

    # print(subbed_problem, nums)

    # request = Request(model="openai/text-davinci-003", prompt=prompt, echo_prompt=False)
    # request_result: RequestResult = service.make_request(auth, request)
    # result = request_result.completions[0].text
    # result =
    rewritten, critique, revision, intro, combined = rewrite_and_revise(subbed_problem, theme, helm_key, include_intro=include_intro)
    # print(rewritten, critique, revision, intro, combined)

    num_dict = constraints.parse_constraints(constraints_string, split_char='|')
    
    answer = None
    if "answer" in num_dict:
       answer = num_dict["answer"] 
       del num_dict["answer"]
    new_nums = list(num_dict.values())
    rewritten = sub.generic_to_problem(rewritten, new_nums)
    if revision:
      revision = sub.generic_to_problem(revision, new_nums)
    if combined:
      combined = sub.generic_to_problem(combined, new_nums)
    
    return rewritten, critique, revision, intro, combined, num_dict.get('answer'), subbed_problem


def demo():
    question = {
        "question": "There were 28 bales of hay in the barn. Tim stacked more bales in the barn today. There are now 54 bales of hay in the barn. How many bales did he store in the barn ?",
        "generic": "There were ___A___ bales of hay in the barn. Tim stacked more bales in the barn today. There are now ___B___ bales of hay in the barn. How many bales did he store in the barn ?",
        "numbers": [28, 54],
        "constraints": "A=randint(20,40)\nB=randint(40,50)\nanswer= B - A",
        "lEquations": ["28+x=54"],
        "lSolutions": [26.0],
        "grammarCheck": 0,
        "templateNumber": 0,
        "sQuestion": "There were 28 bales of hay in the barn. Tim stacked more bales in the barn today. There are now 54 bales of hay in the barn. How many bales did he store in the barn ?",
        "iIndex": 1,
    }

    print("original question:", question["question"])
    print("generic question", question["generic"])
    print("constraints:", question["constraints"])

    for theme in themes:
        print("\nNew theme:", theme)
        nums = constraints.parse_constraints(question["constraints"])
        print("Evaluated constraints:", nums)
        request = Request(
            model="openai/text-davinci-003",
            prompt=prompts.scaled_results_v1(question["generic"], theme),
            echo_prompt=False,
        )
        request_result: RequestResult = service.make_request(auth, request)
        result = request_result.completions[0].text
        result = result[: result.find("==")]
        print("Rewritten problem:", sub.generic_to_problem(result, list(nums.values())))


def batch(question_file, k, themes):
    with open(question_file) as f:
        questions = json.load(f)
        for key, problem in list(questions.items())[:k]:

            print("original problem", "\n")
            print(problem["question"])
            for theme in themes:
                print(f"===== {key} - {theme} =======")
                prompt = prompts.scaled_results_v1(problem["generic"], theme)

                # response = openai.Completion.create(model="text-davinci-003", prompt="Say this is a test", temperature=0, max_tokens=7)
                # print(response)

                request = Request(
                    model="openai/text-davinci-003", prompt=prompt, echo_prompt=False
                )
                request_result: RequestResult = service.make_request(auth, request)
                result = request_result.completions[0].text
                result = result[: result.find("==")]

                print("rewritten for theme: ", theme, "\n")
                print(sub.generic_to_problem(result, problem["numbers"]))


if __name__ == "__main__":
    # batch('questions_with_generics_50.json', 5, themes)
    # demo()
#     constraints_string = "A=1 | B=randint(100,150)| C=2| D=randint(100,150)| E = 3| F=randint(100,150) | G= E| H=randint(2,8)"
#     for theme in themes + ["baseball"]:
#         # problem = "Sam went to 14 football games this year. He went to 29 games  last year. How many football games did Sam go to in all?"
#         problem = """The table below show the points Janet scored on a video game each time she played.
# Game # | Points Scored
# 1 | 155
# 2 | 150
# 3 | 180
# After the first 3 games, she took a break and came back the next day and scored 2 times as many points as she had during all the previous games combined. How many more points did she score after her break?
# """
#         rewritten, revision, intro = one_off(problem, theme, constraints_string)
#         print('-----')
#         print(theme)
#         print(intro)
#         print(revision if revision else rewritten)
#         break

    # In the UI, can just have each X=(expr) on its own line
    # just set constraints.parse_constraints(constraints_string, split_char='\n')
    constraints_string = "A=randint(2,20)|B=randint(5,30)|C=randint(12,55)|answer=A+B+C"
    # problem = """Sandy has 10 books, Benny has 24 books, and Tim has  33 books. How many books do they have together ?"""
    # problem = """Sandy, Jessica, and Kate are nurses. Sandy has 10 patients, Jessica has 24 patients, and Kate has 33 patients. How many patients do they have together?"""
    problem = "Sam had 9 dimes in his bank. His dad gave him 7 more dimes. How many dimes does Sam have now ?"
    for theme in  ["sports"]:
        # problem = "Sam went to 14 football games this year. He went to 29 games  last year. How many football games did Sam go to in all?"

        # rewritten: the straight up rewritten problem
        # critique: the critique if there is one, else None. Should have the "Yes." cut off. Could be displayed to user along with original rewrite
        # revision: None if no revision, otherwise, the revised problem
        # intro: None if no intro asked for, otherwise, the intro to the problem that shouldn't contain any numbers
        # combined: (intro and rewritten/revision) combined via gpt
        # answer: if the constraints_string has an 'answer=(expression)' then answer will be the evaluated expression, else None.
        rewritten, critique, revision, intro, combined, answer, generic= one_off(problem, theme, constraints_string, helm_key)
        print('-----')
        print('critique:', critique)
        print('theme:', theme)
        print('intro:', intro)
        print('new problem:', revision if revision else rewritten)
        print('combined:', combined)
        print('answer', answer)




# theme: sports
# intro: John was the star quarterback of his high school football team. He was known for his skill on the field and his passion for the game. Every day he would go to practice with a smile on his face, ready to learn and to work hard. One day, he opened his locker and was surprised to find his coach had left him a special gift - some brand-new footballs! He quickly figured out just how many he had in total.
# new problem: John had 2 footballs in his locker. His coach gave him 11 more footballs. How many footballs does John have now?

# combined: John was the star quarterback of his high school football team. He was known for his skill on the field and his passion for the game. Every day he would go to practice with a smile on his face, ready to learn and to work hard. One day, he opened his locker and was surprised to find his coach had left him a special gift - some brand-new footballs! He quickly figured out that he had 2 footballs in his locker, and with the 11 more footballs his coach had given him, how many footballs does John have now?
# answer 38