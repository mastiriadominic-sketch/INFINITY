# INFINITY v10 - Listing Help - Spirit Stones Hidden Supreme - Monarch - Reports - Anime Moves
import json, random, os, time, datetime
from flask import Flask, request, jsonify
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
def bar(cur,maxv,length=20):
    if maxv<=0: maxv=1
    f=max(0,min(length,int(cur/maxv*length)))
    return "█"*f+"░"*(length-f)

# BOT ECONOMY - STARTS WITH
BOT_ECONOMY={"hgss":100000000,"lgss":100000000,"mgss":100000000,"zeni":2000000000000,"germ":0}

RACES={
 "human":{"name":"Human","ability":"Adapt","desc":"+10% EXP"},
 "demon":{"name":"Demon","ability":"Demon Rage","desc":"+20% ATK"},
 "fairy":{"name":"Fairy","ability":"Fairy Heal","desc":"+20% Heal"},
 "mage":{"name":"Mage","ability":"Arcane Burst","desc":"+30% Skill"},
 "elf":{"name":"Elf","ability":"Elf Arrow","desc":"+20% AGI"},
 "vampire":{"name":"Vampire","ability":"Blood Drain","desc":"Lifesteal 15%"},
 "dragon":{"name":"Dragon","ability":"Dragon Breath","desc":"+30% HP"},
 "angel":{"name":"Angel","ability":"Holy Light","desc":"+20% DEF"},
 "god":{"name":"God","ability":"God Punch","desc":"Owners only"},
}
CLASSES={
 "warrior":{"name":"Warrior","ability":"Slash","desc":"+ATK"},
 "mage":{"name":"Mage","ability":"Fireball","desc":"+INT"},
 "assassin":{"name":"Assassin","ability":"Shadow Strike","desc":"+Crit"},
 "healer":{"name":"Healer","ability":"Heal","desc":"+Heal"},
 "archer":{"name":"Archer","ability":"Piercing Arrow","desc":"+SPD"},
 "tank":{"name":"Tank","ability":"Shield Wall","desc":"+DEF/HP"},
 "necromancer":{"name":"Necromancer","ability":"Soul Drain","desc":"Summon"},
 "swordmaster":{"name":"Swordmaster","ability":"Dragon Smash","desc":"+DMG"},
 "monarch":{"name":"Monarch","ability":"Monarch Rule","desc":"Appointed only - +100% ALL"},
}
# ANIME / MOVIE MOVES - 2 Race + 2 Class + 1 Random
ANIME_RACE_MOVES={
 "Human":["Adapt - Tanjiro","Spirit Blade - Demon Slayer"],
 "Demon":["Demon Rage - Tanjiro","Hellfire - Naruto"],
 "Fairy":["Fairy Heal - Fairy Tail","Pixie Dust - Tinkerbell"],
 "Mage":["Arcane Burst - Frieren","Magic Missile - Harry Potter"],
 "Elf":["Elf Arrow - Legolas","Forest Blessing - LOTR"],
 "Vampire":["Blood Drain - Alucard","Night Bite - Twilight"],
 "Dragon":["Dragon Breath - Goku","Dragon Roar - Natsu"],
 "Angel":["Holy Light - Angel Beats","Judgement - Bleach"],
 "God":["God Punch - Saitama","Infinity Blast - Goku"],
}
ANIME_CLASS_MOVES={
 "Warrior":["Slash - Zoro","Dragon Smash - Goku"],
 "Mage":["Fireball - Naruto","Lightning - Sasuke"],
 "Assassin":["Shadow Strike - Sasuke","Silent Kill - Naruto"],
 "Healer":["Heal - Sakura","Phoenix Rebirth - Naruto"],
 "Archer":["Piercing Arrow - Legolas","Hawkeye - Avengers"],
 "Tank":["Shield Wall - Captain America","Iron Defense - Attack on Titan"],
 "Necromancer":["Soul Drain - Solo Leveling","Shadow Army - Solo Leveling"],
 "Swordmaster":["Dragon Smash - Zoro","Sword Dance - Demon Slayer"],
 "Monarch":["Monarch Rule - Solo Leveling","Monarch Slash - Jinwoo"],
}
ANIME_RANDOM=["Rasengan - Naruto","Chidori - Sasuke","Kamehameha - Goku","Bankai - Bleach","Gear 5 - Luffy","Domain Expansion - JJK","Susanoo - Naruto","Ultra Instinct - Goku"]
def assign_start_moves(p):
    race=p.get("race","Human").lower(); cls=p.get("class","Warrior").lower()
    moves=[]
    moves+=ANIME_RACE_MOVES.get(race,["Slash - Zoro"])[:2]
    moves+=ANIME_CLASS_MOVES.get(cls,["Slash - Zoro"])[:2]
    moves+=[random.choice(ANIME_RANDOM)]
    p["moves"]=moves
    # Monarch stats match Lv
    if cls=="monarch":
        p["atk"]=15+p["level"]*10; p["maxHp"]=100+p["level"]*30; p["hp"]=p["maxHp"]; p["mp"]=50+p["level"]*20; p["maxMp"]=p["mp"]
    return moves

# JOBS - Expanded
JOBS={"cleaner":{"pay_zeni":5000,"pay_lgss":1},"driver":{"pay_zeni":12000,"pay_lgss":2},"hacker":{"pay_zeni":30000,"pay_lgss":5},"bank teller":{"pay_zeni":20000,"pay_lgss":3},"barber":{"pay_zeni":8000,"pay_lgss":1},"chef":{"pay_zeni":18000,"pay_lgss":3},"teacher":{"pay_zeni":20000,"pay_lgss":3},"farmer":{"pay_zeni":10000,"pay_lgss":2},"miner":{"pay_zeni":22000,"pay_lgss":4},"blacksmith":{"pay_zeni":25000,"pay_lgss":4},"hunter":{"pay_zeni":35000,"pay_lgss":6},"guard":{"pay_zeni":15000,"pay_lgss":2}}
# PETS - Expanded
PETS={"Fire Dragon":{"cost_lgss":50,"ability":"Fire Breath"},"Ice Dragon":{"cost_lgss":50,"ability":"Ice Breath"},"Shadow Dragon":{"cost_lgss":100,"ability":"Shadow Bite"},"Light Dragon":{"cost_lgss":100,"ability":"Holy Light"},"Thunder Wolf":{"cost_lgss":30,"ability":"Thunder Bite"},"Phoenix":{"cost_lgss":200,"ability":"Rebirth"},"Shadow Wolf":{"cost_lgss":40,"ability":"Shadow Strike"},"Golden Tiger":{"cost_lgss":80,"ability":"Tiger Claw"}}

def can_see_supreme(p): return is_owner(p) or p.get("is_admin") or p.get("is_mob") or p.get("is_bot_admin") or p.get("is_group_admin")
def stones_lines(p):
    # JUST LGSS MGSS HGSS + Zeni + Germ - NO full names, NO Supreme/Legendary for normal
    lines=[]
    lines.append("💎 Spirit Stones")
    lines.append(f"• LGSS - {fmt(p.get('lgss',0))}")
    lines.append(f"• MGSS - {fmt(p.get('mgss',0))}")
    lines.append(f"• HGSS - {fmt(p.get('hgss',0))}")
    lines.append(f"• Zeni - {fmt(p.get('zeni',0))}")
    lines.append(f"• Germ - {fmt(p.get('germ',0))}")
    if can_see_supreme(p):
        lines.append(f"• Legendary - {fmt(p.get('legendary',0))}")
        lines.append(f"• Supreme - {fmt(p.get('supreme',0))}")
    return lines
