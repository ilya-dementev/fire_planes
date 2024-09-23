from typing import List

import matplotlib.pyplot as plt
import numpy as np
from math import sqrt

FIELD_SIDE = 1000.0
VIEW_DISTANCE = 50

def shape_crop():
    pass

def shape_split():
    pass

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Track():
    def __init__(self, x1, y1, x2, y2):
        self.p1 = Point(x1, y1)
        self.p2 = Point(x2, y2)
    def xarr(self):
        return [self.p1.x, self.p2.x]
    def yarr(self):
        return [self.p1.y, self.p2.y]

class Stripe():
    def __init__(self, x1, y1, x2, y2):
        # make bottom and top tracks from central one
        # x1_top = x1
        # y1_top = y1
        # x2_top = x2
        # y2_top = y2
        
        # x1_bot = x1
        # y1_bot = y1
        # x2_bot = x2
        # y2_bot = y2

        self.tcnt = Track(x1, y1, x2, y2)

        self.isvert = False
        if (x1 - x2) == 0:
            self.isvert = True

        # create two tracks - top and bottom - from central one
        k_cnt = 0.0
        
        dx_cnt = self.tcnt.p1.x - self.tcnt.p2.x
        # print(f"m_dx = {m_dx}, n_dx = {n_dx}")

        # check track is not || to y axis
        if dx_cnt != 0.0:
            k_cnt = (self.tcnt.p1.y - self.tcnt.p2.y) / dx_cnt
        # print(f"km = {km}, kn = {kn}")
        
        #TODO add vert check
        b_cnt = self.tcnt.p1.y - self.tcnt.p1.x * k_cnt
        # print(f"bm = {bm}, bn = {bn}")

        b_add = VIEW_DISTANCE * sqrt( 1 + k_cnt * k_cnt)
        b_1 = b_cnt + b_add
        b_2 = b_cnt - b_add
        if b_1 >= b_2:
            b_top = b_1
            b_bot = b_2
        else:
            b_top = b_2
            b_bot = b_1
        ############

        # Check for each FIELD_SIDE of field wheather top/bottom lines are crossed with it
        # If so - use cross-points as tracks definition
        
        if self.isvert:
            #      p2_top   p2_bot
            #  ____.________.________
            # |                      |
            # |                      |
            # |    p1_top   p1_bot   |   
            # |____.________.________|

            # inetrnal logical definition for vertical lines: top X is less than bot X
            b_top = x1 - VIEW_DISTANCE
            b_bot = x1 + VIEW_DISTANCE
            
            if b_top >= FIELD_SIDE:
                x1_top = FIELD_SIDE
                x2_top = FIELD_SIDE
            elif b_top <= 0:
                x1_top = 0
                x2_top = 0
            else: # regular point
                x1_top = b_top
                x2_top = b_top

            if b_bot >= FIELD_SIDE:
                x1_bot = FIELD_SIDE
                x2_bot = FIELD_SIDE
            elif b_bot <= 0:
                x1_bot = 0
                x2_bot = 0
            else: # regular point
                x1_bot = b_bot
                x2_bot =b_bot
            
            y1_top = 0
            y2_top = FIELD_SIDE
            y1_bot = 0
            y2_bot = FIELD_SIDE
        else:
            pass

        self.ttop = Track(x1_top, y1_top, x2_top, y2_top)
        self.tbot = Track(x1_bot, y1_bot, x2_bot, y2_bot)


def is_point_on_square(x, y):
    if (x > FIELD_SIDE) or (x < 0) or\
       (y > FIELD_SIDE) or (y < 0):
        # print("1")
        return False
    if x!= FIELD_SIDE and x!= 0:
        if y!= FIELD_SIDE and y!= 0:
            # print(f"2 x={x} y={y}")
            return False
    if y!= FIELD_SIDE and y!= 0:
        if x!= FIELD_SIDE and x!= 0:
            # print("3")
            return False
    return True


def read_input() -> List[Stripe]:
    sl = []
    # sl.append(Stripe(10, 0, 100, FIELD_SIDE))
    # sl.append(Stripe(990, 0, 900, FIELD_SIDE))
    # sl.append(Stripe(0, 500, FIELD_SIDE, 500))
    # sl.append(Stripe(0, 50, FIELD_SIDE, 800))

    raw_sl = [\
        [10, 0, 100, FIELD_SIDE],
        [990, 0, 900, FIELD_SIDE],
        [0, 500, FIELD_SIDE, 500],
        [0, 50, FIELD_SIDE, 800]
    ]
    for r in raw_sl:
        if is_point_on_square(r[0], r[1]) and is_point_on_square(r[2], r[3]):
            sl.append(Stripe(r[0], r[1], r[2], r[3]))
        else:
            print(f"input error: some track point is not on a square: ({r[0]}, {r[1]}, {r[2]}, {r[3]})")
    return sl

