# Poject 1: Gamification
# Ziyi Huang
# Python 3.8.8
# 2021. 10. 9

def initialize():
    '''Initializes the global variables needed for the simulation.
    Note: this function is incomplete, and you may want to modify it'''

    # all integer: current hedon points, current health points, current time
    global cur_hedons, cur_health, cur_time
    # string: last activity, integer: the duration of last activity
    global last_activity, last_activity_duration
    # booleans: if the player is bored with stars, if the player is tired or not, if a star is offered or not
    global bored_with_stars, tired, star_is_offered
    # lists: 2D list that stores the activity and corresponding time, 2D list stores the offered star and corresponding time when it is offered
    global activity_time_list, stars
    # initialize the lists, empty
    activity_time_list = []
    stars = []
    # initialize string as None and integers as 0
    last_activity = None
    last_activity_duration = 0
    cur_hedons = 0
    cur_health = 0
    cur_time = 0

    cur_star_activity = None
    # initialize booleans as False
    bored_with_stars = False
    tired = False
    star_is_offered = False


def perform_activity(activity, duration):
    '''perform an activity according to the two parameters
    parameter: activity (string), duration (positive integer)
    '''

    global cur_time, cur_health, cur_hedons
    global last_activity, last_activity_duration
    # if activity is not one of below, nothing will be performed
    if activity == "running" or "textbooks" or "resting":
        # add the activity to the list
        activity_time_list.append([activity, duration])
        # clear the last activity duration everytime
        last_activity_duration = 0
        # while there is mroe than 1 element in the list
        if len(activity_time_list) >= 2:
            # assign the previous one as the last activity
            last_activity = activity_time_list[-2][0]
            last_activity_duration = activity_time_list[-2][1]
            # check the activity before the last activity
            for i in range (len(activity_time_list)-3, -1, -1):
                # if the previous activity is the same as the last activity
                if last_activity == activity_time_list[i][0]:
                    # adds up the duration time counts for the last activity
                    last_activity_duration += activity_time_list[i][1]
                else:
                    # if doesn't contine with the last one
                    break
            # if the current activity is the same as the last activity
            if activity == last_activity:
                # adds up time
                last_activity_duration += duration
        # update the health points and hedon points, and accumulate the time
        tired = is_tired(activity_time_list, activity, duration, last_activity, last_activity_duration)
        cur_health += estimate_health_delta(activity, duration)
        cur_hedons += estimate_hedons_delta(activity, duration, tired, last_activity, last_activity_duration)
        cur_time += duration


def get_cur_hedons():
    ''' return an integer that represents the current hedon points'''
    return cur_hedons


def get_cur_health():
    ''' return an integer that represents the current health points'''
    return cur_health


def offer_star(activity):
    '''offer a star to the activity
    parameter: activity (string)'''

    global stars, cur_time, star_is_offered, cur_star_activity, bored_with_stars
    # assign the cur_star_activity as activity
    cur_star_activity = activity
    # record the given star and activity in the list
    stars.append([activity, cur_time])
    # a star is been offered
    star_is_offered = True
    # if the player is not bored with stars, then check if 3 stars are offered during the span of 2 hours
    if not bored_with_stars and len(stars) >= 3 and stars[-1][1] - stars[-3][1] < 120:
        # be bored with stars
        bored_with_stars = True


def star_can_be_taken(activity):
    '''check if the star offered is available to use for the activity
    para: activity (string)
    return boolean'''

    global activity_time_list, stars, star_is_offered, cur_time, cur_star_activity
    # firstly, check whether a star is offered or not
    if star_is_offered:
        # A star can only be taken if no time passed between the star’s being offered and the activity, and the user is not bored with stars, and the star was offered for activity.
        if cur_time == stars[-1][1] and cur_star_activity == activity and not bored_with_stars:
            return True
    # otherwise, the star is not available, so return False
    return False


