# INFINITY MERGED - ONE FILE - Web + WhatsApp - Owner: 0779798568 - Lord Infinity
import json, random, os, time, datetime, copy
from flask import Flask, request, jsonify

OWNER_NAME = "Lord Infinity"
OWNER_ID = "260779798568"
OWNER_PHONE = "0779798568"
SECRET_PASSWORD = "2164"
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
    filled=int(cur/maxv*length)
    filled=max(0,min(length,filled))
    return "█"*filled + "░"*(length-filled)

DB_FILE = "infinity_db.json"
DB = {"players": {}, "market": [], "pending_pvp": {}, "disabled": [], "admins": [], "guilds": {}, "disabled_groups": [], "car_listings": [], "last_cmd_time": 0, "backup": None, "backup_disabled": [], "backup_disabled_groups": [], "backup_guilds": {}, "dungeon": None, "guild_fund_requests": [], "groups": {}, "auto_battle": False, "first_lv500": None}
WORLD = {"totalZeni": 20000000000000, "totalPlayers": 0, "labyrinth": None}
if os.path.exists(DB_FILE):
    try:
        if os.path.getsize(DB_FILE) > 0:
            with open(DB_FILE) as f:
                d = json.load(f); DB = d.get("DB", DB); WORLD = d.get("WORLD", WORLD)
    except: pass
def save():
    try:
        with open(DB_FILE,"w") as f: json.dump({"DB":DB,"WORLD":WORLD},f)
    except: pass
def is_owner(pid): return str(pid) in [OWNER_ID,"260779798568","0779798568","me"] or "779798568" in str(pid)
def get_multiplier(p):
    if p.get("race")=="God" and (is_owner(p["id"]) or p["id"] in DB["admins"]): return 1.5
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
        p["exp"]-=exp_need(p["level"]); p["level"]+=1
        p["lifespan"]=p.get("lifespan",80)+random.randint(75,85)
        p["maxHp"]+=25; p["hp"]=p["maxHp"]; p["maxMp"]+=10; p["mp"]=p["maxMp"]
        p["atk"]+=4; p["def"]+=3; p["spd"]+=3; p["agi"]=p.get("agi",10)+2; p["con"]=p.get("con",10)+2
        p["rank"]=rank_for(p["level"])
    return amt
def gain_zeni(p,amt):
    amt=int(amt*get_multiplier(p)); p["zeni"]+=amt; return amt
