class Event:
    """
    時間表現を含むできごと
    """
    def __init__(self,id:int,bnst:int,time_text:str,time_value:int,person_id:int=-1,person_text="",act_ids=[],act_texts=[]) -> None:
        self.id=id
        self.bnst=bnst
        self.time_text=time_text
        self.time_value=time_value
        self.person_id=person_id
        self.person_text=person_text
        self.act_ids=act_ids
        self.act_texts=act_texts