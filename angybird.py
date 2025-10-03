import pygame as pg
import pymunk as pm
import pymunk.pygame_util
import time 

# blablabla
pg.init()
screen = pg.display.set_mode((800, 600))
pg.display.set_caption("Scary birds :-o ")
clock = pg.time.Clock()
pg.mixer.init()
hitsound = pg.mixer.Sound("scream-85294.wav")
hitsound.set_volume(1.0)
running = True

#   physics setup
space = pm.Space()
space.gravity = (0, 900)

#   the ground          (0,0) top-left (800,0) top-right (0,600) bottom-left (800,600) bottom-right
ground = pm.Segment(space.static_body, (0, 555), (800, 555), 5) # x1y1 x2y2 mdraws the line along x axis and then thickness
ground.friction = 1
ground.elasticity = 1
space.add(ground)

#   the guy
massa = 2
radiusa = 15
momenta = pm.moment_for_circle(massa, 0, radiusa)
ballbod = pm.Body(massa, momenta)
ballbod.position = (150, 420)

ball = pm.Circle(ballbod, radiusa)
ball.elasticity = 0.7
ball.friction = 0.6
space.add(ballbod, ball) 

#   mouse
mousebod = pm.Body(body_type=pm.Body.KINEMATIC)
drag_joint = None

draw_options = pm.pygame_util.DrawOptions(screen)

#   target
massb = 1
radiusb = 15
momentb = pm.moment_for_circle(massb, 0, radiusb)
targbod = pm.Body(massb, momentb)
targbod.position = (600, 500)

target = pm.Circle(targbod, radiusb)
target.elasticity = 0.7
target.friction = 0.6
space.add(targbod, target) 

# slingshot
slingshot_anchor = pm.Body(body_type=pm.Body.STATIC)
slingshot_anchor.position = (150, 400)

slingshot_spring = pm.DampedSpring(
    slingshot_anchor, ballbod,
    (0, 0),  # anchor point of anchor
    (0, 0),  # attachment point on ball
    rest_length=50,
    stiffness=500,
    damping=10
)

# collision callback
def targ_hit(arbiter, space, data):
    print("hit")
    hitsound.play()
    return True

ball.collision_type = 1
target.collision_type = 2

space.on_collision(1, 2, post_solve=targ_hit)

space.add(slingshot_spring)
spring_added = True

def handle_physics(event):
    global drag_joint
    global running
    if event.type == pg.QUIT:
        running = False
    if event.type == pg.MOUSEBUTTONDOWN:
        if event.button == 1:  # left click
                mouse_pos = pm.pygame_util.from_pygame(event.pos, screen)
                if ball.point_query(mouse_pos).distance <= 0:  # clicked on ball shape
                    print("picked up")
                    drag_joint = pm.PivotJoint(ballbod, mousebod, (0,0), (0,0))
                    drag_joint.max_force = 75000
                    space.add(drag_joint)
                
    if event.type == pg.MOUSEBUTTONUP:
        if event.button == 1 and drag_joint is not None:
            print("released")
            space.remove(drag_joint)
            drag_joint = None
            
    if event.type == pg.MOUSEMOTION:
        mouse_pos = pm.pygame_util.from_pygame(event.pos, screen)
        mousebod.position = mouse_pos

while running:
    for event in pg.event.get():
        handle_physics(event)

    screen.fill((144, 182, 232))
    space.step(1/60)

    xa, ya = int(ballbod.position.x), int(ballbod.position.y)
    xb, yb = int(targbod.position.x), int(targbod.position.y)
    birdsprite = pg.draw.circle(screen, (255,0,0), (xa, ya), radiusa) # bird
    pigsprite = pg.draw.circle(screen, (50, 255, 20), (xb, yb), radiusb)
    grndsprite = pg.draw.rect(screen, (125, 65, 35), pg.Rect(0, 550, 800, 50)) # ground
    if slingshot_spring is not None:
        ropesprite = pg.draw.line(screen, (139,69,19), slingshot_anchor.position, ballbod.position, 5)
    slingshotsprite = pg.draw.rect(screen, (20, 40, 0), pg.Rect(145, 400, 10, 150)) # slingshot

    vec =  ballbod.position - slingshot_anchor.position
    if spring_added and vec.length < 20 and drag_joint is None:
        space.remove(slingshot_spring)
        spring_added = False

    pg.display.flip()
    clock.tick(60)
pg.quit()
