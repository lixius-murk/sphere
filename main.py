import os
import sys
import pygame
from lazyeye import LazyEye
from bltype import blType

def main():
    m = LazyEye(blType.Achromatopsia)
    
    m.run()  

# class ModulOne():
#     def __init__(self, bl_: blType):
#         self.bl = bl_
    
#     def run(self):
#         pygame.init()
#         display = (800, 600)
#         pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
#         gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
#         glTranslatef(0.0, 0.0, -50)
#         glEnable(GL_NORMALIZE)
#         glEnable(GL_DEPTH_TEST)
#         init_lighting()

#         bound_sz = 20.0
#         speed = 5.0
#         cur_radius = 2.0
#         ball_position = [0, 0, 0]
#         ball_speed = [0.05*speed, 0*speed, 0.03*speed]
#         bounds = [-bound_sz, bound_sz, -bound_sz, bound_sz]

#         start_time = time.time()
#         clock = pygame.time.Clock()

#         while True:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     return
            
#             set_background_color(self.bl)
#             glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
#             cur_time = time.time() - start_time

#             ball_position[0] += ball_speed[0]
#             ball_position[2] += ball_speed[2]

#             if ball_position[0] < bounds[0] or ball_position[0] > bounds[1]:
#                 ball_speed[0] = -ball_speed[0]
#             if ball_position[2] < bounds[2] or ball_position[2] > bounds[3]:
#                 ball_speed[2] = -ball_speed[2]

#             cur_color = calc_cur_color(self.bl, ball_position, bound_sz, cur_time)
#             ball_position[1] = cur_radius - 1

#             glPushMatrix()
#             glRotatef(90, bound_sz/2, 0, 0)
#             #draw_ground(bound_sz + 5.0, self.bl)
            
#             draw_ball(ball_position, cur_radius, cur_color)
#             glPopMatrix()

#             pygame.display.flip()
#             clock.tick(60)
            


if __name__ == "__main__":
    main()


if sys.path[0] in ("", os.getcwd()):
    sys.path.pop(0)

if __package__ == "":
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, path)