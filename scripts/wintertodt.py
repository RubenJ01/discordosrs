import random
import time
from apscheduler.schedulers.background import BackgroundScheduler


class WinterTodt:
    def __init__(self):
        self.wait_time = None
        self.wintertodt_game_time = None
        self.points_earned = None
        self.firemaking_level = None
        self.woodcutting_level = None
        self.bruma_roots = None
        self.burning_bruma_roots = None
        self.chopping_bruma_roots = None
        self.firemaking_xp_earned = None
        self.woodcutting_xp_earned = None

    def initialize_game(self):
        self.wait_time = random.choice([45, 50, 55, 60, 65, 70, 75, 80, 85, 90])
        self.wintertodt_game_time = random.choice([300, 310, 320])
        self.points_earned = 0
        self.firemaking_level = 50
        self.woodcutting_level = 50
        self.bruma_roots = 0
        self.burning_bruma_roots = False
        self.chopping_bruma_roots = True
        self.firemaking_xp_earned = 0
        self.woodcutting_xp_earned = 0

    def event(self):
        if self.chopping_bruma_roots:
            xp_earned = int((self.woodcutting_level * 0.3) * 2)
            print(f"You chop 2 more bruma roots and add them to your inventory earning you "
                  f"{xp_earned} woodcutting experience.")
            self.bruma_roots += 2
            self.woodcutting_xp_earned += xp_earned
            if self.bruma_roots == 20:
                self.burning_bruma_roots = True
                self.chopping_bruma_roots = False
        if self.burning_bruma_roots:
            # this means that the player still has bruma roots in their inventory
            xp_earned = (self.firemaking_level * 3) * 2
            print(f"You add 2 bruma roots to the fire earning you 20 points and {xp_earned} firemaking experience.")
            self.bruma_roots -= 2
            self.points_earned += 20
            self.firemaking_xp_earned += xp_earned
            if self.bruma_roots == 0:
                self.burning_bruma_roots = False
                self.chopping_bruma_roots = True

    def start_game(self):
        self.initialize_game()
        sched = BackgroundScheduler()
        t_end = time.time() + self.wintertodt_game_time + 1
        sched.add_job(self.event, 'interval', seconds=5)
        sched.start()
        while time.time() < t_end:
            pass
        xp_earned = 100 * self.firemaking_level
        self.firemaking_xp_earned += xp_earned
        print(f"The wintertodt has been subdued earning you an additional {xp_earned} firemaking experience. \n")
        print(f"You earned a total of {self.firemaking_xp_earned} firemaking experience and "
              f"{self.woodcutting_xp_earned} woodcutting experience with a total of {self.points_earned} points.")
        sched.shutdown()



wintertodt = WinterTodt()
wintertodt.start_game()
