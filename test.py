import os

src = os.path.abspath(__file__)

dst = "C:\Users\USER\Desktop\chzzkbangon\ab.txt"
os.link(src, dst)