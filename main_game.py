from MyClasses import *

# Number of sessions <= 4
number_of_sessions = 1
# Number of lanes <= 5
number_of_lanes = 5
my_displayhelper = DisplayHelper(number_of_sessions)
session_list = []

for i in range(number_of_sessions):
    session_list.append(GameSession(number_of_lanes=number_of_lanes, draw=True, player_type='qlearner'))

while any([session.live for session in session_list]):
    events = pygame.event.get()
    for session in session_list:
        if session.live:
            session.get_state()
            session.gameloop(events)
            my_displayhelper.draw_on_screen(session.get_surface(), session.session_id)
    pygame.display.flip()

pygame.quit()
quit()