def most_fun_activity_minute():
    '''returns the activity (one of "resting", "running", or "textbooks") which would give the
most hedons if the person performed it for one minute at the current time'''

    global activity_time_list
    # the test duration would be 1 min for all the activities here
    test_duration = 1
    # if no activity has been performed
    if len(activity_time_list) == 0:
        # if a star is offered for textbooks
        if len(stars) != 0 and stars[-1][0] == "textbooks":
            return "textbooks"
        # otherwise, the most fun activity at the time would be running
        return "running"
    # local variables, copy values from activity_time_list, so won't affect the actual list
    last_activity_here = activity_time_list[-1][0]
    last_activity_duration_here = activity_time_list[-1][1]
    # make a new list that pretends running is performed
    pretend_list_running = activity_time_list + ["running", test_duration]
    # check if the player is tired here
    tired_here = is_tired(pretend_list_running, "running", test_duration, last_activity_here, last_activity_duration_here)
    # calculate the hedons for 1-min running
    hd_running = estimate_hedons_delta("running", test_duration, tired_here, last_activity_here, last_activity_duration_here)

    # make a new list that pretends textbooks is performed
    pretend_list_textbooks = activity_time_list + ["textbooks", test_duration]
    tired_here = is_tired(pretend_list_textbooks, "textbooks", test_duration, last_activity_here, last_activity_duration_here)
    # calculate the hedons for 1-min carrying textbooks
    hd_textbooks = estimate_hedons_delta("textbooks", test_duration, tired_here, last_activity_here,last_activity_duration_here)

    # the hedon points for resting is always 0
    hd_resting = 0

    # create a list that stores the calculated hedon points and the corresponding activities in order to compare
    list_compare = [[hd_running, "running"], [hd_textbooks, "textbooks"], [hd_resting, "resting"]]
    # sort the list according to the hedons, the most hedons will be the last element in the lsit
    list_compare.sort()
    # return the activity stored in the last element
    return list_compare[2][1]


################################################################################
#These functions are not required, but we recommend that you use them anyway
#as helper functions

def estimate_health_delta(activity, duration):
    '''calculate the health point for the given activity and duration
    para: activity (stirng), duration (positive int)
    return the estimated health points as an integer'''

    global last_activity, last_activity_duration, cur_time, stars
    # initialize the health point as 0
    estimate_health = 0
    # if running is performed
    if activity == "running":
        # else if the last activity is also running, (current activity = last activity)
        if activity == last_activity:
            # if the total duration of the current activity (added up the duration of the last contiuned same activity)
            if last_activity_duration <= 180:
                # get 3 health points for each minute
                estimate_health += 3 * duration
            # the the duration of last activity already exceed 180 min
            elif last_activity_duration - duration >= 180:
                # get 1 health point for each minute
                estimate_health += duration
            # the last duration is less than 180, but when adds up the current duration, it exceeds 180
            else:
                # 3 points for the time that does not exceed 180, and 1 point for the remaining time that exceeds 180
                estimate_health += 3 * (180 - (last_activity_duration - duration)) + (duration - (180 - (last_activity_duration - duration)))

        # if this is the first time that running is performed (not continuous with the last activity)
        else:
            # less than and equal 180 min
            if duration <= 180:
                # 3 points/min
                estimate_health += 3 * duration
            # greater than 180 min
            else:
                # 3*180 + 1*(duration-180) = duration + 360 = 4*duration - 180
                estimate_health += duration + 360

    # if carrying textbooks is performed
    elif activity == "textbooks":
        # always 2 points/min
        estimate_health += 2 * duration
    # resting does not earn health points, = 0

    return estimate_health


