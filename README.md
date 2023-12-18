# Leetcode Crawler to Download my Submissions #
Apply selenium to download all my leetcode submissions

## Execute File ##
1. open file leetcode_crawler.py and modify settings (line 123, username, password, and webdriver_path)
2. delete all_problems_list.csv and submission.csv
3. execute leetcode_crawler.py to catch all submissions

## Execution Result ##
1. get all problems from [problem list](https://leetcode.com/api/problems/all) and save result to all_problems_list.csv.
2. login to leetcode your account (use selenium to enter username, password and enter).
3. use while loop to get all [submissions](https://leetcode.com/api/submissions/?offset=0&limit=50).
4. get all submission id, if the submission result is "Accepted", get the code and save to folder submission.
5. Return the submission result.

### all_problems_list.csv ###
| question_id | question__title                                | Difficulity | title_slug                                     |
|-------------|------------------------------------------------|-------------|------------------------------------------------|
| 1           | Two Sum                                        | 1           | two-sum                                        |
| 2           | Add Two Numbers                                | 2           | add-two-numbers                                |
| 3           | Longest Substring Without Repeating Characters | 2           | longest-substring-without-repeating-characters |
| 4           | Median of Two Sorted Arrays                    | 3           | median-of-two-sorted-arrays                    |
| 5           | Longest Palindromic Substring                  | 2           | longest-palindromic-substring                  |
| 6           | Zigzag Conversion                              | 2           | zigzag-conversion                              |
| ...           | ...                                | ...           | ...                                |

### submission.csv ### 
| question_id | title                                          | title_slug                                     | lang_name | runtime | question__title                                | Difficulity | memory |
|-------------|------------------------------------------------|------------------------------------------------|-----------|---------|------------------------------------------------|-------------|--------|
| 1           | Two Sum                                        | two-sum                                        | Python    | 0%      | Two Sum                                        | 1           | 0%     |
| 2           | Add Two Numbers                                | add-two-numbers                                | Python    | 8.80%   | Add Two Numbers                                | 2           | 99.36% |
| 3           | Longest Substring Without Repeating Characters | longest-substring-without-repeating-characters | Python    | 11.91%  | Longest Substring Without Repeating Characters | 2           | 10.73% |
| 4           | Median of Two Sorted Arrays                    | median-of-two-sorted-arrays                    | Python    | 0%      | Median of Two Sorted Arrays                    | 3           | 0%     |
| 5           | Longest Palindromic Substring                  | longest-palindromic-substring                  | Python    | 99.87%  | Longest Palindromic Substring                  | 2           | 93.27% |
| 6           | Zigzag Conversion                              | zigzag-conversion                              | Python    | 15.18%  | Zigzag Conversion                              | 2           | 23.52% |
| …           | …                                              | …                                              | …         | …       | …                                              | …           | …      |
