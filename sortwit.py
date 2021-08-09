import itertools
import random
#TO GET STUDENTS
#egrep . students.txt|tr '\n' ' '| sed 's/z/"z/g'| sed 's/ /", /g'
#TO GET INTERESTS:
#cat interests.txt| egrep '\n'
#get students in a list (use grep command from above) (but also translate Z to z)

global email_type
email_type = "@gmail.com"

students = ["z1", "z2", "z3", "z4", "z5", 
        "z6", "z7", "z8"]

#get interests in a list
interests = []
for line in open("sorted_interests.txt"):
    persons_interests = []
    for interest in line.split(';'):
        if interest != '\n':
            persons_interests.append(interest)
    interests.append(persons_interests)

student2name = {}
names = []
for line in open("sorted_names.txt"):
    line = line.strip()
    names.append(line)
#print("names: {} zIDs: {} interests: {}".format(len(names), len(students), len(interests)))
for i in range(len(names)):
    student2name[students[i]] = names[i]
#print(str(len(students)) + ' ' + str(len(interests)))
#link them both in a dictionary
student2interest = {}
for i in range(len(students)):
    student2interest[students[i]] = interests[i]

#SORT... ... ...
#make a class, called pairs, each pair contains a zid name to name, and name to
#name, number of overlapping interests, what the interests are, and the two
#emails

class Pair:
    def __init__(self, student1, student2):
        self.student1 = student1
        self.student2 = student2
        self.interests1 = student2interest[student1]
        self.interests2 = student2interest[student2]
        self.pair = set([student1, student2])
        #in common is a score of how many interests they have in common
        self.student1_name = student2name[student1]
        self.student2_name = student2name[student2]
        self.in_common = list(set(self.interests1).intersection(self.interests2))
        self.in_common_score = len(self.in_common)
        self.student1_email = student1 + email_type 
        self.student2_email = student2 + email_type
#method 1: sort compare each person with every other person... 47! ... give
#dictionary with "pair - how much they have in common"
    def __hash__(self):
        return hash(self.in_common_score)
    
    def __eq__(self, other):
        #other is other pair object
        return self.pair == other.pair
    def __str__(self):
        return "pair: {}, interests: {}, score: {}".format(self.pair, self.in_common, str(self.in_common_score))

all_pairs = set()

#for (every student)
for student1 in students:
    #go through every other student.
    for student2 in students:
        #don't put student in a pair with themself
        if student1 == student2:
            continue
        #create pair
        current_pair = Pair(student1, student2)
        
        #adds pair (if already in then it skips)
        #print(current_pair.in_common_score)
        all_pairs.add(current_pair)

#for pair in all_pairs:
#    print("pair: {}, interests: {}, score: {}".format(pair.pair, pair.in_common, str(pair.in_common_score)))

#                               NON OPTIMAL WAY
#sort pairs in terms of most in common          
#go through in order of highest interests

#convert set to list so we can sort it
all_pairs_list = []
for pair in all_pairs:
    all_pairs_list.append(pair)

all_pairs_list.sort(key=lambda x: x.in_common_score, reverse=True)
def print_pairs(pairs_list):
    for pair in pairs_list:
        print("student1 {}, student2: {} interests in common:{}".format(pair.student1_name, pair.student2_name, pair.in_common))

def get_outcome_score(outcome):
    #outcome is a set / list of all pairs
    score = 0
    for pair in outcome:
        score += pair.in_common_score
    return score
def get_students_matched(student2matches):
    match_score = 0
    for student in student2matches:
        match_score += student2matches[student]
    return match_score

def print_email(student_object):    
    print("==================================")
    #print("{} with email {} to message {} with in common {}".format(student_name, student_email, to_message, common_interests))
    print("""EMAIL TO: {} 
Hi there, {}

Thank you for signing up to the PenPals Program! We are very excited to launch this program, having received an overwhelming volume of interest and support. We hope that you find this experience valuable throughout your T2 journey. 
""".format(student_object.student_email , student_object.name))
    if len(student_object.to_message) == 0:
        print("You have zero people to message! Do not worry though, you have been matched with at least 4 people")
    if len(student_object.to_message) == 1:
        print("You have just one person to message! Don't worry though, you  have been matched with at least 4 people")
        print("")

    for other_student_object in student_object.to_message:
        interests_in_common = list(set(student_object.interests).intersection(other_student_object.interests))
        print("You have been paired with {} based on the following mutual interests: {}. Their email is {}".format(other_student_object.name, interests_in_common, other_student_object.student_email)) 
   
    if len(student_object.to_message) != 0:
        print("""To get in contact with your designated penpal(s), please reach out to them via: 
Facebook messenger (reccommended to start the conversation, then move wherever you're comfortable) 
Emails provided (if you can't find them elsewhere)
""")
        print("Please contact the your matches within the next few days.")
        print("Please be understanding if you don't have any interests matched for one of your matches. You will have more luck in your other matches!")
    
    print("""Thank you again for your interest and participation in this program. If you have any questions please feel free to reply to this email.

Best, 
PenPal Team""")
    return

