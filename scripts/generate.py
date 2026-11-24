#!/usr/bin/env python3
import json, os, pathlib, urllib.request, urllib.parse, re
USER = "arnavsharma294-png"
FILE = pathlib.Path(__file__).resolve().parents[1] / "assets" / "scoreboard.svg"
def api(path):
    headers = {"Accept":"application/vnd.github+json","User-Agent":"cricket-profile"}
    if os.getenv("GH_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GH_TOKEN"]
    with urllib.request.urlopen(urllib.request.Request("https://api.github.com"+path,headers=headers),timeout=30) as r:
        return json.load(r)
repos=[]
page=1
while True:
    batch=api(f"/users/{USER}/repos?per_page=100&type=owner&page={page}")
    repos.extend(r for r in batch if not r["fork"] and not r["private"])
    if len(batch)<100: break
    page+=1
prs=api("/search/issues?q="+urllib.parse.quote("author:"+USER+" is:pr")+"&per_page=1")["total_count"]
values=[len(repos),prs,sum(r["stargazers_count"] for r in repos)]
s=FILE.read_text()
for x,v in zip((53,445,837),values):
    s=re.sub(r'(<text x="'+str(x)+r'" y="180"[^>]*>)[^<]*(</text>)',lambda m:m[1]+str(v)+m[2],s)
FILE.write_text(s)
