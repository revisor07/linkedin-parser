# linkedin-parser

To get the python package run command in the directory you want it to appear in:
  git clone https://github.com/talent-games/linkedin-parser

Dependencies required for the project to run:
  Python3, all modules from linkedin-parser/requirenments.txt

Project contains 3 parts:

Note: to avoid bugs it is recommended to use both input and output, the functionality of default paramenters is not properly tested yet. Either use a full path or relative to the current cd location

1. lnkd gen_urls -i ~/.../initial_input.csv -o ~/.../linkedin_urls.csv

Input format:
  35718,35720,Ben,Newman,JavaScript,38104,2641
File consitst of many lines like that.

Output format:
  Ben Newman,https://www.linkedin.com/in/ben-newman-09241b2
A smaller file with lines corresponding to the lines in input that managed to pass and find a legit url.

2. lnkd save_html -i ~/.../linkedin_urls.csv -o ~/.../
  
Input format:
  Ben Newman,https://www.linkedin.com/in/ben-newman-09241b2

Output format:
  ben-newman-09241b2.html 
HTML file per each line in input
  
3. lnkd extract -i ~/.../ -o ~/.../linkedin_analysis.csv

Input format:
  ~/../ path to directory with html files

Output format:
  Name,Place,Experience,Education
with relative info under the column names


Also there is a help command with the summary of this: lnkd -h