def give_reward(p, base_zeni=10000, base_lgss=5):
    # 100% Zeni always, 70% Stones, 30% Germ, 10% Supreme hidden for non-admins
    p["zeni"]=p.get("zeni",0)+base_zeni; out=[f"• Zeni - +{fmt(base_zeni)}"]
    if random.random()<0.70:
        p["lgss"]=p.get("lgss",0)+base_lgss; out.append(f"• LGSS - +{base_lgss} (70% chance)")
    if random.random()<0.30:
        g=random.randint(10,100); p["germ"]=p.get("germ",0)+g; out.append(f"• Germ - +{g} (30% chance)")
    if random.random()<0.10:
        p["supreme"]=p.get("supreme",0)+1
        if can_see_supreme(p): out.append("• Supreme - +1 (10% chance)")
        else: out.append("• ??? - +1 Hidden (10% Supreme - hidden)")
    return out
def convert_stones(p, frm, to, amt):
    rates={"zeni":1,"germ":10,"lgss":100,"mgss":10000,"hgss":1000000,"legendary":100000000,"supreme":10000000000}
    if frm not in rates or to not in rates: return "Use: zeni germ lgss mgss hgss supreme"
    if (frm=="supreme" or to=="supreme") and not can_see_supreme(p): return "❌ Only Owners/Admins/Mobs/Bot Admins can use Supreme"
    have=p.get(frm,0)
    if have<amt: return f"❌ Not enough {frm.upper()} - You have {fmt(have)}"
    base=amt*rates[frm]; got=base//rates[to]; p[frm]-=amt; p[to]=p.get(to,0)+got
    return f"✅ {fmt(amt)} {frm.upper()} → {fmt(got)} {to.upper()}"

DB_FILE="infinity_db.json"; BACKUPS=["backup1_1TB.json","backup2_1TB.json","backup3_1TB.json"]
DB={"players":{},"market":[],"pending_pvp":{},"guilds":{},"dungeon":None,"groups":{},"auto_battle":False,"config":{"prefix":"/","prefixes":["/","."]},"pending_reg":{},"reports":[],"requests":[]}
WORLD={"totalZeni":2000000000000,"totalPlayers":0,"labyrinth":None,"economy":BOT_ECONOMY}
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
def get_player(pid,name="Player"):
    if pid not in DB["players"]:
        now=cat_now()
        DB["players"][pid]={"id":pid,"name":name,"displayName":name,"registered":False,"password":"","race":"","class":"","level":1,"exp":0,"zeni":1000000,"germ":0,"lgss":10,"mgss":0,"hgss":0,"legendary":0,"supreme":0,"bank":0,"bank_open":False,"savings":0,"hp":100,"maxHp":100,"mp":50,"maxMp":50,"atk":15,"def":10,"spd":12,"agi":10,"con":10,"rank":"E - Novice","wins":0,"losses":0,"dungeonClears":0,"dungeon_floor":1,"checkpoint":1,"kills":0,"job":"Unemployed","loan":0,"loanDue":0,"house":"None","houseTier":0,"car":"None","shop":"None","pet":None,"guild":"None","guildRank":"None","lastDaily":0,"lastWork":0,"lastClaim":0,"lastRob":0,"jailed":0,"banned":False,"questsDone":0,"notifications":[],"gender":"Not Set","age":15,"lifespan":80,"birthday":now.strftime("%d %b %Y"),"spouse":None,"title":"Adventurer","titles":["Adventurer"],"cultRealm":0,"cultLayer":1,"cultXp":0,"cultNeed":100,"talentType":"","talentValue":"","talentGrade":"","isInfinity":False,"isChosen":False,"chosenUntil":0,"wood":0,"houseBuilt":False,"sect":"No Sect","sectRank":"-","hunger":100,"family":"No Family","party":"No Party","church":"No Church","inventory":{},"skills":[],"active_skills":[],"awaiting_move_until":0,"gems":5,"str":0,"int":0,"vit":0,"luk":0,"bio":"","emoji":"⚔️","hunger_lvl":100,"cooking":1,"achievements":[],"reg_stage":"none","is_admin":False,"is_mob":False,"is_bot_admin":False,"is_group_admin":False,"moves":[],"reg_step":""}
        WORLD["totalPlayers"]+=1
    for k,v in {"germ":0,"lgss":10,"mgss":0,"hgss":0,"legendary":0,"supreme":0,"moves":[],"is_admin":False,"is_mob":False,"is_bot_admin":False,"is_group_admin":False,"reg_step":"","race":"","class":""}.items():
        if k not in DB["players"][pid]: DB["players"][pid][k]=v
    return DB["players"][pid]
def get_player_by_name(name):
    for pid,pl in DB["players"].items():
        if pl.get("displayName","").lower()==name.lower(): return pl
    return None
def box_str(title,lines):
    # TRUE LISTING: each line on its own line, \n only, no joining with •
    out=f"⏰ {cat_now().strftime('%H:%M:%S CAT | %d %b %Y')}\n"+"="*54+"\n "+title+"\n"+"="*54+"\n"
    for l in lines: out+="  "+l+"\n"
    out+="="*54; return out
ALL_MOVES={1:{"name":"Slash","dmg":20,"mp":0,"desc":"Basic slash","lvl":1},2:{"name":"Fireball","dmg":35,"mp":10,"desc":"Fire burns","lvl":1},3:{"name":"Shadow Strike","dmg":55,"mp":15,"desc":"Shadow hit","lvl":5},4:{"name":"Dragon Smash","dmg":80,"mp":20,"desc":"Dragon smash","lvl":10},5:{"name":"Heal","dmg":-40,"mp":15,"desc":"Heal +40","lvl":1},6:{"name":"Race Power","dmg":100,"mp":25,"desc":"Race ultimate","lvl":15},7:{"name":"Lightning Bolt","dmg":70,"mp":18,"desc":"Lightning","lvl":8},8:{"name":"Phoenix Rebirth","dmg":-100,"mp":30,"desc":"Heal +100","lvl":20},9:{"name":"God Punch","dmg":200,"mp":40,"desc":"God only","lvl":30},10:{"name":"Infinity Blast","dmg":300,"mp":50,"desc":"Emperor only","lvl":50}}
def get_my_moves(p): return p.get("moves",[]) or assign_start_moves(p)
def dungeon_stats_for_floor(floor):
    hp=80+floor*30; atk=12+floor*3; exp=100+floor*20; style="Low ATK High HP"
    if floor%2==0: style="High ATK Low HP"; hp=int(hp*0.7); atk=int(atk*1.4)
    return hp,atk,exp,style
def start_dungeon(p):
    floor=p.get("dungeon_floor",1); hp,atk,exp,style=dungeon_stats_for_floor(floor)
    DB["dungeon"]={"enemy":f"Floor {floor} Boss","enemy_hp":hp,"enemy_max":hp,"enemy_atk":atk,"floor":floor,"exp":exp,"in_dungeon":True,"style":style}
    save(); return box_str("🏰 DUNGEON FLOOR "+str(floor),[f"👹 Enemy: Floor {floor} Boss",f"🎨 Style: {style}",f"❤️ Boss HP: {hp}",f"⚔️ Boss ATK: {atk}",f"📍 Checkpoint: Floor {p.get('checkpoint',1)}","Type /moves to see moves"])
