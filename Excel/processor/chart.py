from pyecharts import Kline
from pyecharts import Scatter, Overlap
from action import Attitude

class Chart():
    def __init__(self):
        self.history_map = {}
        self.date_list = []
    
    def draw_kline(self, days, history, path):        
        self.date_list = days
        candies = []
        x = []
        sc = Scatter() 
        bear_points = []
        bull_points = []
        unknown_points = []
        for h in history:
            mark = Attitude(h["mark"])
            description = "{} {} {}@{}".format(h["action"], h["description"], h["quantity"], h["price"])
            if mark == Attitude.BEAR:
                bear_points.append([h["date"], h["real_price"], description])
            elif mark == Attitude.BULL:
                bull_points.append([h["date"], h["real_price"], description])
            else:
                unknown_points.append([h["date"], h["real_price"], description])
            if h["date"] not in self.history_map:
                self.history_map[h["date"]] = []
            self.history_map[h["date"]].append(h)
            
        self._add_scatter(sc, bear_points, "bear")
        self._add_scatter(sc, bull_points, "bull")
        self._add_scatter(sc, unknown_points, "unknown")
        
        for day in days:
            candy = [day["open"], day["close"], day["low"], day["high"], day["date"]]
            candies.append(candy)
            key = day["date"].replace("-", "")
            x.append(key)
            if key in self.history_map:
                hs = self.history_map[key]
                i = 5
                for h in hs:
                    candy.append("")
                    candy[i]= "{} {} {}@{}".format(h["action"], h["description"], h["quantity"], h["price"])
                    i += 1

                       
        def _tooltip_formatter(params):
            str = ""
            for i in range(5, len(params[0].data)):
                str += params[0].data[i] + "<br/>"
            #str.append("o {} c {} l {} h {}".format(params[0].data[1], params[0].data[2], params[0].data[3], params[0].data[4]))
            str += "o:" + params[0].data[1] + "<br/>c:" + params[0].data[2]+ "<br/>l:" + params[0].data[3]+ "<br/>h:" + params[0].data[4]
            return (str)
        
        kline = Kline("K")
        kline.add(
            "day K",
            x,
            candies,
            is_datazoom_show=True,
            tooltip_formatter=_tooltip_formatter,
            tooltip_font_size=14,
            
        )
        
        overlap = Overlap(width=1800, height=900)
        overlap.add(kline)
        overlap.add(sc)
    
        overlap.render(path)
        
    def _add_scatter(self, sc, points, name):      
        x_lst = [v[0] for v in points]
        y_lst = [v[1] for v in points]
        extra_data = [v[2] for v in points]
        sc.add(
            name,
            x_lst,
            y_lst,
            extra_data=extra_data,
        )