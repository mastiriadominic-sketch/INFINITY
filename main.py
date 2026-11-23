
#INFINITY v13 - General Returned - Catch Alone - Dungeon Alone - 15min Dungeon - Personal Gate
import json,random,os,time,datetime
from flask import Flask,request,jsonify
OWNER_IDS=["260779798568","0779798568"]
OWNER_NAMES=["lord infinity","infinity","immortal emperor","0779798568"]
OWNER_PASSWORD="2164"
VERIFY_TOKEN=os.environ.get("VERIFY_TOKEN","infinity123")
WHATSAPP_TOKEN=os.environ.get("WHATSAPP_TOKEN","")
WHATSAPP_PHONE_ID=os.environ.get("WHATSAPP_PHONE_ID","")
CAT=datetime.timezone(datetime.timedelta(hours=2))
def cat_now(): return datetime.datetime.now(CAT)
def fmt(n):
    try: return f"{int(n):,}"
    except: return "0"
def time_left(s):
    h=int(s//3600); m=int((s%3600)//60); sec=int(s%60)
    return f"{h}h {m}m {sec}s"
def bar(c,m,l=20):
    if m<=0: m=1
    f=max(0,min(l,int(c/m*l))); return "█"*f+"░"*(l-f)
BOT_ECONOMY={"hgss":100000000,"lgss":100000000,"mgss":100000000,"zeni":2000000000000,"germ":0}
RACES={"human":"Human","demon":"Demon","fairy":"Fairy","mage":"Mage","elf":"Elf","vampire":"Vampire","dragon":"Dragon","angel":"Angel","god":"God"}
CLASSES={"warrior":"Warrior","mage":"Mage","assassin":"Assassin","healer":"Healer","archer":"Archer","tank":"Tank","necromancer":"Necromancer","swordmaster":"Swordmaster","monarch":"Monarch"}
RACE_AB={"Human":"Adapt","Demon":"Demon Rage","Fairy":"Fairy Heal","Mage":"Arcane Burst","Elf":"Elf Arrow","Vampire":"Blood Drain","Dragon":"Dragon Breath","Angel":"Holy Light","God":"God Punch"}
CLASS_AB={"Warrior":"Slash","Mage":"Fireball","Assassin":"Shadow Strike","Healer":"Heal","Archer":"Piercing Arrow","Tank":"Shield Wall","Necromancer":"Soul Drain","Swordmaster":"Dragon Smash","Monarch":"Monarch Rule"}
ANIME_R={"human":["Adapt - Tanjiro","Spirit Blade - Demon Slayer"],"demon":["Demon Rage - Tanjiro","Hellfire - Naruto"],"fairy":["Fairy Heal - Fairy Tail","Pixie Dust - Tinkerbell"],"mage":["Arcane Burst - Frieren","Magic Missile - Harry Potter"],"elf":["Elf Arrow - Legolas","Forest Blessing - LOTR"],"vampire":["Blood Drain - Alucard","Night Bite - Twilight"],"dragon":["Dragon Breath - Goku","Dragon Roar - Natsu"],"angel":["Holy Light - Angel Beats","Judgement - Bleach"],"god":["God Punch - Saitama","Infinity Blast - Goku"]}
ANIME_C={"warrior":["Slash - Zoro","Dragon Smash - Goku"],"mage":["Fireball - Naruto","Lightning - Sasuke"],"assassin":["Shadow Strike - Sasuke","Silent Kill - Naruto"],"healer":["Heal - Sakura","Phoenix Rebirth - Naruto"],"archer":["Piercing Arrow - Legolas","Hawkeye - Avengers"],"tank":["Shield Wall - Captain America","Iron Defense - AOT"],"necromancer":["Soul Drain - Solo Leveling","Shadow Army - Solo Leveling"],"swordmaster":["Dragon Smash - Zoro","Sword Dance - Demon Slayer"],"monarch":["Monarch Rule - Solo Leveling","Monarch Slash - Jinwoo"]}
ANIME_RND=["Rasengan - Naruto","Chidori - Sasuke","Kamehameha - Goku","Bankai - Bleach","Gear 5 - Luffy","Domain Expansion - JJK","Susanoo - Naruto","Ultra Instinct - Goku"]
POKEMONS=["Shadow Wolf","Fire Dragon","Ice Dragon","Thunder Wolf","Phoenix","Golden Tiger","Shadow Dragon","Light Dragon"]
JOBS={"cleaner":(5000,1),"driver":(12000,2),"hacker":(30000,5),"bank teller":(20000,3),"barber":(8000,1),"chef":(18000,3),"teacher":(20000,3),"farmer":(10000,2),"miner":(22000,4),"blacksmith":(25000,4),"hunter":(35000,6),"guard":(15000,2)}
PETS={"Fire Dragon":(50,"Fire Breath"),"Ice Dragon":(50,"Ice Breath"),"Shadow Dragon":(100,"Shadow Bite"),"Light Dragon":(100,"Holy Light"),"Thunder Wolf":(30,"Thunder Bite"),"Phoenix":(200,"Rebirth"),"Shadow Wolf":(40,"Shadow Strike"),"Golden Tiger":(80,"Tiger Claw")}
BOT_RULES=["1. No spamming / calling the bot","   (Auto Block)","2. No insults / nudity content","   (Ban)","3. No chatting bot in DM for spam","   ONLY group links allowed","   (Block)","4. Use /support to get support group link","5. Send link to bot DM","   It will join your group soon","6. Bot MUST be an admin of your group","7. Bot will join a group with 50+ members","8. Bot will NOT join back","   a group where it was removed","9. Bot will leave inactive & dead groups","10. Don't abuse bot or owner in any way","    (Ban)","11. Don't text mods asking to be mod","    (Ban)","12. Spamming in Casino or any group","    = 48 hours ban","13. Don't ask for bot script","    We are not giving / selling our bots","14. We are not accepting new mods now","    If we want, we will announce it","15. The kinder you are as INFINITY user","    The more rewards you will get"]
GROUP_DESC_LINES=["⚡ INFINITY HUNTER ⚡","Web + WhatsApp SAME GAME","Owners: 0779798568 / Lord Infinity / Immortal Emperor","Start: /register YourName"]
def can_supreme(p): return is_owner(p) or p.get("is_admin") or p.get("is_mob") or p.get("is_bot_admin") or p.get("is_group_admin")
def stones_lines(p):
    L=["💎 Spirit Stones",f"• LGSS - {fmt(p.get('lgss',0))}",f"• MGSS - {fmt(p.get('mgss',0))}",f"• HGSS - {fmt(p.get('hgss',0))}",f"• Zeni - {fmt(p.get('zeni',0))}",f"• Germ - {fmt(p.get('germ',0))}"]
    if can_supreme(p): L+=[f"• Legendary - {fmt(p.get('legendary',0))}",f"• Supreme - {fmt(p.get('supreme',0))}"]
    return L
def give_reward(p,bz=10000,bl=5):
    p["zeni"]=p.get("zeni",0)+bz; out=[f"• Zeni - +{fmt(bz)}"]
    if random.random()<0.70: p["lgss"]=p.get("lgss",0)+bl; out.append(f"• LGSS - +{bl} (70% chance)")
    if random.random()<0.30:
        g=random.randint(10,100); p["germ"]=p.get("germ",0)+g; out.append(f"• Germ - +{g} (30% chance)")
    if random.random()<0.10:
        p["supreme"]=p.get("supreme",0)+1
        out.append("• Supreme - +1 (10% chance)" if can_supreme(p) else "• ??? - +1 Hidden (10% Supreme - hidden)")
    return out
def convert_stones(p,frm,to,amt):
    rates={"zeni":1,"germ":10,"lgss":100,"mgss":10000,"hgss":1000000,"legendary":100000000,"supreme":10000000000}
    if frm not in rates or to not in rates: return "Use: zeni germ lgss mgss hgss supreme"
    if (frm=="supreme" or to=="supreme") and not can_supreme(p): return "❌ Only Owners/Admins/Mobs/Bot Admins can use Supreme"
    if p.get(frm,0)<amt: return f"❌ Not enough {frm.upper()} - You have {fmt(p.get(frm,0))}"
    base=amt*rates[frm]; got=base//rates[to]; p[frm]-=amt; p[to]=p.get(to,0)+got; return f"✅ {fmt(amt)} {frm.upper()} → {fmt(got)} {to.upper()}"
def rank_for_gate(lvl):
    if lvl>=500: return "SS"
    if lvl>=300: return "S"
    if lvl>=200: return "A"
    if lvl>=100: return "B"
    if lvl>=50: return "C"
    if lvl>=20: return "D"
    return "E"
def rank_stats(rank): return {"E":(80,12,100),"D":(150,20,150),"C":(300,35,250),"B":(500,50,400),"A":(800,80,600),"S":(1200,120,1000),"SS":(2000,180,2000)}
def maybe_spawn():
    now=time.time()
    if now-WORLD.get("last_dungeon_spawn",0)<900: return None
    if random.random()<0.50: rank=random.choice(["A","S","SS"])
    else: rank=random.choice(["E","E","D","C","B","B"])
    WORLD["last_dungeon_spawn"]=now; WORLD["spawned_dungeon"]={"rank":rank,"expires":now+900,"beasts":["Beast 1","Beast 2","Beast 3"],"created":now}; save(); return rank
DB_FILE="infinity_db.json"; BACKUPS=["backup1_1TB.json","backup2_1TB.json","backup3_1TB.json"]
DB={"players":{},"market":[],"pending_pvp":{},"guilds":{},"dungeon":None,"groups":{},"auto_battle":False,"config":{"prefix":"/","prefixes":["/","."]},"pending_reg":{},"reports":[],"requests":[],"personal_gates":{},"catch_battle":None}
WORLD={"totalZeni":2000000000000,"totalPlayers":0,"labyrinth":None,"economy":BOT_ECONOMY,"last_dungeon_spawn":0,"spawned_dungeon":None}
def load_db():
    global DB,WORLD
    for f in [DB_FILE]+BACKUPS:
        if os.path.exists(f) and os.path.getsize(f)>0:
            try:
                with open(f) as fh: d=json.load(fh); DB=d.get("DB",DB); WORLD=d.get("WORLD",WORLD); return
            except: continue
load_db()
def save():
    data=json.dumps({"DB":DB,"WORLD":WORLD})
    for f in [DB_FILE]+BACKUPS:
        try:
            with open(f,"w") as fh: fh.write(data)
        except: pass
def is_owner_id(pid): return str(pid) in OWNER_IDS or "779798568" in str(pid)
def is_owner(p): return is_owner_id(p["id"]) or p.get("displayName","").lower() in OWNER_NAMES
def get_prefix(): return DB.get("config",{}).get("prefix","/")
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
    amt=int(amt*1.5) if p.get("race")=="God" and is_owner(p) else amt; p["exp"]+=amt
    while p["exp"]>=exp_need(p["level"]):
        p["exp"]-=exp_need(p["level"]); p["level"]+=1; p["maxHp"]+=25; p["hp"]=p["maxHp"]; p["maxMp"]+=10; p["mp"]=p["maxMp"]; p["atk"]+=4; p["def"]+=3; p["spd"]+=3; p["agi"]=p.get("agi",10)+2; p["con"]=p.get("con",10)+2; p["rank"]=rank_for(p["level"])
    return amt
def assign_moves(p):
    r=p.get("race","Human").lower(); c=p.get("class","Warrior").lower()
    m=[]; m+=ANIME_R.get(r,["Slash - Zoro"])[:2]; m+=ANIME_C.get(c,["Slash - Zoro"])[:2]; m+=[random.choice(ANIME_RND)]; p["moves"]=m
    if c=="monarch": p["atk"]=15+p["level"]*10; p["maxHp"]=100+p["level"]*30; p["hp"]=p["maxHp"]; p["mp"]=50+p["level"]*20; p["maxMp"]=p["mp"]
    return m
def get_player(pid,name="Player"):
    if pid not in DB["players"]:
        now=cat_now()
        DB["players"][pid]={"id":pid,"name":name,"displayName":name,"registered":False,"password":"","race":"","class":"","level":1,"exp":0,"zeni":1000000,"germ":0,"lgss":10,"mgss":0,"hgss":0,"legendary":0,"supreme":0,"bank":0,"bank_open":False,"savings":0,"hp":100,"maxHp":100,"mp":50,"maxMp":50,"atk":15,"def":10,"spd":12,"agi":10,"con":10,"rank":"E - Novice","wins":0,"losses":0,"dungeonClears":0,"dungeon_floor":1,"checkpoint":1,"kills":0,"job":"Unemployed","loan":0,"loanDue":0,"house":"None","houseTier":0,"car":"None","shop":"None","pet":None,"guild":"None","guildRank":"None","lastDaily":0,"lastWork":0,"lastClaim":0,"lastRob":0,"jailed":0,"banned":False,"questsDone":0,"notifications":[],"gender":"Not Set","age":15,"lifespan":80,"birthday":now.strftime("%d %b %Y"),"spouse":None,"title":"Adventurer","titles":["Adventurer"],"cultRealm":0,"cultLayer":1,"cultXp":0,"cultNeed":100,"talentType":"","talentValue":"","talentGrade":"","isInfinity":False,"isChosen":False,"chosenUntil":0,"wood":0,"houseBuilt":False,"sect":"No Sect","sectRank":"-","hunger":100,"family":"No Family","party":"No Party","church":"No Church","inventory":{},"skills":[],"active_skills":[],"awaiting_move_until":0,"gems":5,"str":0,"int":0,"vit":0,"luk":0,"bio":"","emoji":"⚔️","hunger_lvl":100,"cooking":1,"achievements":[],"reg_stage":"none","is_admin":False,"is_mob":False,"is_bot_admin":False,"is_group_admin":False,"moves":[],"reg_step":"","pokemon":None}
        WORLD["totalPlayers"]+=1
    for k,v in {"germ":0,"lgss":10,"mgss":0,"hgss":0,"legendary":0,"supreme":0,"moves":[],"is_admin":False,"is_mob":False,"is_bot_admin":False,"is_group_admin":False,"reg_step":"","race":"","class":"","pokemon":None}.items():
        if k not in DB["players"][pid]: DB["players"][pid][k]=v
    return DB["players"][pid]
def get_player_by_name(name):
    for pid,pl in DB["players"].items():
        if pl.get("displayName","").lower()==name.lower(): return pl
    return None
def box_str(title,lines):
    out=f"⏰ {cat_now().strftime('%H:%M:%S CAT | %d %b %Y')}\n"+"="*54+"\n "+title+"\n"+"="*54+"\n"
    for l in lines: out+="  "+l+"\n"
    out+="="*54; return out
def get_my_moves(p): return p.get("moves",[]) or assign_moves(p)
def start_dungeon(p,rank=None,is_gate=False,is_spawned=False):
    floor=p.get("dungeon_floor",1)
    if rank: hp,atk,exp=rank_stats(rank); enemy=f"{rank} Rank Beast"
    else: hp=80+floor*30; atk=12+floor*3; exp=100+floor*20; enemy=f"Floor {floor} Boss"
    DB["dungeon"]={"enemy":enemy,"enemy_hp":hp,"enemy_max":hp,"enemy_atk":atk,"floor":floor,"exp":exp,"in_dungeon":True,"rank":rank,"is_gate":is_gate,"is_spawned":is_spawned}; save()
    return box_str("🏰 DUNGEON ENTERED",[f"• Enemy: {enemy}",f"• Rank: {rank or 'Floor '+str(floor)}",f"• Enemy HP: {hp}",f"• Enemy ATK: {atk}",f"• Type: {'Personal Gate' if is_gate else 'Spawned Dungeon' if is_spawned else 'Dungeon'}","• Type /moves to see moves","• Then /moves <number> to attack"])
def use_move_dungeon(p,num):
    d=DB.get("dungeon")
    if not d or not d.get("in_dungeon"):
        cb=DB.get("catch_battle")
        if cb and cb.get("active"): return use_move_catch(p,num)
        return "❌ NOT in dungeon. Type /dungeon enter"
    moves=get_my_moves(p)
    try: idx=int(num)-1; mv=moves[idx] if 0<=idx<len(moves) else None
    except: mv=num
    if not mv: return "❌ Move not found. Type /moves"
    p["mp"]=max(0,p["mp"]-10); dmg=20+p["atk"]+random.randint(0,10); d["enemy_hp"]-=dmg; out=[f"⚔️ You used {mv}",f"• Damage: {dmg}",f"• Enemy: {d['enemy']}",f"• Enemy HP: {max(0,d['enemy_hp'])}"]
    if d["enemy_hp"]<=0:
        gain_exp(p,d["exp"]); p["dungeonClears"]+=1; cl=d["floor"]; p["dungeon_floor"]=cl+1; DB["dungeon"]=None; rew=give_reward(p,10000,5); save(); return box_str("🎉 FLOOR CLEARED",[f"• Floor {cl} cleared",f"• EXP: +{d['exp']}"]+rew+[f"• Next: {cl+1}"])
    edmg=max(1,d["enemy_atk"]+random.randint(0,10)-p["def"]//2); p["hp"]-=edmg; out.append(f"• Boss hit: -{edmg}"); out.append(f"• Your HP: {max(0,p['hp'])}")
    if p["hp"]<=0: p["hp"]=1; rs=p.get("checkpoint",1); p["dungeon_floor"]=rs; DB["dungeon"]=None; save(); return box_str("💀 YOU DIED",[f"• Died Floor {d['floor']}",f"• Respawn Floor {rs}"])
    save(); return "\n".join(out)+"\nYour turn! /moves <number>"
def start_catch(p):
    mon=random.choice(POKEMONS); hp=100+p["level"]*10; atk=10+p["level"]*2; DB["catch_battle"]={"pokemon":mon,"hp":hp,"max":hp,"atk":atk,"active":True,"owner":p["id"]}; save()
    return box_str("🎯 CATCH BATTLE STARTED",[f"• Wild Pokemon: {mon}",f"• Pokemon HP: {hp}",f"• Pokemon ATK: {atk}","• Fight it with /moves","• If you win, you catch it!","• No cheat - real battle"])
def use_move_catch(p,num):
    cb=DB.get("catch_battle")
    if not cb or not cb.get("active"): return "❌ No catch battle. Type /catch"
    if cb.get("owner")!=p["id"]: return "❌ This catch battle is not yours"
    moves=get_my_moves(p)
    try: idx=int(num)-1; mv=moves[idx] if 0<=idx<len(moves) else None
    except: mv=num
    if not mv: return "❌ Move not found. Type /moves"
    p["mp"]=max(0,p["mp"]-10); dmg=20+p["atk"]+random.randint(0,10); cb["hp"]-=dmg; out=[f"⚔️ You used {mv}",f"• Damage: {dmg}",f"• Pokemon: {cb['pokemon']}",f"• Pokemon HP: {max(0,cb['hp'])}"]
    if cb["hp"]<=0:
        p["pokemon"]=cb["pokemon"]; p["pet"]=cb["pokemon"]; gain_exp(p,100); DB["catch_battle"]=None; save(); return box_str("🎉 CAUGHT!",[f"• You caught: {p['pokemon']}",f"• EXP: +100","• Type /pokemon to see it"])
    edmg=max(1,cb["atk"]+random.randint(0,5)-p["def"]//2); p["hp"]-=edmg; out.append(f"• Pokemon hit: -{edmg}"); out.append(f"• Your HP: {max(0,p['hp'])}")
    if p["hp"]<=0: p["hp"]=1; DB["catch_battle"]=None; save(); return box_str("💀 YOU LOST CATCH",[f"• Pokemon: {cb['pokemon']} escaped",f"• Your HP: 1","• Try again: /catch"])
    save(); return "\n".join(out)+"\nYour turn! /moves <number>"
def apply_owner(p):
    p["isInfinity"]=True; p["isChosen"]=True; p["race"]="God"; p["atk"]=100; p["maxHp"]=300; p["hp"]=300; p["mp"]=9999; p["maxMp"]=9999; p["title"]="Immortal Emperor"; p["supreme"]=100; p["legendary"]=100
    if "Immortal Emperor" not in p.get("titles",[]): p["titles"].append("Immortal Emperor")
def apply_reg(p,race_raw,gender_raw,class_raw=""):
    if race_raw and race_raw.lower() in RACES:
        if race_raw.lower()=="god" and not is_owner(p) and p.get("displayName","").lower() not in OWNER_NAMES: return "God only for Owners"
        p["race"]=RACES[race_raw.lower()]
    if gender_raw and gender_raw.lower() in ["male","female"]: p["gender"]=gender_raw.capitalize()
    if class_raw and class_raw.lower() in CLASSES:
        if class_raw.lower()=="monarch" and not can_supreme(p): return "Monarch only for appointed"
        p["class"]=CLASSES[class_raw.lower()]
    if p.get("displayName","").lower() in OWNER_NAMES: apply_owner(p)
    assign_moves(p); return None
def promote_monarch(p,role):
    p["class"]="Monarch"
    if role=="mob": p["is_mob"]=True
    if role=="admin": p["is_admin"]=True
    if role=="botadmin": p["is_bot_admin"]=True
    if role=="groupadmin": p["is_group_admin"]=True
    assign_moves(p); save(); return p
def welcome_message(name,group_name="This Group"):
    L=[f"👋 Welcome @{name}!","","🏰 Welcome to INFINITY HUNTER",f"👥 Group: {group_name}","","📜 GROUP DESCRIPTION:"]
    for d in GROUP_DESC_LINES: L.append(f"• {d}")
    L.append(""); L.append("📏 BOT RULES:")
    for r in BOT_RULES: L.append(f"• {r}")
    L+=["","👉 START HERE:","• /register YourName","• /register YourName GOD Warrior Male","• /rules","• /menu","• /support"]
    return box_str("👋 WELCOME TO INFINITY",L)
def menu_text(p):
    pre=get_prefix(); tag=f"@{p['displayName']}"; L=[]
    L+=["⚡ INFINITY Hunter",f"• 👤 {tag}",f"• 🏷️ {p.get('title','Adventurer')}",f"• 💠 Lv{p['level']}",f"• 🧬 {p.get('race','-')}",f"• ⚔️ {p.get('class','-')}",f"• 🔑 Prefix: {pre}"]
    L.append("📋 GENERAL")
    for c in ["register <name>","stats","profile","stones","exchange <from> <to> <amt>","races","classes","rename <name>","info","economy","help","ping","rules","welcome @user","support","faq","hi","mods","rank","reset-icon","repo","reset-bio","reset-username","set-bio <text>","set-icon <emoji>","set-username <name>","webpass","webuser","card-events"]: L.append(f"• {pre}{c}")
    L.append("⚔️ BATTLE")
    for c in ["pvp @user","skill cast <magic> @user","skill activate <name>","skill deactivate <name>","move <move>","moves","mymoves","learn","accept","decline","forfeit"]: L.append(f"• {pre}{c}")
    L.append("🐉 CATCH - ALONE (Battle)")
    for c in ["catch","bag","battle","challenge @user","bestiary","equip <item>","givepoke @user <poke>","heal","mart","mart-buy <item>","party","pc","pokemon","spawnpokemon","start-journey","swap <a> <b>","t2party <poke>","t2pc <poke>","trade @user <poke>","trade-confirm","trade-delete","unequip <item>","cancel-evolution"]: L.append(f"• {pre}{c}")
    L.append("🏰 DUNGEON - ALONE")
    for c in ["dungeon enter","dungeon gate enter","gate","enter","inventory","use <item>","sell <item>"]: L.append(f"• {pre}{c}")
    L.append("👥 PARTY")
    for c in ["party create <name>","party invite @user","party accept","party leave","party kick @user"]: L.append(f"• {pre}{c}")
    L.append("🌀 LABYRINTH")
    for c in ["labyrinth status","labyrinth team create","labyrinth team invite","labyrinth team accept","labyrinth enter","labyrinth attack"]: L.append(f"• {pre}{c}")
    L.append("🏠 FAMILY")
    for c in ["family found <name>","family add @user","family accept","family leave","family info"]: L.append(f"• {pre}{c}")
    L.append("🛡️ COUNTRY RAIDS")
    for c in ["raid","raid join","raid start","raid attack","raid claim"]: L.append(f"• {pre}{c}")
    L.append("🪞 HALL OF REFLECTIONS")
    for c in ["arena","arena enter","arena fight"]: L.append(f"• {pre}{c}")
    L.append("🏛️ GUILD")
    for c in ["guild","guild apply","guild info","guild members","guild quest","guild fund","guild create","guild join"]: L.append(f"• {pre}{c}")
    L.append("⛪ CHURCH")
    for c in ["church","church join <god>","pray"]: L.append(f"• {pre}{c}")
    L.append("💰 ECONOMY")
    for c in ["daily","stones","wallet","bank","shop","buy <item>","give @user <amt>"]: L.append(f"• {pre}{c}")
    L.append("💼 JOBS")
    for c in ["job list","job apply <job>","job work","job info"]: L.append(f"• {pre}{c}")
    L.append("💍 MARRIAGE")
    for c in ["marry @user","marry accept","divorce"]: L.append(f"• {pre}{c}")
    L.append("🏠 HOUSING")
    for c in ["house buy","house upgrade","house info","rental list"]: L.append(f"• {pre}{c}")
    L.append("🐉 PETS")
    for c in ["pet list","pet buy <type>","pet name <name>","pet train","pet info"]: L.append(f"• {pre}{c}")
    L.append("🎨 MEDIA")
    for c in ["sticker","deaudio","facebook <url>","gisearch <query>","instagram <url>","lyrics <song>","pinterest <query>","play <song>","soundcloud <song>","spotify <song>","subreddit <name>","tiktok <url>","twitter <url>","yta <query>","yts <query>","ytv <query>"]: L.append(f"• {pre}{c}")
    L.append("🛒 MARKET")
    for c in ["market","market list","market buy <id>"]: L.append(f"• {pre}{c}")
    L.append("📢 REPORTS")
    for c in ["report <text>","request <text>","check reports"]: L.append(f"• {pre}{c}")
    L.append("🏆 LEADERBOARDS")
    for c in ["leaderboard","monarchs"]: L.append(f"• {pre}{c}")
    L.append("⚖️ CRIME")
    for c in ["rob @user <amt>","rob bank <amt>","bail","wanted"]: L.append(f"• {pre}{c}")
    L.append("🏥 HOSPITAL")
    for c in ["hospital","hospital checkup","hospital treat"]: L.append(f"• {pre}{c}")
    L.append("🏦 BANK")
    for c in ["bank","bank register","bank deposit <amt>","bank withdraw <amt>","bank transfer @user <amt>"]: L.append(f"• {pre}{c}")
    L.append("🛠️ UTILS")
    for c in ["calculator <expr>","carbon <code>","coubs <url>","crypto <coin>","img <query>","quotly <text>","react <emoji>","retrieve","screenshot <url>","steal <sticker>","telesticker <url>","track <number>","translator <text>","trivia","upload","urbandictionary <word>","wikipedia <query>"]: L.append(f"• {pre}{c}")
    L.append("🌸 WEEB")
    for c in ["anime <name>","character <name>","diverse","foxgirl","waifu"]: L.append(f"• {pre}{c}")
    L.append("🛡️ MODS")
    for c in ["banlist","chatbot on/off","join","leave","roleslist","set-event <text>","switch"]: L.append(f"• {pre}{c}")
    L.append("👮 OFFICER")
    for c in ["addmod @user","addsudo @user","ban @user","del-battle","delmod @user","delsudo @user","unban @user"]: L.append(f"• {pre}{c}")
    L.append("🛡️ STAFF")
    for c in ["promote @user","demote @user","addadmin @user","addmob @user","addbotadmin @user","addgroupadmin @user"]: L.append(f"• {pre}{c}")
    L.append("🐲 WORLD BOSS")
    for c in ["worldboss","demoncastle"]: L.append(f"• {pre}{c}")
    L.append("🔥 REBIRTH")
    L.append(f"• {pre}rebirth")
    L.append(f"• 💡 Tip: {tag} Type {pre}profile")
    return box_str("⚡ INFINITY Hunter",L)
def owner_help(p):
    pre=get_prefix(); return box_str("👑 OWNER HELP",[f"• 👑 {pre}setprefix <new>",f"• 📢 {pre}broadcast <msg>",f"• 👹 {pre}addmob @user",f"• ➕ {pre}addadmin @user",f"• 🤖 {pre}addbotadmin @user",f"• 👮 {pre}addgroupadmin @user",f"• 🛡️ {pre}kick @user",f"• 🚫 {pre}ban @user",f"• 📊 {pre}check reports"])
def mob_help(p):
    pre=get_prefix(); return box_str("👹 MOB HELP",[f"• ➕ {pre}addadmin @user",f"• 🤖 {pre}addbotadmin @user",f"• 👮 {pre}addgroupadmin @user",f"• 🛡️ {pre}kick @user",f"• 📊 {pre}check reports"])
def botadmin_help(p):
    pre=get_prefix(); return box_str("🤖 BOT ADMIN HELP",[f"• 👮 {pre}addgroupadmin @user",f"• 🛡️ {pre}kick @user",f"• 📊 {pre}check reports"])
def groupadmin_help(p):
    pre=get_prefix(); return box_str("👮 GROUP ADMIN HELP",[f"• 🛡️ {pre}kick @user",f"• 🔇 {pre}sybau @user",f"• 📣 {pre}tagall <msg>",f"• 🔒 {pre}close",f"• 🔓 {pre}open"])
def process_command(sender_id,raw_text,is_group=False,group_id=None):
    if sender_id.startswith("web:"):
        name=sender_id[4:]; p=get_player_by_name(name)
        if not p: p=get_player(sender_id,name)
    else: p=get_player(sender_id,sender_id)
    text=(raw_text or "").strip()
    spawn_note=""
    nr=maybe_spawn()
    if nr: spawn_note=f"\n\n⚠️ WARNING! A RANDOM DUNGEON APPEARED!\n• Rank: {nr}\n• Beasts inside!\n• /dungeon gate enter to enter as group!"
    if p.get("reg_step") in ["race","class","gender"] and not text.startswith(("/",".")):
        step=p["reg_step"]
        if step=="race" and text.lower() in RACES: p["race"]=RACES[text.lower()]; p["reg_step"]="class"; save(); return "❌ Not Done with registration\n👉 Next: Send Class"+spawn_note
        if step=="class" and text.lower() in CLASSES: p["class"]=CLASSES[text.lower()]; p["reg_step"]="gender"; save(); return "❌ Not Done with registration\n👉 Next: Send Gender"+spawn_note
        if step=="gender" and text.lower() in ["male","female"]: p["gender"]=text.capitalize(); p["reg_step"]="pin"; p["reg_stage"]="waiting_pin"; assign_moves(p); save(); return f"✅ Registration Steps Done!\n👤 {p['displayName']} | 🧬 {p['race']} | ⚔️ {p['class']} | ⚧ {p['gender']}\n🔐 Now Create 4-digit PIN"+spawn_note
        return f"❌ Invalid {step}. Try again."
    if text.isdigit() and len(text)==4 and p.get("reg_stage")=="waiting_pin":
        pend=DB.get("pending_reg",{}).get(p["id"])
        if pend: p["password"]=text; p["registered"]=True; p["reg_stage"]="done"; p["displayName"]=pend["name"]; p["name"]=pend["name"]; apply_reg(p,pend.get("race",""),pend.get("gender",""),pend.get("class","")); save(); return f"✅ Registration successfully done ✔\n👤 {p['displayName']}\n🔐 PIN saved!\n👉 Go back to group and continue"+spawn_note
        p["reg_stage"]="none"; save(); return "No pending. Type /register first."
    if text.isdigit():
        if time.time()<=p.get("awaiting_move_until",0):
            n=int(text); p["awaiting_move_until"]=0; return use_move_dungeon(p,n)+spawn_note
        return "⏰ Time expired! Type /moves 5 now."
    pre=get_prefix(); pu=None
    for cand in [pre,"/","."]:
        if text.startswith(cand): pu=cand; break
    if not pu: return f"Use {pre}help"
    stripped=text[len(pu):].strip()
    if not stripped: return f"Use {pre}help"
    parts=stripped.split(" "); cmd=parts[0].lower(); args=parts[1:]; rest=" ".join(args)
    if cmd in ["menu","help"]: return menu_text(p)+spawn_note
    if cmd=="ownerhelp":
        if not is_owner(p): return "❌ Owners only"
        return owner_help(p)
    if cmd=="mobhelp":
        if not p.get("is_mob") and not is_owner(p): return "❌ Mobs only"
        return mob_help(p)
    if cmd=="botadminhelp":
        if not p.get("is_bot_admin") and not is_owner(p): return "❌ Bot Admins only"
        return botadmin_help(p)
    if cmd=="groupadminhelp":
        if not p.get("is_group_admin") and not is_owner(p): return "❌ Group Admins only"
        return groupadmin_help(p)
    if cmd=="ping": return "🏓 Pong! ✅ Bot ON\n👑 Owners: 0779798568 / Lord Infinity / Immortal Emperor"+spawn_note
    if cmd=="setprefix":
        if not is_owner(p): return "❌ Owners only"
        if not args: return f"Use: {pre}setprefix <new> Current: {pre}"
        DB["config"]["prefix"]=args[0]; save(); return f"✅ Prefix changed to: {args[0]}"
    if cmd=="economy":
        e=WORLD.get("economy",BOT_ECONOMY); return box_str("💰 ECONOMY",[f"• HGSS - {fmt(e.get('hgss',0))}",f"• LGSS - {fmt(e.get('lgss',0))}",f"• MGSS - {fmt(e.get('mgss',0))}",f"• Zeni - {fmt(e.get('zeni',0))}",f"• Germ - {fmt(e.get('germ',0))}",f"• Total Players - {len(DB['players'])}"])+spawn_note
    if cmd=="info":
        reg=sum(1 for x in DB["players"].values() if x.get("registered")); e=WORLD.get("economy",BOT_ECONOMY); return box_str("ℹ️ BOT INFO",[f"• Bot: INFINITY v13",f"• Owners: 0779798568 / Lord Infinity / Immortal Emperor",f"• Prefix: {pre}",f"• Registered: {reg}",f"• HGSS: {fmt(e.get('hgss',0))}",f"• LGSS: {fmt(e.get('lgss',0))}",f"• MGSS: {fmt(e.get('mgss',0))}",f"• Zeni: {fmt(e.get('zeni',0))}",f"• Backups: 3x 1TB"])+spawn_note
    if cmd=="rules": return box_str("📏 INFINITY BOT RULES",[f"• {r}" for r in BOT_RULES])
    if cmd=="welcome":
        nm=" ".join(args).replace("@","") or p["displayName"]; return welcome_message(nm,"INFINITY Group")
    if cmd=="support": return box_str("🆘 SUPPORT",["• Join support group:","• Ask in group, tag Admin","• Or DM bot with /report","• Do NOT spam mods"])
    if cmd=="faq": return box_str("❓ FAQ",["• Q: How to register?","• A: /register Name Race Class Gender","• Q: How to get Stones?","• A: 70% from battles, 100% Zeni","• Q: How to get Supreme?","• A: Only Admins/Mobs/Owners","• Q: How to battle?","• A: /dungeon enter then /moves","• Q: How to fight Pokemon?","• A: /catch then /moves","• Q: How to enter Gate?","• A: /gate then /enter in 5 min"])
    if cmd=="hi": return f"👋 Hi @{p['displayName']}! Welcome to INFINITY HUNTER! Type /menu"
    if cmd=="mods": return box_str("👥 MODS",["• Owners: 0779798568","• Lord Infinity","• Immortal Emperor","• Mobs: See /mobhelp","• Bot Admins: See /botadminhelp"])
    if cmd=="rank": return box_str("🏆 RANK",[f"• Rank: {p['rank']}",f"• Level: {p['level']}",f"• EXP: {p['exp']}"])
    if cmd in ["set-bio","set-icon","set-username","reset-bio","reset-username","reset-icon"]:
        if cmd=="set-bio": p["bio"]=" ".join(args); save(); return f"✅ Bio set: {p['bio']}"
        if cmd=="set-icon": p["emoji"]=" ".join(args); save(); return f"✅ Icon set: {p['emoji']}"
        if cmd=="set-username": p["displayName"]=" ".join(args); save(); return f"✅ Username: {p['displayName']}"
        if cmd=="reset-bio": p["bio"]=""; save(); return "✅ Bio reset"
        if cmd=="reset-username": p["displayName"]=p["name"]; save(); return "✅ Username reset"
        if cmd=="reset-icon": p["emoji"]="⚔️"; save(); return "✅ Icon reset"
    if cmd in ["webpass","webuser","repo","card-events"]:
        if cmd=="webpass": return box_str("🔑 WEBPASS",["• Go to website","• Use your Name + PIN","• Web + WhatsApp SAME"])
        if cmd=="webuser": return f"👤 WebUser: @{p['displayName']}"
        if cmd=="repo": return box_str("📦 REPO",["• INFINITY HUNTER v13","• Owner: 0779798568","• No script sharing - Rule 13"])
        if cmd=="card-events": return box_str("📅 CARD EVENTS",["• Daily Boss: 7-Day World Boss","• Weekly: Guild War","• Season: 30 days"])
    if cmd=="gate":
        rank=rank_for_gate(p["level"]); DB.setdefault("personal_gates",{})[p["id"]]={"owner":p["id"],"owner_name":p["displayName"],"rank":rank,"expires":time.time()+300,"created":time.time()}; save()
        return box_str("🚪 GATE SUMMONED!",[f"• Rank: {rank} (Your Rank)",f"• Owner: @{p['displayName']}",f"• Exclusively yours - No one else can enter",f"• Expires in: 5 minutes",f"• To enter: /enter",f"• If you don't enter in 5 min, it disappears!"])+spawn_note
    if cmd=="enter":
        gate=DB.get("personal_gates",{}).get(p["id"])
        if not gate: return "No Gate summoned player Go sleep 😂🥱"
        if time.time()>gate["expires"]:
            del DB["personal_gates"][p["id"]]; save(); return "No Gate summoned player Go sleep 😂🥱"
        rank=gate["rank"]; del DB["personal_gates"][p["id"]]; save(); return start_dungeon(p,rank=rank,is_gate=True)
    if cmd in ["deaudio","facebook","gisearch","instagram","lyrics","pinterest","play","soundcloud","spotify","subreddit","tiktok","twitter","yta","yts","ytv"]: return box_str("🎨 MEDIA",[f"• {cmd} received:",f"• Query: {' '.join(args)}","• Download will be sent"])
    if cmd in ["banlist","chatbot","join","leave","roleslist","set-event","switch"]:
        if cmd=="banlist": return box_str("🚫 BANLIST",[f"• {x['displayName']}" for x in DB["players"].values() if x.get("banned")] or ["• No banned players"])
        if cmd=="chatbot": return f"🤖 Chatbot {args[0] if args else 'on'}"
        if cmd=="join": return "🚪 Bot will join your group soon - Send link to DM"
        if cmd=="leave": return "🚪 Bot left group"
        if cmd=="roleslist": return box_str("📋 ROLES",["• Owner","• Mob","• Admin","• Bot Admin","• Group Admin","• Player"])
        if cmd=="set-event": return f"📅 Event set: {' '.join(args)}"
        if cmd=="switch": return "🔄 Switched"
    if cmd in ["addmod","addsudo","ban","del-battle","delmod","delsudo","unban"]:
        if not (is_owner(p) or p.get("is_mob")): return "❌ Officer / Owner only"
        if cmd=="addmod":
            t=get_player_by_name(" ".join(args))
            if t: t["is_group_admin"]=True; save(); return f"✅ Added Mod @{t['displayName']}"
            return "Player not found"
        if cmd=="addsudo":
            t=get_player_by_name(" ".join(args))
            if t: t["is_bot_admin"]=True; save(); return f"✅ Added Sudo @{t['displayName']}"
            return "Player not found"
        if cmd=="ban":
            t=get_player_by_name(" ".join(args))
            if t: t["banned"]=True; save(); return f"🚫 Banned @{t['displayName']}"
            return "Player not found"
        if cmd=="unban":
            t=get_player_by_name(" ".join(args))
            if t: t["banned"]=False; save(); return f"✅ Unbanned @{t['displayName']}"
            return "Player not found"
        if cmd=="del-battle": DB["dungeon"]=None; DB["catch_battle"]=None; save(); return "🗑️ Battle deleted"
        if cmd in ["delmod","delsudo"]:
            t=get_player_by_name(" ".join(args))
            if t: t["is_group_admin"]=False; t["is_bot_admin"]=False; save(); return f"➖ Removed @{t['displayName']}"
            return "Player not found"
    if cmd=="catch":
        if DB.get("catch_battle") and DB["catch_battle"].get("active"): return "⚠️ Already in catch battle! Use /moves"
        return start_catch(p)
    if cmd in ["bag","battle","challenge","bestiary","equip","givepoke","learn","mart","mart-buy","party","pc","pokemon","spawnpokemon","start-journey","swap","t2party","t2pc","trade","trade-confirm","trade-delete","unequip","cancel-evolution"]:
        if cmd=="bag": return box_str("🎒 BAG",[f"• Pet: {p.get('pet') or 'None'}",f"• Pokemon: {p.get('pokemon') or 'None'}",f"• Moves: {len(p.get('moves',[]))}"])
        if cmd=="battle":
            if DB.get("catch_battle") and DB["catch_battle"].get("active"): return "⚔️ Already in catch battle! Use /moves"
            return start_catch(p)
        if cmd=="bestiary": return box_str("📖 BESTIARY",[f"• {x}" for x in POKEMONS])
        if cmd=="mart": return box_str("🛒 MART",["• Small Heal - 1 LGSS","• Medium Heal - 3 LGSS","• MP Potion - 1 LGSS","• Phoenix Elixir - 10 LGSS"])
        if cmd=="mart-buy": return f"🛍️ Bought {' '.join(args)} from Mart"
        if cmd=="pokemon": return box_str("🐉 POKEMON",[f"• Pet: {p.get('pet') or 'None'}",f"• Pokemon: {p.get('pokemon') or 'None'}",f"• Class: {p.get('class')}"])
        if cmd=="spawnpokemon": return f"✨ Wild {random.choice(POKEMONS)} appeared! Type /catch to fight it!"
        if cmd=="start-journey": return "🚀 Journey started! Type /catch to fight Pokemon!"
        if cmd=="trade": return f"🔄 Trade sent to {' '.join(args)} - They type /trade-confirm"
        if cmd=="trade-confirm": return "✅ Trade confirmed!"
        if cmd=="trade-delete": return "❌ Trade deleted"
        if cmd=="cancel-evolution": return "🚫 Evolution cancelled"
        return f"✅ {cmd} done: {' '.join(args)}"
    if cmd in ["calculator","carbon","coubs","crypto","img","quotly","react","retrieve","screenshot","steal","sticker","telesticker","track","translator","trivia","upload","urbandictionary","wikipedia"]:
        if cmd=="calculator":
            try: return f"🧮 Result: {eval(' '.join(args))}"
            except: return "🧮 Invalid expression"
        if cmd=="trivia": return box_str("❓ TRIVIA",["• Q: Who is Lord Infinity?","• A: Owner of INFINITY HUNTER"])
        if cmd=="crypto": return box_str("🪙 CRYPTO",[f"• Coin: {' '.join(args)}","• Price: Check real exchange"])
        return box_str("🛠️ UTILS",[f"• {cmd}: {' '.join(args)}","• Done ✅"])
    if cmd in ["anime","character","diverse","foxgirl","waifu"]:
        if cmd=="anime": return box_str("🎌 ANIME",[f"• Anime: {' '.join(args) or 'Naruto'}","• Moves from anime used in game"])
        if cmd=="character": return box_str("👤 CHARACTER",[f"• Character: {' '.join(args) or 'Goku'}","• Move: Kamehameha"])
        if cmd=="waifu": return "💖 Waifu: Random waifu sent!"
        if cmd=="foxgirl": return "🦊 Foxgirl: Random foxgirl sent!"
        if cmd=="diverse": return "🌈 Diverse: Random image sent!"
    if cmd=="report":
        if not rest: return f"Use: {pre}report @name <reason>"
        rid=len(DB.get("reports",[]))+1; DB.setdefault("reports",[]).append({"id":rid,"from":p["displayName"],"text":rest,"status":"pending","type":"report"}); save(); return f"✅ Reported successfully player\n🔒 Private not public\n🆔 Report #{rid}\n[Bot deleted your report message for privacy]"
    if cmd=="request":
        if not rest: return f"Use: {pre}request <what you want>"
        rid=len(DB.get("requests",[]))+1; DB.setdefault("requests",[]).append({"id":rid,"from":p["displayName"],"text":rest,"status":"pending","type":"request"}); save(); return f"✅ Request #{rid} received: {rest}\n📝 This stays public"
    if cmd=="check":
        if is_group: return "❌ /check reports only works in DM, not in group!"
        if not (is_owner(p) or p.get("is_admin") or p.get("is_mob") or p.get("is_bot_admin")): return "❌ Staff only"
        if args and args[0]=="reports":
            reps=DB.get("reports",[])+DB.get("requests",[])
            if not reps: return "📭 No reports/requests"
            lines=["📋 REPORTS / REQUESTS"]
            for r in reps: lines.append(f"• #{r['id']} [{r['type']}] {r['from']}: {r['text']} - {r['status']}")
            lines.append(f"• Use: {pre}check report <num> approve/deny"); return box_str("📋 CHECK REPORTS",lines)
        if args and args[0]=="report" and len(args)>=3:
            try: num=int(args[1])
            except: return "Report number must be number"
            action=args[2].lower()
            for lst in [DB.get("reports",[]),DB.get("requests",[])]:
                for r in lst:
                    if r["id"]==num: r["status"]=action; save(); return f"✅ Report #{num} {action}d by {p['displayName']}"
            return "Report not found"
        return f"Use: {pre}check reports OR {pre}check report <num> approve/deny"
    if cmd in ["addbotadmin","addmob","addadmin","addgroupadmin"]:
        if cmd=="addbotadmin" and not (is_owner(p) or p.get("is_mob") or p.get("is_admin")): return "❌ Owners/Mobs/Admins only"
        if cmd=="addmob" and not is_owner(p): return "❌ Owners only can promote Mobs"
        if cmd=="addadmin" and not (is_owner(p) or p.get("is_mob")): return "❌ Owners/Mobs only"
        if cmd=="addgroupadmin" and not (is_owner(p) or p.get("is_mob") or p.get("is_bot_admin") or p.get("is_admin")): return "❌ Staff only"
        t=get_player_by_name(" ".join(args).replace("@","").strip())
        if not t: return "❌ Player not found - They must register first!"
        role={"addbotadmin":"botadmin","addmob":"mob","addadmin":"admin","addgroupadmin":"groupadmin"}[cmd]; promote_monarch(t,role); rn={"botadmin":"Bot Admin","mob":"Mob","admin":"Admin","groupadmin":"Group Admin"}[role]; return f"✅ Successfully Added\n🎉 Congratulations player @{t['displayName']} you are now a {rn}\n👑 Class changed to Monarch - Stats + Moves match Lv{t['level']}\n📩 Check your DM for {rn} commands!"
    if cmd=="promote":
        if not (is_owner(p) or p.get("is_mob")): return "❌ Owners/Mobs only"
        t=get_player_by_name(" ".join(args))
        if not t: return "Player not found"
        return f"✅ Promoted @{t['displayName']}"
    if cmd=="demote":
        if not (is_owner(p) or p.get("is_mob")): return "❌ Owners/Mobs only"
        t=get_player_by_name(" ".join(args))
        if not t: return "Player not found"
        t["is_admin"]=False; t["is_mob"]=False; t["is_bot_admin"]=False; t["class"]="Warrior"; assign_moves(t); save(); return f"⬇️ Demoted @{t['displayName']} - Class back to Warrior"
    if cmd=="races": return box_str("🧬 RACES",[f"• {RACES[k]} - {RACE_AB[RACES[k]]}" for k in RACES])
    if cmd=="classes": return box_str("⚔️ CLASSES",[f"• {CLASSES[k]} - {CLASS_AB[CLASSES[k]]}" for k in CLASSES])
    if cmd=="stones": return box_str("💎 SPIRIT STONES", stones_lines(p)+[f"• Exchange: {pre}exchange lgss mgss 10"])
    if cmd=="exchange":
        if len(args)<3: return f"Use: {pre}exchange <from> <to> <amt>"
        try: amt=int(args[2])
        except: return "Amount must be number"
        r=convert_stones(p,args[0].lower(),args[1].lower(),amt); save(); return r
    if cmd=="register":
        if not args: return f"Use: {pre}register <name> <race> <class> <gender>\nExample: {pre}register Dominic GOD Warrior Male\nOr slow: {pre}register Dominic then send Race, Class, Gender"
        ra=""; ca=""; ga=""; np=args[:]
        if len(np)>=1 and np[-1].lower() in ["male","female"]: ga=np[-1]; np=np[:-1]
        if len(np)>=1 and np[-1].lower() in CLASSES: ca=np[-1]; np=np[:-1]
        if len(np)>=1 and np[-1].lower() in RACES: ra=np[-1]; np=np[:-1]
        name=" ".join(np)
        if not name: return "Enter name!"
        if p.get("registered") and p.get("reg_stage")=="done": return f"✅ Already {p['displayName']}"
        if not ra and not ca and not ga:
            DB.setdefault("pending_reg",{})[p["id"]]={"name":name,"race":"","gender":"","class":"","group_id":group_id,"sender":sender_id}; p["displayName"]=name; p["name"]=name; p["reg_step"]="race"; p["reg_stage"]="waiting_pin"; save(); return f"👤 Name saved: {name}\n❌ Not Done with registration\n👉 Next: Send Race"
        if is_group:
            DB.setdefault("pending_reg",{})[p["id"]]={"name":name,"race":ra,"gender":ga,"class":ca,"group_id":group_id,"sender":sender_id}; p["reg_stage"]="waiting_pin"; p["displayName"]=name; p["name"]=name; apply_reg(p,ra,ga,ca); p["registered"]=False; save(); return f"✅ Registration Done ✔ Player\n👤 {name}\n📩 For the Final step please check your DM with this BOT and finish the final step"
        else:
            DB.setdefault("pending_reg",{})[p["id"]]={"name":name,"race":ra,"gender":ga,"class":ca,"group_id":group_id,"sender":sender_id}; p["reg_stage"]="waiting_pin"; p["displayName"]=name; p["name"]=name; apply_reg(p,ra,ga,ca); p["registered"]=False; save(); return f"👤 Player, your registration: {pre}Register {name} {ra} {ca} {ga}\n✅ Step 1 Done!\n🔐 Now Create 4-digit PIN - Type 4 numbers"
    if not p["registered"] and cmd not in ["register","help","menu","ping","info","economy","link","password","prefix","races","classes","ownerhelp","mobhelp","rules","welcome","support","faq","hi"]: return f"❌ Not registered. Type {pre}register <name>"
    if cmd=="profile":
        lines=[f"✨ {p['displayName']} {p['rank']}",f"👑 Title: {p.get('title','Adventurer')}",f"🧬 Race: {p.get('race','-')}",f"⚔️ Class: {p.get('class','-')}",f"⚧ Gender: {p['gender']}",f"❤️ HP {p['hp']}/{p['maxHp']}",f"🔵 MP {p['mp']}/{p['maxMp']}",f"⚔️ ATK {p['atk']}",f"🛡️ DEF {p['def']}",f"💨 SPD {p['spd']}",f"💠 Level {p['level']}",f"⚡ EXP {p['exp']}/{exp_need(p['level'])}"]; lines+=stones_lines(p); lines+=[f"🏠 House: {p['house']}",f"🚗 Car: {p.get('car')}",f"🐉 Pet: {p.get('pet') or 'None'}",f"🐉 Pokemon: {p.get('pokemon') or 'None'}",f"📝 Bio: {p.get('bio','-')}"]; return box_str("👤 PROFILE",lines)
    if cmd=="stats":
        STR=p.get("str",0)+p["atk"]//5; AGI=p.get("agi",10); INT=p.get("int",0)+p["maxMp"]//20; VIT=p.get("vit",0)+p.get("con",10); DEF=p["def"]; LUK=p.get("luk",0)+p["spd"]//3
        lines=[f"🧩 {p['rank']}",f"💠 LV.{p['level']}",f"💎 GEMS: {p.get('gems',5)}","━━━━━━━━━━━━━━━━━━",f"💪 STR: {STR}",f"⚡ AGI: {AGI}",f"🧠 INT: {INT}",f"❤️ VIT: {VIT}",f"🛡️ DEF: {DEF}",f"🍀 LUK: {LUK}","━━━━━━━━━━━━━━━━━━",f"❤️ HP {p['hp']} / {p['maxHp']}",bar(p["hp"],p["maxHp"],22),f"⚡ XP {p['exp']} / {exp_need(p['level'])}",bar(p["exp"],exp_need(p["level"]),22),"━━━━━━━━━━━━━━━━━━"]; lines+=stones_lines(p); lines+=["━━━━━━━━━━━━━━━━━━",f"🏆 Rank: {p['rank']}",f"👑 Title: {p.get('title','Adventurer')}",f"🧬 Race: {p.get('race')}",f"⚔️ Class: {p.get('class')}"]; return box_str(f"📊 {p['displayName'].upper()} — ATTRIBUTES",lines)
    if cmd=="wallet": return box_str("💰 WALLET", stones_lines(p))
    if cmd=="daily":
        now=time.time(); left=86400-(now-p.get("lastDaily",0))
        if left>0: return box_str("⏳ DAILY WAIT",[f"Wait {time_left(left)}"])
        p["lastDaily"]=now; gain_exp(p,30); rew=give_reward(p,10000,10); save(); return box_str("🎁 DAILY",rew+[f"⚡ +30 EXP"])
    if cmd=="claim": rew=give_reward(p,5000,5); save(); return box_str("🎁 CLAIMED",rew)
    if cmd in ["moves","move"]:
        if args:
            try: return use_move_dungeon(p,args[0])+spawn_note
            except: return "Use /moves <number>"
        if DB.get("catch_battle") and DB["catch_battle"].get("active"):
            moves=get_my_moves(p); lines=["🎯 CATCH BATTLE",f"• Pokemon: {DB['catch_battle']['pokemon']}",f"• Pokemon HP: {DB['catch_battle']['hp']}",f"• Your HP: {p['hp']}/{p['maxHp']}",""]
            for i,m in enumerate(moves,1): lines.append(f"• {i}. {m}")
            p["awaiting_move_until"]=time.time()+5; save(); return box_str("⚔️ CHOOSE MOVE - CATCH",lines)
        if not DB.get("dungeon") or not DB["dungeon"].get("in_dungeon"):
            moves=get_my_moves(p); lines=[f"{p['displayName']} Lv{p['level']}",f"🧬 {p.get('race')} | ⚔️ {p.get('class')}"]
            for i,m in enumerate(moves,1): lines.append(f"• {i}. {m}")
            return box_str("📚 MY MOVES - 5 Moves",lines)
        moves=get_my_moves(p); lines=[f"⚔️ BATTLE Floor {DB['dungeon']['floor']}",f"❤️ HP: {p['hp']}/{p['maxHp']}",f"🔵 MP: {p['mp']}/{p['maxMp']}",f"🐉 Enemy: {DB['dungeon']['enemy']}",""]
        for i,m in enumerate(moves,1): lines.append(f"• {i}. {m}")
        lines+=["",f"⚡ QUICK: Type NUMBER e.g. 5 in 5 sec",f"⏰ After 5 sec use {pre}moves 5"]; p["awaiting_move_until"]=time.time()+5; save(); return box_str("⚔️ CHOOSE MOVE",lines)
    if cmd=="mymoves":
        moves=get_my_moves(p); lines=[f"{p['displayName']} Lv{p['level']}",f"🧬 {p.get('race')} | ⚔️ {p.get('class')}"]
        for i,m in enumerate(moves,1): lines.append(f"• {i}. {m}")
        return box_str("📚 MY MOVES",lines)
    if cmd=="learn": return box_str("🎓 LEARN",[f"• {m}" for m in get_my_moves(p)])
    if cmd=="dungeon":
        if args and args[0]=="enter":
            if DB.get("dungeon") and DB["dungeon"].get("in_dungeon"): return "⚠️ Already in dungeon!"
            return start_dungeon(p)
        if args and args[0]=="gate" and len(args)>=2 and args[1]=="enter":
            sd=WORLD.get("spawned_dungeon")
            if not sd: return "❌ No spawned dungeon right now. Wait 15 min for next one."
            if time.time()>sd["expires"]: WORLD["spawned_dungeon"]=None; save(); return "❌ Spawned dungeon expired. Wait 15 min."
            return start_dungeon(p,rank=sd["rank"],is_spawned=True)
        if args and args[0]=="leave": DB["dungeon"]=None; save(); return "🚪 Left dungeon"
        return f"Use {pre}dungeon enter | {pre}dungeon gate enter"
    if cmd=="leaderboard":
        s=sorted([x for x in DB["players"].values() if x.get("registered")], key=lambda x: x.get("level",1), reverse=True)[:10]; lines=["🏆 LEADERBOARD - Web + WhatsApp SAME"]
        for i,x in enumerate(s,1): lines.append(f"• {i}. {x['displayName']} Lv{x['level']} LGSS {fmt(x.get('lgss',0))}")
        return box_str("🏆 LEADERBOARD",lines)
    if cmd=="job":
        if not args or args[0]=="list":
            lines=["💼 JOBS - Pay in Zeni + LGSS"]
            for k in JOBS: lines.append(f"• {k} - {fmt(JOBS[k][0])} Zeni + {JOBS[k][1]} LGSS")
            return box_str("💼 JOBS",lines)
        if args[0]=="apply": p["job"]=" ".join(args[1:]); save(); return f"💼 You are now {p['job']}"
        if args[0]=="work":
            now=time.time(); left=2*3600-(now-p.get("lastWork",0))
            if left>0: return box_str("⏳ WORK WAIT",[f"Wait {time_left(left)}"])
            p["lastWork"]=now; j=JOBS.get(p["job"],(1000,1)); p["zeni"]+=j[0]; p["lgss"]=p.get("lgss",0)+j[1]; gain_exp(p,20); rew=give_reward(p,0,0); save(); return box_str("💼 WORK DONE",[f"• Zeni - +{fmt(j[0])}",f"• LGSS - +{j[1]}"]+rew)
        if args[0]=="info": return box_str("💼 JOB INFO",[f"• Job: {p['job']}"])
        return "Job done"
    if cmd=="pet":
        if not args or args[0]=="list":
            lines=["🐉 PETS"]
            for k in PETS: lines.append(f"• {k} - {PETS[k][0]} LGSS - {PETS[k][1]}")
            return box_str("🐉 PETS",lines)
        if args[0]=="buy":
            tn=" ".join(args[1:])
            if tn not in PETS: return "Pet not found. Type /pet list"
            cost=PETS[tn][0]
            if p.get("lgss",0)<cost: return f"Need {cost} LGSS"
            p["lgss"]-=cost; p["pet"]=tn; save(); return box_str("🐉 PET",[f"• You got {tn}",f"• Ability: {PETS[tn][1]}"])
        if args[0]=="name": p["pet"]=" ".join(args[1:]); save(); return f"🐉 Pet named: {p['pet']}"
        if args[0]=="train": gain_exp(p,50); save(); return "🐉 Dragon trained +50 EXP"
        if args[0]=="info": return box_str("🐉 PET INFO",[f"• Pet: {p.get('pet') or 'None'}"])
        return "Pet done"
    if cmd=="bank":
        if not args: return box_str("🏦 BANK", stones_lines(p))
        if args[0] in ["register","open"]:
            if p.get("bank_open"): return "✅ Bank already open"
            if p.get("lgss",0)<10: return "Need 10 LGSS"
            p["lgss"]-=10; p["bank_open"]=True; save(); return "🏦 Bank opened -10 LGSS"
        if args[0]=="deposit":
            amt=p.get("lgss",0) if len(args)<2 or args[1]=="all" else int(args[1]); p["lgss"]-=amt; p["bank"]+=amt; save(); return f"💎 Deposited {fmt(amt)} LGSS"
        if args[0]=="withdraw":
            amt=p["bank"] if len(args)<2 or args[1]=="all" else int(args[1]); p["bank"]-=amt; p["lgss"]=p.get("lgss",0)+amt; save(); return f"💎 Withdrew {fmt(amt)} LGSS"
        return "Bank done"
    if cmd=="heal":
        if p.get("lgss",0)<1: return "Need 1 LGSS"
        p["lgss"]-=1; p["hp"]=p["maxHp"]; p["mp"]=p["maxMp"]; save(); return "💊 Healed - HP/MP full"
    if cmd=="link": return box_str("📱 WHATSAPP LINKED",["Bot linked to 0779798568"])
    if cmd=="password": return "❌ Wrong password."
    if cmd=="race":
        if not args: return box_str("🧬 RACES",[f"• {RACES[k]} - {RACE_AB[RACES[k]]}" for k in RACES])
        if args[0].lower()=="god" and not is_owner(p): return "God only for Owners"
        p["race"]=RACES[args[0].lower()]; assign_moves(p); save(); return f"🧬 You are {p['race']}"
    if cmd=="class":
        if not args: return box_str("⚔️ CLASSES",[f"• {CLASSES[k]} - {CLASS_AB[CLASSES[k]]}" for k in CLASSES])
        if args[0].lower()=="monarch" and not can_supreme(p): return "Monarch only for appointed"
        p["class"]=CLASSES[args[0].lower()]; assign_moves(p); save(); return f"⚔️ You are {p['class']}"
    if cmd=="gender":
        if not args or args[0].lower() not in ["male","female"]: return "Use /gender male or female"
        p["gender"]=args[0].capitalize(); save(); return f"Gender: {p['gender']}"
    if cmd in ["labyrinth","family","families","raid","arena","worldboss","demoncastle","rebirth","guild","church","pray","kick","tagall","hidetag","close","open","sybau","unsybau","marry","divorce","spouse","house","rental","market","achievements","hunger","eat","tavern","feast","cook","quests","season","share","core","buy","bio","web","emoji","broadcast","rob","bail","breakout","wanted","hospital","immortal","skill","inventory","use","sell","go","notifications","monarchs","duel","train","gym","shop","equip","unequip"]:
        if cmd=="labyrinth" and args and args[0]=="force":
            if not is_owner(p): return "Only Owners"
            WORLD["labyrinth"]=800; save(); return "🌀 Labyrinth OPEN"
        if cmd=="raid" and args and args[0]=="claim": rew=give_reward(p,10000,10); save(); return box_str("🎁 RAID CLAIM",rew)
        if cmd=="arena" and args and args[0]=="enter": return "🪞 Entered Hall! Use /arena fight"
        if cmd=="guild" and args and args[0]=="create": p["guild"]=" ".join(args[1:]); save(); return f"🏛️ Guild: {p['guild']}"
        if cmd=="rob": return "🥷 Rob attempted"
        if cmd=="hospital": return "🏥 Hospital - /hospital checkup / treat"
        if cmd=="skill" and args and args[0]=="cast": return f"✨ Cast {' '.join(args[1:])}"
        return f"✅ {cmd} done: {' '.join(args)}"
    return f"❌ No Such Command - Type {pre}menu"
app=Flask(__name__)
HTML="""<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>INFINITY HUNTER</title><style>body{background:#050510;color:#fff;font-family:Arial;margin:0}input,select{width:100%;padding:14px;margin:8px 0;background:#000;color:#fff;border:2px solid #7B2FFF;border-radius:12px;box-sizing:border-box}button{width:100%;padding:14px;background:#FFD700;color:#000;border:none;border-radius:12px;font-weight:900;margin:8px 0}button:disabled{background:#333;color:#777}.card{background:#111128;border:1px solid #333;padding:16px;border-radius:16px;margin:12px}pre{white-space:pre-wrap;background:#000;padding:12px;border-radius:10px}.hidden{display:none}</style></head><body><div id='landing' style='text-align:center;padding:60px 16px'><h1 style='color:#FFD700'>⚡ INFINITY HUNTER ⚡</h1><button onclick='showAuth()' style='max-width:300px'>ENTER →</button></div><div id='auth' class='hidden' style='text-align:center;padding:20px'><div class='card' style='max-width:460px;margin:auto;text-align:left'><h2>📝 REGISTER / 🔑 LOGIN</h2><input id='name' placeholder='Name'><input id='pass' type='password' placeholder='Enter Password'><label>🧬 Race</label><select id='race'><option value=''>-- Pick Race --</option><option value='Human'>Human - Adapt</option><option value='Demon'>Demon - Demon Rage</option><option value='Fairy'>Fairy - Fairy Heal</option><option value='Mage'>Mage - Arcane Burst</option><option value='Elf'>Elf - Elf Arrow</option><option value='Vampire'>Vampire - Blood Drain</option><option value='Dragon'>Dragon - Dragon Breath</option><option value='Angel'>Angel - Holy Light</option><option value='God'>God - Owners Only</option></select><label>⚔️ Class</label><select id='class'><option value=''>-- Pick Class --</option><option value='Warrior'>Warrior - Slash</option><option value='Mage'>Mage - Fireball</option><option value='Assassin'>Assassin - Shadow Strike</option><option value='Healer'>Healer - Heal</option><option value='Archer'>Archer - Piercing Arrow</option><option value='Tank'>Tank - Shield Wall</option><option value='Necromancer'>Necromancer - Soul Drain</option><option value='Swordmaster'>Swordmaster - Dragon Smash</option></select><label>⚧ Gender</label><select id='gender'><option value='Male'>Male</option><option value='Female'>Female</option></select><button id='regbtn' onclick='doAuth("register")' disabled>⚡ REGISTER - Pick Race + Class</button><button onclick='doAuth("login")' style='background:#7B2FFF;color:#fff'>🔑 LOGIN</button><p id='authmsg'></p></div></div><div id='dash' class='hidden'><div style='background:#111128;padding:12px;display:flex;justify-content:space-between'><b>⚡ INFINITY HUNTER - CHAT</b><span id='who'></span></div><div style='padding:12px'><div class='card'><div id='chat'></div><input id='cmd' placeholder='Type e.g. /menu /profile /stones'><button onclick='sendChat()'>▶ SEND</button></div></div></div><script>let myName='';function showAuth(){document.getElementById('landing').classList.add('hidden');document.getElementById('auth').classList.remove('hidden');}function check(){let r=document.getElementById('race').value;let c=document.getElementById('class').value;let b=document.getElementById('regbtn');if(r&&c){b.disabled=false;b.textContent='⚡ REGISTER';}else{b.disabled=true;b.textContent='⚡ REGISTER - Pick Race + Class';}}document.getElementById('race').onchange=check;document.getElementById('class').onchange=check;async function doAuth(mode){let name=document.getElementById('name').value.trim();let pass=document.getElementById('pass').value.trim();let race=document.getElementById('race').value;let cls=document.getElementById('class').value;let gender=document.getElementById('gender').value;if(!name||!pass){document.getElementById('authmsg').textContent='Enter Name + Password';return;}if(mode=='register'&&(!race||!cls)){document.getElementById('authmsg').textContent='Pick Race + Class!';return;}let r=await fetch('/api/auth',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,pass,race,class:cls,gender,mode})});let j=await r.json();document.getElementById('authmsg').textContent=j.msg;if(j.ok){myName=name;document.getElementById('auth').classList.add('hidden');document.getElementById('dash').classList.remove('hidden');document.getElementById('who').textContent='@'+name;}}async function sendChat(){let t=document.getElementById('cmd').value;if(!t)return;let d=document.createElement('div');d.textContent='You: '+t;document.getElementById('chat').appendChild(d);document.getElementById('cmd').value='';let r=await fetch('/api/command',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:myName,text:t})});let j=await r.json();let d2=document.createElement('div');d2.textContent='Bot: '+j.reply;document.getElementById('chat').appendChild(d2);}</script></body></html>"""
@app.route('/')
def home(): return HTML
@app.route('/api/auth',methods=['POST'])
def api_auth():
    data=request.json or {}; name=(data.get('name') or '').strip(); pwd=(data.get('pass') or '').strip(); race=(data.get('race') or '').strip(); cls=(data.get('class') or '').strip(); gender=(data.get('gender') or 'Male').strip(); mode=data.get('mode','register')
    if not name or not pwd: return jsonify({"ok":False,"msg":"Enter Name + Password"})
    if name.lower() in OWNER_NAMES and pwd!=OWNER_PASSWORD: return jsonify({"ok":False,"msg":"Owners: Wrong password"})
    ex=get_player_by_name(name)
    if mode=="login":
        if not ex or not ex.get("registered"): return jsonify({"ok":False,"msg":"Not registered. Click REGISTER"})
        if ex.get("password") and ex.get("password")!=pwd: return jsonify({"ok":False,"msg":"Wrong password"})
        return jsonify({"ok":True,"msg":f"Welcome back {name}!"})
    if mode=="register" and (not race or not cls): return jsonify({"ok":False,"msg":"Pick Race + Class!"})
    if ex and ex.get("registered"): return jsonify({"ok":True,"msg":"Already registered - Logged in!"})
    p=get_player(f"web:{name}",name); p["password"]=pwd; p["registered"]=True; p["displayName"]=name; p["name"]=name; p["reg_stage"]="done"
    if name.lower() in OWNER_NAMES: apply_owner(p)
    else: apply_reg(p,race,gender,cls)
    save(); return jsonify({"ok":True,"msg":f"Registered {name}! Race: {p.get('race')} Class: {p.get('class')}"})
@app.route('/api/command',methods=['POST'])
def api_cmd():
    data=request.json or {}; name=data.get('name','Player'); text=data.get('text','/menu'); reply=process_command(f"web:{name}",text,is_group=False); save(); return jsonify({"reply":reply})
@app.route('/webhook',methods=['GET'])
def verify():
    if request.args.get('hub.verify_token')==VERIFY_TOKEN: return request.args.get('hub.challenge','')
    return "Invalid token",403
@app.route('/webhook',methods=['POST'])
def webhook():
    try:
        data=request.json or {}
        for entry in data.get('entry',[]):
            for change in entry.get('changes',[]):
                val=change.get('value',{})
                for msg in val.get('messages',[]):
                    sender=msg.get('from',''); text=msg.get('text',{}).get('body','')
                    if 'joined' in text.lower() or 'added' in text.lower():
                        nm=get_player(sender,sender).get('displayName',sender); send_whatsapp(sender,welcome_message(nm,"INFINITY Group")); continue
                    p_tmp=get_player(sender,sender); is_group=False; group_id=None
                    if text.lower().startswith(('/register','.register')) and p_tmp.get("reg_stage")!="waiting_pin": is_group=True; group_id="group_"+sender
                    if text.startswith('/') or text.startswith('.') or text.isdigit():
                        reply=process_command(sender,text,is_group=is_group,group_id=group_id); save(); send_whatsapp(sender,reply)
                        if is_group and "Registration Done" in reply:
                            pend=DB.get("pending_reg",{}).get(sender)
                            if pend: send_whatsapp(sender,f"👤 Player: /Register {pend['name']} {pend.get('race','')} {pend.get('class','')} {pend.get('gender','')}\n🔐 Now Create 4-digit PIN")
                        if text.isdigit() and len(text)==4 and "Registration successfully done" in reply: send_whatsapp(sender,f"🎉 Registration Successfully Done @{p_tmp.get('displayName','Player')}\n👋 Welcome to INFINITY HUNTER @{p_tmp.get('displayName','Player')}\n👉 Now do /help")
    except Exception as e: print("Webhook error",e)
    return "OK",200
def send_whatsapp(to,text):
    if not WHATSAPP_TOKEN or not WHATSAPP_PHONE_ID: print(f"WHATSAPP TO {to}: {text}"); return
    try:
        import urllib.request,json as js
        url=f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_ID}/messages"; payload=js.dumps({"messaging_product":"whatsapp","to":to,"type":"text","text":{"body":text[:4000]}}).encode(); req=urllib.request.Request(url,data=payload,headers={"Authorization":f"Bearer {WHATSAPP_TOKEN}","Content-Type":"application/json"}); urllib.request.urlopen(req,timeout=10)
    except Exception as e: print("Send error",e)
@app.route('/health')
def health(): return "OK - Infinity v13"
if __name__=='__main__':
    port=int(os.environ.get('PORT',10000)); print(f"INFINITY v13 LIVE on port {port}"); app.run(host='0.0.0.0',port=port)