def get_player(pid,name="Player"):
    if pid not in DB["players"]:
        now=cat_now()
        DB["players"][pid]={"id":pid,"name":name,"displayName":name,"registered":False,"race":"Human","level":1,"exp":0,"zeni":1000000,"bank":0,"bank_open":False,"bank_opened_at":0,"bank_deposit_total":0,"last_bank_profit":0,"savings":0,"hp":100,"maxHp":100,"mp":50,"maxMp":50,"atk":15,"def":10,"spd":12,"agi":10,"con":10,"rank":"E - Novice","wins":0,"losses":0,"dungeonClears":0,"dungeon_floor":1,"checkpoint":1,"kills":0,"job":"Unemployed","loan":0,"loanDue":0,"house":"None","houseTier":0,"property":"None","car":"None","shop":"None","pet":None,"guild_permit":False,"guild":"None","guildRank":"None","lastDaily":0,"lastWork":0,"lastClaim":0,"lastRob":0,"jailed":0,"banned":False,"questsDone":0,"notifications":[],"gender":"Not Set","age":15,"lifespan":80,"birthday":now.strftime("%d %b %Y"),"used_codes":[],"spouse":None,"title":"Adventurer","titles":["Adventurer"],"emoji":"Sword","password":"","cultRealm":0,"cultLayer":1,"cultXp":0,"cultNeed":100,"talentType":"","talentValue":"","talentGrade":"","isInfinity":False,"isChosen":False,"chosenUntil":0,"wood":0,"houseBuilt":False,"sect":"No Sect","sectRank":"-","hunger":100,"family":"No Family","party":"No Party","church":"No Church","inventory":{},"skills":[],"active_skills":[],"awaiting_move_until":0,"gems":5,"str":0,"int":0,"vit":0,"luk":0}
        WORLD["totalPlayers"]+=1
    defaults={"password":"","cultRealm":0,"cultLayer":1,"cultXp":0,"cultNeed":100,"talentType":"","talentValue":"","talentGrade":"","isInfinity":False,"isChosen":False,"chosenUntil":0,"wood":0,"houseBuilt":False,"sect":"No Sect","sectRank":"-","hunger":100,"family":"No Family","party":"No Party","church":"No Church","inventory":{},"skills":[],"active_skills":[],"awaiting_move_until":0,"gems":5,"str":0,"int":0,"vit":0,"luk":0}
    for k,v in defaults.items():
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
            if num==9 and p.get("race")!="God" and not is_owner(p["id"]): continue
            if num==10 and not is_owner(p["id"]): continue
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
        DB["dungeon"]=None; save()
        return box_str("FLOOR CLEARED",[f"Floor {cleared} cleared",f"+{fmt(r)} Zeni",f"+{d['exp']} EXP",f"Next Floor: {cleared+1}",f"Checkpoint: {p['checkpoint']}","Type /dungeon enter for NEXT DUNGEON"])
    edmg=max(1,d["enemy_atk"]+random.randint(0,10)-p["def"]//2); p["hp"]-=edmg; out.append(f"Boss hit you -{edmg} Your HP: {max(0,p['hp'])}")
    if p["hp"]<=0:
        p["hp"]=1; respawn=p.get("checkpoint",1); p["dungeon_floor"]=respawn; DB["dungeon"]=None; save()
        return box_str("YOU DIED",[f"Died on Floor {d['floor']}",f"Respawn at Checkpoint Floor {respawn}","HP set to 1"])
    save(); return "\n".join(out)+"\nYour turn! /moves <number> again"
def apply_register_details(p, race_raw, gender_raw):
    pretty={"human":"Human","demon":"Demon","fairy":"Fairy","mage":"Mage","elf":"Elf","vampire":"Vampire","dragon":"Dragon","angel":"Angel","god":"God"}
    if race_raw:
        r=race_raw.lower()
        if r in pretty:
            if r=="god" and not is_owner(p["id"]) and p.get("displayName","").lower()!="infinity": return "God only for Admins / Infinity"
            p["race"]=pretty[r]
    if gender_raw:
        g=gender_raw.lower()
        if g in ["male","female"]: p["gender"]=g.capitalize()
    if p.get("displayName","").lower()=="infinity" and p.get("race")=="God" and p.get("gender")=="Male":
        p["isInfinity"]=True; p["isChosen"]=True; p["chosenUntil"]=time.time()+2*24*3600
        p["race"]="God"; p["atk"]=100; p["maxHp"]=300; p["hp"]=300; p["mp"]=9999; p["maxMp"]=9999
        p["cultRealm"]=1; p["cultLayer"]=9; p["talentType"]="Bloodline"; p["talentValue"]="Primordial Chaos Bloodline"; p["talentGrade"]="Divine Grade"; p["talentRevealed"]=True
        p["title"]="Immortal Emperor"
        if "Immortal Emperor" not in p.get("titles",[]): p["titles"].append("Immortal Emperor")
    return None

def process_command(sender_id, raw_text):
    if sender_id.startswith("web:"):
        name=sender_id[4:]; p=get_player_by_name(name)
        if not p: p=get_player(sender_id, name)
    else:
        p=get_player(sender_id, sender_id)
    text=(raw_text or "").strip()
    # ===== NEW: BARE NUMBER WITHIN 5 SECONDS AFTER /moves =====
    # If player is fighting and just types "5" (no /) within 5 sec of /moves, use it
    if text.isdigit() and not text.startswith("/"):
        if time.time() <= p.get("awaiting_move_until",0):
            num=int(text)
            p["awaiting_move_until"]=0
            return use_move_in_dungeon(p, num)
        else:
            return "⏰ Time expired! 5 seconds passed.\nYou must type /moves 5 now.\nType /moves to see moves again."
    if not text.startswith("/"): return "Use /help - Example: /register Infinity"
    parts=text[1:].split(" "); cmd=parts[0].lower(); args=parts[1:]; rest=" ".join(args)
    # ===== NEW HELP - EXACTLY LIKE SCREENSHOT 1 - NO PLAYER/DAILY/LIFE LABELS =====
    if cmd=="help": return box_str("HELP MENU",[
        "• /register <name> — Join the world",
        "• /stats — View your stats",
        "• /profile — View your profile card",
        "• /rename <new name> — Change your display name",
        "• /info — Bot stats, uptime, and population by race",
        "• /help — Show this menu",
        "• /ping — Check if bot is alive",
        "",
        "⚔️  BATTLE",
        "• /pvp @user — Challenge someone",
        "• /skill cast <magic> @user — Cast magic",
        "• /skill activate <name> — Use buff skill, or reactivate a deactivated passive",
        "• /skill deactivate <name> — Turn off an always-on passive (e.g. Gluttony)",
        "• /move <move> — Use a move in battle",
        "• /moves — See your options during battle",
        "• /mymoves — View your full moveset anytime",
        "• /learn — View/confirm newly unlocked race moves",
        "• /accept — Accept a PvP challenge",
        "• /decline — Decline a challenge",
        "• /forfeit — Forfeit current battle",
        "",
        "🏰  DUNGEON",
        "• /dungeon enter — Enter the dungeon",
        "• /inventory — View your items",
        "• /use <item> [qty] — Use an item, or several at once (chests, tickets, potions, EXP booster)",
        "• Battle potions: Small Heal, Medium Heal, MP Potion, Greater MP Potion, Phoenix Elixir (full restore, clears stuns and debuffs), Stat Boost (+20% ATK and DEF for 3 turns) — use in any battle",
        "• /sell <item> [qty] — Sell for Zeni, one or several at once",
        "",
        "👥  PARTY",
        "• /party create <name> — Create a party",
        "• /party invite @user — Invite someone",
        "• /party accept — Accept an invite",
        "• /party leave — Leave your party",
        "• /party kick @user — Remove a member (leader only)",
        "",
        "• /register Steps:",
        "• Step 1: /register Infinity",
        "• Step 2: /register Infinity God male",
    ])
    if cmd=="ping": return "Pong! Alive! Lord Infinity Bot is ON ✅ Owner: 0779798568"
    if cmd=="info":
        reg=sum(1 for pl in DB["players"].values() if pl.get("registered"))
        return box_str("BOT INFO",["Bot: INFINITY AND BEYOND v6 MERGED","Owner Line: 0779798568 - Lord Infinity",f"Players registered: {reg}",f"Players total: {len(DB['players'])}",f"Economy: {fmt(WORLD['totalZeni'])}",f"Auto Battle: {'ON' if DB.get('auto_battle') else 'OFF'}"])
    if cmd=="register":
        if not args: return "Use: /register <name>  Example: /register Infinity\nThen: /register Infinity God male"
        name=args[0]; race_arg=args[1] if len(args)>=2 else ""; gender_arg=args[2] if len(args)>=3 else ""
        if p["registered"]:
            if len(args)>=2:
                if name.lower()!=p["displayName"].lower(): return f"You are already {p['displayName']}! Use /register {p['displayName']} {race_arg} {gender_arg}"
                err=apply_register_details(p, race_arg, gender_arg)
                if err: return err
                save(); return box_str("REGISTRATION COMPLETE",[f"Name: {p['displayName']}",f"Title: {p.get('title','Adventurer')}",f"Race: {p['race']}",f"Gender: {p['gender']}","1,000,000 Zeni","Web + WhatsApp SAME ACCOUNT ✅","Type /profile"])
            return f"Already registered as {p['displayName']}! Type /profile\nTo finish setup type: /register {p['displayName']} <race> <gender>  Example: /register {p['displayName']} God male"
        ex=get_player_by_name(name)
        if ex and ex["id"]!=p["id"]: return f"⚠️ Name '{name}' is already taken!"
        p["registered"]=True; p["displayName"]=name; p["name"]=name; p["zeni"]=1000000; p["race"]=random.choice(["Human","Demon"]); p["birthday"]=cat_now().strftime("%d %b %Y"); p["age"]=15; p["lifespan"]=random.randint(70,95)
        if race_arg or gender_arg:
            err=apply_register_details(p, race_arg, gender_arg)
            if err: return err
            save(); return box_str("WELCOME - IMMORTAL EMPEROR" if p.get("title")=="Immortal Emperor" else "WELCOME",[f"Hello {p['displayName']}",f"Title: {p.get('title','Adventurer')}",f"Race: {p['race']}",f"Gender: {p['gender']}","1,000,000 Zeni","Web + WhatsApp SAME ACCOUNT ✅","Type /profile"])
        save(); return box_str("WELCOME - STEP 1 DONE",[f"Hello {p['displayName']}",f"Race: {p['race']} (temporary)","1,000,000 Zeni","","⚠️ NOW DO STEP 2:",f"/register {name} <race> <gender>",f"Example: /register {name} God male","Races: Human Demon Fairy Mage Elf Vampire Dragon Angel God"])
    if not p["registered"] and cmd not in ["register","help","ping","info","link","password"]: return "Not registered. Type /register <name>  Example: /register Infinity"
    if cmd=="profile": return box_str("PROFILE",[f"{p['displayName']} {p['rank']}",f"Title: {p.get('title','Adventurer')}",f"Race: {p['race']} Gender: {p['gender']}",f"HP {p['hp']}/{p['maxHp']} MP {p['mp']}/{p['maxMp']}",f"ATK {p['atk']} DEF {p['def']} SPD {p['spd']}",f"Level {p['level']} EXP {p['exp']}/{exp_need(p['level'])}",f"Zeni {fmt(p['zeni'])} Bank {fmt(p['bank'])} Job: {p['job']}",f"House: {p['house']} Car: {p.get('car')}",f"Dungeon Floor: {p.get('dungeon_floor',1)} Checkpoint: {p.get('checkpoint',1)}",f"Cultivation: Realm {p.get('cultRealm',0)} Layer {p.get('cultLayer',1)}",f"Talent: {p.get('talentType','-')} {p.get('talentValue','-')} {p.get('talentGrade','')}",f"Perks: {', '.join(p.get('titles',[]))}"])
    # ===== NEW STATS - BUILT CARD LIKE SCREENSHOT 2 =====
    if cmd=="stats":
        # Map old stats to screenshot attributes
        STR=p.get("str",0)+p["atk"]//5; AGI=p.get("agi",10); INT=p.get("int",0)+p["maxMp"]//20; VIT=p.get("vit",0)+p.get("con",10); DEF=p["def"]; LUK=p.get("luk",0)+p["spd"]//3
        hp_pct=int(p["hp"]/max(1,p["maxHp"])*100); xp_pct=int(p["exp"]/max(1,exp_need(p["level"]))*100)
        rank_short=p["rank"].split(" - ")[0] if " - " in p["rank"] else p["rank"]
        return box_str(f"{p['displayName'].upper()} — ATTRIBUTES",[
            f"🧩 {rank_short} | 💠 LV.{p['level']} | 💎 GEMS: {p.get('gems',5)}",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━",
            f"💪 STR: {STR} (+{STR*2}% DMG)  |  ⚡ AGI: {AGI} (+{AGI}% Crit/Dodge)",
            f"🧠 INT: {INT} (+{INT}% Skill)  |  ❤️ VIT: {VIT} (+{VIT*10} Max HP)",
            f"🛡️ DEF: {DEF} (-{DEF} Boss DMG)  |  🍀 LUK: {LUK} (+{LUK}% Luck)",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━",
            f"❤️ HP {p['hp']} / {p['maxHp']} ({hp_pct}%)",
            bar(p["hp"], p["maxHp"], 22),
            f"⚡ XP {p['exp']} / {exp_need(p['level'])} ({xp_pct}%)",
            bar(p["exp"], exp_need(p["level"]), 22),
            "━━━━━━━━━━━━━━━━━━━━━━━━━━",
            f"💰 Zeni: {fmt(p['zeni'])}  |  🏦 Bank: {fmt(p['bank'])}",
            f"🏆 Rank: {p['rank']}  |  Title: {p.get('title','Adventurer')}",
            "",
            "📊 HUNTER ATTRIBUTES — Upgrade with /addstat [stat] [amt]!",
        ])
    if cmd=="addstat":
        if len(args)<2: return "Use: /addstat [stat] [amt]  Example: /addstat STR 5\nStats: STR AGI INT VIT DEF LUK"
        stat=args[0].lower(); 
        try: amt=int(args[1])
        except: return "Amount must be number"
        if p.get("gems",5)<amt: return f"Not enough GEMS! You have {p.get('gems',5)}"
        keymap={"str":"str","agi":"agi","int":"int","vit":"vit","def":"def","luk":"luk"}
        if stat not in keymap: return "Stats: STR AGI INT VIT DEF LUK"
        if stat=="def": p["def"]+=amt
        elif stat=="agi": p["agi"]+=amt
        else: p[keymap[stat]]=p.get(keymap[stat],0)+amt
        p["gems"]-=amt; save(); return f"✅ +{amt} {stat.upper()}! GEMS left: {p['gems']}\nType /stats to see built card"
    if cmd=="wallet": return box_str("WALLET",[f"Cash: {fmt(p['zeni'])}",f"Bank: {fmt(p['bank'])}",f"Assets: {fmt(total_assets(p))}",f"House: {p['house']} Car: {p.get('car')}"])
    if cmd=="daily":
        now=time.time(); left=86400-(now-p.get("lastDaily",0))
        if left>0: return box_str("DAILY WAIT",[f"Wait {time_left(left)}"])
        p["lastDaily"]=now; r=gain_zeni(p,10000); gain_exp(p,30); save(); return box_str("DAILY",[f"+{fmt(r)} Zeni","+30 EXP"])
    if cmd=="claim":
        now=time.time(); left=86400-(now-p.get("lastClaim",0))
        if left>0: return box_str("CLAIM WAIT",[f"Wait {time_left(left)}"])
        p["lastClaim"]=now; r=gain_zeni(p,5000); save(); return box_str("CLAIMED",[f"+{fmt(r)} Zeni"])
    # ===== NEW MOVES + MOVE - 5 SECOND RULE =====
    if cmd in ["moves","move"]:
        # /move 5 = same as /moves 5
        if args:
            try: num=int(args[0])
            except: return "Use /moves <number>  Example: /moves 5"
            p["awaiting_move_until"]=0; return use_move_in_dungeon(p,num)
        # No args: show options + start 5 sec window
        if not DB.get("dungeon") or not DB["dungeon"].get("in_dungeon"):
            # Not fighting - just show list like before
            my=get_my_moves(p); lines=[f"{p['displayName']} Lv{p['level']}"]
            for num in my: mv=ALL_MOVES[num]; lines.append(f"{num}. {mv['name']} - {mv['dmg']} dmg - {mv['desc']}")
            return box_str("MY MOVES",lines)
        # Fighting: show battle options + 5 sec timer
        my=get_my_moves(p); lines=[f"⚔️ BATTLE - Floor {DB['dungeon']['floor']} Boss HP: {DB['dungeon']['enemy_hp']}",f"Your HP: {p['hp']}/{p['maxHp']} MP: {p['mp']}/{p['maxMp']}",""]
        for num in my: mv=ALL_MOVES[num]; lines.append(f"{num}. {mv['name']} - {mv['dmg']} dmg - {mv['mp']} MP - {mv['desc']}")
        lines+=["", "⚡ QUICK: Just type the NUMBER e.g. 5 - within 5 seconds!","⏰ After 5 seconds you MUST type /moves 5"]
        p["awaiting_move_until"]=time.time()+5; save()
        return box_str("CHOOSE YOUR MOVE",lines)
    if cmd=="mymoves":
        my=get_my_moves(p); lines=[f"{p['displayName']} Lv{p['level']} Rank: {p['rank']}",f"HP {p['hp']} MP {p['mp']}"]
        for num in my: mv=ALL_MOVES[num]; lines.append(f"{num}. {mv['name']} - {mv['dmg']} dmg - {mv['desc']}")
        return box_str("MY MOVES",lines)
    if cmd=="learn":
        my=get_my_moves(p); lines=["Newly unlocked race moves:"]
        for num in my: mv=ALL_MOVES[num]; lines.append(f"{num}. {mv['name']} Lv{mv['lvl']} - {mv['desc']}")
        lines.append("Type /mymoves to confirm")
        return box_str("LEARN",lines)
    if cmd=="skill":
        if not args: return "Use: /skill cast <magic> @user | /skill activate <name> | /skill deactivate <name>"
        if args[0]=="cast":
            magic=" ".join(args[1:-1]) if len(args)>2 else " ".join(args[1:]); target=args[-1] if len(args)>1 else ""
            return box_str("SKILL CAST",[f"You cast {magic} on {target}","Damage based on your INT + Race Power"])
        if args[0]=="activate":
            name=" ".join(args[1:]); 
            if name not in p.get("active_skills",[]): p["active_skills"].append(name)
            save(); return f"✅ Activated: {name}"
        if args[0]=="deactivate":
            name=" ".join(args[1:])
            if name in p.get("active_skills",[]): p["active_skills"].remove(name)
            save(); return f"❌ Deactivated: {name} (always-on passive off)"
        return "Use: /skill cast /skill activate /skill deactivate"
    if cmd=="dungeon":
        if args and args[0]=="enter":
            if DB.get("dungeon") and DB["dungeon"].get("in_dungeon"): return "Already in dungeon! Use /moves"
            return start_dungeon(p)
        if args and args[0]=="floor": return box_str("DUNGEON FLOOR",[f"Current Floor: {p.get('dungeon_floor',1)}",f"Checkpoint: {p.get('checkpoint',1)}",f"Clears: {p.get('dungeonClears',0)}","Next: /dungeon enter"])
        if args and args[0]=="leave": DB["dungeon"]=None; save(); return "Left dungeon"
        return "Use /dungeon enter | /dungeon floor | /dungeon leave"
    if cmd=="inventory":
        inv=p.get("inventory",{})
        if not inv: return box_str("INVENTORY",["Empty - No items","Buy potions with /use /sell to trade"])
        lines=[f"{k} x{v}" for k,v in inv.items()]; return box_str("INVENTORY",lines)
    if cmd=="use":
        if not args: return "Use: /use <item> [qty]  Example: /use Small Heal 1"
        qty=1
        try: qty=int(args[-1]); item=" ".join(args[:-1])
        except: item=" ".join(args)
        inv=p.get("inventory",{})
        if inv.get(item,0)<qty: 
            # Potion effect even if not in inventory for now - give heal
            if "heal" in item.lower(): p["hp"]=min(p["maxHp"],p["hp"]+100); save(); return f"Used {item} +100 HP"
            return f"You don't have {item}"
        inv[item]-=qty; save(); return f"Used {item} x{qty}"
    if cmd=="sell":
        if not args: return "Use: /sell <item> [qty]"
        qty=1
        try: qty=int(args[-1]); item=" ".join(args[:-1])
        except: item=" ".join(args)
        price=1000*qty; r=gain_zeni(p,price); save(); return f"Sold {item} x{qty} for +{fmt(price)} Zeni"
    if cmd=="party":
        if not args: return "Use: /party create /invite /accept /leave /kick"
        if args[0]=="create": p["party"]=" ".join(args[1:]) or "My Party"; save(); return f"Party created: {p['party']}"
        if args[0]=="invite": return f"Invite sent to {' '.join(args[1:])} - They type /party accept"
        if args[0]=="accept": p["party"]=p.get("party","Party"); save(); return f"Joined party: {p['party']}"
        if args[0]=="leave": p["party"]="No Party"; save(); return "Left party"
        if args[0]=="kick": return f"Kicked {' '.join(args[1:])} (leader only)"
        return "Use: /party create /invite /accept /leave /kick"
    if cmd=="job":
        if not args or args[0]=="list": return box_str("JOBS",["cleaner 5k driver 12k","hacker 30k bank teller 20k","barber 8k chef 18k teacher 20k","farmer 10k miner 22k"])
        if args[0]=="apply": p["job"]=" ".join(args[1:]); save(); return box_str("JOB",[f"You are now {p['job']}"])
        if args[0]=="work":
            now=time.time(); left=2*3600-(now-p.get("lastWork",0))
            if left>0: return box_str("WORK WAIT",[f"Wait {time_left(left)}"])
            p["lastWork"]=now; pay={"cleaner":5000,"driver":12000,"hacker":30000,"bank teller":20000,"barber":8000,"chef":18000,"teacher":20000,"farmer":10000,"miner":22000}.get(p["job"],1000); r=gain_zeni(p,pay); gain_exp(p,20); save(); return box_str("WORK DONE",[f"+{fmt(r)} Zeni"])
    if cmd=="bank":
        if not args: return box_str("BANK",[f"Cash {fmt(p['zeni'])}",f"Bank {fmt(p['bank'])}",f"Open: {'YES' if p.get('bank_open') else 'NO'}","Use /bank open /bank deposit /bank withdraw /bank transfer @user <amount>"])
        if args[0]=="open":
            if p.get("bank_open"): return "Bank already open"
            if p["zeni"]<100000000: return "Need 100M Zeni to open bank"
            p["zeni"]-=100000000; WORLD["totalZeni"]+=100000000; p["bank_open"]=True; p["bank_opened_at"]=time.time(); save(); return box_str("BANK OPENED",["Paid 100M to Economy",f"Economy now: {fmt(WORLD['totalZeni'])}"])
        if args[0]=="deposit":
            if not p.get("bank_open"): return "Open bank first: /bank open - Need 100M"
            try: amt=p["zeni"] if len(args)<2 else int(args[1])
            except: amt=0
            if p["zeni"]<amt: return "Not enough"
            p["zeni"]-=amt; p["bank"]+=amt; save(); return f"Deposited {fmt(amt)} Bank {fmt(p['bank'])}"
        if args[0]=="withdraw":
            if not p.get("bank_open"): return "Open bank first"
            try: amt=p["bank"] if len(args)<2 else int(args[1])
            except: amt=0
            if p["bank"]<amt: return "Not enough"
            p["bank"]-=amt; p["zeni"]+=amt; save(); return f"Withdrew {fmt(amt)}"
        if args[0]=="transfer":
            if len(args)<3: return "Use /bank transfer @user <amount>"
            try: amt=int(args[-1])
            except: return "Amount must be number"
            target_name=" ".join(args[1:-1]).replace("@","").strip(); t=get_player_by_name(target_name)
            if not t: return f"Player {target_name} not found!"
            if p["bank"]<amt: return "Not enough in bank!"
            p["bank"]-=amt; t["zeni"]+=amt; save(); return f"Sent {fmt(amt)} to {t['displayName']} from Bank!"
        if args[0]=="loan":
            try: amt=int(args[1])
            except: amt=0
            if p["loan"]>0: return "Already have loan"
            p["loan"]=amt; p["loanDue"]=int(amt*1.2); p["zeni"]+=amt; save(); return f"LOAN Got {fmt(amt)} - Repay {fmt(p['loanDue'])} with /bank repay"
        if args[0]=="repay":
            amt=min(p["zeni"],p["loanDue"]); p["zeni"]-=amt; p["loanDue"]-=amt
            if p["loanDue"]<=0: p["loan"]=0; p["loanDue"]=0; save(); return "Loan repaid!"
            save(); return f"Repaid {fmt(amt)} Left {fmt(p['loanDue'])}"
    if cmd=="give":
        if len(args)<2: return "Use /give <player> <amount>"
        try: amt=int(args[-1])
        except: amt=0
        tid=" ".join(args[:-1]).replace("@","")
        if amt<=0: return "Amount must be >0"
        if p["zeni"]<amt: return "Not enough Zeni"
        t=get_player_by_name(tid)
        if not t: t=get_player(tid,tid)
        p["zeni"]-=amt; t["zeni"]+=amt; save(); return f"Gave {fmt(amt)} to {t['displayName']}"
    if cmd=="gamble":
        try: amt=int(args[0])
        except: amt=0
        if amt<=0 or p["zeni"]<amt: return "Use /gamble <amount>"
        roll=random.randint(0,99)
        if roll<45: r=gain_zeni(p,amt); save(); return box_str("YOU WON",[f"Roll {roll}",f"+{fmt(r)}"])
        else: p["zeni"]-=amt; save(); return box_str("YOU LOST",[f"Roll {roll}",f"-{fmt(amt)}"])
    if cmd=="rob":
        if not args: return "Use /rob <player> or /rob bank"
        now=time.time()
        if now-p.get("lastRob",0)<600: return "Rob cooldown. Wait 10 mins"
        p["lastRob"]=now
        if args[0]=="bank":
            if random.randint(1,100)<=45: amt=random.randint(1000000,5000000); r=gain_zeni(p,amt); save(); return box_str("ROB BANK SUCCESS",[f"Stole {fmt(r)}"])
            else: p["jailed"]=time.time()+600; fine=int(p["zeni"]*0.15); p["zeni"]-=fine; save(); return box_str("ROB BANK FAILED",["Caught! Jailed 10 mins",f"Fine: {fmt(fine)}"])
        target_name=" ".join(args).replace("@","").strip() if args[0]!="guild" else " ".join(args[1:])
        t=get_player_by_name(target_name)
        if not t: return "Target not found"
        if random.randint(1,100)<=45: pct=random.randint(5,15); amt=int(t["zeni"]*pct/100); t["zeni"]-=amt; r=gain_zeni(p,amt); save(); return box_str("ROB SUCCESS",[f"Robbed {t['displayName']}",f"Stole {fmt(r)}"])
        else: p["jailed"]=time.time()+300; fine=int(p["zeni"]*0.10); p["zeni"]-=fine; save(); return box_str("ROB FAILED",["Caught! Jailed 5 mins",f"Fine: {fmt(fine)}"])
    if cmd=="heal":
        if p["zeni"]<1000: return "Need 1000 Zeni"
        p["zeni"]-=1000; p["hp"]=p["maxHp"]; p["mp"]=p["maxMp"]; save(); return box_str("HEALED",["HP and MP full"])
    if cmd=="leaderboard":
        s=sorted(DB["players"].values(), key=lambda x: x.get("level",1), reverse=True)[:5]
        lines=["Top players"]
        for i,x in enumerate(s,1): lines.append(f"{i}. {x['displayName']} Lv{x['level']} {x['rank']}")
        return box_str("LEADERBOARD",lines)
    if cmd=="guild":
        if not args: return box_str("GUILDS",[f"Total: {len(DB['guilds'])}"])
        if args[0]=="create":
            gn=" ".join(args[1:]) or "My Guild"
            if gn in DB["guilds"]: return "Guild exists"
            if p["zeni"]<500000000: return "Need 500M to create guild"
            p["zeni"]-=500000000; DB["guilds"][gn]={"leader":p["displayName"],"leader_id":p["id"],"members":[p["displayName"]],"vault":500000000,"level":1}; p["guild"]=gn; p["guildRank"]="Leader"; save(); return box_str("GUILD CREATED",[f"{gn} created!","Deposited 500M to vault"])
        if args[0]=="join":
            gn=" ".join(args[1:])
            if gn not in DB["guilds"]: return "Guild not found"
            p["guild"]=gn; p["guildRank"]="Member"; save(); return f"Joined {gn}"
        if args[0]=="info":
            gn=p.get("guild","None")
            if gn not in DB["guilds"]: return "You are in no guild"
            g=DB["guilds"][gn]; return box_str("GUILD INFO",[f"Name: {gn}",f"Leader: {g['leader']}",f"Vault: {fmt(g.get('vault',0))}",f"Members: {len(g.get('members',[]))}"])
    if cmd=="marry":
        if not args: return "Use /marry <player>"
        t=get_player_by_name(" ".join(args))
        if not t: return "Player not found"
        p["spouse"]=t["displayName"]; t["spouse"]=p["displayName"]; save(); return box_str("MARRIED",[f"{p['displayName']} + {t['displayName']}"])
    if cmd=="house":
        if args and args[0]=="buy":
            if len(args)<2: return box_str("HOUSES",["1 Hut 100k 2 House 500k","3 Mansion 2M 4 Palace 10M"])
            tier=int(args[1]); prices={1:100000,2:500000,3:2000000,4:10000000}; names={1:"Hut",2:"House",3:"Mansion",4:"Palace"}
            if p["zeni"]<prices[tier]: return "Not enough"
            p["zeni"]-=prices[tier]; p["house"]=names[tier]; p["houseBuilt"]=True; save(); return box_str("BOUGHT",[f"You bought {names[tier]}"])
    if cmd=="car":
        if not args or args[0]=="list": return box_str("CARS",["Boda Boda 200k Corolla 2M","BMW 8M Lamborghini 30M Bugatti 100M"])
        if args[0]=="buy":
            name=" ".join(args[1:]); cost={"Boda Boda":200000,"Toyota Corolla":2000000,"BMW":8000000,"Lamborghini":30000000,"Bugatti":100000000}.get(name,200000)
            if p["zeni"]<cost: return f"Need {fmt(cost)}"
            p["zeni"]-=cost; p["car"]=name; p["spd"]+=5; save(); return box_str("BOUGHT",[f"You bought {name}"])
    if cmd=="pet":
        if not args: return box_str("PETS",["Fire 500k Ice 500k Shadow 1M"])
        if args[0]=="buy":
            tn=" ".join(args[1:]); cost=500000
            if p["zeni"]<cost: return f"Need {fmt(cost)}"
            p["zeni"]-=cost; p["pet"]=tn; save(); return box_str("PET",[f"You got {tn}"])
    if cmd=="immortal":
        if not is_owner(sender_id) and p.get("displayName","").lower()!="infinity": return "No Such Command Player - Only Lord Infinity (0779798568)"
        if not args: return box_str("IMMORTAL MENU",["/Immortal set <stat> <value>","/Immortal set economy zeni <amount>","/Immortal autobattle on/off","/Immortal stats","/Immortal players"])
        sub=args[0].lower()
        if sub=="autobattle": DB["auto_battle"]=(len(args)>1 and args[1].lower()=="on"); save(); return f"Auto Battle {'ON' if DB['auto_battle'] else 'OFF'}"
        if sub=="set":
            if len(args)>=4 and args[1].lower()=="economy" and args[2].lower()=="zeni": WORLD["totalZeni"]=int(args[3]); save(); return f"Economy Zeni = {fmt(WORLD['totalZeni'])} - Only Emperor"
            if len(args)<3: return "Use /Immortal set atk 100"
            stat=args[1].lower(); val=int(args[2]); mp={"atk":"atk","hp":"maxHp","mp":"maxMp","def":"def","spd":"spd","agi":"agi","con":"con"}
            if stat not in mp: return "Stats: atk hp mp def spd agi con"
            p[mp[stat]]=val
            if stat=="hp": p["hp"]=val
            if stat=="mp": p["mp"]=val
            save(); return f"{stat} = {val}"
        if sub=="stats": return box_str("IMMORTAL STATS",[f"Lv{p['level']}",f"HP {p['hp']} MP {p['mp']}",f"ATK {p['atk']} DEF {p['def']}",f"Zeni {fmt(p['zeni'])}"])
        if sub=="players": return f"Players: {len(DB['players'])}"
    if cmd=="link":
        if not is_owner(sender_id) and p.get("displayName","").lower()!="infinity": return "No Such Command Player - Only Lord Infinity"
        if not args or args[0].lower()!="whatsapp": return "Use /link whatsapp"
        return box_str("WHATSAPP LINKED",["Type /password 2164","Bot linked to WhatsApp 0779798568"])
    if cmd=="password":
        if args and args[0]=="2164": return box_str("WHATSAPP LINKED",["Password correct!","Bot linked to WhatsApp 0779798568"])
        return "Wrong password."
    if cmd=="race":
        if not args: return box_str("RACES",["human demon fairy mage elf vampire dragon angel God - Admins only"])
        ch=" ".join(args).lower()
        if ch=="god" and not is_owner(sender_id) and p.get("displayName","").lower()!="infinity": return "God only for Admins"
        pretty={"human":"Human","demon":"Demon","fairy":"Fairy","mage":"Mage","elf":"Elf","vampire":"Vampire","dragon":"Dragon","angel":"Angel","god":"God"}
        if ch not in pretty: return "Race not found"
        p["race"]=pretty[ch]; save(); return f"You are {p['race']}"
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
    if cmd=="market": return box_str("MARKET",[f"Items: {len(DB['market'])}"])
    if cmd=="quests": return box_str("QUESTS",["Work 1x Dungeon 1x PvP 1x"])
    if cmd=="go": return box_str("WHERE TO GO",["/go work /go home /go bar /go shop /go bank"])
    if cmd=="pvp":
        if not args: return "Use /pvp <player>"
        DB["pending_pvp"][p["id"]]=" ".join(args); save(); return f"Challenge sent to {' '.join(args)} - They type /accept"
    if cmd=="accept":
        if not DB.get("pending_pvp"): return "No challenge - Use /pvp first"
        return "Challenge accepted! Type /moves to fight!"
    if cmd=="decline": DB["pending_pvp"]={}; save(); return "Challenge declined"
    if cmd=="forfeit": DB["dungeon"]=None; save(); return "You forfeited current battle"
    if cmd=="labyrinth":
        if not args: return "Labyrinth Closed"
        if args[0]=="force":
            if p.get("displayName","").lower()!="infinity" and not is_owner(sender_id): return "Only Lord Infinity can force Labyrinth"
            WORLD["labyrinth"]=800; return "Labyrinth OPEN"
        if args[0]=="enter": return "Labyrinth Beast HP 800 - Use /moves"
    if cmd=="raid":
        if args and args[0]=="start": return "Raid Beast HP 1000 - Use /moves"
        return "Use /raid start"
    if cmd=="arena":
        if args and args[0]=="enter":
            if p["zeni"]<250000: return "Need 250k"
            p["zeni"]-=250000; save(); return "Entered Arena! /arena fight"
        if args and args[0]=="fight": return "Reflection HP 200 - Use /moves"
    return "No Such Command Player - Type /help"

app = Flask(__name__)
HTML = """<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>INFINITY HUNTER</title><style>body{background:#050510;color:#fff;font-family:Arial;padding:16px}input{width:100%;padding:12px;margin:6px 0;background:#000;color:#fff;border:2px solid #7B2FFF;border-radius:10px}button{width:100%;padding:13px;background:#FFD700;color:#000;border:none;border-radius:12px;font-weight:900;margin:6px 0}.card{background:#111128;border:1px solid #333;padding:12px;border-radius:16px;margin:8px 0}pre{white-space:pre-wrap;background:#000;padding:10px;border-radius:10px}</style></head><body><h1 style='color:#FFD700;text-align:center'>⚡ INFINITY HUNTER ⚡</h1><p style='text-align:center'>Web + WhatsApp SAME GAME • Owner: 0779798568 Lord Infinity</p><div class='card'><h3>REGISTER / LOGIN</h3><input id='name' placeholder='Name e.g. infinity'><input id='pass' placeholder='4-digit e.g. 2164' maxlength='4'><button onclick='doCmd("/register "+document.getElementById("name").value)'>⚡ REGISTER / LOGIN - PRESS THIS</button><p style='font-size:12px'>Infinity + 2164 = Lord Infinity Perks • Other names any 4-digit pass</p></div><div class='card'><h3>PLAY</h3><input id='cmd' placeholder='Type command e.g. /profile /daily /dungeon enter /moves 2'><button onclick='doCmd(document.getElementById("cmd").value)'>▶ SEND COMMAND</button><div style='display:flex;gap:6px;flex-wrap:wrap'><button onclick='doCmd("/profile")' style='width:48%;background:#7B2FFF;color:#fff'>👤 PROFILE</button><button onclick='doCmd("/daily")' style='width:48%;background:#7B2FFF;color:#fff'>🎁 DAILY</button><button onclick='doCmd("/dungeon enter")' style='width:48%;background:#FF0000;color:#fff'>🏰 DUNGEON</button><button onclick='doCmd("/moves")' style='width:48%;background:#00AA00;color:#fff'>⚔️ MOVES</button><button onclick='doCmd("/stats")' style='width:48%;background:#7B2FFF;color:#fff'>📊 STATS</button><button onclick='doCmd("/leaderboard")' style='width:48%;background:#FFD700;color:#000'>🏆 LEADERBOARD</button></div></div><pre id='out'>Welcome! Register first: Type name above and press REGISTER.</pre><script>let myName='';async function doCmd(text){if(!text) return; if(text.startsWith('/register')) myName=text.replace('/register ','').trim(); if(!myName) myName=document.getElementById('name').value.trim()||'Player'; let r=await fetch('/api/command',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:myName,text:text})}); let j=await r.json(); document.getElementById('out').textContent=j.reply;}</script></body></html>"""
@app.route('/')
def home(): return HTML
@app.route('/api/command', methods=['POST'])
def api_cmd():
    data=request.json or {}; name=data.get('name','Player'); text=data.get('text','/help')
    reply=process_command(f"web:{name}", text); save()
    p=get_player_by_name(name)
    return jsonify({"reply":reply,"player":p})
@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token')==VERIFY_TOKEN:
        return request.args.get('hub.challenge','')
    return "Invalid token",403
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data=request.json or {}
        for entry in data.get('entry',[]):
            for change in entry.get('changes',[]):
                for msg in change.get('value',{}).get('messages',[]):
                    sender=msg.get('from','')
                    text=msg.get('text',{}).get('body','')
                    if text.startswith('/') or text.isdigit():
                        reply=process_command(sender, text); save()
                        send_whatsapp(sender, reply)
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
def health(): return "OK - Infinity Bot Live - Owner 0779798568"
if __name__=='__main__':
    port=int(os.environ.get('PORT',10000))
    print(f"INFINITY MERGED LIVE on port {port} - Owner 0779798568")
    app.run(host='0.0.0.0', port=port)