class Student:
    def __init__(self, student, student2name, student2interests):
        self.student = student
        self.name = student2name[student]
        self.student_email = student + email_type
        self.interests = student2interests[student]
        self.to_message = [] #list of names
        self.to_email = [] #zIDs of ppl to email
        self.to_message_me = []
        self.matched_with_man = False
        self.matches = set() #set of other student objects
        men = ["z1", "z2"]
        if student in men:
            self.man = True
        else:
            self.man = False
    
    def Can_Add(self, other_student, the_pair, student_objects):
        #find other student object
        for student_object in student_objects:
            if student_object.student == other_student:
                other_student_object = student_object
                #see if already added wit this person
                if self.name in other_student_object.to_message_me:
                    return False
                #see if capacity is already two
                elif len(other_student_object.to_message_me) ==2:
                    return False
                #if non man matches with man, but have matched  w man before
                elif self.man == False and other_student_object.man == True and self.matched_with_man == True:
                    return False
                else:
                    return True
                #and matched_with_man is true
    def Can_Match(self, other_student_object):
        #if both non men, just return true
        if self.man == False and other_student_object.man == False:
            return True

        #if im woman, they man, and I've matched with man 
        if self.man == False and other_student_object.man == True and self.matched_with_man == True:
            return False
        #if im man, they're woman who's matched
        
        elif self.man == True and other_student_object.man == False and other_student_object.matched_with_man == True:
            return False
        
        #implicitly matched_with_man == False
        #if im a non man matching with a man
        elif self.man != True and other_student_object.man == True:
            self.matched_with_man = True
            return True
        else:
            return True

    def Match(self, other_student_object):
        self.matches.add(other_student_object)
        other_student_object.matches.add(self)
    def Is_Already_Matched(self, other_student_object):
        matches_zIDs = []
        all_matches = self.to_message + self.to_message_me
        for match in all_matches:
            matches_zIDs.append(match.student)
        return (other_student_object.student in matches_zIDs)
    def Get_Matches(self):
        #used post sorting emails
        matches = self.to_message + self.to_message_me
        return len(matches)
    
def get_student_object(student, student_objects):
    for student_object in student_objects:
        if student_object.student == student:
            return student_object

def convert_name_to_student_object(name, student_object):
    #find zID
    for student in students:
        if student2name[student] == name:
            #get student object
            return get_student_object(student, student_objects)
#then go through everyone, assign the highest match for each person
#...
#for every student..
#populate dictionariyi
                                        #get pairs
all_outcomes = []
for i in range(1):
    global student_objects
    student_objects = []
    #populate
    for student in students:
       student_objects.append(Student(student, student2name, student2interest))
    all_pairs_list = list(all_pairs) 
    
    #shuffle order of students
    #print(i)
#    random.shuffle(students)
    student2matches = {}
    current_outcome = []
    for student in students:
        student2matches[student] = 0

    for _ in range(4):
        for student in students:
            #get current student object

            for pair in all_pairs_list:
                #if BOTH students in the pair haven't been matched >4
                if student2matches[pair.student1] <4 and student2matches[pair.student2] <4:
                    
                    student1_obj = get_student_object(pair.student1, student_objects)
                    student2_obj = get_student_object(pair.student2, student_objects)

                    if student1_obj.Can_Match(student2_obj):
                        
                        current_outcome.append(pair)
                        student2matches[pair.student1] += 1
                        student2matches[pair.student2] += 1
                        all_pairs_list.remove(pair)
                        student1_obj.Match(student2_obj)


    
    all_outcomes.append(current_outcome)
#print_pairs(current_outcome)i
                    #COMPARE, GET BEST OUTCOME
                    #go
                    #through list, compare which has highest score
highest_score = 0
for outcome in all_outcomes:
    current_score = get_outcome_score(outcome)
    if current_score > highest_score:
        highest_score = current_score
        best_outcome = current_outcome

                            #FOUND BEST OUTCOME
                            #NOW SORTING EMAIL
#student to people messaging them
student2messengers = {}
#populate as zero at the beginning
for student in students:
    student2messengers[student] = 0

def test_woman_dont_match_with_more_than_one_man(student_objects):
    for student_object in student_objects:
        #if your a non man...
        if student_object.man == False:
            #loop thru ur matches, if man add to tally
            man_tally = 0
            for match in student_object.matches:
                if match.man == True:
                    man_tally += 1
            if man_tally > 1:
                print("women matches with >1 man!")

def get_everyone_with_less_than_4_matches(student_objects):
    less_than_4 = []
    for student_object in student_objects:
        if len(student_object.matches) != 4:
            less_than_4.append(student_object)
    return less_than_4

