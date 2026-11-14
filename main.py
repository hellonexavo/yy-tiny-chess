import json
import os
import sys
import urllib.error
import urllib.request
ENV_URL = os.environ.get("MAKEFUN_ENV_URL") or sys.exit("MAKEFUN_ENV_URL is not set")
VALUE = {"p": 1, "n": 3, "b": 3, "r": 5, "q": 9, "k": 100}
def post(path, body):
    req = urllib.request.Request(
        ENV_URL + path,
        data=json.dumps(body).encode(),
        headers={"content-type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req) as res:
            return json.load(res)
    except urllib.error.HTTPError as e:
        sys.exit(f"{path}: HTTP {e.code} {e.read().decode(errors='replace')}")
def board_of(fen):
    board = {}
    for i, row in enumerate(fen.split()[0].split("/")):
        file = 0
        for c in row:
            if c.isdigit():
                file += int(c)
            else:
                board["abcdefgh"[file] + str(8 - i)] = c
                file += 1
    return board
def choose(fen, legal):
    board = board_of(fen)
    side = fen.split()[1]
    own = str.isupper if side == "w" else str.islower
    enemy = str.islower if side == "w" else str.isupper
    weights = {"p":100,"n":320,"b":330,"r":500,"q":900,"k":20000}
    def attacks(b, sq, piece):
        x,y = "abcdefgh".index(sq[0]),int(sq[1])-1
        kind=piece.lower(); white=piece.isupper()
        directions=[]
        if kind=="p": directions=[(1,1 if white else -1),(-1,1 if white else -1)]
        if kind=="n": directions=[(i,j) for i,j in ((1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1))]
        if kind in "bq": directions += [(1,1),(1,-1),(-1,1),(-1,-1)]
        if kind in "rq": directions += [(1,0),(-1,0),(0,1),(0,-1)]
        if kind=="k": directions=[(i,j) for i in (-1,0,1) for j in (-1,0,1) if i or j]
        out=set()
        for dx,dy in directions:
            xx,yy=x+dx,y+dy
            while 0<=xx<8 and 0<=yy<8:
                dest="abcdefgh"[xx]+str(yy+1);out.add(dest)
                if dest in b or kind in "pnk":break
                xx+=dx;yy+=dy
        return out
    def threat(b, sq, predicate):
        return [weights[p.lower()] for loc,p in b.items() if predicate(p) and sq in attacks(b,loc,p)]
    def evaluate(move):
        src,dst=move[:2],move[2:4]
        piece=board[src]; victim=board.get(dst)
        if piece.lower()=="p" and src[0]!=dst[0] and victim is None:victim="p"
        gain=weights[victim.lower()] if victim else 0
        promo=weights[move[4]]-100 if len(move)==5 else 0
        before=threat(board,src,enemy)
        after=dict(board);after.pop(src)
        if piece.lower()=="p" and src[0]!=dst[0] and dst not in board:
            after.pop(dst[0]+src[1],None)
        after[dst]=piece.upper() if len(move)==5 and own(piece) and side=="w" else (piece.lower() if len(move)==5 else piece)
        attackers=threat(after,dst,enemy)
        defenders=threat(after,dst,own)
        risk=0
        if attackers:
            risk=weights[piece.lower()] * (0.95 if not defenders else 0.45)
            if min(attackers)<weights[piece.lower()]:risk=weights[piece.lower()]*0.95
        saved=weights[piece.lower()]*0.3 if before else 0
        x="abcdefgh".index(dst[0]);y=int(dst[1])-1
        center=(3.5-abs(x-3.5))+(3.5-abs(y-3.5))
        advance=(y if side=="w" else 7-y)
        positional=(center*5 if piece.lower() in "nb" else center*2)
        if piece.lower()=="p":positional+=advance*3
        if piece.lower()=="k":positional-=center*3
        return gain+promo-risk+saved+positional
    return max(sorted(legal),key=evaluate)
while True:
    g = post("/game", {})
    if g["status"] == "done":
        break
    while g["status"] == "your_move":
        g = post("/move", {"game": g["game"], "move": choose(g["fen"], g["legal_moves"])})
    print(f"game {g['game']}: {g['outcome']} by {g['reason']}", file=sys.stderr)
print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost", file=sys.stderr)