def estimate_hedons_delta(activity, duration, tired, last_activity, last_activity_duration):
    '''calculate the hedon point for the given activity and duration
    para: activity (stirng), duration (positive int)
    return the estimated health points as an integer'''

    # initialize the hedon point as 0
    estimate_hedons = 0
    # if a star is availble to use for the current activity
    if star_can_be_taken(activity):
        # for the first 10 min
        if duration <= 10:
            # get extra 3 points/min
            estimate_hedons += 3 * duration
        else:
            # maximum 30 points for the first 10 min
            estimate_hedons += 30
    # if the player is not tired
    if not tired:
        # if runnig is performed
        if activity == "running":
            if activity == last_activity:
                if last_activity_duration <= 10:
                    estimate_hedons += 2 * duration

                elif last_activity_duration - duration >= 10:
                    estimate_hedons -= 2 * duration

                else:
                    # 2 points for the time that does not exceed 10, and -2 point for the remaining time that exceeds 10
                    # duration - (10 - (last_activity_duration - duration)) = - 10 + last_activity_duration
                    estimate_hedons += 2 * (10 - (last_activity_duration - duration)) - 2 * (duration - (10 - (last_activity_duration - duration)))

            else:
                if duration <= 10:
                    estimate_hedons += 2 * duration
                else:
                    # 20 - 2 * (duration - 10) = 40 - 2 * duration
                    estimate_hedons += 40 - 2 * duration

        # if carring textbooks
        elif activity == "textbooks":
            if activity == last_activity:
                if last_activity_duration <= 20:
                    estimate_hedons += duration

                elif last_activity_duration - duration >= 20:
                    estimate_hedons -= duration

                else:
                    # 1 points for the time that does not exceed 20, and -1 point for the remaining time that exceeds 20
                    # duration - (20 - (last_activity_duration - duration)) = duration - 20 + last_activity_duration
                    estimate_hedons += 20 - (last_activity_duration - duration) - (duration - 20 + last_activity_duration)

            else:
                #print("first")
                if duration <= 20:
                    #print("20")
                    estimate_hedons += duration
                else:
                    estimate_hedons += 40 - duration
    # if tired
    if tired:
        # -2 pt/min for any activity
        estimate_hedons -= 2 * duration
    return estimate_hedons


def is_tired(activity_time_list, activity, duration, last_activity, last_activity_duration):
    '''check if the player is tired or not
    para:
        activity_time_list (2D list)
        activity (string)
        duration (positive integer)
        last_activity (string)
        last_activity_duration (positive integer)
    return Boolean'''

    # if there is more than 1 activity performed and the current activity is not resting (player won't be tired while resting)
    if len(activity_time_list) > 1 and activity != "resting":
        # check if the player has rested for more than 120 min without interruption
        if last_activity == "resting" and last_activity_duration >= 120:
            # not tired
            return False
        # doesn't have enough rest
        else:
            return True


################################################################################

