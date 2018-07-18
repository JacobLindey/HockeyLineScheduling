
class Line:

    def __init__(self, ln, gd=0, fl=1, toi=0, tob=0):
        self.line_num = ln
        self.goal_differential = gd
        self.fatigue_level = fl
        self.toi = toi
        self.tob = tob
        self.on_ice = False

    def __str__(self):
        return "LINE: {ln:1d} |::| gd: {gd:5.3f}, fl: {fl:6.4f}, comb: {comb:6.4f} toi: {toi:5d}, " \
               "tob: {tob:5d}, on_ice: {oi}".format(ln=self.line_num, gd=self.goal_differential, fl=self.fatigue_level,
                                                    comb=self.fatigue_level*self.goal_differential, toi=self.toi, tob=self.tob,
                                                    oi=self.on_ice)

    def copy(self):
        temp_line = Line(self.line_num)
        temp_line.goal_differential = self.goal_differential
        temp_line.fatigue_level = self.fatigue_level
        temp_line.toi = self.toi
        temp_line.tob = self.tob
        temp_line.on_ice = self.on_ice
        return temp_line

    def set_line(self, gd, fl=1, toi=0, tob=0):
        self.goal_differential = gd
        self.fatigue_level = fl
        self.toi = toi
        self.tob = tob

    def calc_fatigue(self, interval):
        """
        Determines which readiness function to use and passes control
        :param interval: the length of time that has passed
        :return: None
        """
        if self.on_ice:
            self.fatigue_level = self.fatigue(interval)
        else:
            self.fatigue_level = self.recovery(interval)

    def recovery(self, interval, x_f=300):
        """
        Linear place holder TODO
        :param interval:
        :param x_f:
        :return:
        """
        r = self.fatigue_level + interval / x_f
        if r > 1:
            r = 1
        return r

    def fatigue(self, interval, x_f=70):
        """
        Linear place holder TODO
        :param interval:
        :param x_f:
        :return:
        """
        r = self.fatigue_level - interval / x_f
        if r < 0:
            r = 0
        return r

