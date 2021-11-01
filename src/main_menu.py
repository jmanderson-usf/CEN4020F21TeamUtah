# made a connection to main.py Username.db and added a function to count the jobs posted to enforce limit
from links_menu import LinksMenu
from profile_menu import ProfileMenu
from utils.jobs import get_all_jobs, job_entry, number_job_rows, apply_job_entry, increase_app_count
from utils.user import get_user
from messages_menu import MessagesMenu
from db.db import get_db


conn = get_db()
c = conn.cursor()


# For ICU-36 sprint 6 - function to print all jobs in the table


def select_all_jobs():
    for i in get_all_jobs():
        count = 1
        print("Job #" + count)
        print("Title: " + i[1])
        print("Description: " + i[2])
        print("Employer: " + i[3])
        print("Location: " + i[4])
        print("Salary: " + i[5])
        count = +1


def get_user_selection():
    selection_text = input("Please make a choice from the menu: ")
    return int(selection_text)

# FOR ICU-34 SPRINT 6 created for inserting applications for all users


def find_deleted_appl():
    query = """SELECT * FROM Applications WHERE username = ?;"""
    user = (get_user(),)
    c.execute(query, user)
    conn.commit()
    count = 0
    for i in c.fetchall():
        count = count + 1

    query = """SELECT applnumber FROM Username WHERE username = ?;"""
    c.execute(query, user)
    conn.commit()

    count2 = 0
    for i in c.fetchall():
        count2 = count2 + 1

    if count != count2:
        print("A job that you had applied to has been deleted")
#

# NEW MENU CREATED
# POST A JOB WORK DONE HERE


def job_intern_menu():
    choice = 0
    while choice != 3:

        print("""
1 - Post a job
2 - Apply for a job
3 - Delete a job
4 - Go back

""")
        selection = get_user_selection()
        if selection == 1:
            jobs_posted = number_job_rows()
            # FOR ICU-35 SPRINT 6  "The number of job listings that the system can support will be increased to ten"
            if jobs_posted == 10:
                print(
                    "The maximum amount of jobs posted have been reached. Please come back again later.")
                return
            job_title = input("Job Title: ")
            job_description = input("Job Description: ")
            employer = input("Employer: ")
            location = input("Location: ")
            salary = input("Salary: ")

            username = get_user()
            job_entry(username, job_title, job_description,
                      employer, location, salary)

        # implemented for ICU-36 sprint 6
        elif selection == 2:
            # apply for a job
            job_select = input(
                int(print("Choose the number of the job you want to apply to: ")))
            select_all_jobs()
            if job_select > number_job_rows + 1:
                print("Please select a job in the appropiate range.")
            elif job_select <= number_job_rows + 1:
                user = get_user()
                query = """SELECT * FROM Jobs"""
                c.execute(query)
                conn.commit()
                tp_list = [tuple()]
                for i in c.fetchall():
                    tp_list.append()

                if tp_list[job_select, 0] == user:
                    print("You cannot apply to a job you created. Please try again.")
                    return
                else:
                    title = tp_list[job_select, 1]
                    grad_date = input(
                        str(print("Please enter a graduation date: ")))
                    start_date = input(
                        str(print("Please enter a start date: ")))
                    description = input(str(print(
                        "Please write a brief paragraph explaining why you think you would be a good fit for the job: ")))
                    # FOR ICU-34 SPRINT 6 "The entered information will be stored in a way that associates it with the job that has been applied for"
                    apply_job_entry(user, title, grad_date,
                                    start_date, description)
                    increase_app_count(user)

        # FOR ICU-35 SPRINT 6 implement deletion of items that the user has not posted himself
        elif selection == 3:
            tp_list = [tuple()]
            print("This is the list of possible jobs that you can delete\n")
            count = 0
            for i in select_all_jobs():
                if i[0] == get_user():
                    tp_list.append(i)
                    print("Job # " + count + "\n")
                    print("\nJob Title: " + i[1] + "\n")
                    print("Employer: " + i[2] + "\n")
                    print("Location: " + i[3] + "\n")
                    print("Salary: " + i[4] + "\n")

            selection2 = input(int(print("Which job do you wish to delete?")))
            select_title = tp_list[selection2, 1]
            query = """DELETE * FROM Jobs WHERE title = ?;"""
            c.execute(query, select_title)
            conn.commit()

        # RETURNS BACK TO THE PREVIOUS MENU
        elif selection == 4:
            return
        else:
            print("Invalid Input. Please choose a number between 1-4.")
#

# MENU SHOWED AFTER SELECTING "LEARN A NEW SKILL"


def learn_skills_menu():
    while True:
        print(
            """
1 - Networking
2 - Time Management
3 - Public Speaking
4 - Agile and Scrum
5 - Leadership
6 - Go Back
"""
        )

        selection = None

        try:
            selection = get_user_selection()
        except:
            print("Invalid selection")
            continue
        if selection == 6:
            return
        elif selection > 6:
            print("Invalid selection")
        else:
            print("Under Construction")

# LOGOUT OPTION THAT SHOULD LEAD TO MENU BEFORE YOU LOGIN


def logout():
    print("Thank you for using InCollege!")


# FUNCTION TO ENUMARATE THE OPTIONS FROM OPTIONS AND ACTIONS 2 DIMENSIONAL ARRAY


def print_menu_options(optionsAndActions):
    options = [
        f"{i + 1} - {x[0]}"
        for i, x
        in enumerate(optionsAndActions)
    ]
    options_text = "\n".join(options)

    print(options_text)

# FUNCTION TO GET THE SELECTION FROM PRINT_MENU_OPTIONS


def get_user_action_selection(optionsAndActions):
    selection = get_user_selection() - 1

    try:
        if selection < 0:
            raise Exception()

        action = optionsAndActions[selection][1]

        if action is None:
            print("Under Construction")

        return action

    except:
        print("Invalid selection")

# MAIN MENU FUNCTION THAT CALLS ALL THE OTHER MISCELANIOUS MENU FUNCTIONS


def main_menu():

    print()

    # MENU SHOWN AFTER YOU SUCCESFULLY LOGIN
    optionsAndActions = [
        ("View/Edit Profile", ProfileMenu().run),
        ("Job/Internship Search", job_intern_menu),
        ("Find Someone You Know", None),
        ("Messages", MessagesMenu().run),
        ("Learn a New Skill", learn_skills_menu),
        ("InCollege Important links", LinksMenu().run),
        ("Log Out", logout)
    ]

    # user = get_user()

    while True:
        # read_friend_requests(user)
        print("\n")
        print_menu_options(optionsAndActions)
        print("\n")

        action = get_user_action_selection(optionsAndActions)

        if action is not None:
            action()

        if action == logout:
            return
