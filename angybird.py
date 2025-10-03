import pygame as pg
import pymunk as pm
import pymunk.pygame_util

#blablabla
pg.init()
screen = pg.display.set_mode((800, 600))
pg.display.set_caption("Scary birds :-o ")
clock = pg.time.Clock()

#   physics setup
space = pm.Space()
space.gravity = (0, 900)

#   the ground          (0,0) top-left (800,0) top-right (0,600) bottom-left (800,600) bottom-right
ground = pm.Segment(space.static_body, (0, 555), (800, 555), 5)#x1y1 x2y2 mdraws the line along x axis and then thickness
ground.friction = 1
ground.elasticity = 1
space.add(ground)

#   the guy
mass = 1
radius = 15
moment = pm.moment_for_circle(mass, 0, radius)
ballbod = pm.Body(mass, moment)
ballbod.position = (150, 400)

ball = pm.Circle(ballbod, radius)
ball.elasticity = 0.7
ball.friction = 0.6
space.add(ballbod, ball) 

#   mouse
mousebod = pm.Body(body_type=pm.Body.KINEMATIC)
drag_joint = None

draw_options = pm.pygame_util.DrawOptions(screen)

#   slingshot
slingshot_anchor = pymunk.Body(body_type=pymunk.Body.STATIC)
slingshot_anchor.position = (150, 400)

slingshot_spring = pymunk.DampedSpring(
    slingshot_anchor, ballbod,
    (0, 0),  # anchor point of anchor
    (0, 0),  # attachment point on ball
    rest_length=50,
    stiffness=500,
    damping=10
)

space.add(slingshot_spring)


running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                mouse_pos = pymunk.pygame_util.from_pygame(event.pos, screen)
                if ball.point_query(mouse_pos).distance <= 0:  # clicked on ball shape
                    print("picked up")
                    drag_joint = pymunk.PivotJoint(ballbod, mousebod, (0,0), (0,0))
                    drag_joint.max_force = 75000
                    space.add(drag_joint)
                
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1 and drag_joint is not None:
                
                print("released")
                space.remove(slingshot_spring)
                slingshot_spring = None
            
        if event.type == pg.MOUSEMOTION:
            mouse_pos = pymunk.pygame_util.from_pygame(event.pos, screen)
            mousebod.position = mouse_pos

        if event.type == pg.MOUSEBUTTONUP and drag_joint is not None:
            space.remove(drag_joint)
            drag_joint = None

    screen.fill((144, 182, 232))
    space.step(1/60)

    x, y = int(ballbod.position.x), int(ballbod.position.y)
    pg.draw.circle(screen, (255,0,0), (x, y), radius)
    pg.draw.rect(screen, (125, 65, 35), pg.Rect(0, 550, 800, 50))
    pg.draw.line(screen, (139,69,19), slingshot_anchor.position, ballbod.position, 5)
    pg.draw.rect(screen, (20, 40, 0), pg.Rect(145, 400, 10, 150))

    pg.display.flip()
    clock.tick(60)
pg.quit()