if __name__ == '__main__':
    '''
    initialize()
    perform_activity("running", 30)
    print(get_cur_hedons())            # -20 = 10 * 2 + 20 * (-2)             # Test 1
    print(get_cur_health(), "\n")            # 90 = 30 * 3                          # Test 2
    print(most_fun_activity_minute(), "\n")  # resting                              # Test 3
    perform_activity("resting", 30)
    offer_star("running")
    print(most_fun_activity_minute(), "\n")  # running                              # Test 4
    perform_activity("textbooks", 30)
    print(get_cur_health())            # 150 = 90 + 30*2                      # Test 5
    print(get_cur_hedons(), "\n")            # tired, -80 = -20 + 30 * (-2)         # Test 6
    offer_star("running")
    perform_activity("running", 20)
    print(get_cur_health())            # 210 = 150 + 20 * 3                   # Test 7
    print(get_cur_hedons(), "\n")            # using star and tired, -90 = -80 + 10 * (3-2) + 10 * (-2)   # Test 8
    perform_activity("running", 170)
    print(get_cur_health())            # continuous with previous since no rest/interuption, 700 = 210 + 160 * 3 + 10 * 1         # Test 9
    print(get_cur_hedons(), "\n")            # tired, -430 = -90 + 170 * (-2)       # Test 10

    print()
    initialize()

    offer_star("textbooks")
    print(most_fun_activity_minute(), "\n")

    perform_activity("textbooks", 20)
    print(get_cur_health())
    print(get_cur_hedons(), "\n")

    print(most_fun_activity_minute(), "\n")

    perform_activity("resting", 30)
    perform_activity("resting", 80)
    perform_activity("resting", 10)

    offer_star("running")

    print(most_fun_activity_minute(), "\n")

    perform_activity("textbooks", 30)
    print(get_cur_health())
    print(get_cur_hedons(), "\n")

    offer_star("textbooks")

    perform_activity("running", 20)
    print(get_cur_health())
    print(get_cur_hedons(), "\n")

    print(most_fun_activity_minute(), "\n")

    perform_activity("running", 50)
    print(get_cur_health())
    print(get_cur_hedons(), "\n")

    offer_star("textbooks")
    print(most_fun_activity_minute(), "\n")

    perform_activity("resting", 120)

    perform_activity("running", 10)
    print(get_cur_health())
    print(get_cur_hedons(), "\n")

    perform_activity("textbooks", 30)
    print(get_cur_health())
    print(get_cur_hedons(), "\n")

    perform_activity("running", 20)
    print(get_cur_health())
    print(get_cur_hedons(), "\n")

    perform_activity("textbooks", 40)
    print(get_cur_health())
    print(get_cur_hedons(), "\n")

    initialize()

    offer_star("running")

    perform_activity("running", 20)
    print(get_cur_health())            # 60 = 20 * 3
    print(get_cur_hedons(), "\n")      # using star, 30 = 30 + 20 - 20

    perform_activity("running", 140) # tired
    print(get_cur_health()) # 60 + 140 x 3 = 480
    print(get_cur_hedons(), "\n") # 30 -140 x 2 = -250

    perform_activity("running", 10)
    print(get_cur_health()) # 480 + 30 = 510
    print(get_cur_hedons(), "\n") # -250 - 20 = -270

    perform_activity("running", 20)
    print(get_cur_health()) # 510 + 10 x 3 + 10 x 1 = 550
    print(get_cur_hedons(), "\n")  # -270 - 60 = -310

    '''
    initialize()
    perform_activity("textbooks", 70)
    print(get_cur_health())
    print(get_cur_hedons())
    perform_activity("textbooks", 60)
    print(get_cur_health())
    print(get_cur_hedons())
    print(most_fun_activity_minute())
    offer_star("textbooks")
    perform_activity("textbooks", 80)
    print(get_cur_health())
    print(get_cur_hedons())
    #offer_star("running")
    offer_star("textbooks")
    perform_activity("textbooks", 30)
    print(get_cur_health())
    print(get_cur_hedons())
    perform_activity("textbooks", 120)
    print(get_cur_health())
    print(get_cur_hedons())
    perform_activity("running", 20)
    print(get_cur_health())
    print(get_cur_hedons())
    perform_activity("textbooks", 110)
    print(get_cur_health())
    print(get_cur_hedons())
    offer_star("textbooks")
    perform_activity("textbooks", 30)
    print(get_cur_health())
    print(get_cur_hedons())
    perform_activity("running", 80)
    print(get_cur_health())
    print(get_cur_hedons())
    perform_activity("running", 110)
    print(get_cur_health())
    print(get_cur_hedons())
    offer_star("textbooks")
    perform_activity("textbooks", 110)
    print(get_cur_health())
    print(get_cur_hedons())
    perform_activity("textbooks", 10)
    print(get_cur_health())
    print(get_cur_hedons())
    perform_activity("running", 110)
    print(get_cur_health())
    print(get_cur_hedons())
    offer_star("textbooks")
    print("here")
    perform_activity("running", 130)
    print(get_cur_health())
    print(get_cur_hedons())
    perform_activity("resting", 120)
    print(get_cur_health())
    print(get_cur_hedons())
    offer_star("textbooks")
    perform_activity("textbooks", 40)
    print(get_cur_health())
    print(get_cur_hedons())
    perform_activity("textbooks", 40)
    print(get_cur_health())
    print(get_cur_hedons())
    perform_activity("running", 90)
    print(get_cur_health())
    print(get_cur_hedons())
    perform_activity("running", 140)
    print(get_cur_health())
    print(get_cur_hedons())
    perform_activity("running", 80)
    print(get_cur_health())
    print(get_cur_hedons())
    print(most_fun_activity_minute())