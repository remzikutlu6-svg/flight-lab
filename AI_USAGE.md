# AI Usage Disclosure

<!--
Fill in this file before you submit. Submissions without it are not graded.
If you used no AI tools, delete everything below and write only:
No AI tools were used.
-->

## Tools used

- I used ChatGPT

## Conversation links

- Link 1:https://chatgpt.com/share/6af8556c-1c0c-83ed-ba85-a539c8cf0259
- Link 2:

## What I used them for

- I used ChatGPT to understand date validation and CSV files
  I asked about filtering and sorting flight data
  I also used it for argparse JSON logging and error handling

## Which parts of the code were AI-generated or substantially AI-assisted

| --- | --- | --- |
| validator.py | load_airports validate_row to_record | generated and explained |
| csv_loader.py | parse_files | generated and modified |
| query.py | run_query run_queries | generated and explained |
| flight_parser.py | main | generated and modified |
## Key prompts

1.how can i check if a date has the correct format in python using datetime
2.how can i read csv files in python and skip empty lines and comments but still get the correct line numbers
3.how can i filter a list of dictionaries in python using multiple conditions and then sort the results by a key and limit the number of results
4.how can i use argparse in python to accept different command line options and make sure only one of three options is selected

## What I changed or verified myself

I used some code examples from ai conversations and wrote the other parts by myself I also used python documentation and online resources to understand some functions and changed the code for my project. I tested the code by myself and all 29 public tests passed

## Resources
https://docs.python.org/3.13/library/csv.html
https://docs.python.org/3.13/library/datetime.html
https://docs.python.org/3.13/library/re.html
https://docs.python.org/3.13/library/argparse.html
https://docs.python.org/3.13/library/logging.html
https://docs.python.org/3.13/library/json.html
https://docs.python.org/3.13/howto/sorting.html