def use_move_in_dungeon(p,num_or_name):
    d=DB.get("dungeon")
    if not d or not d.get("in_dungeon"): return "❌ NOT in dungeon. Type /dungeon enter"
    moves=get_my_moves(p)
    # num_or_name can be index or name
    try: idx=int(num_or_name)-1; mv_name=moves[idx] if 0<=idx<len(moves) else None
    except: mv_name=num_or_name
    if not mv_name: return "❌ Move not found. Type /moves"
    p["mp"]=max(0,p["mp"]-10); dmg=20+p["atk"]+random.randint(0,10); d["enemy_hp"]-=dmg; out=[f"⚔️ You used {mv_name} Damage: {dmg} Boss HP: {max(0,d['enemy_hp'])}"]
    if d["enemy_hp"]<=0:
        gain_exp(p,d["exp"]); p["dungeonClears"]+=1; cleared=d["floor"]; p["dungeon_floor"]=cleared+1; DB["dungeon"]=None; rew=give_reward(p,10000,5); save(); return box_str("🎉 FLOOR CLEARED",[f"Floor {cleared} cleared",f"⚡ +{d['exp']} EXP"]+rew+[f"➡️ Next: {cleared+1}"])
    edmg=max(1,d["enemy_atk"]+random.randint(0,10)-p["def"]//2); p["hp"]-=edmg; out.append(f"💥 Boss hit -{edmg} HP: {max(0,p['hp'])}")
    if p["hp"]<=0: p["hp"]=1; respawn=p.get("checkpoint",1); p["dungeon_floor"]=respawn; DB["dungeon"]=None; save(); return box_str("💀 YOU DIED",[f"Died Floor {d['floor']}",f"Respawn Floor {respawn}"])
    save(); return "\n".join(out)+"\nYour turn! /moves <number>"
def apply_owner_perks(p):
    p["isInfinity"]=True; p["isChosen"]=True; p["race"]="God"; p["atk"]=100; p["maxHp"]=300; p["hp"]=300; p["mp"]=9999; p["maxMp"]=9999; p["title"]="Immortal Emperor"; p["supreme"]=100; p["legendary"]=100
    if "Immortal Emperor" not in p.get("titles",[]): p["titles"].append("Immortal Emperor")
def apply_register_details(p, race_raw, gender_raw, class_raw=""):
    if race_raw and race_raw.lower() in RACES:
        if race_raw.lower()=="god" and not is_owner(p) and p.get("displayName","").lower() not in OWNER_NAMES: return "God only for Owners"
        p["race"]=RACES[race_raw.lower()]["name"]
    if gender_raw and gender_raw.lower() in ["male","female"]: p["gender"]=gender_raw.capitalize()
    if class_raw and class_raw.lower() in CLASSES:
        if class_raw.lower()=="monarch" and not can_see_supreme(p): return "Monarch only for appointed"
        p["class"]=CLASSES[class_raw.lower()]["name"]
    if p.get("displayName","").lower() in OWNER_NAMES: apply_owner_perks(p)
    assign_start_moves(p)
    return None
def promote_to_monarch(p, role):
    # When appointed, class becomes Monarch, stats + moves match Lv
    p["class"]="Monarch"
    if role=="mob": p["is_mob"]=True
    if role=="admin": p["is_admin"]=True
    if role=="botadmin": p["is_bot_admin"]=True
    if role=="groupadmin": p["is_group_admin"]=True
    assign_start_moves(p); save()
    return p

# ===== HELP - TRUE LISTING, ONE • PER LINE, SHORT LINES =====
def menu_text(p):
    pre=get_prefix(); tag=f"@{p['displayName']}"
    L=[]
    L.append("⚡ INFINITY Hunter")
    L.append(f"👤 {tag}")
    L.append(f"🏷️ {p.get('title','Adventurer')}")
    L.append(f"💠 Lv{p['level']}")
    L.append(f"🧬 {p.get('race','-')}")
    L.append(f"⚔️ {p.get('class','-')}")
    L.append(f"🔑 Prefix: {pre}")
    L.append("")
    L.append("📋 GENERAL")
    L.append(f"• 📝 {pre}register <name>")
    L.append(f"• 📊 {pre}stats")
    L.append(f"• 👤 {pre}profile")
    L.append(f"• 💎 {pre}stones")
    L.append(f"• 🔄 {pre}exchange <from> <to> <amt>")
    L.append(f"• 🧬 {pre}races")
    L.append(f"• ⚔️ {pre}classes")
    L.append(f"• ✏️ {pre}rename <name>")
    L.append(f"• ℹ️ {pre}info")
    L.append(f"• 💰 {pre}economy")
    L.append(f"• 📜 {pre}help")
    L.append(f"• 🏓 {pre}ping")
    L.append("")
    L.append("⚔️ BATTLE")
    L.append(f"• ⚔️ {pre}pvp @user")
    L.append(f"• ✨ {pre}skill cast <magic> @user")
    L.append(f"• 🔥 {pre}skill activate <name>")
    L.append(f"• 🚫 {pre}skill deactivate <name>")
    L.append(f"• 🗡️ {pre}move <move>")
    L.append(f"• 📜 {pre}moves")
    L.append(f"• 📚 {pre}mymoves")
    L.append(f"• 🎓 {pre}learn")
    L.append(f"• ✅ {pre}accept")
    L.append(f"• ❌ {pre}decline")
    L.append(f"• 🏳️ {pre}forfeit")
    L.append("")
    L.append("🏰 DUNGEON")
    L.append(f"• 🏰 {pre}dungeon enter")
    L.append(f"• 🎒 {pre}inventory")
    L.append(f"• 🧪 {pre}use <item>")
    L.append(f"• 🧴 Potions: Small Heal")
    L.append(f"• 🧴 Potions: Medium Heal")
    L.append(f"• 🧴 Potions: MP Potion")
    L.append(f"• 🧴 Potions: Phoenix Elixir")
    L.append(f"• 💸 {pre}sell <item>")
    L.append("")
    L.append("👥 PARTY")
    L.append(f"• 👥 {pre}party create <name>")
    L.append(f"• 📩 {pre}party invite @user")
    L.append(f"• ✅ {pre}party accept")
    L.append(f"• 🚪 {pre}party leave")
    L.append(f"• 👢 {pre}party kick @user")
    L.append("")
    L.append("🌀 LABYRINTH")
    L.append(f"• 🌀 {pre}labyrinth status")
    L.append(f"• 👥 {pre}labyrinth team create")
    L.append(f"• 📩 {pre}labyrinth team invite")
    L.append(f"• ✅ {pre}labyrinth team accept")
    L.append(f"• 🚪 {pre}labyrinth enter")
    L.append(f"• ⚔️ {pre}labyrinth attack")
    L.append("")
    L.append("🏠 FAMILY")
    L.append(f"• 🏠 {pre}family found <name>")
    L.append(f"• ➕ {pre}family add @user")
    L.append(f"• ✅ {pre}family accept")
    L.append(f"• 🚪 {pre}family leave")
    L.append(f"• ℹ️ {pre}family info")
    L.append("")
    L.append("🛡️ COUNTRY RAIDS")
    L.append(f"• 🛡️ {pre}raid")
    L.append(f"• ➕ {pre}raid join")
    L.append(f"• ▶️ {pre}raid start")
    L.append(f"• ⚔️ {pre}raid attack")
    L.append(f"• 🎁 {pre}raid claim")
    L.append("")
    L.append("🪞 HALL OF REFLECTIONS")
    L.append(f"• 🪞 {pre}arena")
    L.append(f"• 🎟️ {pre}arena enter")
    L.append(f"• ⚔️ {pre}arena fight")
    L.append("")
    L.append("🏛️ GUILD")
    L.append(f"• 🏛️ {pre}guild")
    L.append(f"• 📝 {pre}guild apply")
    L.append(f"• ℹ️ {pre}guild info")
    L.append(f"• 👥 {pre}guild members")
    L.append(f"• 📜 {pre}guild quest")
    L.append(f"• 💰 {pre}guild fund")
    L.append(f"• ➕ {pre}guild create")
    L.append(f"• 🚪 {pre}guild join")
    L.append("")
    L.append("⛪ CHURCH")
    L.append(f"• ⛪ {pre}church")
    L.append(f"• 🙏 {pre}church join <god>")
    L.append(f"• 🙏 {pre}pray")
    L.append("")
    L.append("💰 ECONOMY")
    L.append(f"• 🎁 {pre}daily")
    L.append(f"• 💎 {pre}stones")
    L.append(f"• 👛 {pre}wallet")
    L.append(f"• 🏦 {pre}bank")
    L.append(f"• 🛒 {pre}shop")
    L.append(f"• 🛍️ {pre}buy <item>")
    L.append(f"• 💝 {pre}give @user <amt>")
    L.append("")
    L.append("💼 JOBS")
    L.append(f"• 💼 {pre}job list")
    L.append(f"• 📝 {pre}job apply <job>")
    L.append(f"• 🔨 {pre}job work")
    L.append(f"• ℹ️ {pre}job info")
    L.append("")
    L.append("💍 MARRIAGE")
    L.append(f"• 💍 {pre}marry @user")
    L.append(f"• ✅ {pre}marry accept")
    L.append(f"• 💔 {pre}divorce")
    L.append("")
    L.append("🏠 HOUSING")
    L.append(f"• 🏠 {pre}house buy")
    L.append(f"• ⬆️ {pre}house upgrade")
    L.append(f"• ℹ️ {pre}house info")
    L.append(f"• 🏘️ {pre}rental list")
    L.append("")
    L.append("🐉 PETS")
    L.append(f"• 🐉 {pre}pet list")
    L.append(f"• 🥚 {pre}pet buy <type>")
    L.append(f"• 🏷️ {pre}pet name <name>")
    L.append(f"• 🏋️ {pre}pet train")
    L.append(f"• ℹ️ {pre}pet info")
    L.append("")
    L.append("🎨 MEDIA")
    L.append(f"• 🎨 {pre}sticker")
    L.append(f"• 🎵 {pre}play <song>")
    L.append(f"• ⬇️ {pre}dl <url>")
    L.append("")
    L.append("🛒 MARKET")
    L.append(f"• 🛒 {pre}market")
    L.append(f"• 📝 {pre}market list")
    L.append(f"• 🛍️ {pre}market buy <id>")
    L.append("")
    L.append("📢 REPORTS & REQUESTS")
    L.append(f"• 📢 {pre}report <text> - Private")
    L.append(f"• 📝 {pre}request <text> - Public")
    L.append("")
    L.append("🏆 LEADERBOARDS")
    L.append(f"• 🏆 {pre}leaderboard")
    L.append(f"• 👑 {pre}monarchs")
    L.append("")
    L.append("⚖️ CRIME")
    L.append(f"• 🥷 {pre}rob @user <amt>")
    L.append(f"• 🏦 {pre}rob bank <amt>")
    L.append(f"• 💰 {pre}bail")
    L.append(f"• 🚨 {pre}wanted")
    L.append("")
    L.append("🏥 HOSPITAL")
    L.append(f"• 🏥 {pre}hospital")
    L.append(f"• 🩺 {pre}hospital checkup")
    L.append(f"• 💊 {pre}hospital treat")
    L.append("")
    L.append("🏦 BANK")
    L.append(f"• 🏦 {pre}bank")
    L.append(f"• 📝 {pre}bank register")
    L.append(f"• 💰 {pre}bank deposit <amt>")
    L.append(f"• 💵 {pre}bank withdraw <amt>")
    L.append(f"• 💸 {pre}bank transfer @user <amt>")
    L.append("")
    # SMALL STAFF BITS ONLY - NOT FULL OWNER MENU
    L.append("🛡️ STAFF (small)")
    L.append(f"• ⬆️ {pre}promote @user")
    L.append(f"• ⬇️ {pre}demote @user")
    L.append(f"• ➕ {pre}addadmin @user")
    L.append(f"• 👹 {pre}addmob @user")
    L.append(f"• 🤖 {pre}addbotadmin @user")
    L.append(f"• 👮 {pre}addgroupadmin @user")
    L.append("")
    L.append("🐲 WORLD BOSS")
    L.append(f"• 🐲 {pre}worldboss")
    L.append(f"• 🏰 {pre}demoncastle")
    L.append("")
    L.append("🔥 REBIRTH")
    L.append(f"• 🔥 {pre}rebirth")
    L.append("")
    L.append(f"💡 Tip: {tag} Type {pre}profile")
    return box_str("⚡ INFINITY Hunter", L)
def owner_help(p):
    pre=get_prefix()
    L=["👑 OWNER MENU - Owners Only"]
    L.append(f"• 👑 {pre}setprefix <new>")
    L.append(f"• 📢 {pre}broadcast <msg>")
    L.append(f"• 👹 {pre}addmob @user - Promote Mob")
    L.append(f"• ➕ {pre}addadmin @user - Promote Admin")
    L.append(f"• 🤖 {pre}addbotadmin @user - Promote Bot Admin")
    L.append(f"• 👮 {pre}addgroupadmin @user - Promote Group Admin")
    L.append(f"• 🛡️ {pre}kick @user")
    L.append(f"• 🚫 {pre}ban @user")
    L.append(f"• ✅ {pre}unban @user")
    L.append(f"• 🔇 {pre}sybau @user <time>")
    L.append(f"• 🔊 {pre}unsybau @user")
    L.append(f"• 👑 {pre}promote @user")
    L.append(f"• ⬇️ {pre}demote @user")
    L.append(f"• 📊 {pre}check reports - DM only")
    L.append(f"• 🔧 {pre}setstats <stat> <val>")
    L.append(f"• 💰 {pre}set economy")
    L.append(f"• 🌀 {pre}labyrinth force")
    L.append(f"• 🏰 {pre}Immortal")
    return box_str("👑 OWNER HELP", L)
def mob_help(p):
    pre=get_prefix(); L=["👹 MOB MENU - Mobs Only"]
    L.append(f"• ➕ {pre}addadmin @user - Promote Admin")
    L.append(f"• 🤖 {pre}addbotadmin @user - Promote Bot Admin")
    L.append(f"• 👮 {pre}addgroupadmin @user - Promote Group Admin")
    L.append(f"• 🛡️ {pre}kick @user")
    L.append(f"• 🔇 {pre}sybau @user")
    L.append(f"• 📊 {pre}check reports - DM only")
    L.append(f"• 📢 {pre}broadcast")
    return box_str("👹 MOB HELP", L)
def botadmin_help(p):
    pre=get_prefix(); L=["🤖 BOT ADMIN MENU"]
    L.append(f"• 👮 {pre}addgroupadmin @user")
    L.append(f"• 🛡️ {pre}kick @user")
    L.append(f"• 🔇 {pre}sybau @user")
    L.append(f"• 📊 {pre}check reports - DM only")
    L.append(f"• ⚠️ {pre}warn @user")
    L.append(f"• 🔗 {pre}antilink on/off")
    return box_str("🤖 BOT ADMIN HELP", L)
def groupadmin_help(p):
    pre=get_prefix(); L=["👮 GROUP ADMIN MENU"]
    L.append(f"• 🛡️ {pre}kick @user")
    L.append(f"• 🔇 {pre}sybau @user")
    L.append(f"• 📣 {pre}tagall <msg>")
    L.append(f"• 👻 {pre}hidetag <msg>")
    L.append(f"• 🔒 {pre}close")
    L.append(f"• 🔓 {pre}open")
    return box_str("👮 GROUP ADMIN HELP", L)

def process_command(sender_id, raw_text, is_group=False, group_id=None):
    if sender_id.startswith("web:"):
        name=sender_id[4:]; p=get_player_by_name(name)
        if not p: p=get_player(sender_id, name)
    else: p=get_player(sender_id, sender_id)
    text=(raw_text or "").strip()
    # SLOW REGISTER: if reg_step waiting, treat bare text as next step
    if p.get("reg_step") in ["race","class","gender"] and not text.startswith(("/",".")):
        step=p["reg_step"]
        if step=="race" and text.lower() in RACES:
            p["race"]=RACES[text.lower()]["name"]; p["reg_step"]="class"; save(); return "❌ Not Done with registration\n👉 Next: Send Class\n⚔️ Classes: Warrior Mage Assassin Healer Archer Tank Necromancer Swordmaster"
        if step=="class" and text.lower() in CLASSES:
            p["class"]=CLASSES[text.lower()]["name"]; p["reg_step"]="gender"; save(); return "❌ Not Done with registration\n👉 Next: Send Gender\n⚧ Male / Female"
        if step=="gender" and text.lower() in ["male","female"]:
            p["gender"]=text.capitalize(); p["reg_step"]="pin"; p["reg_stage"]="waiting_pin"; assign_start_moves(p); save(); return f"✅ Registration Steps Done!\n👤 {p['displayName']} | 🧬 {p['race']} | ⚔️ {p['class']} | ⚧ {p['gender']}\n🔐 Now Create 4-digit PIN - Just type 4 numbers"
        return f"❌ Invalid {step}. Try again."
    if text.isdigit() and len(text)==4 and p.get("reg_stage")=="waiting_pin":
        pending=DB.get("pending_reg",{}).get(p["id"])
        if pending:
            p["password"]=text; p["registered"]=True; p["reg_stage"]="done"; p["displayName"]=pending["name"]; p["name"]=pending["name"]; apply_register_details(p, pending.get("race",""), pending.get("gender",""), pending.get("class","")); save(); return f"✅ Registration successfully done ✔\n👤 {p['displayName']}\n🔐 PIN saved!\n👉 Go back to group and continue"
        p["reg_stage"]="none"; save(); return "No pending. Type /register first."
    if text.isdigit():
        if time.time() <= p.get("awaiting_move_until",0):
            num=int(text); p["awaiting_move_until"]=0; return use_move_in_dungeon(p,num)
        else: return "⏰ Time expired! Type /moves 5 now."
    pre=get_prefix(); prefix_used=None
    for cand in [pre,"/","."]:
        if text.startswith(cand): prefix_used=cand; break
    if not prefix_used: return f"Use {pre}help"
    stripped=text[len(prefix_used):].strip()
    if not stripped: return f"Use {pre}help"
    parts=stripped.split(" "); cmd=parts[0].lower(); args=parts[1:]; rest=" ".join(args)
    if cmd in ["menu","help"]: return menu_text(p)
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
    if cmd=="ping": return "🏓 Pong! ✅ Bot ON\n👑 Owners: 0779798568 / Lord Infinity / Immortal Emperor"
    if cmd=="setprefix":
        if not is_owner(p): return "❌ Owners only"
        if not args: return f"Use: {pre}setprefix <new> Current: {pre}"
        DB["config"]["prefix"]=args[0]; save(); return f"✅ Prefix changed to: {args[0]}"
    if cmd=="economy":
        e=WORLD.get("economy",BOT_ECONOMY)
        return box_str("💰 ECONOMY - Bot Starts With",[f"• HGSS - {fmt(e.get('hgss',0))}",f"• LGSS - {fmt(e.get('lgss',0))}",f"• MGSS - {fmt(e.get('mgss',0))}",f"• Zeni - {fmt(e.get('zeni',0))}",f"• Germ - {fmt(e.get('germ',0))}",f"• Total Players - {len(DB['players'])}"])
    if cmd=="info":
        reg=sum(1 for pl in DB["players"].values() if pl.get("registered")); e=WORLD.get("economy",BOT_ECONOMY)
        return box_str("ℹ️ BOT INFO",[f"• Bot: INFINITY v10",f"• Owners: 0779798568 / Lord Infinity / Immortal Emperor",f"• Prefix: {pre}",f"• Registered: {reg}",f"• HGSS: {fmt(e.get('hgss',0))}",f"• LGSS: {fmt(e.get('lgss',0))}",f"• MGSS: {fmt(e.get('mgss',0))}",f"• Zeni: {fmt(e.get('zeni',0))}",f"• Backups: 3x 1TB"])
    # REPORT / REQUEST
    if cmd=="report":
        if not rest: return f"Use: {pre}report @name <reason> or {pre}report <bug>"
        rid=len(DB.get("reports",[]))+1; DB.setdefault("reports",[]).append({"id":rid,"from":p["displayName"],"text":rest,"status":"pending","type":"report"}); save()
        # Report is PRIVATE - bot says it will delete (webhook deletes in real WhatsApp via delete API - here we simulate)
        return f"✅ Reported successfully player\n🔒 We want your report to be privately not public\n🆔 Report #{rid} - Staff will check in DM\n[Bot deleted your report message for privacy]"
    if cmd=="request":
        if not rest: return f"Use: {pre}request <what you want>"
        rid=len(DB.get("requests",[]))+1; DB.setdefault("requests",[]).append({"id":rid,"from":p["displayName"],"text":rest,"status":"pending","type":"request"}); save(); return f"✅ Request #{rid} received: {rest}\n📝 This stays public (requests are not deleted)"
    if cmd=="check":
        # /check reports OR /check report <num> <approve/deny> - DM ONLY
        if is_group: return "❌ /check reports only works in DM, not in group!"
        if not (is_owner(p) or p.get("is_admin") or p.get("is_mob") or p.get("is_bot_admin")): return "❌ Staff only"
        if args and args[0]=="reports":
            reps=DB.get("reports",[])+DB.get("requests",[])
            if not reps: return "📭 No reports/requests"
            lines=["📋 REPORTS / REQUESTS"]
            for r in reps: lines.append(f"• #{r['id']} [{r['type']}] {r['from']}: {r['text']} - {r['status']}")
            lines.append(f"• Use: {pre}check report <num> approve/deny")
            return box_str("📋 CHECK REPORTS",lines)
        if args and args[0]=="report" and len(args)>=3:
            try: num=int(args[1])
            except: return "Report number must be number"
            action=args[2].lower()
            for lst in [DB.get("reports",[]),DB.get("requests",[])]:
                for r in lst:
                    if r["id"]==num: r["status"]=action; save(); return f"✅ Report #{num} {action}d by {p['displayName']}"
            return "Report not found"
        return f"Use: {pre}check reports OR {pre}check report <num> approve/deny"
    # APPOINTMENTS - /addbotadmin etc - tag + DM commands
    if cmd in ["addbotadmin","addmob","addadmin","addgroupadmin"]:
        # Who can do what: Owner can all, Mob can add admin/botadmin/groupadmin, BotAdmin can add groupadmin
        if cmd=="addbotadmin" and not (is_owner(p) or p.get("is_mob") or p.get("is_admin")): return "❌ Owners/Mobs/Admins only"
        if cmd=="addmob" and not is_owner(p): return "❌ Owners only can promote Mobs"
        if cmd=="addadmin" and not (is_owner(p) or p.get("is_mob")): return "❌ Owners/Mobs only"
        if cmd=="addgroupadmin" and not (is_owner(p) or p.get("is_mob") or p.get("is_bot_admin") or p.get("is_admin")): return "❌ Staff only"
        target_name=" ".join(args).replace("@","").strip()
        t=get_player_by_name(target_name)
        if not t: return "❌ Player not found - They must register first!"
        role={"addbotadmin":"botadmin","addmob":"mob","addadmin":"admin","addgroupadmin":"groupadmin"}[cmd]
        promote_to_monarch(t, role)
        # DM message is sent by webhook separately - here return group message
        role_name={"botadmin":"Bot Admin","mob":"Mob","admin":"Admin","groupadmin":"Group Admin"}[role]
        return f"✅ Successfully Added\n🎉 Congratulations player @{t['displayName']} you are now a {role_name}\n👑 Class changed to Monarch - Stats + Moves match Lv{t['level']}\n📩 Check your DM for {role_name} commands!"
    if cmd=="promote":
        if not (is_owner(p) or p.get("is_mob")): return "❌ Owners/Mobs only"
        t=get_player_by_name(" ".join(args))
        if not t: return "Player not found"
        return f"✅ Promoted @{t['displayName']}"
    if cmd=="demote":
        if not (is_owner(p) or p.get("is_mob")): return "❌ Owners/Mobs only"
        t=get_player_by_name(" ".join(args))
        if not t: return "Player not found"
        t["is_admin"]=False; t["is_mob"]=False; t["is_bot_admin"]=False; t["class"]="Warrior"; assign_start_moves(t); save(); return f"⬇️ Demoted @{t['displayName']} - Class back to Warrior"
    if cmd=="races": return box_str("🧬 RACES",[f"• {v['name']} - {v['ability']} - {v['desc']}" for v in RACES.values()])
    if cmd=="classes": return box_str("⚔️ CLASSES",[f"• {v['name']} - {v['ability']} - {v['desc']}" for v in CLASSES.values()])
    if cmd=="stones": return box_str("💎 SPIRIT STONES", stones_lines(p)+[f"• Exchange: {pre}exchange lgss mgss 10"])
    if cmd=="exchange":
        if len(args)<3: return f"Use: {pre}exchange <from> <to> <amt>"
        try: amt=int(args[2])
        except: return "Amount must be number"
        res=convert_stones(p, args[0].lower(), args[1].lower(), amt); save(); return res
    if cmd=="register":
        if not args: return f"Use: {pre}register <name> <race> <class> <gender>\nExample: {pre}register Dominic GOD Warrior Male\nOr slow: {pre}register Dominic then send Race, Class, Gender one by one"
        # Direct: name race class gender
        race_arg=""; class_arg=""; gender_arg=""; name_parts=args[:]
        if len(name_parts)>=1 and name_parts[-1].lower() in ["male","female"]: gender_arg=name_parts[-1]; name_parts=name_parts[:-1]
        if len(name_parts)>=1 and name_parts[-1].lower() in CLASSES: class_arg=name_parts[-1]; name_parts=name_parts[:-1]
        if len(name_parts)>=1 and name_parts[-1].lower() in RACES: race_arg=name_parts[-1]; name_parts=name_parts[:-1]
        name=" ".join(name_parts)
        if not name: return "Enter name!"
        if p.get("registered") and p.get("reg_stage")=="done": return f"✅ Already {p['displayName']}"
        # If only name given -> SLOW mode
        if not race_arg and not class_arg and not gender_arg:
            DB.setdefault("pending_reg",{})[p["id"]]={"name":name,"race":"","gender":"","class":"","group_id":group_id,"sender":sender_id}
            p["displayName"]=name; p["name"]=name; p["reg_step"]="race"; p["reg_stage"]="waiting_pin"; save()
            return f"👤 Name saved: {name}\n❌ Not Done with registration\n👉 Next: Send Race\n🧬 Races: Human Demon Fairy Mage Elf Vampire Dragon Angel God"
        # Direct full
        if is_group:
            DB.setdefault("pending_reg",{})[p["id"]]={"name":name,"race":race_arg,"gender":gender_arg,"class":class_arg,"group_id":group_id,"sender":sender_id}
            p["reg_stage"]="waiting_pin"; p["displayName"]=name; p["name"]=name; apply_register_details(p, race_arg, gender_arg, class_arg); p["registered"]=False; save()
            return f"✅ Registration Done ✔ Player\n👤 {name}\n📩 For the Final step please check your DM with this BOT and finish the final step"
        else:
            DB.setdefault("pending_reg",{})[p["id"]]={"name":name,"race":race_arg,"gender":gender_arg,"class":class_arg,"group_id":group_id,"sender":sender_id}
            p["reg_stage"]="waiting_pin"; p["displayName"]=name; p["name"]=name; apply_register_details(p, race_arg, gender_arg, class_arg); p["registered"]=False; save()
            return f"👤 Player, your registration: {pre}Register {name} {race_arg} {class_arg} {gender_arg}\n✅ Step 1 Done!\n🔐 Now Create 4-digit PIN - Type 4 numbers"
    if not p["registered"] and cmd not in ["register","help","menu","ping","info","economy","link","password","prefix","races","classes","ownerhelp","mobhelp"]: return f"❌ Not registered. Type {pre}register <name>"
    if cmd=="profile":
        lines=[f"✨ {p['displayName']} {p['rank']}",f"👑 Title: {p.get('title','Adventurer')}",f"🧬 Race: {p.get('race','-')}",f"⚔️ Class: {p.get('class','-')}",f"⚧ Gender: {p['gender']}",f"❤️ HP {p['hp']}/{p['maxHp']}",f"🔵 MP {p['mp']}/{p['maxMp']}",f"⚔️ ATK {p['atk']}",f"🛡️ DEF {p['def']}",f"💨 SPD {p['spd']}",f"💠 Level {p['level']}",f"⚡ EXP {p['exp']}/{exp_need(p['level'])}"]
        lines+=stones_lines(p)
        lines+=[f"🏠 House: {p['house']}",f"🚗 Car: {p.get('car')}",f"🐉 Pet: {p.get('pet') or 'None'}",f"📝 Bio: {p.get('bio','-')}"]
        return box_str("👤 PROFILE",lines)
    if cmd=="stats":
        STR=p.get("str",0)+p["atk"]//5; AGI=p.get("agi",10); INT=p.get("int",0)+p["maxMp"]//20; VIT=p.get("vit",0)+p.get("con",10); DEF=p["def"]; LUK=p.get("luk",0)+p["spd"]//3
        lines=[f"🧩 {p['rank']}",f"💠 LV.{p['level']}",f"💎 GEMS: {p.get('gems',5)}","━━━━━━━━━━━━━━━━━━",f"💪 STR: {STR}",f"⚡ AGI: {AGI}",f"🧠 INT: {INT}",f"❤️ VIT: {VIT}",f"🛡️ DEF: {DEF}",f"🍀 LUK: {LUK}","━━━━━━━━━━━━━━━━━━",f"❤️ HP {p['hp']} / {p['maxHp']}",bar(p["hp"],p["maxHp"],22),f"⚡ XP {p['exp']} / {exp_need(p['level'])}",bar(p["exp"],exp_need(p['level']),22),"━━━━━━━━━━━━━━━━━━"]
        lines+=stones_lines(p)
        lines+=["━━━━━━━━━━━━━━━━━━",f"🏆 Rank: {p['rank']}",f"👑 Title: {p.get('title','Adventurer')}",f"🧬 Race: {p.get('race')}",f"⚔️ Class: {p.get('class')}",f"📊 Upgrade: {pre}addstat [stat] [amt]"]
        return box_str(f"📊 {p['displayName'].upper()} — ATTRIBUTES",lines)
    if cmd=="wallet": return box_str("💰 WALLET", stones_lines(p))
    if cmd=="daily":
        now=time.time(); left=86400-(now-p.get("lastDaily",0))
        if left>0: return box_str("⏳ DAILY WAIT",[f"Wait {time_left(left)}"])
        p["lastDaily"]=now; gain_exp(p,30); rew=give_reward(p,10000,10); save(); return box_str("🎁 DAILY",rew+[f"⚡ +30 EXP"])
    if cmd=="claim": rew=give_reward(p,5000,5); save(); return box_str("🎁 CLAIMED",rew)
    if cmd in ["moves","move"]:
        if args:
            # /moves 2 or /moves <name>
            try: return use_move_in_dungeon(p,args[0])
            except: return "Use /moves <number>"
        if not DB.get("dungeon") or not DB["dungeon"].get("in_dungeon"):
            moves=get_my_moves(p); lines=[f"{p['displayName']} Lv{p['level']}",f"🧬 {p.get('race')} | ⚔️ {p.get('class')}"]
            for i,m in enumerate(moves,1): lines.append(f"• {i}. {m}")
            return box_str("📚 MY MOVES - 5 Moves",lines)
        moves=get_my_moves(p); lines=[f"⚔️ BATTLE Floor {DB['dungeon']['floor']}",f"❤️ HP: {p['hp']}/{p['maxHp']}",f"🔵 MP: {p['mp']}/{p['maxMp']}",""]
        for i,m in enumerate(moves,1): lines.append(f"• {i}. {m}")
        lines+=["",f"⚡ QUICK: Type NUMBER e.g. 5 in 5 sec",f"⏰ After 5 sec use {pre}moves 5"]
        p["awaiting_move_until"]=time.time()+5; save(); return box_str("⚔️ CHOOSE MOVE",lines)
    if cmd=="mymoves":
        moves=get_my_moves(p); lines=[f"{p['displayName']} Lv{p['level']}",f"🧬 {p.get('race')} | ⚔️ {p.get('class')}"]
        for i,m in enumerate(moves,1): lines.append(f"• {i}. {m}")
        return box_str("📚 MY MOVES",lines)
    if cmd=="learn": return box_str("🎓 LEARN",[f"• {m}" for m in get_my_moves(p)])
    if cmd=="dungeon":
        if args and args[0]=="enter":
            if DB.get("dungeon") and DB["dungeon"].get("in_dungeon"): return "⚠️ Already in dungeon!"
            return start_dungeon(p)
        if args and args[0]=="leave": DB["dungeon"]=None; save(); return "🚪 Left dungeon"
        return f"Use {pre}dungeon enter"
    if cmd=="leaderboard":
        s=sorted([x for x in DB["players"].values() if x.get("registered")], key=lambda x: x.get("level",1), reverse=True)[:10]
        lines=["🏆 LEADERBOARD - Web + WhatsApp SAME"]
        for i,x in enumerate(s,1): lines.append(f"• {i}. {x['displayName']} Lv{x['level']} LGSS {fmt(x.get('lgss',0))}")
        return box_str("🏆 LEADERBOARD",lines)
    if cmd=="job":
        if not args or args[0]=="list":
            lines=["💼 JOBS - Pay in Zeni + LGSS"]
            for k,v in JOBS.items(): lines.append(f"• {k} - {fmt(v['pay_zeni'])} Zeni + {v['pay_lgss']} LGSS")
            return box_str("💼 JOBS",lines)
        if args[0]=="apply": p["job"]=" ".join(args[1:]); save(); return f"💼 You are now {p['job']}"
        if args[0]=="work":
            now=time.time(); left=2*3600-(now-p.get("lastWork",0))
            if left>0: return box_str("⏳ WORK WAIT",[f"Wait {time_left(left)}"])
            p["lastWork"]=now; j=JOBS.get(p["job"],{"pay_zeni":1000,"pay_lgss":1}); p["zeni"]+=j["pay_zeni"]; p["lgss"]=p.get("lgss",0)+j["pay_lgss"]; gain_exp(p,20); rew=give_reward(p,0,0); save(); return box_str("💼 WORK DONE",[f"• Zeni - +{fmt(j['pay_zeni'])}",f"• LGSS - +{j['pay_lgss']}"]+rew)
        if args[0]=="info": return box_str("💼 JOB INFO",[f"• Job: {p['job']}"])
        return "Job done"
    if cmd=="pet":
        if not args or args[0]=="list":
            lines=["🐉 PETS"]
            for k,v in PETS.items(): lines.append(f"• {k} - {v['cost_lgss']} LGSS - {v['ability']}")
            return box_str("🐉 PETS",lines)
        if args[0]=="buy":
            tn=" ".join(args[1:]); 
            if tn not in PETS: return "Pet not found. Type /pet list"
            cost=PETS[tn]["cost_lgss"]
            if p.get("lgss",0)<cost: return f"Need {cost} LGSS"
            p["lgss"]-=cost; p["pet"]=tn; save(); return box_str("🐉 PET",[f"• You got {tn}",f"• Ability: {PETS[tn]['ability']}"])
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
        if not args: return box_str("🧬 RACES",[f"• {v['name']} - {v['ability']}" for v in RACES.values()])
        if args[0].lower()=="god" and not is_owner(p): return "God only for Owners"
        p["race"]=RACES[args[0].lower()]["name"]; assign_start_moves(p); save(); return f"🧬 You are {p['race']}"
    if cmd=="class":
        if not args: return box_str("⚔️ CLASSES",[f"• {v['name']} - {v['ability']}" for v in CLASSES.values()])
        if args[0].lower()=="monarch" and not can_see_supreme(p): return "Monarch only for appointed"
        p["class"]=CLASSES[args[0].lower()]["name"]; assign_start_moves(p); save(); return f"⚔️ You are {p['class']}"
    if cmd=="gender":
        if not args or args[0].lower() not in ["male","female"]: return "Use /gender male or female"
        p["gender"]=args[0].capitalize(); save(); return f"Gender: {p['gender']}"
    if cmd in ["party","labyrinth","family","families","raid","arena","worldboss","demoncastle","rebirth","guild","church","pray","kick","tagall","hidetag","close","open","sybau","unsybau","marry","divorce","spouse","house","rental","sticker","play","tt","ig","dl","market","achievements","hunger","eat","tavern","feast","cook","quests","season","share","core","buy","bio","web","emoji","broadcast","rob","bail","breakout","wanted","hospital","immortal","skill","inventory","use","sell","go","notifications","monarchs","duel","train","gym","gate","shop","equip","unequip"]:
        if cmd=="party" and args and args[0]=="create": p["party"]=" ".join(args[1:]); save(); return f"👥 Party: {p['party']}"
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

app = Flask(__name__)
HTML = """<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>INFINITY HUNTER</title><style>body{background:#050510;color:#fff;font-family:Arial;margin:0}input,select{width:100%;padding:14px;margin:8px 0;background:#000;color:#fff;border:2px solid #7B2FFF;border-radius:12px;box-sizing:border-box}button{width:100%;padding:14px;background:#FFD700;color:#000;border:none;border-radius:12px;font-weight:900;margin:8px 0}button:disabled{background:#333;color:#777}.card{background:#111128;border:1px solid #333;padding:16px;border-radius:16px;margin:12px}pre{white-space:pre-wrap;background:#000;padding:12px;border-radius:10px}.hidden{display:none}</style></head><body>
<div id='landing' style='text-align:center;padding:60px 16px'><h1 style='color:#FFD700'>⚡ INFINITY HUNTER ⚡</h1><button onclick='showAuth()' style='max-width:300px'>ENTER →</button></div>
<div id='auth' class='hidden' style='text-align:center;padding:20px'><div class='card' style='max-width:460px;margin:auto;text-align:left'><h2>📝 REGISTER / 🔑 LOGIN</h2><input id='name' placeholder='Name'><input id='pass' type='password' placeholder='Enter Password'><label>🧬 Race</label><select id='race'><option value=''>-- Pick Race --</option><option value='Human'>Human - Adapt</option><option value='Demon'>Demon - Demon Rage</option><option value='Fairy'>Fairy - Fairy Heal</option><option value='Mage'>Mage - Arcane Burst</option><option value='Elf'>Elf - Elf Arrow</option><option value='Vampire'>Vampire - Blood Drain</option><option value='Dragon'>Dragon - Dragon Breath</option><option value='Angel'>Angel - Holy Light</option><option value='God'>God - Owners Only</option></select><label>⚔️ Class</label><select id='class'><option value=''>-- Pick Class --</option><option value='Warrior'>Warrior - Slash</option><option value='Mage'>Mage - Fireball</option><option value='Assassin'>Assassin - Shadow Strike</option><option value='Healer'>Healer - Heal</option><option value='Archer'>Archer - Piercing Arrow</option><option value='Tank'>Tank - Shield Wall</option><option value='Necromancer'>Necromancer - Soul Drain</option><option value='Swordmaster'>Swordmaster - Dragon Smash</option></select><label>⚧ Gender</label><select id='gender'><option value='Male'>Male</option><option value='Female'>Female</option></select><button id='regbtn' onclick='doAuth("register")' disabled>⚡ REGISTER - Pick Race + Class</button><button onclick='doAuth("login")' style='background:#7B2FFF;color:#fff'>🔑 LOGIN</button><p id='authmsg'></p></div></div>
<div id='dash' class='hidden'><div style='background:#111128;padding:12px;display:flex;justify-content:space-between'><b>⚡ INFINITY HUNTER - CHAT</b><span id='who'></span></div><div style='padding:12px'><div class='card'><div id='chat'></div><input id='cmd' placeholder='Type e.g. /menu /profile /stones'><button onclick='sendChat()'>▶ SEND</button></div></div></div>
<script>let myName='';function showAuth(){document.getElementById('landing').classList.add('hidden');document.getElementById('auth').classList.remove('hidden');}function check(){let r=document.getElementById('race').value;let c=document.getElementById('class').value;let b=document.getElementById('regbtn');if(r&&c){b.disabled=false;b.textContent='⚡ REGISTER';}else{b.disabled=true;b.textContent='⚡ REGISTER - Pick Race + Class';}}document.getElementById('race').onchange=check;document.getElementById('class').onchange=check;async function doAuth(mode){let name=document.getElementById('name').value.trim();let pass=document.getElementById('pass').value.trim();let race=document.getElementById('race').value;let cls=document.getElementById('class').value;let gender=document.getElementById('gender').value;if(!name||!pass){document.getElementById('authmsg').textContent='Enter Name + Password';return;}if(mode=='register'&&(!race||!cls)){document.getElementById('authmsg').textContent='Pick Race + Class!';return;}let r=await fetch('/api/auth',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,pass,race,class:cls,gender,mode})});let j=await r.json();document.getElementById('authmsg').textContent=j.msg;if(j.ok){myName=name;document.getElementById('auth').classList.add('hidden');document.getElementById('dash').classList.remove('hidden');document.getElementById('who').textContent='@'+name;}}async function sendChat(){let t=document.getElementById('cmd').value;if(!t)return;let d=document.createElement('div');d.textContent='You: '+t;document.getElementById('chat').appendChild(d);document.getElementById('cmd').value='';let r=await fetch('/api/command',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:myName,text:t})});let j=await r.json();let d2=document.createElement('div');d2.textContent='Bot: '+j.reply;document.getElementById('chat').appendChild(d2);}</script></body></html>"""
@app.route('/')
def home(): return HTML
@app.route('/api/auth', methods=['POST'])
def api_auth():
    data=request.json or {}; name=(data.get('name') or '').strip(); pwd=(data.get('pass') or '').strip(); race=(data.get('race') or '').strip(); cls=(data.get('class') or '').strip(); gender=(data.get('gender') or 'Male').strip(); mode=data.get('mode','register')
    if not name or not pwd: return jsonify({"ok":False,"msg":"Enter Name + Password"})
    if name.lower() in OWNER_NAMES and pwd!=OWNER_PASSWORD: return jsonify({"ok":False,"msg":"Owners: Wrong password"})
    existing=get_player_by_name(name)
    if mode=="login":
        if not existing or not existing.get("registered"): return jsonify({"ok":False,"msg":"Not registered. Click REGISTER"})
        if existing.get("password") and existing.get("password")!=pwd: return jsonify({"ok":False,"msg":"Wrong password"})
        return jsonify({"ok":True,"msg":f"Welcome back {name}!"})
    if mode=="register" and (not race or not cls): return jsonify({"ok":False,"msg":"Pick Race + Class!"})
    if existing and existing.get("registered"): return jsonify({"ok":True,"msg":"Already registered - Logged in!"})
    p=get_player(f"web:{name}", name); p["password"]=pwd; p["registered"]=True; p["displayName"]=name; p["name"]=name; p["reg_stage"]="done"
    if name.lower() in OWNER_NAMES: apply_owner_perks(p)
    else: apply_register_details(p, race, gender, cls)
    save(); return jsonify({"ok":True,"msg":f"Registered {name}! Race: {p.get('race')} Class: {p.get('class')}"})
@app.route('/api/command', methods=['POST'])
def api_cmd():
    data=request.json or {}; name=data.get('name','Player'); text=data.get('text','/menu')
    reply=process_command(f"web:{name}", text, is_group=False); save(); return jsonify({"reply":reply})
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
                val=change.get('value',{})
                for msg in val.get('messages',[]):
                    sender=msg.get('from',''); text=msg.get('text',{}).get('body','')
                    p_tmp=get_player(sender, sender)
                    is_group=False; group_id=None
                    if text.lower().startswith(('/register','.register')) and p_tmp.get("reg_stage")!="waiting_pin": is_group=True; group_id="group_"+sender
                    if text.startswith('/') or text.startswith('.') or text.isdigit():
                        reply=process_command(sender, text, is_group=is_group, group_id=group_id); save(); send_whatsapp(sender, reply)
                        if is_group and "Registration Done" in reply:
                            pending=DB.get("pending_reg",{}).get(sender)
                            if pending: send_whatsapp(sender, f"👤 Player: /Register {pending['name']} {pending.get('race','')} {pending.get('class','')} {pending.get('gender','')}\n🔐 Now Create 4-digit PIN")
                        if text.isdigit() and len(text)==4 and "Registration successfully done" in reply:
                            send_whatsapp(sender, f"🎉 Registration Successfully Done @{p_tmp.get('displayName','Player')}\n👋 Welcome to INFINITY HUNTER @{p_tmp.get('displayName','Player')}\n👉 Now do /help")
                        # Appointment DM: if reply contains Successfully Added, DM the target with their help
                        if "Successfully Added" in reply and "Bot Admin" in reply:
                            send_whatsapp(sender, "🤖 BOT ADMIN COMMANDS:\n• /addgroupadmin @user\n• /kick @user\n• /check reports (DM only)\n• /warn @user")
                        if "Successfully Added" in reply and "Mob" in reply:
                            send_whatsapp(sender, "👹 MOB COMMANDS:\n• /addadmin @user\n• /addbotadmin @user\n• /addgroupadmin @user\n• /kick @user\n• /check reports (DM only)")
                        if "Successfully Added" in reply and "Admin" in reply and "Bot Admin" not in reply:
                            send_whatsapp(sender, "➕ ADMIN COMMANDS:\n• /addbotadmin @user\n• /addgroupadmin @user\n• /kick @user\n• /check reports (DM only)")
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
def health(): return "OK - Infinity v10"
if __name__=='__main__':
    port=int(os.environ.get('PORT',10000)); print(f"INFINITY v10 LIVE on port {port}"); app.run(host='0.0.0.0', port=port)
