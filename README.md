# interest-matching
A group of people all nominate interests. The program matches them with 2-4 people with as many similar interests as possible. 

## Example output
```
EMAIL TO: id@email.com 
Hi there, --------

Thank you for signing up to the PenPals Program! We are very excited to launch this program, having received an overwhelming volume of interest and support. We hope that you find this experience valuable throughout your T2 journey. 

You have been paired with ------- based on the following mutual interests: ['Cooking/Food', 'Baking']. Their email is -------
You have been paired with ----- based on the following mutual interests: ['Anime', 'Cooking/Food']. Their email is ------
You have been paired with -------- based on the following mutual interests: ['Cooking/Food', 'Baking']. Their email is --------
To get in contact with your designated penpal(s), please reach out to them via: 
Facebook messenger (reccommended to start the conversation, then move wherever you're comfortable) 
Emails provided (if you can't find them elsewhere)

Please contact the your matches within the next few days.
Please be understanding if you don't have any interests matched for one of your matches. You will have more luck in your other matches!
Thank you again for your interest and participation in this program. If you have any questions please feel free to reply to this email.

Best, 
PenPal Team
```
## Setup
Keep in mind this was made as a one off to a very specific situation, so a few changes need to be made:

1. in `sorted_interests.txt`, put interests for each person in the format
```
interest1;interest2;
interest1;interest2;
```
2. in `students.txt`, place student ids in the format:
```
z1

z2

```
3. in `sorted_names.txt`, place names in this format:
```
name1
name2
```
4. At the top of `sortwit.py`, set `email_type` to the service being used (eg `@gmail.com`) and make a `students` list with each of their ids eg  `["z1", "z2", "z3", "z4", "z5", "z6", "z7", "z8"]`

5. run `py sortwit.py`