import score

#time_remaining = score.something1
#time_to_end = score.something2

# Import activities into the activities dictionary
activities = []
itinerary = []

# ----------

# Helper functions
def transportation():
    '''Adds a transportation activity.'''

def update(current_location, time_):
    '''Updates current time & location after an activity is added.'''
    time_remaining -= act.time + t_act.time

# Main loop
while time_remaining > time_to_end:
    best_score = -100 # set to lowest score

    for activity in activities:
        current_score = score(act)
        activities[act] = current_score
        if current_score > best_score:
            best_score = current_score
            best_act = act

    t_act = transportation()
    itinerary.append(best_act)
    update(current_location, current_time)
