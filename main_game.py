from MyClasses import *

number_of_sessions = 4
my_displayhelper = DisplayHelper(number_of_sessions)
session_list = []
for i in range(number_of_sessions):
    session_list.append(GameSession(draw=True))

while any([session.live for session in session_list]):
    events = pygame.event.get()
    for session in session_list:
        if session.live:
            session.gameloop(events)
            my_displayhelper.draw_on_screen(session.get_surface(), session.session_id)
    pygame.display.flip()

pygame.quit()
quit()