def test_every_has_at_least_4_matches(student_objects):
    for student_object in student_objects:
        if len(student_object.matches) < 4:
            return False
    return True


students_with_less_than_4_matches = get_everyone_with_less_than_4_matches(student_objects)
all_pairs_list = list(all_pairs)
all_pairs_list.sort(key=lambda x: x.in_common_score, reverse=True)
for student in students_with_less_than_4_matches:
    #match with ppl...
    while len(student.matches) < 4:
         
        for pair in all_pairs_list:
            #if BOTH students in the pair haven't been matched >4            
            student1_obj = get_student_object(pair.student1, student_objects)
            student2_obj = get_student_object(pair.student2, student_objects)
            
            #if student is in pair
            if student1_obj.student == student.student or student2_obj.student == student.student:
                if student1_obj.student == student.student:
                    other_student = student2_obj
                if student2_obj.student == student.student:
                    other_student = student1_obj
                #if they've ALREADY MATCHED, with this person
                already_matched = False
                for match in student.matches:
                    if match.student == other_student.student:
                        already_matched = True
                
                if already_matched == False:
                    best_outcome.append(pair)
                    student2matches[student.student] += 1
                    student2matches[other_student.student] += 1
                    all_pairs_list.remove(pair)
                    student.Match(other_student)
            #if matches == 4 after added thingone
            #break
            if len(student.matches) == 4:
                break
        #print("...")

#print_pairs(best_outcome) 
#test_woman_dont_match_with_more_than_one_man(student_objects)
#print(test_every_has_at_least_4_matches(student_objects))
def print_all_emails(student_objects):
    for student_object in student_objects:
        print_email(student_object)

def print_how_many_email_matches(student_objects):
    failures = 0
    need_more_matches_students = []
    for student_object in student_objects:
        print("{} has {} {}".format(student_object.name,
            len(student_object.to_message), len(student_object.to_message_me))) 
        if len(student_object.to_message) + len(student_object.to_message_me) < 4:
            failures += 1
            need_more_matches_students.append(student_object)
    #print(failures)
    #for student in need_more_matches_students:
    #    print(student.name, student.to_match)
def print_email_matchups(student_objects):
    #for each student
    for student_object in student_objects:
        print("=== {} ===".format(student_object.name))
        print("messaging...")
        if len(student_object.to_message) == 0:
            print("No one..")
        for other_student_object in student_object.to_message:
            interests_in_common = list(set(student_object.interests).intersection(other_student_object.interests))
            print(other_student_object.name, interests_in_common, other_student_object.student_email) 
        print("gonna be messaged by...")
        if len(student_object.to_message_me) == 0:
            print("No one..")
        for other_student_object in student_object.to_message_me:
            interests_in_common = list(set(student_object.interests).intersection(other_student_object.interests))
            print(other_student_object.name, interests_in_common, other_student_object.student_email)

def sort_emails(student_objects):
    #go through each student
    for student_object in student_objects:
        #select two people they match with
        list_matches = list(student_object.matches)
        for match in list_matches:
            if len(student_object.to_message) < 3:
            #if True:   
                student_object.to_message.append(match)
                match.to_message_me.append(student_object)
                
                student_object.matches.remove(match)
                match.matches.remove(student_object)
                #list_matches.remove(match)
def test_how_many_occcurances_of_each_name(student_objects):
    for student_object in student_objects:
        occurances = 0
        for line in open("email_matchups_test.txt"):
            if student_object.name in line:
                occurances += 1
        print("{} {}".format(student_object.name, occurances))
        if occurances < 5:
            print("                 {}".format(student_object.name))
def print_person_and_interests(student_objects):
    for student_object in student_objects:
        print("{}: {}".format(student_object.name, student_object.interests))

def find_new_person(name, student_objects):
    #go through each student, if their matches are less than 5 and in common = highest
    student_object = convert_name_to_student_object(name, student_objects)
    
    high_score = 0
    for other_student_object in student_objects:
        interests_in_common = list(set(student_object.interests).intersection(other_student_object.interests))
        interest_score = len(interests_in_common)
        
        if interest_score > high_score and student_object.Is_Already_Matched(other_student_object) == False:
            #if they have only  4 matches:
            num_match = other_student_object.Get_Matches()
            
            if num_match < 4:
                high_score = interest_score
                #add to matches of both students
                best_match = other_student_object
                common_with_bff = interests_in_common
    #todo: remove from each others matches
    #print out {student} to message {new student} with common interests
    #print("{} to message {} with common interests {}".format(student_object.name, best_match.name, common_with_bff))

sort_emails(student_objects)
print_all_emails(student_objects)
#test_how_many_occcurances_of_each_name(student_objects)

#print_person_and_interests(student_objects)
#print_how_many_email_matches(student_objects)
find_new_person("Fox", student_objects)
find_new_person("Falco", student_objects)
#print_email_matchups(student_objects)



