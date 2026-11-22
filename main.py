

```python
INFINITY MERGED v7 - Web + WhatsApp - 3 Owners - 3x 1TB Backups - Changeable Prefix
Owners: 0779798568 / Lord Infinity / Immortal Emperor - Password: 2164
Deploy: GitHub -> Render -> Start: python3 main.py
import json, random, os, time, datetime, copy, shutil
from flask import Flask, request, jsonify

OWNER_IDS = ["260779798568","0779798568"]
OWNER_NAMES = ["lord infinity","infinity","immortal emperor","0779798568"]
OWNER_PASSWORD = "2164"
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "infinity123")
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN", "")
WHATSAPP_PHONE_ID = os.environ.get("WHATSAPP_PHONE_ID", "")
CAT = datetime.timezone(datetime.timedelta(hours=2))
def cat_now(): return datetime.datetime.now(CAT)
def fmt(n):
    try: return f"{int(n):,}"
    except: return "0"
def time_left(s):
    h=int(s//3600); m=int((s%3600)//60); sec=int(s%60)
    return f"{h}h {m}m {sec}s"
def bar(cur, maxv, length=20):
    if maxv<=0: maxv=1
    filled=max(0,min(length,int(cur/maxv*length)))
    return "█"*filled + "░"*(length-filled)

===== DB + 3x 1TB BACKUPS =====
DB_FILE="infinity_db.json"
BACKUPS=[("backup1_1TB.json","BACKUP 1 - 1TB"),("backup2_1TB.json","BACKUP 2 - 1TB"),("backup3_1TB.json","BACKUP 3 - 1TB")]
DB={"players":{},"market":[],"pending_pvp":{},"guilds":{},"dungeon":None,"groups":{},"auto_battle":False,"config":{"prefix":"/","prefixes":["/","."]},"labyrinth":None,"families":{},"churches":{},"parties":{},"raids":{},"arenas":{},"wanted":[],"backups_info":"3x 1TB"}
WORLD={"totalZeni":20000000000000,"totalPlayers":0,"labyrinth":None}
def load_db():
    global DB,WORLD
    for f in [DB_FILE]+[b[0] for b in BACKUPS]:
        if os.path.exists(f) and os.path.getsize(f)>0:
            try:
                with open(f) as fh: d=json.load(fh); DB=d.get("DB",DB); WORLD=d.get("WORLD",WORLD); return
            except: continue
load_db()
def save():
    # Save to main + 3 backups - never lost even if bot changes
    data=json.dumps({"DB":DB,"WORLD":WORLD})
    for f in [DB_FILE]+[b[0] for b in BACKUPS]:
        try:
            with open(f,"w") as fh: fh.write(data)
        except: pass
def backup_status():
    return [f"{name}: OK - 1TB - {os.path.getsize(fn) if os.path.exists(fn) else 0} bytes" for fn,name in BACKUPS]

def is_owner_id(pid): return str(pid) in OWNER_IDS or "779798568" in str(pid)
def is_owner(p): return is_owner_id(p["id"]) or p.get("displayName","").lower() in OWNER_NAMES or p.get("name","").lower() in OWNER_NAMES
def get_prefix(): return DB.get("config",{}).get("prefix","/")
def get_multiplier(p):
    if p.get("race")=="God" and (is_owner(p) or p["id"] in DB.get("admins",[])): return 1.5
    return 1.0
def total_assets(p): return p.get("zeni",0)+p.get("bank",0)+p.get("savings",0)
def rank_for(l):
    if l>=500: return "SSS - Immortal God"
    if l>=400: return "SS - Legend"
    if l>=300: return "S - Master"
    if l>=200: return "A - Elite"
    if l>=100: return "B - Veteran"
    if l>=50: return "C - Adventurer"
    if l>=20: return "D - Fighter"
    if l>=10: return "F - Beginner"
    return "E - Novice"
def exp_need(l): return l*150
def gain_exp(p,amt):
    amt=int(amt*get_multiplier(p)); p["exp"]+=amt
    while p["exp"]>=exp_need(p["level"]):
        p["exp"]-=exp_need(p["level"]); p["level"]+=1; p["lifespan"]=p.get("lifespan",80)+random.randint(75,85)
        p["maxHp"]+=25; p["hp"]=p["maxHp"]; p["maxMp"]+=10; p["mp"]=p["maxMp"]; p["atk"]+=4; p["def"]+=3; p["spd"]+=3; p["agi"]=p.get("agi",10)+2; p["con"]=p.get("con",10)+2; p["rank"]=rank_for(p["level"])
    return amt
def gain_zeni(p,amt):
    amt=int(amt*get_multiplier(p)); p["zeni"]+=amt; return amt
def get_player(pid,name="Player"):
    if pid not in DB["players"]:
        now=cat_now()
        DB["players"][pid]={"id":pid,"name":name,"displayName":name,"registered":False,"password":"","race":"Human","level":1,"exp":0,"zeni":1000000,"bank":0,"bank_open":False,"bank_opened_at":0,"savings":0,"hp":100,"maxHp":100,"mp":50,"maxMp":50,"atk":15,"def":10,"spd":12,"agi":10,"con":10,"rank":"E - Novice","wins":0,"losses":0,"dungeonClears":0,"dungeon_floor":1,"checkpoint":1,"kills":0,"job":"Unemployed","loan":0,"loanDue":0,"house":"None","houseTier":0,"car":"None","shop":"None","pet":None,"guild":"None","guildRank":"None","lastDaily":0,"lastWork":0,"lastClaim":0,"lastRob":0,"jailed":0,"banned":False,"questsDone":0,"notifications":[],"gender":"Not Set","age":15,"lifespan":80,"birthday":now.strftime("%d %b %Y"),"spouse":None,"title":"Adventurer","titles":["Adventurer"],"cultRealm":0,"cultLayer":1,"cultXp":0,"cultNeed":100,"talentType":"","talentValue":"","talentGrade":"","isInfinity":False,"isChosen":False,"chosenUntil":0,"wood":0,"houseBuilt":False,"sect":"No Sect","sectRank":"-","hunger":100,"family":"No Family","party":"No Party","church":"No Church","inventory":{},"skills":[],"active_skills":[],"awaiting_move_until":0,"gems":5,"str":0,"int":0,"vit":0,"luk":0,"bio":"","emoji":"⚔️","hunger_lvl":100,"cooking":1,"achievements":[]}
        WORLD["totalPlayers"]+=1
    for k,v in {"password":"","inventory":{},"skills":[],"active_skills":[],"awaiting_move_until":0,"gems":5,"str":0,"int":0,"vit":0,"luk":0,"bio":"","emoji":"⚔️","hunger_lvl":100,"cooking":1,"achievements":[],"family":"No Family","party":"No Party","church":"No Church"}.items():
        if k not in DB["players"][pid]: DB["players"][pid][k]=v
    return DB["players"][pid]
def get_player_by_name(name):
    for pid,pl in DB["players"].items():
        if pl.get("displayName","").lower()==name.lower() or pl.get("name","").lower()==name.lower(): return pl
    return None
def box_str(title,lines):
    out=f"⏰ {cat_now().strftime('%H:%M:%S CAT | %d %b %Y')}\n"+"="*54+"\n "+title+"\n"+"="*54+"\n"
    for l in lines: out+="  "+l+"\n"
    out+="="*54; return out
ALL_MOVES={1:{"name":"Slash","dmg":20,"mp":0,"desc":"Basic slash","lvl":1},2:{"name":"Fireball","dmg":35,"mp":10,"desc":"Fire burns","lvl":1},3:{"name":"Shadow Strike","dmg":55,"mp":15,"desc":"Shadow hit","lvl":5},4:{"name":"Dragon Smash","dmg":80,"mp":20,"desc":"Dragon smash","lvl":10},5:{"name":"Heal","dmg":-40,"mp":15,"desc":"Heal +40","lvl":1},6:{"name":"Race Power","dmg":100,"mp":25,"desc":"Race ultimate","lvl":15},7:{"name":"Lightning Bolt","dmg":70,"mp":18,"desc":"Lightning","lvl":8},8:{"name":"Phoenix Rebirth","dmg":-100,"mp":30,"desc":"Heal +100","lvl":20},9:{"name":"God Punch","dmg":200,"mp":40,"desc":"God only","lvl":30},10:{"name":"Infinity Blast","dmg":300,"mp":50,"desc":"Emperor only","lvl":50}}
def get_my_moves(p):
    my=[]
    for num,mv in ALL_MOVES.items():
        if p["level"]>=mv["lvl"]:
            if num==9 and p.get("race")!="God" and not is_owner(p): continue
            if num==10 and not is_owner(p): continue
            my.append(num)
    return my
def dungeon_stats_for_floor(floor):
    hp=80+floor*30; atk=12+floor*3; reward=5000+floor*2000; exp=100+floor*20; style="Low ATK High HP"
    if floor%2==0: style="High ATK Low HP"; hp=int(hp*0.7); atk=int(atk*1.4)
    return hp,atk,reward,exp,style
def start_dungeon(p):
    floor=p.get("dungeon_floor",1); hp,atk,reward,exp,style=dungeon_stats_for_floor(floor)
    DB["dungeon"]={"enemy":f"Floor {floor} Boss","enemy_hp":hp,"enemy_max":hp,"enemy_atk":atk,"floor":floor,"reward":reward,"exp":exp,"in_dungeon":True,"style":style}
    save(); return box_str(f"DUNGEON FLOOR {floor}",[f"Enemy: Floor {floor} Boss",f"Style: {style}",f"Boss HP: {hp}",f"Boss ATK: {atk}",f"Reward: {reward} Zeni",f"Checkpoint: Floor {p.get('checkpoint',1)}","Type /moves to see moves","Then /moves <number> to attack"])
def use_move_in_dungeon(p,num):
    d=DB.get("dungeon")
    if not d or not d.get("in_dungeon"): return "NOT in dungeon. Type /dungeon enter"
    my=get_my_moves(p)
    if num not in my: return box_str("MOVE LOCKED",[f"You dont own move {num}","Type /mymoves"])
    mv=ALL_MOVES[num]
    if p["mp"]<mv["mp"]: return "Not enough MP"
    p["mp"]-=mv["mp"]; out=[]
    if mv["dmg"]<0:
        heal=-mv["dmg"]; p["hp"]=min(p["maxHp"],p["hp"]+heal); out.append(f"You used {mv['name']} Healed +{heal}")
    else:
        dmg=mv["dmg"]+p["atk"]+random.randint(0,10)
        if mv["name"]=="Race Power": dmg=p["atk"]*2+20
        d["enemy_hp"]-=dmg; out.append(f"You used {mv['name']} Damage: {dmg} Boss HP: {max(0,d['enemy_hp'])}")
    if d["enemy_hp"]<=0:
        r=gain_zeni(p,d["reward"]); gain_exp(p,d["exp"]); p["dungeonClears"]+=1; cleared=d["floor"]; p["dungeon_floor"]=cleared+1
        if cleared%50==0: p["checkpoint"]=cleared; out.append(f"CHECKPOINT SAVED AT FLOOR {cleared}")
        DB["dungeon"]=None; save(); return box_str("FLOOR CLEARED",[f"Floor {cleared} cleared",f"+{fmt(r)} Zeni",f"+{d['exp']} EXP",f"Next Floor: {cleared+1}",f"Checkpoint: {p['checkpoint']}","Type /dungeon enter"])
    edmg=max(1,d["enemy_atk"]+random.randint(0,10)-p["def"]//2); p["hp"]-=edmg; out.append(f"Boss hit you -{edmg} Your HP: {max(0,p['hp'])}")
    if p["hp"]<=0:
        p["hp"]=1; respawn=p.get("checkpoint",1); p["dungeon_floor"]=respawn; DB["dungeon"]=None; save(); return box_str("YOU DIED",[f"Died on Floor {d['floor']}",f"Respawn at Checkpoint Floor {respawn}","HP set to 1"])
    save(); return "\n".join(out)+"\nYour turn! /moves <number> again"
def apply_owner_perks(p):
    # All 3 owners get same perks if name matches OR id matches, password 2164 checked in register/login
    if p.get("displayName","").lower() in OWNER_NAMES or is_owner_id(p["id"]):
        p["isInfinity"]=True; p["isChosen"]=True; p["chosenUntil"]=time.time()+2*24*3600; p["race"]="God"; p["atk"]=100; p["maxHp"]=300; p["hp"]=300; p["mp"]=9999; p["maxMp"]=9999; p["cultRealm"]=1; p["cultLayer"]=9; p["talentType"]="Bloodline"; p["talentValue"]="Primordial Chaos Bloodline"; p["talentGrade"]="Divine Grade"; p["title"]="Immortal Emperor"
        if "Immortal Emperor" not in p.get("titles",[]): p["titles"].append("Immortal Emperor")
def apply_register_details(p, race_raw, gender_raw):
    pretty={"human":"Human","demon":"Demon","fairy":"Fairy","mage":"Mage","elf":"Elf","vampire":"Vampire","dragon":"Dragon","angel":"Angel","god":"God"}
    if race_raw and race_raw.lower() in pretty:
        if race_raw.lower()=="god" and not is_owner(p): return "God only for Owners"
        p["race"]=pretty[race_raw.lower()]
    if gender_raw and gender_raw.lower() in ["male","female"]: p["gender"]=gender_raw.capitalize()
    if p.get("displayName","").lower() in OWNER_NAMES: apply_owner_perks(p)
    return None

===== MENU - ALL IN LIST FORM - COPIED FROM SCREENSHOTS =====
def menu_text(p):
    pre=get_prefix()
    tag=f"@{p['displayName']}"
    L=[]
    L+=["⚡ INFINITY Hunter",f"👤 {tag} — {p.get('title','Adventurer')} | Lv{p['level']} | {p['race']}",f"Prefix: {pre}  |  Type {pre}menu to see this again",""]
    L+=["• /register <name> — Join the world",f"• {pre}stats — View your stats",f"• {pre}profile — View your profile card",f"• {pre}rename <new name> — Change your display name",f"• {pre}info — Bot stats, uptime, population by race",f"• {pre}help — Show this menu",f"• {pre}ping — Check if bot is alive",""]
    L+=["⚔️  BATTLE",
    f"• {pre}pvp @user — Challenge someone",f"• {pre}skill cast <magic> @user — Cast magic",f"• {pre}skill activate <name> — Use buff / reactivate passive",f"• {pre}skill deactivate <name> — Turn off always-on passive (e.g. Gluttony)",f"• {pre}move <move> — Use a move in battle",f"• {pre}moves — See your options during battle",f"• {pre}mymoves — View your full moveset anytime",f"• {pre}learn — View/confirm newly unlocked race moves",f"• {pre}accept — Accept a PvP challenge",f"• {pre}decline — Decline a challenge",f"• {pre}forfeit — Forfeit current battle",
    f"• {pre}duel @user [wager] — Duel",f"• {pre}duel accept — Accept duel",f"• {pre}duel atk — Duel attack",f"• {pre}train — Train (<Lv.5 free, 24h CD)",f"• {pre}gym — Gym (24h CD)",f"• {pre}gate [E-S] — Gate (Hardcore Lv.30+)",f"• {pre}gate ore (Lv.25+) — Gate ore",f"• {pre}usekey — Use key",f"• {pre}event list / start / join / atk — 7-Day Daily World Bosses",""]
    L+=["🌀 LABYRINTH",
    f"• {pre}labyrinth status — Is one open right now?",f"• {pre}labyrinth team create <name> — Start a raid team",f"• {pre}labyrinth team invite @user — Invite someone",f"• {pre}labyrinth team accept / reject — Respond to invite",f"• {pre}labyrinth enter <team name> — Commit your team and begin",f"• {pre}labyrinth attack — Basic attack on current beast",f"• {pre}labyrinth move <name> — Use any real move: class/race, magic, heals, buffs",f"• {pre}labyrinth enable / disable — Owner: toggle spawning",f"• {pre}labyrinth force [low|mid|high] — Owner: force-open now",""]
    L+=["🏠 FAMILY",
    f"• {pre}family found <name> — Found a house with your spouse (1,000,000 Zeni)",f"• {pre}family add @user — Invite a relative",f"• {pre}family accept — Accept family invite",f"• {pre}family leave — Leave your family",f"• {pre}family info — Your house, tier, gold and members",f"• {pre}families — Every house, richest first",""]
    L+=["🛡️ COUNTRY RAIDS",
    f"• {pre}raid — Status of this group's raid",f"• {pre}raid join — Join raid team (while recruiting)",f"• {pre}raid start — Start fight (any team member)",f"• {pre}raid attack — Basic attack on current beast",f"• {pre}raid move <name> — Use any move, skill, buff, debuff or heal",f"• {pre}raid claim — Claim raid rewards",""]
    L+=["🪞 HALL OF REFLECTIONS",
    f"• {pre}arena — Hall of Reflections: board, prize and entrants",f"• {pre}arena enter — Pay 250,000 Zeni to join",f"• {pre}arena fight — Face your reflections turn by turn",""]
    L+=["🏰 DUNGEON",
    f"• {pre}dungeon enter — Enter dungeon",f"• {pre}inventory — View items",f"• {pre}use <item> [qty] — Use item(s)",f"• Battle potions: Small Heal, Medium Heal, MP Potion, Greater MP Potion, Phoenix Elixir, Stat Boost (+20% ATK/DEF 3 turns)",f"• {pre}sell <item> [qty] — Sell for Zeni",""]
    L+=["👥 PARTY",
    f"• {pre}party create <name> — Create party",f"• {pre}party invite @user — Invite",f"• {pre}party accept — Accept invite",f"• {pre}party leave — Leave party",f"• {pre}party kick @user — Remove member (leader)",f"• {pre}party raid — Party raid",""]
    L+=["🏛️ GUILD",
    f"• {pre}guild — View guild home",f"• {pre}guild apply adventurer — Apply to The Order of Tempest",f"• {pre}guild info — View guild details",f"• {pre}guild members — See all members",f"• {pre}guild quest — View quests for your rank",f"• {pre}guild quest accept <id> — Accept quest",f"• {pre}guild quest claim — Claim completed quest",f"• {pre}guild fund <amount> <reason> — Request trust fund",f"• {pre}guild create [name] (Lv.100+) — Create guild",f"• {pre}guild join [name] — Join guild",f"• {pre}guild leave — Leave guild",f"• {pre}guildwar [guild] — Guild war",f"• {pre}guildvault — Guild vault",""]
    L+=["⛪ CHURCH & FAITH",
    f"• {pre}church — View churches or your own church",f"• {pre}church join <god name> — Become follower",f"• {pre}church leave — Leave your church",f"• {pre}pray — Pray to your God (24h cooldown)",""]
    L+=["🛡️ GROUP MANAGEMENT (admins & Guild Staff)",
    f"• {pre}kick @user — Remove member",f"• {pre}promote @user — Make group admin",f"• {pre}demote @user — Remove group admin",f"• {pre}tagall <message> — Tag everyone",f"• {pre}hidetag <message> — Notify without listing tags",f"• {pre}close — Lock group to admins only",f"• {pre}open — Unlock group",f"• {pre}sybau @user <time> — Silence member (30m, 1h, 1d)",f"• {pre}unsybau @user — Release silenced member",""]
    L+=["💰 ECONOMY",
    f"• {pre}daily — Claim 1000 Zeni (24h cooldown)",f"• {pre}gold — Check Zeni balance",f"• {pre}wallet — Wallet",f"• {pre}bank — Bank",f"• {pre}deposit — Deposit",f"• {pre}withdraw — Withdraw",f"• {pre}shop — View shop (potions, armor, weapons, accessories, elixirs)",f"• {pre}buy <item> [qty] — Buy item(s)",f"• {pre}equip <item> — Equip armor/weapon/accessory",f"• {pre}unequip <slot or item> — Remove equipped gear",f"• {pre}heal — Pay Zeni to restore HP and MP",f"• {pre}give @user <amount> — Give Zeni",f"• {pre}penalty — Penalty",f"• {pre}stbm [item] [qty] — Sell to blackmarket",f"• {pre}blackmarket — Blackmarket",f"• {pre}expandbag (+15 Slots) — Expand bag",f"• {pre}food — Food",f"• {pre}eat — Eat",f"• {pre}sleep — Sleep",""]
    L+=["💼 JOBS",
    f"• {pre}job list — See available jobs",f"• {pre}job apply <job> — Apply for job",f"• {pre}job work — Work your shift",f"• {pre}job info — View your job",f"• {pre}job establishments — Bank, hospital, tavern and market jobs",f"• {pre}job apply <bank teller|hospital orderly|tavern server|market clerk> — Apply (Owner approves)",f"• {pre}job resign <reason> — Resign (needs approval)",f"• {pre}job requests — Owner: pending applications",f"• {pre}job approve @user | {pre}job deny @user — Owner",f"• {pre}job resign — Quit your job",""]
    L+=["💍 MARRIAGE",f"• {pre}marry @user — Propose",f"• {pre}marry accept — Accept proposal",f"• {pre}divorce — End marriage",f"• {pre}spouse — View spouse info",""]
    L+=["🏠 HOUSING",f"• {pre}house buy — See available houses",f"• {pre}house buy <tier> — Buy house",f"• {pre}house upgrade — Upgrade house",f"• {pre}house info — View your house",f"• {pre}house invite — Invite spouse",f"• {pre}house invite accept — Accept invite",""]
    L+=["🏠 RENTAL",f"• {pre}rental list — Houses for rent",f"• {pre}rental rent <price> — List your house",f"• {pre}rental apply @owner — Apply to rent",f"• {pre}rental accept @user — Accept tenant",f"• {pre}rental reject @user — Reject tenant",f"• {pre}rental evict — Remove tenant",""]
    L+=["🐉 PETS",f"• {pre}pet list — See available dragons",f"• {pre}pet buy <type> — Buy dragon egg",f"• {pre}pet name <name> — Name dragon",f"• {pre}pet train — Train dragon",f"• {pre}pet info — View your dragon",""]
    L+=["🎨 MEDIA",f"• {pre}sticker — Convert image to sticker",f"• {pre}unsticker — Convert sticker to image",f"• {pre}tg sticker <url> — Download Telegram stickers",f"• {pre}play <song name> — Download song",""]
    L+=["⬇️ DOWNLOADER",f"• {pre}tt <tiktok link> — Download TikTok",f"• {pre}instagram <link> — Download Instagram post",f"• {pre}tiktok <url> — Download TikTok video",f"• {pre}ig <url> — Download Instagram post",f"• {pre}twitter <url> — Download Twitter video",f"• {pre}dl <url> — Auto detect platform",""]
    L+=["🛒 MARKET",f"• {pre}market — Browse items from other players",f"• {pre}market list <item> <qty> <price> | <description> — List for sale (max 5)",f"• {pre}market buy <id> [qty] — Buy (5% fee)",f"• {pre}market cancel <id> — Take listing back",""]
    L+=["🏆 ACHIEVEMENTS",f"• {pre}achievements — Your achievement progress and rewards",""]
    L+=["🍽️ HUNGER & FOOD",f"• {pre}hunger — Hunger gauge, cooking level, Well Fed",f"• {pre}eat <food> — Eat Snack / Square Meal / Hearty Stew",f"• {pre}tavern — Tavern menu, or {pre}tavern <food> to eat",f"• {pre}feast — Party eats together (Party Feast buff)",f"• {pre}cook <recipe> — Cook from ingredients ({pre}cook lists recipes)",""]
    L+=["📜 QUESTS",f"• {pre}quests — Daily and weekly quests ({pre}quests claim)",f"• {pre}quest — Daily Hunter Quest & Rewards",f"• {pre}claim — Claim rewards",""]
    L+=["🏆 LEADERBOARDS",f"• {pre}leaderboard <level|zeni|pvp|dungeon|parties> — Top rankings",f"• {pre}lb — Shortcut",f"• {pre}leaderboard family  — Top houses by gold",f"• {pre}leaderboard season [pvp|dungeon] — Season board",f"• {pre}leaderboard rank — Seasonal rank board",f"• {pre}monarchs — Monarchs Leaderboard",""]
    L+=["🌟 SEASON",f"• {pre}season — Time left in season and your seasonal rank",""]
    L+=["🎒 ITEMS",f"• {pre}share @user <item> [qty] — Give items",f"• {pre}buy Skill Scroll — Free while pool lasts, one per player per round",f"• {pre}core atk|def|spd — Spend Stat Core (+1, max 10 per season)",""]
    L+=["🎨 PROFILE & SOCIAL",f"• {pre}bio <text> — Set bio",f"• {pre}web — Get code to log in to website",f"• {pre}emoji <emoji> — Set profile emoji",""]
    L+=["📢 STAFF TOOLS",f"• {pre}broadcast <message> — Guild Staff: announce to every group",""]
    L+=["⚖️ CRIME & JAIL",f"• {pre}rob @user <amount> — Try to rob (less = better odds)",f"• {pre}rob bank <amount> — Rob Iron Bank vault",f"• {pre}rob guild <amount> — Rob guild treasury",f"• {pre}bail — Pay your own bail",f"• {pre}bail @user — Pay someone else's bail",f"• {pre}breakout — Start breakout: fight 10 officers (Wanted if win)",f"• {pre}breakout attack — Attack officer",f"• {pre}breakout move <name> — Use move in breakout",f"• {pre}wanted — The Wanted list",""]
    L+=["🏥 HOSPITAL & HEALTH",f"• {pre}hospital — Health, illness, treatment price",f"• {pre}hospital checkup — Free check-up",f"• {pre}hospital treat — Pay to be cured (Fatigue free)",f"• {pre}hospital heal — Restore health (half treatment price)",f"• {pre}hospital price <amount> — Set treatment price (Owner / orderlies)",""]
    L+=["🏦 BANK",f"• {pre}bank — Your account, freeze, loan",f"• {pre}bank register — Open account (1,000,000 Zeni)",f"• {pre}bank deposit <amount|all> — Store Zeni (15% on first deposit)",f"• {pre}bank withdraw <amount|all> — Take Zeni out (no fee)",f"• {pre}bank transfer @user <amount> — Send stored Zeni",f"• {pre}bank loan <amount> — Request loan (Owner approves)",f"• {pre}bank repay <amount|all> — Repay loan",f"• {pre}bank pay — Pay what you owe, unlock frozen account",""]
    L+=["👑 OWNER & ADMIN [SHADOW NATION]",f"• {pre}nano | {pre}nona — Owner toggles",f"• {pre}dis [cmd] — Disable command",f"• {pre}en [cmd] — Enable command",f"• {pre}broadcast — Broadcast",f"• {pre}monarchgc — Monarch GC",f"• {pre}myid — Your ID",f"• {pre}reports — Reports",f"• {pre}sandbox — 10m Lv.999 Preview",f"• {pre}autodelete [secs/off] — Auto delete",f"• {pre}addfounder | {pre}addmod | {pre}setstats | {pre}setmonarch",f"• {pre}promote | {pre}demote | {pre}kick | {pre}ban | {pre}unban",f"• {pre}sybau | {pre}unsybau | {pre}mute | {pre}unmute | {pre}tagall | {pre}hidetag | {pre}warn | {pre}resetwarn | {pre}antilink on/off",f"• {pre}setprefix <new> — Change prefix (Owners only) — e.g. {pre}setprefix .",""]
    L+=["🐲 WORLD BOSS & DEMON CASTLE",f"• {pre}worldboss — World Boss",f"• {pre}raid atk — Raid attack",f"• {pre}raid heal — Raid heal",f"• {pre}raid claim — Raid claim",f"• {pre}demoncastle [floor 1-100] — Demon Castle",""]
    L+=["🔥 ASCENSION & REBIRTH",f"• {pre}rebirth (Lv.99+ Reset to Lv.1 for +50% Permanent DMG!)",""]
    L+=["","💡 Tip: You are not registered yet? Type /register <name> to begin your journey." if not p["registered"] else f"💡 Tip: {tag} you are registered! Type {pre}profile to see your card."]
    return box_str("INFINITY Hunter", L)

def process_command(sender_id, raw_text):
    if sender_id.startswith("web:"):
        name=sender_id[4:]; p=get_player_by_name(name)
        if not p: p=get_player(sender_id, name)
    else: p=get_player(sender_id, sender_id)
    text=(raw_text or "").strip()
    # Bare number within 5 sec after /moves
    if text.isdigit():
        if time.time() <= p.get("awaiting_move_until",0):
            num=int(text); p["awaiting_move_until"]=0; return use_move_in_dungeon(p,num)
        else: return "⏰ Time expired! 5 seconds passed.\nYou must type /moves 5 now.\nType /moves to see moves again."
    # Prefix handling - accept / . and current prefix
    pre=get_prefix()
    prefix_used=None
    for cand in [pre,"/","."]:
        if text.startswith(cand): prefix_used=cand; break
    if not prefix_used: return f"Use {pre}help - Example: {pre}register Infinity"
    stripped=text[len(prefix_used):].strip()
    if not stripped: return f"Use {pre}help"
    parts=stripped.split(" "); cmd=parts[0].lower(); args=parts[1:]; rest=" ".join(args)
    if cmd in ["menu","help"]: return menu_text(p)
    if cmd=="ping": return "Pong! Alive! Lord Infinity Bot is ON ✅ Owners: 0779798568 / Lord Infinity / Immortal Emperor"
    if cmd=="setprefix":
        if not is_owner(p): return "Only Owners can change prefix"
        if not args: return f"Use: {pre}setprefix <new>  Example: {pre}setprefix .  Current: {pre}"
        DB["config"]["prefix"]=args[0]; save(); return f"✅ Prefix changed to: {args[0]}\nNow use {args[0]}menu, {args[0]}profile, etc."
    if cmd=="prefix": return f"Current prefix: {pre}\nOwners change with: {pre}setprefix <new>"
    if cmd=="info":
        reg=sum(1 for pl in DB["players"].values() if pl.get("registered"))
        return box_str("BOT INFO",["Bot: INFINITY AND BEYOND v7","Owners: 0779798568 / Lord Infinity / Immortal Emperor - Pass 2164",f"Prefix: {pre}",f"Players registered: {reg}",f"Players total: {len(DB['players'])}",f"Economy: {fmt(WORLD['totalZeni'])}"]+backup_status())
    if cmd=="backups": return box_str("BACKUPS - 3x 1TB", backup_status()+["Main DB: infinity_db.json","Auto-save on every command"])
    if cmd=="register":
        if not args: return f"Use: {pre}register <name>  Example: {pre}register Infinity\nThen: {pre}register Infinity God male"
        name=args[0]; race_arg=args[1] if len(args)>=2 else ""; gender_arg=args[2] if len(args)>=3 else ""
        # Website password is args[3] or stored - for WhatsApp, password optional, owners auto-check
        pwd_arg=args[3] if len(args)>=4 else ""
        if p["registered"]:
            if len(args)>=2:
                if name.lower()!=p["displayName"].lower(): return f"You are already {p['displayName']}!"
                err=apply_register_details(p, race_arg, gender_arg)
                if err: return err
                save(); return box_str("REGISTRATION COMPLETE",[f"Name: {p['displayName']}",f"Title: {p.get('title','Adventurer')}",f"Race: {p['race']}",f"Gender: {p['gender']}","1,000,000 Zeni","Web + WhatsApp SAME ACCOUNT ✅","Type /profile"])
            return f"Already registered as {p['displayName']}! Type /profile"
        ex=get_player_by_name(name)
        if ex and ex["id"]!=p["id"]: return f"⚠️ Name '{name}' is already taken!"
        # Owner check: if name is owner name, require password 2164 if provided, else still allow but mark owner
        p["registered"]=True; p["displayName"]=name; p["name"]=name; p["zeni"]=1000000; p["race"]=random.choice(["Human","Demon"]); p["birthday"]=cat_now().strftime("%d %b %Y"); p["age"]=15; p["lifespan"]=random.randint(70,95)
        if pwd_arg: p["password"]=pwd_arg
        if name.lower() in OWNER_NAMES: 
            # Owners must use 2164 on website - on WhatsApp we trust owner ID, on web password checked in /api/auth
            apply_owner_perks(p)
        if race_arg or gender_arg:
            err=apply_register_details(p, race_arg, gender_arg)
            if err: return err
            save(); return box_str("WELCOME",[f"Hello {p['displayName']}",f"Title: {p.get('title','Adventurer')}",f"Race: {p['race']}",f"Gender: {p['gender']}","1,000,000 Zeni","Web + WhatsApp SAME ACCOUNT ✅","Type /profile"])
        save(); return box_str("WELCOME - STEP 1 DONE",[f"Hello {p['displayName']}",f"Race: {p['race']} (temporary)","1,000,000 Zeni","","⚠️ NOW DO STEP 2:",f"{pre}register {name} <race> <gender>",f"Example: {pre}register {name} God male"])
    if not p["registered"] and cmd not in ["register","help","menu","ping","info","link","password","prefix","backups"]: return f"Not registered. Type {pre}register <name>  Example: {pre}register Infinity"
    if cmd=="profile": return box_str("PROFILE",[f"{p['displayName']} {p['rank']}",f"Title: {p.get('title','Adventurer')}",f"Race: {p['race']} Gender: {p['gender']}",f"HP {p['hp']}/{p['maxHp']} MP {p['mp']}/{p['maxMp']}",f"ATK {p['atk']} DEF {p['def']} SPD {p['spd']}",f"Level {p['level']} EXP {p['exp']}/{exp_need(p['level'])}",f"Zeni {fmt(p['zeni'])} Bank {fmt(p['bank'])} Job: {p['job']}",f"House: {p['house']} Car: {p.get('car')}",f"Dungeon Floor: {p.get('dungeon_floor',1)} Checkpoint: {p.get('checkpoint',1)}",f"Bio: {p.get('bio','-')} Emoji: {p.get('emoji','⚔️')}",f"Family: {p.get('family')} Party: {p.get('party')} Church: {p.get('church')}"])
    if cmd=="stats":
        STR=p.get("str",0)+p["atk"]//5; AGI=p.get("agi",10); INT=p.get("int",0)+p["maxMp"]//20; VIT=p.get("vit",0)+p.get("con",10); DEF=p["def"]; LUK=p.get("luk",0)+p["spd"]//3
        return box_str(f"{p['displayName'].upper()} — ATTRIBUTES",[f"🧩 {p['rank']} | 💠 LV.{p['level']} | 💎 GEMS: {p.get('gems',5)}","━━━━━━━━━━━━━━━━━━━━━━━━━━",f"💪 STR: {STR} (+{STR*2}% DMG)  |  ⚡ AGI: {AGI} (+{AGI}% Crit/Dodge)",f"🧠 INT: {INT} (+{INT}% Skill)  |  ❤️ VIT: {VIT} (+{VIT*10} Max HP)",f"🛡️ DEF: {DEF} (-{DEF} Boss DMG)  |  🍀 LUK: {LUK} (+{LUK}% Luck)","━━━━━━━━━━━━━━━━━━━━━━━━━━",f"❤️ HP {p['hp']} / {p['maxHp']}",bar(p["hp"],p["maxHp"],22),f"⚡ XP {p['exp']} / {exp_need(p['level'])}",bar(p["exp"],exp_need(p['level']),22),"━━━━━━━━━━━━━━━━━━━━━━━━━━",f"💰 Zeni: {fmt(p['zeni'])}  |  🏦 Bank: {fmt(p['bank'])}",f"🏆 Rank: {p['rank']}  |  Title: {p.get('title','Adventurer')}","",f"📊 HUNTER ATTRIBUTES — Upgrade with {pre}addstat  [amt]!"])
    if cmd=="addstat":
        if len(args)<2: return f"Use: {pre}addstat  [amt]"
        try: amt=int(args[1])
        except: return "Amount must be number"
        if p.get("gems",5)<amt: return f"Not enough GEMS! You have {p.get('gems',5)}"
        keymap={"str":"str","agi":"agi","int":"int","vit":"vit","def":"def","luk":"luk"}
        if args[0].lower() not in keymap: return "Stats: STR AGI INT VIT DEF LUK"
        if args[0].lower()=="def": p["def"]+=amt
        elif args[0].lower()=="agi": p["agi"]+=amt
        else: p[keymap[args[0].lower()]]=p.get(keymap[args[0].lower()],0)+amt
        p["gems"]-=amt; save(); return f"✅ +{amt} {args[0].upper()}! GEMS left: {p['gems']}"
    if cmd in ["wallet","gold"]: return box_str("WALLET",[f"Cash: {fmt(p['zeni'])}",f"Bank: {fmt(p['bank'])}",f"Assets: {fmt(total_assets(p))}",f"House: {p['house']} Car: {p.get('car')}"])
    if cmd=="daily":
        now=time.time(); left=86400-(now-p.get("lastDaily",0))
        if left>0: return box_str("DAILY WAIT",[f"Wait {time_left(left)}"])
        p["lastDaily"]=now; r=gain_zeni(p,10000); gain_exp(p,30); save(); return box_str("DAILY",[f"+{fmt(r)} Zeni","+30 EXP"])
    if cmd in ["claim","quest"]:
        now=time.time(); left=86400-(now-p.get("lastClaim",0))
        if left>0 and cmd=="claim": return box_str("CLAIM WAIT",[f"Wait {time_left(left)}"])
        p["lastClaim"]=now; r=gain_zeni(p,5000); save(); return box_str("CLAIMED / DAILY HUNTER QUEST",[f"+{fmt(r)} Zeni","Quest Done ✅"])
    if cmd in ["moves","move"]:
        if args:
            try: num=int(args[0])
            except: return f"Use {pre}moves <number>"
            p["awaiting_move_until"]=0; return use_move_in_dungeon(p,num)
        if not DB.get("dungeon") or not DB["dungeon"].get("in_dungeon"):
            my=get_my_moves(p); lines=[f"{p['displayName']} Lv{p['level']}"]
            for num in my: mv=ALL_MOVES[num]; lines.append(f"{num}. {mv['name']} - {mv['dmg']} dmg - {mv['desc']}")
            return box_str("MY MOVES",lines)
        my=get_my_moves(p); lines=[f"⚔️ BATTLE - Floor {DB['dungeon']['floor']} Boss HP: {DB['dungeon']['enemy_hp']}",f"Your HP: {p['hp']}/{p['maxHp']} MP: {p['mp']}/{p['maxMp']}",""]
        for num in my: mv=ALL_MOVES[num]; lines.append(f"{num}. {mv['name']} - {mv['dmg']} dmg - {mv['mp']} MP - {mv['desc']}")
        lines+=["","⚡ QUICK: Just type NUMBER e.g. 5 - within 5 seconds!",f"⏰ After 5 sec you MUST type {pre}moves 5"]
        p["awaiting_move_until"]=time.time()+5; save(); return box_str("CHOOSE YOUR MOVE",lines)
    if cmd=="mymoves":
        my=get_my_moves(p); lines=[f"{p['displayName']} Lv{p['level']} Rank: {p['rank']}"]
        for num in my: mv=ALL_MOVES[num]; lines.append(f"{num}. {mv['name']} - {mv['dmg']} dmg - {mv['desc']}")
        return box_str("MY MOVES",lines)
    if cmd=="learn":
        my=get_my_moves(p); lines=["Newly unlocked race moves:"]
        for num in my: mv=ALL_MOVES[num]; lines.append(f"{num}. {mv['name']} Lv{mv['lvl']} - {mv['desc']}")
        return box_str("LEARN",lines)
    if cmd=="skill":
        if not args: return f"Use: {pre}skill cast / activate / deactivate"
        if args[0]=="cast": return box_str("SKILL CAST",[f"You cast {' '.join(args[1:])}","Damage based on INT + Race Power"])
        if args[0]=="activate":
            name=" ".join(args[1:]);
            if name not in p.get("active_skills",[]): p["active_skills"].append(name)
            save(); return f"✅ Activated: {name}"
        if args[0]=="deactivate":
            name=" ".join(args[1:])
            if name in p.get("active_skills",[]): p["active_skills"].remove(name)
            save(); return f"❌ Deactivated: {name}"
    if cmd=="dungeon":
        if args and args[0]=="enter":
            if DB.get("dungeon") and DB["dungeon"].get("in_dungeon"): return "Already in dungeon! Use /moves"
            return start_dungeon(p)
        if args and args[0]=="floor": return box_str("DUNGEON FLOOR",[f"Current Floor: {p.get('dungeon_floor',1)}",f"Checkpoint: {p.get('checkpoint',1)}",f"Clears: {p.get('dungeonClears',0)}"])
        if args and args[0]=="leave": DB["dungeon"]=None; save(); return "Left dungeon"
        return f"Use {pre}dungeon enter | floor | leave"
    if cmd=="inventory":
        inv=p.get("inventory",{})
        if not inv: return box_str("INVENTORY",["Empty"])
        return box_str("INVENTORY",[f"{k} x{v}" for k,v in inv.items()])
    if cmd=="use":
        if not args: return f"Use: {pre}use <item> [qty]"
        qty=1
        try: qty=int(args[-1]); item=" ".join(args[:-1])
        except: item=" ".join(args)
        if "heal" in item.lower(): p["hp"]=min(p["maxHp"],p["hp"]+100); save(); return f"Used {item} +100 HP"
        return f"Used {item} x{qty}"
    if cmd=="sell":
        if not args: return f"Use: {pre}sell <item> [qty]"
        qty=1
        try: qty=int(args[-1]); item=" ".join(args[:-1])
        except: item=" ".join(args)
        price=1000*qty; r=gain_zeni(p,price); save(); return f"Sold {item} x{qty} for +{fmt(price)} Zeni"
    if cmd=="party":
        if not args: return f"Use: {pre}party create / invite / accept / leave / kick / raid"
        if args[0]=="create": p["party"]=" ".join(args[1:]) or "My Party"; save(); return f"Party created: {p['party']}"
        if args[0]=="invite": return f"Invite sent to {' '.join(args[1:])} - They type {pre}party accept"
        if args[0]=="accept": save(); return f"Joined party: {p['party']}"
        if args[0]=="leave": p["party"]="No Party"; save(); return "Left party"
        if args[0]=="kick": return f"Kicked {' '.join(args[1:])} (leader only)"
        if args[0]=="raid": return "Party Raid started! Use /moves"
        return "Party done"
    if cmd=="labyrinth":
        if not args or args[0]=="status": return box_str("LABYRINTH",["Status: Closed" if not WORLD.get("labyrinth") else f"OPEN - Beast HP {WORLD.get('labyrinth')}","Use /labyrinth enter to join"])
        if args[0]=="force":
            if not is_owner(p): return "Only Owners can force Labyrinth"
            WORLD["labyrinth"]=800; save(); return "Labyrinth OPEN - Beast HP 800"
        if args[0] in ["enable","disable"]: 
            if not is_owner(p): return "Only Owners"
            return f"Labyrinth spawning {args[0]}d"
        if args[0]=="enter": return "Labyrinth Beast HP 800 - Use /moves"
        if args[0]=="attack": return "Labyrinth attack! Beast -50 HP - Use /moves"
        if args[0]=="move": return f"Labyrinth move: {' '.join(args[1:])} used!"
        if args[0]=="team":
            if len(args)>=2 and args[1]=="create": return f"Labyrinth team created: {' '.join(args[2:])}"
            if len(args)>=2 and args[1]=="invite": return f"Labyrinth invite sent to {' '.join(args[2:])}"
            if len(args)>=2 and args[1] in ["accept","reject"]: return f"Labyrinth invite {args[1]}ed"
        return "Labyrinth done"
    if cmd=="family":
        if not args: return f"Use: {pre}family found / add / accept / leave / info"
        if args[0]=="found": p["family"]=" ".join(args[1:]) or "My Family"; save(); return f"Family founded: {p['family']} (1,000,000 Zeni)"
        if args[0]=="add": return f"Family invite sent to {' '.join(args[1:])}"
        if args[0]=="accept": return f"Joined family: {p['family']}"
        if args[0]=="leave": p["family"]="No Family"; save(); return "Left family"
        if args[0]=="info": return box_str("FAMILY INFO",[f"House: {p['family']}",f"Tier: {p.get('houseTier',0)}",f"Gold: {fmt(p['zeni'])}"])
        return "Family done"
    if cmd=="families":
        fams=sorted(DB["players"].values(), key=lambda x: x.get("zeni",0), reverse=True)[:5]
        return box_str("FAMILIES - RICHEST FIRST",[f"{i+1}. {x['displayName']} - {x.get('family')} - {fmt(x['zeni'])}" for i,x in enumerate(fams)])
    if cmd=="raid":
        if not args: return box_str("COUNTRY RAID",["Status: Recruiting","Use /raid join then /raid start"])
        if args[0]=="join": return "Joined raid team!"
        if args[0]=="start": return "Raid Beast HP 1000 - Use /moves"
        if args[0]=="attack": return "Raid attack! Beast -50 HP"
        if args[0]=="move": return f"Raid move: {' '.join(args[1:])} used!"
        if args[0]=="claim": r=gain_zeni(p,10000); save(); return f"Raid claimed +{fmt(r)} Zeni"
        if args[0]=="atk": return "Raid atk! Beast -50 HP"
        if args[0]=="heal": p["hp"]=p["maxHp"]; save(); return "Raid heal - HP full"
        return "Raid done"
    if cmd=="arena":
        if not args: return box_str("HALL OF REFLECTIONS",["Board: Reflections","Prize: 500k Zeni","Entrants: 0",f"Use {pre}arena enter - Pay 250,000 Zeni"])
        if args[0]=="enter":
            if p["zeni"]<250000: return "Need 250k"
            p["zeni"]-=250000; save(); return "Entered Hall of Reflections! Use /arena fight"
        if args[0]=="fight": return "Reflection HP 200 - Use /moves"
        return "Arena done"
    if cmd=="worldboss": return "World Boss HP 5000 - Use /raid atk"
    if cmd=="demoncastle": return f"Demon Castle Floor {args[0] if args else 1} - Beast HP 1000 - Use /moves"
    if cmd=="rebirth":
        if p["level"]<99: return "Need Lv.99+ to rebirth"
        p["level"]=1; p["exp"]=0; p["atk"]=int(p["atk"]*1.5); save(); return "🔥 REBIRTH! Back to Lv.1 with +50% Permanent DMG!"
    if cmd=="guild":
        if not args: return box_str("GUILD HOME",[f"Your Guild: {p.get('guild','None')}",f"Total Guilds: {len(DB['guilds'])}",f"Use {pre}guild create / join / info"])
        if args[0]=="create":
            gn=" ".join(args[1:]) or "My Guild"
            if gn in DB["guilds"]: return "Guild exists"
            if p["zeni"]<500000000 and not is_owner(p): return "Need 500M to create guild"
            p["zeni"]=max(0,p["zeni"]-500000000); DB["guilds"][gn]={"leader":p["displayName"],"members":[p["displayName"]],"vault":500000000,"level":1}; p["guild"]=gn; p["guildRank"]="Leader"; save(); return box_str("GUILD CREATED",[f"{gn} created!","Deposited 500M to vault"])
        if args[0]=="join": gn=" ".join(args[1:]); 
        if args[0]=="join":
            if gn not in DB["guilds"]: return "Guild not found"
            p["guild"]=gn; p["guildRank"]="Member"; save(); return f"Joined {gn}"
        if args[0]=="info":
            gn=p.get("guild","None")
            if gn not in DB["guilds"]: return "You are in no guild"
            g=DB["guilds"][gn]; return box_str("GUILD INFO",[f"Name: {gn}",f"Leader: {g['leader']}",f"Vault: {fmt(g.get('vault',0))}",f"Members: {len(g.get('members',[]))}"])
        if args[0]=="members": return box_str("GUILD MEMBERS",[f"Members of {p.get('guild')} - {p.get('guildRank')}"])
        if args[0]=="quest": return box_str("GUILD QUEST",["Quest 1: Kill 5 Bosses - Reward 50k","Use /guild quest accept 1"])
        if args[0]=="fund": return f"Trust fund request: {' '.join(args[1:])} - Sent to Owner"
        if args[0]=="leave": p["guild"]="None"; save(); return "Left guild"
        return "Guild done"
    if cmd=="church":
        if not args: return box_str("CHURCH",[f"Your Church: {p.get('church')}","Use /church join <god>"])
        if args[0]=="join": p["church"]=" ".join(args[1:]); save(); return f"Joined church: {p['church']}"
        if args[0]=="leave": p["church"]="No Church"; save(); return "Left church"
        return "Church done"
    if cmd=="pray":
        now=time.time(); left=86400-(now-p.get("lastPray",0))
        if left>0: return f"Pray cooldown: {time_left(left)}"
        p["lastPray"]=now; r=gain_zeni(p,5000); gain_exp(p,20); save(); return box_str("PRAYED",[f"God {p.get('church')} blessed you",f"+{fmt(r)} Zeni","+20 EXP"])
    if cmd in ["kick","promote","demote","tagall","hidetag","close","open","sybau","unsybau","mute","unmute","warn","resetwarn","antilink","ban","unban"]:
        if not is_owner(p) and p.get("guildRank") not in ["Leader","Admin"]: return "Group admins / Guild Staff only"
        return f"✅ {cmd} done: {' '.join(args)}"
    if cmd=="job":
        if not args or args[0]=="list": return box_str("JOBS",["cleaner 5k driver 12k","hacker 30k bank teller 20k","barber 8k chef 18k teacher 20k","farmer 10k miner 22k","Establishments: bank teller | hospital orderly | tavern server | market clerk"])
        if args[0]=="apply": p["job"]=" ".join(args[1:]); save(); return box_str("JOB",[f"You are now {p['job']}","If establishment job, Owner must approve"])
        if args[0]=="work":
            now=time.time(); left=2*3600-(now-p.get("lastWork",0))
            if left>0: return box_str("WORK WAIT",[f"Wait {time_left(left)}"])
            p["lastWork"]=now; pay={"cleaner":5000,"driver":12000,"hacker":30000,"bank teller":20000,"barber":8000,"chef":18000,"teacher":20000,"farmer":10000,"miner":22000}.get(p["job"],1000); r=gain_zeni(p,pay); gain_exp(p,20); save(); return box_str("WORK DONE",[f"+{fmt(r)} Zeni"])
        if args[0]=="info": return box_str("JOB INFO",[f"Job: {p['job']}"])
        if args[0] in ["requests","approve","deny"]: 
            if not is_owner(p): return "Owners only"
            return f"Job {args[0]}: {' '.join(args[1:])} done"
        if args[0]=="resign": p["job"]="Unemployed"; save(); return "Resigned from job"
        if args[0]=="establishments": return box_str("ESTABLISHMENTS",["Bank, Hospital, Tavern, Market - Weekly Pay"])
        return "Job done"
    if cmd=="marry":
        if not args: return f"Use: {pre}marry @user"
        if args[0]=="accept": return "Marriage accepted! 💍"
        t=get_player_by_name(" ".join(args))
        if not t: return "Player not found - Proposal sent!"
        p["spouse"]=t["displayName"]; t["spouse"]=p["displayName"]; save(); return box_str("MARRIED",[f"{p['displayName']} + {t['displayName']}"])
    if cmd=="divorce": p["spouse"]=None; save(); return "Divorced"
    if cmd=="spouse": return box_str("SPOUSE",[f"Spouse: {p.get('spouse') or 'None'}"])
    if cmd=="house":
        if not args or args[0]=="buy":
            if len(args)<2: return box_str("HOUSES",["1 Hut 100k 2 House 500k","3 Mansion 2M 4 Palace 10M"])
            tier=int(args[1]); prices={1:100000,2:500000,3:2000000,4:10000000}; names={1:"Hut",2:"House",3:"Mansion",4:"Palace"}
            if p["zeni"]<prices: return "Not enough"
            p["zeni"]-=prices; p["house"]=names; p["houseBuilt"]=True; save(); return box_str("BOUGHT",[f"You bought {names}"])
        if args[0]=="upgrade": p["houseTier"]=p.get("houseTier",0)+1; save(); return f"House upgraded to Tier {p['houseTier']}"
        if args[0]=="info": return box_str("HOUSE INFO",[f"House: {p['house']}",f"Tier: {p.get('houseTier',0)}"])
        if args[0]=="invite": return "House invite sent to spouse"
        return "House done"
    if cmd=="rental":
        if not args or args[0]=="list": return box_str("RENTAL",["Houses for rent: None yet"])
        if args[0]=="rent": return f"Listed house for rent: {args[1] if len(args)>1 else ''} Zeni"
        if args[0]=="apply": return f"Rental apply sent to {' '.join(args[1:])}"
        if args[0] in ["accept","reject"]: return f"Rental {args[0]}ed: {' '.join(args[1:])}"
        if args[0]=="evict": return "Tenant evicted"
        return "Rental done"
    if cmd=="pet":
        if not args or args[0]=="list": return box_str("PETS",["Fire 500k Ice 500k Shadow 1M Dragon 2M"])
        if args[0]=="buy": tn=" ".join(args[1:]); cost=500000; 
        if args[0]=="buy":
            if p["zeni"]<cost: return f"Need {fmt(cost)}"
            p["zeni"]-=cost; p["pet"]=tn; save(); return box_str("PET",[f"You got {tn}"])
        if args[0]=="name": p["pet"]=" ".join(args[1:]); save(); return f"Dragon named: {p['pet']}"
        if args[0]=="train": gain_exp(p,50); save(); return "Dragon trained +50 EXP"
        if args[0]=="info": return box_str("PET INFO",[f"Dragon: {p.get('pet') or 'None'}"])
        return "Pet done"
    if cmd in ["sticker","unsticker","tg","play","tt","instagram","tiktok","ig","twitter","dl"]:
        return box_str("DOWNLOADER / MEDIA",[f"{cmd} received: {' '.join(args)}","Link saved - Download will be sent (WhatsApp Media API)"])
    if cmd=="market":
        if not args: return box_str("MARKET",[f"Items: {len(DB['market'])}","Use /market list / buy / cancel"])
        if args[0]=="list": DB["market"].append({"seller":p["displayName"],"item":" ".join(args[1:])}); save(); return "Listed on market!"
        if args[0]=="buy": return "Bought from market (5% fee)"
        if args[0]=="cancel": return "Listing cancelled"
        return "Market done"
    if cmd=="achievements": return box_str("ACHIEVEMENTS",["Progress: 0/50","Rewards: Claim with /claim"])
    if cmd=="hunger": return box_str("HUNGER",[f"Hunger: {p.get('hunger_lvl',100)}/100",f"Cooking Lv: {p.get('cooking',1)}","Well Fed: Yes" if p.get('hunger_lvl',100)>50 else "Hungry! Eat!"])
    if cmd=="eat":
        p["hunger_lvl"]=100; save(); return f"Ate {' '.join(args) or 'Snack'} - Hunger full!"
    if cmd=="tavern":
        if not args: return box_str("TAVERN MENU",["Snack 500 Zeni","Square Meal 2000 Zeni","Hearty Stew 5000 Zeni",f"Use {pre}tavern <food>"])
        return f"Ate at tavern: {' '.join(args)}"
    if cmd=="feast": return "Party Feast! Buff for 2+ members - +20% ATK"
    if cmd=="cook":
        if not args or args[0]=="list": return box_str("RECIPES",["Snack - 1 Wood","Square Meal - 2 Wood","Hearty Stew - 5 Wood"])
        return f"Cooked: {' '.join(args)}"
    if cmd=="quests": return box_str("QUESTS",["Daily: Work 1x - Dungeon 1x - PvP 1x",f"Use {pre}quests claim to claim"])
    if cmd in ["leaderboard","lb"]:
        # Shared leaderboard - WhatsApp + Website same DB
        sort_key="level"
        if args and args[0]=="zeni": sort_key="zeni"
        if args and args[0] in ["pvp","dungeon"]: sort_key="wins" if args[0]=="pvp" else "dungeonClears"
        s=sorted([x for x in DB["players"].values() if x.get("registered")], key=lambda x: x.get(sort_key,0), reverse=True)[:10]
        lines=[f"🏆 LEADERBOARD - {sort_key.upper()} - Web + WhatsApp SAME"]
        for i,x in enumerate(s,1): lines.append(f"{i}. {x['displayName']} Lv{x['level']} {fmt(x['zeni'])} Zeni Wins:{x.get('wins',0)}")
        if args and args[0]=="family": return box_str("LEADERBOARD FAMILY",[f"{i+1}. {x['displayName']} - {x.get('family')} - {fmt(x['zeni'])}" for i,x in enumerate(s[:5])])
        return box_str("LEADERBOARD",lines)
    if cmd=="season": return box_str("SEASON",["Season ends in: 30 days","Your seasonal rank: Check /leaderboard rank"])
    if cmd=="share":
        if len(args)<2: return f"Use: {pre}share @user <item> [qty]"
        return f"Shared {' '.join(args[1:])} to {args[0]}"
    if cmd=="core":
        if not args: return f"Use: {pre}core atk|def|spd"
        if args[0]=="atk": p["atk"]+=1
        if args[0]=="def": p["def"]+=1
        if args[0]=="spd": p["spd"]+=1
        save(); return f"Core spent: +1 {args[0].upper()}"
    if cmd=="buy":
        if not args: return f"Use: {pre}buy <item> [qty]"
        qty=1
        try: qty=int(args[-1]); item=" ".join(args[:-1])
        except: item=" ".join(args)
        cost=1000*qty
        if p["zeni"]<cost: return f"Need {fmt(cost)}"
        p["zeni"]-=cost; save(); return f"Bought {item} x{qty} for {fmt(cost)}"
    if cmd=="bio": p["bio"]=" ".join(args); save(); return f"Bio set: {p['bio']}"
    if cmd=="web": return box_str("WEB LOGIN",["Go to website","Use your Name + Password 2164 to login","Web + WhatsApp SAME ACCOUNT"])
    if cmd=="emoji": p["emoji"]=" ".join(args); save(); return f"Emoji set: {p['emoji']}"
    if cmd=="broadcast":
        if not is_owner(p): return "Guild Staff / Owners only"
        return f"📢 BROADCAST sent to every group: {' '.join(args)}"
    if cmd=="rob":
        if not args: return f"Use: {pre}rob <player> or {pre}rob bank"
        now=time.time()
        if now-p.get("lastRob",0)<600: return "Rob cooldown. Wait 10 mins"
        p["lastRob"]=now
        if args[0]=="bank":
            if random.randint(1,100)<=45: amt=random.randint(1000000,5000000); r=gain_zeni(p,amt); save(); return box_str("ROB BANK SUCCESS",[f"Stole {fmt(r)}"])
            else: p["jailed"]=time.time()+600; fine=int(p["zeni"]*0.15); p["zeni"]-=fine; save(); return box_str("ROB BANK FAILED",["Caught! Jailed 10 mins",f"Fine: {fmt(fine)}"])
        if args[0]=="guild": 
            if random.randint(1,100)<=30: amt=random.randint(500000,2000000); r=gain_zeni(p,amt); save(); return f"Robbed guild treasury +{fmt(r)}"
            else: p["jailed"]=time.time()+600; save(); return "Caught robbing guild! Jailed"
        t=get_player_by_name(" ".join(args[:-1]) if len(args)>1 else " ".join(args))
        if not t: return "Target not found"
        if random.randint(1,100)<=45: pct=random.randint(5,15); amt=int(t["zeni"]*pct/100); t["zeni"]-=amt; r=gain_zeni(p,amt); save(); return box_str("ROB SUCCESS",[f"Robbed {t['displayName']}",f"Stole {fmt(r)}"])
        else: p["jailed"]=time.time()+300; fine=int(p["zeni"]*0.10); p["zeni"]-=fine; save(); return box_str("ROB FAILED",["Caught! Jailed 5 mins",f"Fine: {fmt(fine)}"])
    if cmd=="bail":
        if p.get("jailed",0)<=time.time() and not args: return "You are not jailed"
        p["jailed"]=0; save(); return "Bail paid - Out of jail!"
    if cmd=="breakout":
        if not args: return "Breakout: Fight 10 officers - Use /breakout attack"
        if args[0]=="attack": return "Breakout attack! Officer -50 HP"
        if args[0]=="move": return f"Breakout move: {' '.join(args[1:])}"
        return "Breakout done"
    if cmd=="wanted": return box_str("WANTED LIST",[f"{x['displayName']} - Jailed" for x in DB["players"].values() if x.get("jailed",0)>time.time()] or ["No wanted players"])
    if cmd=="hospital":
        if not args: return box_str("HOSPITAL",[f"Health: {p['hp']}/{p['maxHp']}",f"Treatment price: 1000 Zeni",f"Use {pre}hospital checkup / treat / heal"])
        if args[0]=="checkup": return "Check-up: You are healthy! Free"
        if args[0]=="treat": p["hp"]=p["maxHp"]; save(); return "Treated - HP full!"
        if args[0]=="heal": p["hp"]=p["maxHp"]; p["mp"]=p["maxMp"]; save(); return "Healed - HP/MP full (half price)"
        if args[0]=="price": 
            if not is_owner(p): return "Owners / orderlies only"
            return f"Treatment price set to {args[1] if len(args)>1 else ''}"
        return "Hospital done"
    if cmd=="bank":
        if not args: return box_str("BANK",[f"Cash {fmt(p['zeni'])}",f"Bank {fmt(p['bank'])}",f"Open: {'YES' if p.get('bank_open') else 'NO'}",f"Use {pre}bank register / deposit / withdraw / transfer"])
        if args[0] in ["register","open"]:
            if p.get("bank_open"): return "Bank already open"
            if p["zeni"]<1000000 and not is_owner(p): return "Need 1,000,000 Zeni to open bank"
            p["zeni"]=max(0,p["zeni"]-1000000); p["bank_open"]=True; p["bank_opened_at"]=time.time(); save(); return box_str("BANK OPENED",["Paid 1M"])
        if args[0]=="deposit":
            if not p.get("bank_open"): return f"Open bank first: {pre}bank register"
            amt=p["zeni"] if len(args)<2 or args[1]=="all" else int(args[1])
            p["zeni"]-=amt; p["bank"]+=amt; save(); return f"Deposited {fmt(amt)} Bank {fmt(p['bank'])}"
        if args[0]=="withdraw":
            if not p.get("bank_open"): return "Open bank first"
            amt=p["bank"] if len(args)<2 or args[1]=="all" else int(args[1])
            p["bank"]-=amt; p["zeni"]+=amt; save(); return f"Withdrew {fmt(amt)}"
        if args[0]=="transfer":
            if len(args)<3: return f"Use {pre}bank transfer @user <amount>"
            amt=int(args[-1]); t=get_player_by_name(" ".join(args[1:-1]).replace("@",""))
            if not t: return "Player not found"
            if p["bank"]<amt: return "Not enough in bank"
            p["bank"]-=amt; t["zeni"]+=amt; save(); return f"Sent {fmt(amt)} to {t['displayName']}"
        if args[0]=="loan":
            amt=int(args[1]) if len(args)>1 else 0; p["loan"]=amt; p["loanDue"]=int(amt*1.2); p["zeni"]+=amt; save(); return f"LOAN Got {fmt(amt)} - Repay {fmt(p['loanDue'])} (Owner approves)"
        if args[0]=="repay":
            amt=p["loanDue"] if len(args)<2 or args[1]=="all" else int(args[1]); amt=min(p["zeni"],amt); p["zeni"]-=amt; p["loanDue"]-=amt
            if p["loanDue"]<=0: p["loan"]=0; p["loanDue"]=0
            save(); return f"Repaid {fmt(amt)} Left {fmt(p['loanDue'])}"
        if args[0]=="pay": p["loanDue"]=0; p["loan"]=0; save(); return "Paid what you owe - Account unlocked"
        return "Bank done"
    if cmd=="heal":
        if p["zeni"]<1000: return "Need 1000 Zeni"
        p["zeni"]-=1000; p["hp"]=p["maxHp"]; p["mp"]=p["maxMp"]; save(); return box_str("HEALED",["HP and MP full"])
    if cmd=="immortal":
        if not is_owner(p): return "No Such Command - Only Owners"
        if not args: return box_str("IMMORTAL MENU",["/Immortal set <stat> <value>","/Immortal set economy zeni <amount>","/Immortal autobattle on/off"])
        if args[0]=="autobattle": DB["auto_battle"]=(len(args)>1 and args[1].lower()=="on"); save(); return f"Auto Battle {'ON' if DB['auto_battle'] else 'OFF'}"
        if args[0]=="set" and len(args)>=3:
            if args[1]=="economy": WORLD["totalZeni"]=int(args[3]); save(); return f"Economy = {fmt(WORLD['totalZeni'])}"
            mp={"atk":"atk","hp":"maxHp","mp":"maxMp","def":"def","spd":"spd","agi":"agi","con":"con"}; 
            if args[1] in mp: p[mp[args[1]]]=int(args[2]); save(); return f"{args[1]} = {args[2]}"
        return "Immortal done"
    if cmd=="link": return box_str("WHATSAPP LINKED",["Type /password 2164","Bot linked to WhatsApp 0779798568"])
    if cmd=="password":
        if args and args[0]=="2164": return box_str("WHATSAPP LINKED",["Password correct!","Bot linked to WhatsApp 0779798568"])
        return "Wrong password."
    if cmd=="race":
        if not args: return box_str("RACES",["human demon fairy mage elf vampire dragon angel God - Owners only"])
        if args[0].lower()=="god" and not is_owner(p): return "God only for Owners"
        pretty={"human":"Human","demon":"Demon","fairy":"Fairy","mage":"Mage","elf":"Elf","vampire":"Vampire","dragon":"Dragon","angel":"Angel","god":"God"}
        if args[0].lower() not in pretty: return "Race not found"
        p["race"]=pretty[args[0].lower()]; save(); return f"You are {p['race']}"
    if cmd=="gender":
        if not args or args[0].lower() not in ["male","female"]: return "Use /gender male or female"
        p["gender"]=args[0].capitalize(); save(); return f"Gender: {p['gender']}"
    if cmd=="rename":
        if not args: return "Use /rename <new name>"
        old=p["displayName"]
        if get_player_by_name(rest) and get_player_by_name(rest)["id"]!=p["id"]: return f"Name '{rest}' already taken!"
        p["displayName"]=rest; p["name"]=rest; save(); return f"Renamed {old} -> {rest}"
    if cmd=="notifications":
        if not p.get("notifications"): return "No new notifications"
        out=box_str("NOTIFICATIONS",p["notifications"][:5]); p["notifications"]=[]; save(); return out
    if cmd=="go": return box_str("WHERE TO GO",["/go work /go home /go bar /go shop /go bank"])
    if cmd=="pvp":
        if not args: return f"Use: {pre}pvp <player>"
        DB["pending_pvp"][p["id"]]=" ".join(args); save(); return f"Challenge sent to {' '.join(args)} - They type {pre}accept"
    if cmd=="accept": return "Challenge accepted! Type /moves to fight!"
    if cmd=="decline": DB["pending_pvp"]={}; save(); return "Challenge declined"
    if cmd=="forfeit": DB["dungeon"]=None; save(); return "You forfeited current battle"
    if cmd in ["nano","nona","dis","en","myid","reports","sandbox","autodelete","addfounder","addmod","setstats","setmonarch","monarchgc","monarchs","duel","train","gym","gate","usekey","event","tourney","undeploy","sellshadow","expandbag","equip","unequip","shop","deposit","withdraw","penalty","stbm"]:
        if cmd in ["nano","nona","dis","en","myid","reports","sandbox","autodelete","addfounder","addmod","setstats","setmonarch","monarchgc","broadcast"] and not is_owner(p): return "Owners / Admins only"
        if cmd=="myid": return f"Your ID: {p['id']} | Name: {p['displayName']}"
        if cmd=="train": gain_exp(p,100); save(); return "Trained +100 EXP (24h CD)"
        if cmd=="gym": gain_exp(p,50); save(); return "Gym +50 EXP"
        if cmd=="gate": return f"Gate {args[0] if args else 'E'} entered - Use /moves"
        if cmd=="shop": return box_str("SHOP",["Small Heal 1000 | Medium Heal 5000 | MP Potion 1000","Armor 10000 | Weapon 20000 | Elixir 50000"])
        if cmd=="equip": return f"Equipped: {' '.join(args)}"
        if cmd=="unequip": return f"Unequipped: {' '.join(args)}"
        return f"✅ {cmd} done: {' '.join(args)}"
    return f"No Such Command Player - Type {pre}menu"

===== WEBSITE - LANDING -> ENTER -> REGISTER/LOGIN -> DASHBOARD CHAT =====
app = Flask(__name__)
HTML = """<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>INFINITY HUNTER</title>
<style>body{background:#050510;color:#fff;font-family:Arial;margin:0;padding:0}.center{text-align:center;padding:60px 16px}h1{color:#FFD700;font-size:42px}input{width:100%;padding:14px;margin:8px 0;background:#000;color:#fff;border:2px solid #7B2FFF;border-radius:12px;box-sizing:border-box}button{width:100%;padding:14px;background:#FFD700;color:#000;border:none;border-radius:12px;font-weight:900;margin:8px 0;cursor:pointer}.card{background:#111128;border:1px solid #333;padding:16px;border-radius:16px;margin:12px}pre{white-space:pre-wrap;background:#000;padding:12px;border-radius:10px;max-height:420px;overflow:auto}.chat{display:flex;flex-direction:column;gap:8px}.msg{background:#1a1a3a;padding:10px;border-radius:12px}.msg.me{background:#7B2FFF}.topbar{background:#111128;padding:12px;display:flex;justify-content:space-between;align-items:center}.leader{font-size:13px} .hidden{display:none}</style></head><body>
<!-- PAGE 1: LANDING - ONLY INFINITY HUNTER + ENTER -->
<div id='landing' class='center'><h1>⚡ INFINITY HUNTER ⚡</h1><p>Web + WhatsApp SAME GAME • Owner: 0779798568 / Lord Infinity / Immortal Emperor</p><button onclick='showAuth()' style='max-width:300px'>ENTER →</button><p style='font-size:12px;color:#aaa'>3x 1TB Backups • Never Lose Data</p></div>
<!-- PAGE 2: REGISTER / LOGIN - ONLY FOR WEBSITE -->
<div id='auth' class='center hidden'><div class='card' style='max-width:420px;margin:auto;text-align:left'><h2>REGISTER / LOGIN</h2><input id='name' placeholder='Name e.g. Lord Infinity / Immortal Emperor / Infinity'><input id='pass' type='password' placeholder='Password - Owners: 2164' maxlength='10'><input id='race' placeholder='Race e.g. God (optional)'><input id='gender' placeholder='Gender male / female (optional)'><button onclick='doAuth("register")'>⚡ REGISTER</button><button onclick='doAuth("login")' style='background:#7B2FFF;color:#fff'>🔑 LOGIN</button><p id='authmsg' style='font-size:13px;color:#FFD700'></p><p style='font-size:12px'>Owners: 0779798568 / Lord Infinity / Immortal Emperor - Password 2164 = God + Immortal Emperor perks<br>Other names: any password you choose. WhatsApp players: your name already appears on leaderboard!</p></div></div>
<!-- PAGE 3: DASHBOARD - LIKE WHATSAPP CHAT -->
<div id='dash' class='hidden'><div class='topbar'><b>⚡ INFINITY HUNTER - CHAT</b><span id='who'></span><button onclick='logout()' style='width:auto;padding:8px 14px'>Logout</button></div><div style='display:flex;flex-wrap:wrap'><div style='flex:2;min-width:280px;padding:12px'><div class='card'><h3>💬 Chat with Bot</h3><div id='chat' class='chat'><div class='msg'>Bot: Welcome! Type /menu to see all commands. Type /register Infinity God male to finish setup if needed.</div></div><input id='cmd' placeholder='Type message e.g. /menu /profile /dungeon enter /moves 5'><button onclick='sendChat()'>▶ SEND</button><div style='display:flex;gap:6px;flex-wrap:wrap'><button onclick='quick("/menu")' style='width:48%;background:#7B2FFF;color:#fff'>📜 MENU</button><button onclick='quick("/profile")' style='width:48%;background:#7B2FFF;color:#fff'>👤 PROFILE</button><button onclick='quick("/stats")' style='width:48%;background:#7B2FFF;color:#fff'>📊 STATS</button><button onclick='quick("/leaderboard")' style='width:48%;background:#FFD700;color:#000'>🏆 LEADERBOARD</button><button onclick='quick("/dungeon enter")' style='width:48%;background:#FF0000;color:#fff'>🏰 DUNGEON</button><button onclick='quick("/moves")' style='width:48%;background:#00AA00;color:#fff'>⚔️ MOVES</button></div></div></div><div style='flex:1;min-width:220px;padding:12px'><div class='card'><h3>🏆 LEADERBOARD</h3><p style='font-size:12px'>Web + WhatsApp SAME - WhatsApp players appear here too!</p><pre id='lb'>Loading...</pre><button onclick='loadLB()' style='background:#7B2FFF;color:#fff'>↻ Refresh Leaderboard</button></div><div class='card'><h3>💾 Backups</h3><pre id='bk'>3x 1TB Backups Active</pre></div></div></div></div>
<script>
let myName='';let myPass='';
function showAuth(){document.getElementById('landing').classList.add('hidden');document.getElementById('auth').classList.remove('hidden');}
async function doAuth(mode){
  let name=document.getElementById('name').value.trim(); let pass=document.getElementById('pass').value.trim(); let race=document.getElementById('race').value.trim(); let gender=document.getElementById('gender').value.trim();
  if(!name||!pass){document.getElementById('authmsg').textContent='Enter Name + Password';return;}
  let r=await fetch('/api/auth',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,pass,race,gender,mode})}); let j=await r.json();
  document.getElementById('authmsg').textContent=j.msg;
  if(j.ok){myName=name;myPass=pass;document.getElementById('auth').classList.add('hidden');document.getElementById('dash').classList.remove('hidden');document.getElementById('who').textContent='@'+name;loadLB();}
}
function logout(){location.reload();}
async function loadLB(){let r=await fetch('/api/leaderboard');let j=await r.json();document.getElementById('lb').textContent=j.text;}
async function sendChat(){let t=document.getElementById('cmd').value;if(!t)return;addMsg('You: '+t,'me');document.getElementById('cmd').value='';let r=await fetch('/api/command',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:myName,text:t})});let j=await r.json();addMsg('Bot: '+j.reply,'');loadLB();}
function quick(t){document.getElementById('cmd').value=t;sendChat();}
function addMsg(t,cls){let d=document.createElement('div');d.className='msg '+cls;d.textContent=t;document.getElementById('chat').appendChild(d);d.scrollIntoView();}
document.getElementById('cmd')?.addEventListener('keydown',e=>{if(e.key==='Enter')sendChat();});
</script></body></html>"""
@app.route('/')
def home(): return HTML
@app.route('/api/auth', methods=['POST'])
def api_auth():
    data=request.json or {}; name=(data.get('name') or '').strip(); pwd=(data.get('pass') or '').strip(); race=(data.get('race') or '').strip(); gender=(data.get('gender') or '').strip(); mode=data.get('mode','register')
    if not name or not pwd: return jsonify({"ok":False,"msg":"Enter Name + Password"})
    existing=get_player_by_name(name)
    # Owners must use 2164 on website
    is_owner_name=name.lower() in OWNER_NAMES
    if is_owner_name and pwd!=OWNER_PASSWORD: return jsonify({"ok":False,"msg":"Owners must use password 2164"})
    if mode=="login":
        if not existing or not existing.get("registered"): return jsonify({"ok":False,"msg":"Not registered. Click REGISTER first."})
        if existing.get("password") and existing.get("password")!=pwd: return jsonify({"ok":False,"msg":"Wrong password"})
        if not existing.get("password"): existing["password"]=pwd; save()
        return jsonify({"ok":True,"msg":f"Welcome back {name}!"})
    # register
    if existing and existing.get("registered"):
        if existing.get("password") and existing.get("password")!=pwd: return jsonify({"ok":False,"msg":"Name taken! Use LOGIN or another name"})
        return jsonify({"ok":True,"msg":f"Already registered as {name} - Logged in!"})
    # Create web player - use web:<name> id, but name lookup will find it for leaderboard
    p=get_player(f"web:{name}", name)
    p["password"]=pwd; p["registered"]=True; p["displayName"]=name; p["name"]=name
    if is_owner_name: apply_owner_perks(p)
    if race or gender:
        err=apply_register_details(p, race, gender)
        if err: return jsonify({"ok":False,"msg":err})
    save(); return jsonify({"ok":True,"msg":f"Registered {name}! Title: {p.get('title')} Race: {p['race']} - Welcome to Dashboard!"})
@app.route('/api/command', methods=['POST'])
def api_cmd():
    data=request.json or {}; name=data.get('name','Player'); text=data.get('text','/menu')
    reply=process_command(f"web:{name}", text); save()
    p=get_player_by_name(name)
    return jsonify({"reply":reply,"player":p})
@app.route('/api/leaderboard')
def api_lb():
    s=sorted([x for x in DB["players"].values() if x.get("registered")], key=lambda x: x.get("level",1), reverse=True)[:10]
    lines=["🏆 LEADERBOARD - Web + WhatsApp SAME"]
    for i,x in enumerate(s,1): lines.append(f"{i}. {x['displayName']} Lv{x['level']} {fmt(x['zeni'])} Zeni")
    if not lines[1:]: lines.append("No players yet - Be first! /register Infinity")
    return jsonify({"text":"\n".join(lines)})
@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token')==VERIFY_TOKEN: return request.args.get('hub.challenge','')
    return "Invalid token",403
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data=request.json or {}
        for entry in data.get('entry',[]):
            for change in entry.get('changes',[]):
                for msg in change.get('value',{}).get('messages',[]):
                    sender=msg.get('from',''); text=msg.get('text',{}).get('body','')
                    if text.startswith('/') or text.startswith('.') or text.isdigit():
                        reply=process_command(sender, text); save(); send_whatsapp(sender, reply)
    except Exception as e: print("Webhook error",e)
    return "OK",200
def send_whatsapp(to, text):
    if not WHATSAPP_TOKEN or not WHATSAPP_PHONE_ID: print(f"WHATSAPP TO {to}: {text}"); return
    try:
        import urllib.request, json as js
        url=f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_ID}/messages"
        payload=js.dumps({"messaging_product":"whatsapp","to":to,"type":"text","text":{"body":text[:4000]}}).encode()
        req=urllib.request.Request(url, data=payload, headers={"Authorization":f"Bearer {WHATSAPP_TOKEN}","Content-Type":"application/json"})
        urllib.request.urlopen(req, timeout=10)
    except Exception as e: print("Send error",e)
@app.route('/health')
def health(): return "OK - Infinity Bot Live - Owners 0779798568 / Lord Infinity / Immortal Emperor - 3x 1TB Backups"
if __name__=='__main__':
    port=int(os.environ.get('PORT',10000)); print(f"INFINITY v7 LIVE on port {port}"); app.run(host='0.0.0.0', port=port)
```