def are_tracks_crossed(tm: Track, tn: Track):
    is_crossed = False

    km = 0.0
    kn = 0.0
    m_dx = tm.p1.x - tm.p2.x
    n_dx = tn.p1.x - tn.p2.x
    print(f"m_dx = {m_dx}, n_dx = {n_dx}")

    # check track is not || to y axis
    if m_dx != 0.0:
        km = (tm.p1.y - tm.p2.y) / m_dx
    if n_dx != 0.0:
        kn = (tn.p1.y - tn.p2.y) / n_dx
    print(f"km = {km}, kn = {kn}")

    if (km == kn) and m_dx != 0 and n_dx != 0:
        return (False, 0, 0) # 2 tracks are || but not || to y axis
    
    if m_dx == 0 and n_dx == 0:
        return (False, 0, 0) # 2 tracks || to y axis
    
    bm = tm.p1.y - tm.p1.x * km    
    bn = tn.p1.y - tn.p1.x * kn
    print(f"bm = {bm}, bn = {bn}")

    if m_dx == 0:
        xcross = tm.p1.x
    elif n_dx == 0:
        xcross = tn.p1.x
    else:
        xcross = (bn - bm) / (km - kn)
    
    ycross = km * xcross + bm

    if \
        (xcross <= max(tm.p1.x, tm.p2.x)) and (xcross >= min(tm.p1.x, tm.p2.x)) and \
        (ycross <= max(tm.p1.y, tm.p2.y)) and (ycross >= min(tm.p1.y, tm.p2.y)) and \
        (xcross <= max(tn.p1.x, tn.p2.x)) and (xcross >= min(tn.p1.x, tn.p2.x)) and \
        (ycross <= max(tn.p1.y, tn.p2.y)) and (ycross >= min(tn.p1.y, tn.p2.y)):
        is_crossed = True

    return (is_crossed, xcross, ycross)

# TODO implement
def is_shape_inFIELD_SIDE_stripe() -> bool:
    pass

# TODO implement
def get_single_point(shape: List[Point]) -> Point:
    return Point(0,0)

def main():

    start_shape = [Point(0,0), Point(0, FIELD_SIDE), Point(FIELD_SIDE, FIELD_SIDE), Point(FIELD_SIDE, 0)]
    unchecked = [start_shape]

    stripes = []
    stripes = read_input()

    print(unchecked)
    print(unchecked[0][0].y)

    for stripe in stripes:
        for shape in unchecked:
            stripe_shape_crosses = 0
            print(f"shape len = {len(shape)}")
            for i in range(0, len(shape)): # loop over all shape points
                plt.plot(shape[i].x, shape[i].y, marker="o")

                if i < len(shape) - 1:
                    shape_track = Track(shape[i].x, shape[i].y, shape[i+1].x, shape[i+1].y)
                elif i == (len(shape) - 1):
                    shape_track = Track(shape[i].x, shape[i].y, shape[0].x, shape[0].y)
                
                (crt, xct, yct) = are_tracks_crossed(shape_track, stripe.ttop)
                if crt:
                    stripe_shape_crosses += 1
                    print(f"cross of top track: x={xct} y={yct}")
                (crb, xcb, ycb) = are_tracks_crossed(shape_track, stripe.tbot)
                if crb:
                    stripe_shape_crosses += 1
                    print(f"cross of bot track: x={xcb} y={ycb}")

            print(f"crosses: {stripe_shape_crosses}")
            if stripe_shape_crosses in (0):
                if is_shape_inFIELD_SIDE_stripe():
                    # remove shape
                else:
                    # stripe does not affect this shape
                    pass
            if stripe_shape_crosses in (1):
                # stripe touches the shape
                # NOTE this is tricky place. If poin is touched - we must remove it by the challenge definition.
                # But what point will be the boundary now????? We suppose not to remove the point
                pass
            elif stripe_shape_crosses in (2, 3):
                shape_crop()
            elif stripe_shape_crosses == 4: # in cross checking do check that 2 points are not equal (touch a corner)
                shape_split()
            else:
                print("ERROR cannot be [{stripe_shape_crosses}] crosses")
        
        plt.grid(True)
        plt.show()

    OK = True
    if len(unchecked) >= 1:
        OK = False
        for shape in unchecked:
            if len(shape) >=3:
                p = get_single_point(shape)


# T = [\
#     [0, 1, 1,    0,   2,   9,  0, 0],
#     [1, 9, 2.7, 11, 2.6,  12,  3, 1],
#     [2, 4, 0,    4,   0,   4,  0, 6]
#     ]

# for row in T:
#     t1 = Track(row[0], row[1], row[2], row[3])
#     t2 = Track(row[4], row[5], row[6], row[7])
#     (isc, xc, yc) = are_tracks_crossed(t1, t2)
#     print(f"result = {isc}, {xc}, {yc}")
#     plt.plot(t1.xarr(), t1.yarr(), marker="o")
#     plt.plot(t2.xarr(), t2.yarr(), marker="o")
#     plt.plot(xc, yc, marker="o")

# plt.grid(True)
# plt.show()


main()
