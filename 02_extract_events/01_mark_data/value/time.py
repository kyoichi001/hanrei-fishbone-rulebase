class Time:
    def __init__(self,year:int=0,month:int=0,day:int=0) -> None:
        self.year=year
        self.month=month
        self.day=day
    def value(self)->int:
        return self.year*10000+self.month*100+self.day