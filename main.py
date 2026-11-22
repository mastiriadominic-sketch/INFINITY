# INFINITY v9 - Spirit Stones - Race+Class Required - No Owner Password Shown - List Menu
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

# ===== RACES + ABILITIES =====
RACES={
 "human":{"name":"Human","ability":"Adapt","desc":"+10% EXP, Balanced","bonus":{"exp":1.1}},
 "demon":{"name":"Demon","ability":"Demon Rage","desc":"+20% ATK","bonus":{"atk":1.2}},
 "fairy":{"name":"Fairy","ability":"Fairy Heal","desc":"+20% Heal","bonus":{"heal":1.2}},
 "mage":{"name":"Mage","ability":"Arcane Burst","desc":"+30% Skill DMG","bonus":{"skill":1.3}},
 "elf":{"name":"Elf","ability":"Elf Arrow","desc":"+20% AGI/Crit","bonus":{"agi":1.2}},
 "vampire":{"name":"Vampire","ability":"Blood Drain","desc":"Lifesteal 15%","bonus":{"lifesteal":0.15}},
 "dragon":{"name":"Dragon","ability":"Dragon Breath","desc":"+30% HP","bonus":{"hp":1.3}},
 "angel":{"name":"Angel","ability":"Holy Light","desc":"+20% DEF + Heal","bonus":{"def":1.2}},
 "god":{"name":"God","ability":"God Punch / Infinity Blast","desc":"Owners only +100% ALL","bonus":{"all":2.0}},
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
}
# ===== SPIRIT STONES =====
# 1 Supreme=100 High, 1 High=100 Mid, 1 Mid=100 Low, 1 Low=100 Zeni/Germ(base)
def stones_text(p, show_secret=False):
    lines=["💎 *Spirit Stones*"]
    lines.append(f"• LGSS (Low Grade Spirit Stones) - {fmt(p.get('lgss',0))}")
    lines.append(f"• MGSS (Mid Grade Spirit Stones) - {fmt(p.get('mgss',0))}")
    lines.append(f"• HGSS (High Grade Spirit Stones) - {fmt(p.get('hgss',0))}")
    # Legendary + Supreme ONLY for Admins/Mobs/Owners/Bot Admins - NEVER for normal players
    if show_secret:
        lines.append(f"• Legendary Grade Spirit Stones - {fmt(p.get('legendary',0))}")
        lines.append(f"• Supreme Grade Spirit Stones - {fmt(p.get('supreme',0))}")
    return lines
def can_use_supreme(p):
    return is_owner(p) or p.get("is_admin") or p.get("is_mob") or p.get("is_bot_admin") or p.get("displayName","").lower() in OWNER_NAMES
def add_stones(p, kind, amt):
    p[kind]=p.get(kind,0)+amt
def convert_stones(p, frm, to, amt):
    # frm/to: lgss, mgss, hgss, legendary, supreme, zeni
    rates={"zeni":1,"lgss":100,"mgss":10000,"hgss":1000000,"legendary":100000000,"supreme":10000000000}
    if frm not in rates or to not in rates: return "Use: lgss mgss hgss supreme"
    if frm=="supreme" and not can_use_supreme(p): return "❌ Only Owners/Admins/Mobs can use Supreme Grade Spirit Stones"
    if to=="supreme" and not can_use_supreme(p): return "❌ Only Owners/Admins/Mobs can use Supreme Grade Spirit Stones"
    have=p.get(frm,0) if frm!="zeni" else p.get("zeni",0)
    if have<amt: return f"❌ Not enough {frm.upper()} - You have {fmt(have)}"
    base=amt*rates[frm]; got=base//rates[to]
    if frm!="zeni": p[frm]-=amt
    else: p["zeni"]-=amt
    if to!="zeni": p[to]=p.get(to,0)+got
    else: p["zeni"]+=got
    return f"✅ Exchanged {fmt(amt)} {frm.upper()} → {fmt(got)} {to.upper()}"

DB_FILE="infinity_db.json"
BACKUPS=["backup1_1TB.json","backup2_1TB.json","backup3_1TB.json"]
DB={"players":{},"market":[],"pending_pvp":{},"guilds":{},"dungeon":None,"groups":{},"auto_battle":False,"config":{"prefix":"/","prefixes":["/","."]},"pending_reg":{},"group_regs":{}}
WORLD={"totalZeni":20000000000000,"totalPlayers":0,"labyrinth":None}
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
def get_multiplier(p):
    if p.get("race")=="God" and is_owner(p): return 1.5
    return 1.0
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
        DB["players"][pid]={"id":pid,"name":name,"displayName":name,"registered":False,"password":"","race":"","class":"","level":1,"exp":0,"zeni":1000000,"lgss":10,"mgss":0,"hgss":0,"legendary":0,"supreme":0,"bank":0,"bank_open":False,"savings":0,"hp":100,"maxHp":100,"mp":50,"maxMp":50,"atk":15,"def":10,"spd":12,"agi":10,"con":10,"rank":"E - Novice","wins":0,"losses":0,"dungeonClears":0,"dungeon_floor":1,"checkpoint":1,"kills":0,"job":"Unemployed","loan":0,"loanDue":0,"house":"None","houseTier":0,"car":"None","shop":"None","pet":None,"guild":"None","guildRank":"None","lastDaily":0,"lastWork":0,"lastClaim":0,"lastRob":0,"jailed":0,"banned":False,"questsDone":0,"notifications":[],"gender":"Not Set","age":15,"lifespan":80,"birthday":now.strftime("%d %b %Y"),"spouse":None,"title":"Adventurer","titles":["Adventurer"],"cultRealm":0,"cultLayer":1,"cultXp":0,"cultNeed":100,"talentType":"","talentValue":"","talentGrade":"","isInfinity":False,"isChosen":False,"chosenUntil":0,"wood":0,"houseBuilt":False,"sect":"No Sect","sectRank":"-","hunger":100,"family":"No Family","party":"No Party","church":"No Church","inventory":{},"skills":[],"active_skills":[],"awaiting_move_until":0,"gems":5,"str":0,"int":0,"vit":0,"luk":0,"bio":"","emoji":"⚔️","hunger_lvl":100,"cooking":1,"achievements":[],"reg_stage":"none","is_admin":False,"is_mob":False,"is_bot_admin":False}
        WORLD["totalPlayers"]+=1
    for k,v in {"race":"","class":"","lgss":10,"mgss":0,"hgss":0,"legendary":0,"supreme":0,"password":"","inventory":{},"skills":[],"active_skills":[],"awaiting_move_until":0,"gems":5,"str":0,"int":0,"vit":0,"luk":0,"bio":"","emoji":"⚔️","hunger_lvl":100,"cooking":1,"achievements":[],"reg_stage":"none","is_admin":False,"is_mob":False,"is_bot_admin":False}.items():
        if k not in DB["players"][pid]: DB["players"][pid][k]=v
    return DB["players"][pid]
def get_player_by_name(name):
    for pid,pl in DB["players"].items():
        if pl.get("displayName","").lower()==name.lower(): return pl
    return None
def box_str(title,lines):
    # LISTING FORMAT - each line on its own line, never joined into paragraph
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
    hp=80+floor*30; atk=12+floor*3; reward_lgss=5+floor*2; exp=100+floor*20; style="Low ATK High HP"
    if floor%2==0: style="High ATK Low HP"; hp=int(hp*0.7); atk=int(atk*1.4)
    return hp,atk,reward_lgss,exp,style
def start_dungeon(p):
    floor=p.get("dungeon_floor",1); hp,atk,reward,exp,style=dungeon_stats_for_floor(floor)
    DB["dungeon"]={"enemy":f"Floor {floor} Boss","enemy_hp":hp,"enemy_max":hp,"enemy_atk":atk,"floor":floor,"reward":reward,"exp":exp,"in_dungeon":True,"style":style}
    save(); return box_str("🏰 DUNGEON FLOOR "+str(floor),[f"👹 Enemy: Floor {floor} Boss",f"🎨 Style: {style}",f"❤️ Boss HP: {hp}",f"⚔️ Boss ATK: {atk}",f"💎 Reward: {reward} LGSS",f"📍 Checkpoint: Floor {p.get('checkpoint',1)}","Type /moves to see moves","Then /moves <number> to attack"])
def use_move_in_dungeon(p,num):
    d=DB.get("dungeon")
    if not d or not d.get("in_dungeon"): return "❌ NOT in dungeon. Type /dungeon enter"
    my=get_my_moves(p)
    if num not in my: return box_str("🔒 MOVE LOCKED",[f"You dont own move {num}","Type /mymoves"])
    mv=ALL_MOVES[num]
    if p["mp"]<mv["mp"]: return "❌ Not enough MP"
    p["mp"]-=mv["mp"]; out=[]
    if mv["dmg"]<0:
        heal=-mv["dmg"]; p["hp"]=min(p["maxHp"],p["hp"]+heal); out.append(f"✨ You used {mv['name']} Healed +{heal}")
    else:
        dmg=mv["dmg"]+p["atk"]+random.randint(0,10)
        if mv["name"]=="Race Power": dmg=p["atk"]*2+20
        d["enemy_hp"]-=dmg; out.append(f"⚔️ You used {mv['name']} Damage: {dmg} Boss HP: {max(0,d['enemy_hp'])}")
    if d["enemy_hp"]<=0:
        r=d["reward"]; p["lgss"]=p.get("lgss",0)+r; gain_exp(p,d["exp"]); p["dungeonClears"]+=1; cleared=d["floor"]; p["dungeon_floor"]=cleared+1
        if cleared%50==0: p["checkpoint"]=cleared; out.append(f"📍 CHECKPOINT SAVED AT FLOOR {cleared}")
        DB["dungeon"]=None; save(); return box_str("🎉 FLOOR CLEARED",[f"Floor {cleared} cleared",f"💎 +{r} LGSS",f"⚡ +{d['exp']} EXP",f"➡️ Next Floor: {cleared+1}",f"📍 Checkpoint: {p['checkpoint']}","Type /dungeon enter"])
    edmg=max(1,d["enemy_atk"]+random.randint(0,10)-p["def"]//2); p["hp"]-=edmg; out.append(f"💥 Boss hit you -{edmg} Your HP: {max(0,p['hp'])}")
    if p["hp"]<=0:
        p["hp"]=1; respawn=p.get("checkpoint",1); p["dungeon_floor"]=respawn; DB["dungeon"]=None; save(); return box_str("💀 YOU DIED",[f"Died on Floor {d['floor']}",f"Respawn at Checkpoint Floor {respawn}","HP set to 1"])
    save(); return "\n".join(out)+"\nYour turn! /moves <number> again"
def apply_owner_perks(p):
    p["isInfinity"]=True; p["isChosen"]=True; p["chosenUntil"]=time.time()+2*24*3600; p["race"]="God"; p["atk"]=100; p["maxHp"]=300; p["hp"]=300; p["mp"]=9999; p["maxMp"]=9999; p["cultRealm"]=1; p["cultLayer"]=9; p["talentType"]="Bloodline"; p["talentValue"]="Primordial Chaos Bloodline"; p["talentGrade"]="Divine Grade"; p["title"]="Immortal Emperor"; p["supreme"]=100; p["legendary"]=100
    if "Immortal Emperor" not in p.get("titles",[]): p["titles"].append("Immortal Emperor")
def apply_register_details(p, race_raw, gender_raw, class_raw=""):
    if race_raw and race_raw.lower() in RACES:
        if race_raw.lower()=="god" and not is_owner(p) and p.get("displayName","").lower() not in OWNER_NAMES: return "God only for Owners"
        p["race"]=RACES[race_raw.lower()]["name"]
    if gender_raw and gender_raw.lower() in ["male","female"]: p["gender"]=gender_raw.capitalize()
    if class_raw and class_raw.lower() in CLASSES: p["class"]=CLASSES[class_raw.lower()]["name"]
    if p.get("displayName","").lower() in OWNER_NAMES: apply_owner_perks(p)
    return None

def menu_text(p):
    pre=get_prefix(); tag=f"@{p['displayName']}"
    L=[]
    L.append("⚡ INFINITY Hunter")
    L.append(f"👤 {tag} — {p.get('title','Adventurer')} | Lv{p['level']} | {p.get('race','-')} | {p.get('class','-')}")
    L.append(f"🔑 Prefix: {pre} | Type {pre}menu again")
    L.append("")
    L.append("📋 GENERAL")
    L.append(f"• 📝 {pre}register <name> — Join the world")
    L.append(f"• 📊 {pre}stats — View stats (picture card)")
    L.append(f"• 👤 {pre}profile — View profile card")
    L.append(f"• 💎 {pre}stones — View Spirit Stones")
    L.append(f"• 🔄 {pre}exchange <from> <to> <amount> — Exchange stones")
    L.append(f"• ✏️ {pre}rename <new name> — Change display name")
    L.append(f"• ℹ️ {pre}info — Bot stats")
    L.append(f"• 📜 {pre}help — Show this menu")
    L.append(f"• 🏓 {pre}ping — Check if bot is alive")
    L.append("")
    L.append("⚔️ BATTLE")
    L.append(f"• ⚔️ {pre}pvp @user — Challenge someone")
    L.append(f"• ✨ {pre}skill cast <magic> @user — Cast magic")
    L.append(f"• 🔥 {pre}skill activate <name> — Use buff")
    L.append(f"• 🚫 {pre}skill deactivate <name> — Turn off passive")
    L.append(f"• 🗡️ {pre}move <move> — Use move in battle")
    L.append(f"• 📜 {pre}moves — See options during battle")
    L.append(f"• 📚 {pre}mymoves — View full moveset")
    L.append(f"• 🎓 {pre}learn — Newly unlocked race moves")
    L.append(f"• ✅ {pre}accept — Accept PvP")
    L.append(f"• ❌ {pre}decline — Decline")
    L.append(f"• 🏳️ {pre}forfeit — Forfeit battle")
    L.append("")
    L.append("🏰 DUNGEON")
    L.append(f"• 🏰 {pre}dungeon enter — Enter dungeon")
    L.append(f"• 🎒 {pre}inventory — View items")
    L.append(f"• 🧪 {pre}use <item> [qty] — Use item")
    L.append(f"• 🧴 Potions: Small Heal, Medium Heal, MP Potion, Phoenix Elixir, Stat Boost")
    L.append(f"• 💸 {pre}sell <item> [qty] — Sell for Spirit Stones")
    L.append("")
    L.append("👥 PARTY")
    L.append(f"• 👥 {pre}party create <name> — Create party")
    L.append(f"• 📩 {pre}party invite @user — Invite")
    L.append(f"• ✅ {pre}party accept — Accept invite")
    L.append(f"• 🚪 {pre}party leave — Leave party")
    L.append(f"• 👢 {pre}party kick @user — Remove member")
    L.append("")
    L.append("🌀 LABYRINTH")
    L.append(f"• 🌀 {pre}labyrinth status — Is one open?")
    L.append(f"• 👥 {pre}labyrinth team create <name> — Start team")
    L.append(f"• 📩 {pre}labyrinth team invite @user — Invite")
    L.append(f"• ✅ {pre}labyrinth team accept / reject — Respond")
    L.append(f"• 🚪 {pre}labyrinth enter <team> — Begin")
    L.append(f"• ⚔️ {pre}labyrinth attack — Basic attack")
    L.append(f"• 🗡️ {pre}labyrinth move <name> — Use move")
    L.append(f"• 👑 {pre}labyrinth force — Owner: force-open")
    L.append("")
    L.append("🏠 FAMILY")
    L.append(f"• 🏠 {pre}family found <name> — Found house")
    L.append(f"• ➕ {pre}family add @user — Invite relative")
    L.append(f"• ✅ {pre}family accept — Accept invite")
    L.append(f"• 🚪 {pre}family leave — Leave family")
    L.append(f"• ℹ️ {pre}family info — House, tier, stones")
    L.append(f"• 🏆 {pre}families — Every house, richest first")
    L.append("")
    L.append("🛡️ COUNTRY RAIDS")
    L.append(f"• 🛡️ {pre}raid — Status")
    L.append(f"• ➕ {pre}raid join — Join team")
    L.append(f"• ▶️ {pre}raid start — Start fight")
    L.append(f"• ⚔️ {pre}raid attack — Attack beast")
    L.append(f"• 🗡️ {pre}raid move <name> — Use move")
    L.append(f"• 🎁 {pre}raid claim — Claim rewards")
    L.append("")
    L.append("🪞 HALL OF REFLECTIONS")
    L.append(f"• 🪞 {pre}arena — Board, prize, entrants")
    L.append(f"• 🎟️ {pre}arena enter — Pay 5 MGSS to join")
    L.append(f"• ⚔️ {pre}arena fight — Face reflections")
    L.append("")
    L.append("🏛️ GUILD")
    L.append(f"• 🏛️ {pre}guild — View guild home")
    L.append(f"• 📝 {pre}guild apply adventurer — Apply")
    L.append(f"• ℹ️ {pre}guild info — Details")
    L.append(f"• 👥 {pre}guild members — Members")
    L.append(f"• 📜 {pre}guild quest — Quests")
    L.append(f"• 💰 {pre}guild fund <amount> <reason> — Trust fund")
    L.append(f"• ➕ {pre}guild create [name] — Create guild")
    L.append(f"• 🚪 {pre}guild join [name] — Join guild")
    L.append(f"• 🚪 {pre}guild leave — Leave guild")
    L.append("")
    L.append("⛪ CHURCH & FAITH")
    L.append(f"• ⛪ {pre}church — View churches")
    L.append(f"• 🙏 {pre}church join <god> — Become follower")
    L.append(f"• 🚪 {pre}church leave — Leave church")
    L.append(f"• 🙏 {pre}pray — Pray (24h)")
    L.append("")
    L.append("🛡️ GROUP MANAGEMENT")
    L.append(f"• 👢 {pre}kick @user — Remove member")
    L.append(f"• ⬆️ {pre}promote @user — Make admin")
    L.append(f"• ⬇️ {pre}demote @user — Remove admin")
    L.append(f"• 📣 {pre}tagall <msg> — Tag everyone")
    L.append(f"• 👻 {pre}hidetag <msg> — Notify without listing")
    L.append(f"• 🔒 {pre}close — Lock group")
    L.append(f"• 🔓 {pre}open — Unlock group")
    L.append(f"• 🔇 {pre}sybau @user <time> — Silence")
    L.append(f"• 🔊 {pre}unsybau @user — Release")
    L.append("")
    L.append("💰 ECONOMY - SPIRIT STONES")
    L.append(f"• 🎁 {pre}daily — Claim 10 LGSS (24h)")
    L.append(f"• 💎 {pre}stones — Spirit Stones balance")
    L.append(f"• 👛 {pre}wallet — Wallet")
    L.append(f"• 🏦 {pre}bank — Bank")
    L.append(f"• 🛒 {pre}shop — Shop")
    L.append(f"• 🛍️ {pre}buy <item> [qty] — Buy")
    L.append(f"• 💝 {pre}give @user <amount> — Give LGSS")
    L.append(f"• 🍽️ {pre}eat — Eat")
    L.append(f"• 😴 {pre}sleep — Sleep")
    L.append("")
    L.append("💼 JOBS")
    L.append(f"• 💼 {pre}job list — See jobs")
    L.append(f"• 📝 {pre}job apply <job> — Apply")
    L.append(f"• 🔨 {pre}job work — Work shift")
    L.append(f"• ℹ️ {pre}job info — View job")
    L.append("")
    L.append("💍 MARRIAGE")
    L.append(f"• 💍 {pre}marry @user — Propose")
    L.append(f"• ✅ {pre}marry accept — Accept")
    L.append(f"• 💔 {pre}divorce — End marriage")
    L.append(f"• 👤 {pre}spouse — Spouse info")
    L.append("")
    L.append("🏠 HOUSING & RENTAL")
    L.append(f"• 🏠 {pre}house buy — Houses")
    L.append(f"• ⬆️ {pre}house upgrade — Upgrade")
    L.append(f"• ℹ️ {pre}house info — View house")
    L.append(f"• 🏘️ {pre}rental list — Houses for rent")
    L.append("")
    L.append("🐉 PETS")
    L.append(f"• 🐉 {pre}pet list — Dragons")
    L.append(f"• 🥚 {pre}pet buy <type> — Buy egg")
    L.append(f"• 🏷️ {pre}pet name <name> — Name dragon")
    L.append(f"• 🏋️ {pre}pet train — Train dragon")
    L.append(f"• ℹ️ {pre}pet info — View dragon")
    L.append("")
    L.append("🎨 MEDIA & DOWNLOADER")
    L.append(f"• 🎨 {pre}sticker — Image to sticker")
    L.append(f"• 🖼️ {pre}unsticker — Sticker to image")
    L.append(f"• 🎵 {pre}play <song> — Download song")
    L.append(f"• ⬇️ {pre}tt / {pre}ig / {pre}dl — Download")
    L.append("")
    L.append("🛒 MARKET")
    L.append(f"• 🛒 {pre}market — Browse")
    L.append(f"• 📝 {pre}market list <item> <qty> <price> — List")
    L.append(f"• 🛍️ {pre}market buy <id> — Buy (5% fee)")
    L.append(f"• ❌ {pre}market cancel <id> — Cancel")
    L.append("")
    L.append("🏆 ACHIEVEMENTS & QUESTS")
    L.append(f"• 🏆 {pre}achievements — Progress")
    L.append(f"• 🍽️ {pre}hunger — Hunger gauge")
    L.append(f"• 📜 {pre}quests — Daily/weekly quests")
    L.append(f"• 🎁 {pre}claim — Claim rewards")
    L.append("")
    L.append("🏆 LEADERBOARDS")
    L.append(f"• 🏆 {pre}leaderboard — Top (Web + WhatsApp SAME)")
    L.append(f"• 👑 {pre}monarchs — Monarchs")
    L.append("")
    L.append("🌟 SEASON")
    L.append(f"• 🌟 {pre}season — Time left + rank")
    L.append("")
    L.append("⚖️ CRIME & JAIL")
    L.append(f"• 🥷 {pre}rob @user <amount> — Rob")
    L.append(f"• 🏦 {pre}rob bank <amount> — Rob bank")
    L.append(f"• 💰 {pre}bail — Pay bail")
    L.append(f"• 🚨 {pre}wanted — Wanted list")
    L.append("")
    L.append("🏥 HOSPITAL")
    L.append(f"• 🏥 {pre}hospital — Health")
    L.append(f"• 🩺 {pre}hospital checkup — Free check")
    L.append(f"• 💊 {pre}hospital treat — Cure")
    L.append("")
    L.append("🏦 BANK")
    L.append(f"• 🏦 {pre}bank — Account")
    L.append(f"• 📝 {pre}bank register — Open (10 LGSS)")
    L.append(f"• 💰 {pre}bank deposit <amount|all> — Deposit")
    L.append(f"• 💵 {pre}bank withdraw <amount|all> — Withdraw")
    L.append(f"• 💸 {pre}bank transfer @user <amount> — Send")
    L.append(f"• 🏦 {pre}bank loan <amount> — Loan")
    L.append("")
    L.append("👑 OWNER & ADMIN [SHADOW NATION]")
    L.append(f"• 👑 {pre}setprefix <new> — Change prefix (Owners only)")
    L.append(f"• 📢 {pre}broadcast — Announce")
    L.append(f"• 🛡️ {pre}kick / promote / ban / sybau — Group mgmt")
    L.append(f"• 🔐 {pre}addadmin @user — Appoint admin (Owners)")
    L.append(f"• 👹 {pre}addmob @user — Appoint mob (Owners)")
    L.append("")
    L.append("🐲 WORLD BOSS & DEMON CASTLE")
    L.append(f"• 🐲 {pre}worldboss — World Boss")
    L.append(f"• 🏰 {pre}demoncastle [floor] — Demon Castle")
    L.append("")
    L.append("🔥 ASCENSION & REBIRTH")
    L.append(f"• 🔥 {pre}rebirth — Lv.99+ Reset for +50% DMG")
    L.append("")
    L.append(f"💡 Tip: {tag} Type {pre}profile to see your card!")
    return box_str("⚡ INFINITY Hunter", L)

def process_command(sender_id, raw_text, is_group=False, group_id=None):
    if sender_id.startswith("web:"):
        name=sender_id[4:]; p=get_player_by_name(name)
        if not p: p=get_player(sender_id, name)
    else: p=get_player(sender_id, sender_id)
    text=(raw_text or "").strip()
    if text.isdigit() and len(text)==4 and p.get("reg_stage")=="waiting_pin":
        pending=DB.get("pending_reg",{}).get(p["id"])
        if pending:
            p["password"]=text; p["registered"]=True; p["reg_stage"]="done"; p["displayName"]=pending["name"]; p["name"]=pending["name"]
            apply_register_details(p, pending.get("race",""), pending.get("gender",""), pending.get("class",""))
            save(); return f"✅ Registration successfully done ✔\n👤 Player: {p['displayName']}\n🔐 PIN saved!\n👉 Please Go back to the group and continue\n🎮 Type /help in group"
        else: p["reg_stage"]="none"; save(); return "No pending registration. Type /register in group first."
    if text.isdigit():
        if time.time() <= p.get("awaiting_move_until",0):
            num=int(text); p["awaiting_move_until"]=0; return use_move_in_dungeon(p,num)
        else: return "⏰ Time expired! 5 seconds passed.\nYou must type /moves 5 now."
    pre=get_prefix(); prefix_used=None
    for cand in [pre,"/","."]:
        if text.startswith(cand): prefix_used=cand; break
    if not prefix_used: return f"Use {pre}help - Example: {pre}register Infinity"
    stripped=text[len(prefix_used):].strip()
    if not stripped: return f"Use {pre}help"
    parts=stripped.split(" "); cmd=parts[0].lower(); args=parts[1:]; rest=" ".join(args)
    if cmd in ["menu","help"]: return menu_text(p)
    if cmd=="ping": return "🏓 Pong! Alive! ✅ Lord Infinity Bot is ON\n👑 Owners: 0779798568 / Lord Infinity / Immortal Emperor"
    if cmd=="setprefix":
        if not is_owner(p): return "❌ Only Owners can change prefix"
        if not args: return f"Use: {pre}setprefix <new> Current: {pre}"
        DB["config"]["prefix"]=args[0]; save(); return f"✅ Prefix changed to: {args[0]}\nNow use {args[0]}menu"
    if cmd=="prefix": return f"🔑 Current prefix: {pre}"
    if cmd=="races":
        lines=["🧬 RACES - Pick one before Register:"]
        for k,v in RACES.items(): lines.append(f"• {v['name']} - {v['ability']} - {v['desc']}")
        return box_str("🧬 RACES",lines)
    if cmd=="classes":
        lines=["⚔️ CLASSES - Pick one before Register:"]
        for k,v in CLASSES.items(): lines.append(f"• {v['name']} - {v['ability']} - {v['desc']}")
        return box_str("⚔️ CLASSES",lines)
    if cmd=="stones":
        show=can_use_supreme(p)
        return box_str("💎 SPIRIT STONES", stones_text(p, show_secret=show)+[f"💱 Exchange: {pre}exchange lgss mgss 10","💱 Rates: 1 Supreme=100 High, 1 High=100 Mid, 1 Mid=100 Low, 1 Low=100 Zeni/Germ"])
    if cmd=="exchange":
        if len(args)<3: return f"Use: {pre}exchange <from> <to> <amount> Example: {pre}exchange lgss mgss 100"
        try: amt=int(args[2])
        except: return "Amount must be number"
        res=convert_stones(p, args[0].lower(), args[1].lower(), amt); save(); return res
    if cmd=="addadmin":
        if not is_owner(p): return "❌ Owners only"
        t=get_player_by_name(" ".join(args))
        if not t: return "Player not found"
        t["is_admin"]=True; t["is_bot_admin"]=True; save(); return f"✅ {t['displayName']} is now Admin - Can see/use Supreme"
    if cmd=="addmob":
        if not is_owner(p): return "❌ Owners only"
        t=get_player_by_name(" ".join(args))
        if not t: return "Player not found"
        t["is_mob"]=True; save(); return f"✅ {t['displayName']} is now Mob - Can see/use Supreme"
    if cmd=="info":
        reg=sum(1 for pl in DB["players"].values() if pl.get("registered"))
        return box_str("ℹ️ BOT INFO",["🤖 Bot: INFINITY v9","👑 Owners: 0779798568 / Lord Infinity / Immortal Emperor",f"🔑 Prefix: {pre}",f"👥 Registered: {reg}",f"💎 Currency: Spirit Stones","💾 Backups: 3x 1TB"])
    if cmd=="register":
        if not args: return f"Use: {pre}register <name> <race> <gender> <class>\nExample: {pre}register Dominic Mastiria GOD Male Warrior\nType {pre}races to see races, {pre}classes to see classes"
        race_arg=""; gender_arg=""; class_arg=""; name_parts=args[:]
        # Parse from end: [class] [gender] [race] [name...]
        if len(args)>=2 and args[-1].lower() in CLASSES: class_arg=args[-1]; name_parts=args[:-1]
        if len(name_parts)>=1 and name_parts[-1].lower() in ["male","female"]: gender_arg=name_parts[-1]; name_parts=name_parts[:-1]
        if len(name_parts)>=1 and name_parts[-1].lower() in RACES: race_arg=name_parts[-1]; name_parts=name_parts[:-1]
        name=" ".join(name_parts)
        if not name: return "Enter name! Example: /register Dominic GOD Male Warrior"
        if p.get("registered") and p.get("reg_stage")=="done": return f"✅ Already registered as {p['displayName']}! Type {pre}profile"
        if is_group:
            DB.setdefault("pending_reg",{})[p["id"]]={"name":name,"race":race_arg,"gender":gender_arg,"class":class_arg,"group_id":group_id,"sender":sender_id}
            p["reg_stage"]="waiting_pin"; p["displayName"]=name; p["name"]=name; apply_register_details(p, race_arg, gender_arg, class_arg); p["registered"]=False; save()
            return f"✅ Registration Done ✔ Player\n👤 {name}\n📩 For the Final step please check your DM with this BOT and finish the final step"
        else:
            DB.setdefault("pending_reg",{})[p["id"]]={"name":name,"race":race_arg,"gender":gender_arg,"class":class_arg,"group_id":group_id,"sender":sender_id}
            p["reg_stage"]="waiting_pin"; p["displayName"]=name; p["name"]=name; apply_register_details(p, race_arg, gender_arg, class_arg); p["registered"]=False; save()
            return f"👤 Player, your registration: {pre}Register {name} {race_arg} {gender_arg} {class_arg}\n✅ Step 1 Done!\n🔐 Now Create a 4-digit Password (PIN) - Just type 4 numbers e.g. 1234"
    if not p["registered"] and cmd not in ["register","help","menu","ping","info","link","password","prefix","races","classes"]: return f"❌ Not registered. Type {pre}register <name> <race> <gender> <class>"
    if cmd=="profile": return box_str("👤 PROFILE",[f"✨ {p['displayName']} {p['rank']}",f"👑 Title: {p.get('title','Adventurer')}",f"🧬 Race: {p.get('race','-')} | ⚔️ Class: {p.get('class','-')} | ⚧ Gender: {p['gender']}",f"❤️ HP {p['hp']}/{p['maxHp']} 🔵 MP {p['mp']}/{p['maxMp']}",f"⚔️ ATK {p['atk']} 🛡️ DEF {p['def']} 💨 SPD {p['spd']}",f"💠 Level {p['level']} ⚡ EXP {p['exp']}/{exp_need(p['level'])}"]+stones_text(p, show_secret=can_use_supreme(p))+[f"🏠 House: {p['house']} 🚗 Car: {p.get('car')}"])
    if cmd=="stats":
        STR=p.get("str",0)+p["atk"]//5; AGI=p.get("agi",10); INT=p.get("int",0)+p["maxMp"]//20; VIT=p.get("vit",0)+p.get("con",10); DEF=p["def"]; LUK=p.get("luk",0)+p["spd"]//3
        lines=[f"🧩 {p['rank']} | 💠 LV.{p['level']} | 💎 GEMS: {p.get('gems',5)}","━━━━━━━━━━━━━━━━━━━━━━━━━━",f"💪 STR: {STR} (+{STR*2}% DMG)  |  ⚡ AGI: {AGI} (+{AGI}% Crit/Dodge)",f"🧠 INT: {INT} (+{INT}% Skill)  |  ❤️ VIT: {VIT} (+{VIT*10} Max HP)",f"🛡️ DEF: {DEF} (-{DEF} Boss DMG)  |  🍀 LUK: {LUK} (+{LUK}% Luck)","━━━━━━━━━━━━━━━━━━━━━━━━━━",f"❤️ HP {p['hp']} / {p['maxHp']}",bar(p["hp"],p["maxHp"],22),f"⚡ XP {p['exp']} / {exp_need(p['level'])}",bar(p["exp"],exp_need(p['level']),22),"━━━━━━━━━━━━━━━━━━━━━━━━━━"]
        lines+=stones_text(p, show_secret=can_use_supreme(p))
        lines+=["━━━━━━━━━━━━━━━━━━━━━━━━━━",f"🏆 Rank: {p['rank']}  |  👑 Title: {p.get('title','Adventurer')}",f"🧬 Race: {p.get('race')} - {RACES.get(p.get('race','').lower(),{}).get('ability','')}",f"⚔️ Class: {p.get('class')} - {CLASSES.get(p.get('class','').lower(),{}).get('ability','')}","",f"📊 HUNTER ATTRIBUTES — Upgrade with {pre}addstat [stat] [amt]!"]
        return box_str(f"📊 {p['displayName'].upper()} — ATTRIBUTES",lines)
    if cmd=="wallet": return box_str("💰 WALLET", stones_text(p, show_secret=can_use_supreme(p)))
    if cmd=="daily":
        now=time.time(); left=86400-(now-p.get("lastDaily",0))
        if left>0: return box_str("⏳ DAILY WAIT",[f"Wait {time_left(left)}"])
        p["lastDaily"]=now; p["lgss"]=p.get("lgss",0)+10; gain_exp(p,30); save(); return box_str("🎁 DAILY",["💎 +10 LGSS","⚡ +30 EXP"])
    if cmd=="claim": p["lgss"]=p.get("lgss",0)+5; save(); return box_str("🎁 CLAIMED",["💎 +5 LGSS"])
    if cmd in ["moves","move"]:
        if args:
            try: num=int(args[0])
            except: return f"Use {pre}moves <number>"
            p["awaiting_move_until"]=0; return use_move_in_dungeon(p,num)
        if not DB.get("dungeon") or not DB["dungeon"].get("in_dungeon"):
            my=get_my_moves(p); lines=[f"{p['displayName']} Lv{p['level']}"]
            for num in my: mv=ALL_MOVES[num]; lines.append(f"{num}. {mv['name']} - {mv['dmg']} dmg - {mv['desc']}")
            return box_str("📚 MY MOVES",lines)
        my=get_my_moves(p); lines=[f"⚔️ BATTLE - Floor {DB['dungeon']['floor']} Boss HP: {DB['dungeon']['enemy_hp']}",f"❤️ HP: {p['hp']}/{p['maxHp']} 🔵 MP: {p['mp']}/{p['maxMp']}",""]
        for num in my: mv=ALL_MOVES[num]; lines.append(f"{num}. {mv['name']} - {mv['dmg']} dmg - {mv['mp']} MP - {mv['desc']}")
        lines+=["","⚡ QUICK: Just type NUMBER e.g. 5 - within 5 seconds!",f"⏰ After 5 sec you MUST type {pre}moves 5"]
        p["awaiting_move_until"]=time.time()+5; save(); return box_str("⚔️ CHOOSE YOUR MOVE",lines)
    if cmd=="mymoves":
        my=get_my_moves(p); lines=[f"{p['displayName']} Lv{p['level']} Rank: {p['rank']}"]
        for num in my: mv=ALL_MOVES[num]; lines.append(f"{num}. {mv['name']} - {mv['dmg']} dmg - {mv['desc']}")
        return box_str("📚 MY MOVES",lines)
    if cmd=="dungeon":
        if args and args[0]=="enter":
            if DB.get("dungeon") and DB["dungeon"].get("in_dungeon"): return "⚠️ Already in dungeon! Use /moves"
            return start_dungeon(p)
        if args and args[0]=="floor": return box_str("🏰 DUNGEON FLOOR",[f"Current Floor: {p.get('dungeon_floor',1)}",f"Checkpoint: {p.get('checkpoint',1)}"])
        if args and args[0]=="leave": DB["dungeon"]=None; save(); return "🚪 Left dungeon"
        return f"Use {pre}dungeon enter | floor | leave"
    if cmd=="leaderboard":
        s=sorted([x for x in DB["players"].values() if x.get("registered")], key=lambda x: x.get("level",1), reverse=True)[:10]
        lines=["🏆 LEADERBOARD - Web + WhatsApp SAME"]
        for i,x in enumerate(s,1): lines.append(f"{i}. 👤 {x['displayName']} Lv{x['level']} 💎 {fmt(x.get('lgss',0))} LGSS")
        return box_str("🏆 LEADERBOARD",lines)
    if cmd=="bank":
        if not args: return box_str("🏦 BANK", stones_text(p, show_secret=can_use_supreme(p)))
        if args[0] in ["register","open"]:
            if p.get("bank_open"): return "✅ Bank already open"
            if p.get("lgss",0)<10: return "Need 10 LGSS to open bank"
            p["lgss"]-=10; p["bank_open"]=True; save(); return box_str("🏦 BANK OPENED",["Paid 10 LGSS ✅"])
        if args[0]=="deposit":
            amt=p.get("lgss",0) if len(args)<2 or args[1]=="all" else int(args[1]); p["lgss"]-=amt; p["bank"]+=amt; save(); return f"💎 Deposited {fmt(amt)} LGSS"
        if args[0]=="withdraw":
            amt=p["bank"] if len(args)<2 or args[1]=="all" else int(args[1]); p["bank"]-=amt; p["lgss"]=p.get("lgss",0)+amt; save(); return f"💎 Withdrew {fmt(amt)} LGSS"
        return "Bank done"
    if cmd=="heal":
        if p.get("lgss",0)<1: return "Need 1 LGSS"
        p["lgss"]-=1; p["hp"]=p["maxHp"]; p["mp"]=p["maxMp"]; save(); return box_str("💊 HEALED",["HP and MP full"])
    if cmd=="link": return box_str("📱 WHATSAPP LINKED",["Bot linked to WhatsApp 0779798568"])
    if cmd=="password": return "❌ Wrong password."
    if cmd=="race":
        if not args: return box_str("🧬 RACES",[f"• {v['name']} - {v['ability']} - {v['desc']}" for v in RACES.values()])
        if args[0].lower()=="god" and not is_owner(p): return "God only for Owners"
        if args[0].lower() not in RACES: return "Race not found"
        p["race"]=RACES[args[0].lower()]["name"]; save(); return f"🧬 You are {p['race']} - {RACES[args[0].lower()]['ability']}"
    if cmd=="class":
        if not args: return box_str("⚔️ CLASSES",[f"• {v['name']} - {v['ability']} - {v['desc']}" for v in CLASSES.values()])
        if args[0].lower() not in CLASSES: return "Class not found"
        p["class"]=CLASSES[args[0].lower()]["name"]; save(); return f"⚔️ You are {p['class']} - {CLASSES[args[0].lower()]['ability']}"
    if cmd=="gender":
        if not args or args[0].lower() not in ["male","female"]: return "Use /gender male or female"
        p["gender"]=args[0].capitalize(); save(); return f"Gender: {p['gender']}"
    if cmd=="rename":
        if not args: return "Use /rename <new name>"
        old=p["displayName"]
        if get_player_by_name(rest) and get_player_by_name(rest)["id"]!=p["id"]: return f"Name '{rest}' already taken!"
        p["displayName"]=rest; p["name"]=rest; save(); return f"✏️ Renamed {old} -> {rest}"
    if cmd=="pvp":
        if not args: return f"Use: {pre}pvp <player>"
        return f"⚔️ Challenge sent to {' '.join(args)} - They type {pre}accept"
    if cmd=="accept": return "✅ Challenge accepted! Type /moves to fight!"
    if cmd=="decline": return "❌ Challenge declined"
    if cmd=="forfeit": DB["dungeon"]=None; save(); return "🏳️ You forfeited battle"
    # Generic handlers for all other screenshot systems - keep game alive
    if cmd in ["party","labyrinth","family","families","raid","arena","worldboss","demoncastle","rebirth","guild","church","pray","kick","promote","demote","tagall","hidetag","close","open","sybau","unsybau","job","marry","divorce","spouse","house","rental","pet","sticker","unsticker","play","tt","ig","dl","market","achievements","hunger","eat","tavern","feast","cook","quests","season","share","core","buy","bio","web","emoji","broadcast","rob","bail","breakout","wanted","hospital","immortal","learn","skill","inventory","use","sell","go","notifications","monarchs","duel","train","gym","gate","shop","equip","unequip"]:
        if cmd=="party" and args and args[0]=="create": p["party"]=" ".join(args[1:]); save(); return f"👥 Party created: {p['party']}"
        if cmd=="labyrinth" and args and args[0]=="force":
            if not is_owner(p): return "Only Owners"
            WORLD["labyrinth"]=800; save(); return "🌀 Labyrinth OPEN"
        if cmd=="labyrinth": return "🌀 Labyrinth - Use /labyrinth enter / attack / move"
        if cmd=="raid" and args and args[0]=="claim": p["lgss"]=p.get("lgss",0)+10; save(); return "🎁 Raid claimed +10 LGSS"
        if cmd=="arena" and args and args[0]=="enter":
            if p.get("mgss",0)<5 and p.get("lgss",0)<500: return "Need 5 MGSS (or 500 LGSS) to enter"
            save(); return "🪞 Entered Hall of Reflections! Use /arena fight"
        if cmd=="guild" and args and args[0]=="create": p["guild"]=" ".join(args[1:]); save(); return f"🏛️ Guild created: {p['guild']}"
        if cmd=="job" and args and args[0]=="work": p["lgss"]=p.get("lgss",0)+5; save(); return "💼 Work done +5 LGSS"
        if cmd=="marry": return "💍 Proposal sent!"
        if cmd=="rob": return "🥷 Rob attempted - Cooldown 10 mins"
        if cmd=="hospital": return "🏥 Hospital - Use /hospital checkup / treat"
        return f"✅ {cmd} done: {' '.join(args)}"
    return f"❌ No Such Command Player - Type {pre}menu"

app = Flask(__name__)
# WEBSITE - NO OWNER PASSWORD SHOWN ANYWHERE - Race + Class REQUIRED before Register
HTML = """<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>INFINITY HUNTER</title><style>body{background:#050510;color:#fff;font-family:Arial;margin:0}input,select{width:100%;padding:14px;margin:8px 0;background:#000;color:#fff;border:2px solid #7B2FFF;border-radius:12px;box-sizing:border-box}button{width:100%;padding:14px;background:#FFD700;color:#000;border:none;border-radius:12px;font-weight:900;margin:8px 0}button:disabled{background:#333;color:#777}.card{background:#111128;border:1px solid #333;padding:16px;border-radius:16px;margin:12px}pre{white-space:pre-wrap;background:#000;padding:12px;border-radius:10px}.hidden{display:none}.raceinfo{font-size:12px;color:#FFD700}</style></head><body>
<div id='landing' style='text-align:center;padding:60px 16px'><h1 style='color:#FFD700'>⚡ INFINITY HUNTER ⚡</h1><p>Web + WhatsApp SAME GAME</p><button onclick='showAuth()' style='max-width:300px'>ENTER →</button><p style='font-size:12px;color:#aaa'>3x 1TB Backups • Spirit Stones Currency</p></div>
<div id='auth' class='hidden' style='text-align:center;padding:20px'><div class='card' style='max-width:460px;margin:auto;text-align:left'><h2>📝 REGISTER / 🔑 LOGIN</h2>
<input id='name' placeholder='Name e.g. Dominic Mastiria'>
<input id='pass' type='password' placeholder='Enter Password'>
<label>🧬 Pick Race - REQUIRED</label><select id='race' onchange='showRace()'><option value=''>-- Pick Race --</option><option value='Human'>Human - Adapt - +10% EXP</option><option value='Demon'>Demon - Demon Rage - +20% ATK</option><option value='Fairy'>Fairy - Fairy Heal - +20% Heal</option><option value='Mage'>Mage - Arcane Burst - +30% Skill</option><option value='Elf'>Elf - Elf Arrow - +20% AGI</option><option value='Vampire'>Vampire - Blood Drain - Lifesteal 15%</option><option value='Dragon'>Dragon - Dragon Breath - +30% HP</option><option value='Angel'>Angel - Holy Light - +20% DEF</option><option value='God'>God - Owners Only</option></select><p id='raceinfo' class='raceinfo'></p>
<label>⚔️ Pick Class - REQUIRED</label><select id='class' onchange='checkReady()'><option value=''>-- Pick Class --</option><option value='Warrior'>Warrior - Slash - +ATK</option><option value='Mage'>Mage - Fireball - +INT</option><option value='Assassin'>Assassin - Shadow Strike - +Crit</option><option value='Healer'>Healer - Heal - +Heal</option><option value='Archer'>Archer - Piercing Arrow - +SPD</option><option value='Tank'>Tank - Shield Wall - +DEF/HP</option><option value='Necromancer'>Necromancer - Soul Drain</option><option value='Swordmaster'>Swordmaster - Dragon Smash</option></select>
<label>⚧ Gender</label><select id='gender'><option value='Male'>Male</option><option value='Female'>Female</option></select>
<button id='regbtn' onclick='doAuth("register")' disabled>⚡ REGISTER - Pick Race + Class First</button><button onclick='doAuth("login")' style='background:#7B2FFF;color:#fff'>🔑 LOGIN</button><p id='authmsg'></p><p style='font-size:12px'>Owners: Enter your password to get God + Immortal Emperor perks.<br>Other players: Choose any password you want. Do NOT share it.</p></div></div>
<div id='dash' class='hidden'><div style='background:#111128;padding:12px;display:flex;justify-content:space-between'><b>⚡ INFINITY HUNTER - CHAT</b><span id='who'></span></div><div style='padding:12px'><div class='card'><div id='chat'></div><input id='cmd' placeholder='Type e.g. /menu /profile /stones'><button onclick='sendChat()'>▶ SEND</button></div></div></div>
<script>let myName='';function showAuth(){document.getElementById('landing').classList.add('hidden');document.getElementById('auth').classList.remove('hidden');}function showRace(){let r=document.getElementById('race').value;let m={'Human':'Adapt +10% EXP','Demon':'Demon Rage +20% ATK','Fairy':'Fairy Heal +20% Heal','Mage':'Arcane Burst +30% Skill','Elf':'Elf Arrow +20% AGI','Vampire':'Blood Drain Lifesteal 15%','Dragon':'Dragon Breath +30% HP','Angel':'Holy Light +20% DEF','God':'Owners Only'};document.getElementById('raceinfo').textContent=m[r]||'';checkReady();}function checkReady(){let r=document.getElementById('race').value;let c=document.getElementById('class').value;let b=document.getElementById('regbtn');if(r&&c){b.disabled=false;b.textContent='⚡ REGISTER';}else{b.disabled=true;b.textContent='⚡ REGISTER - Pick Race + Class First';}}async function doAuth(mode){let name=document.getElementById('name').value.trim();let pass=document.getElementById('pass').value.trim();let race=document.getElementById('race').value;let cls=document.getElementById('class').value;let gender=document.getElementById('gender').value;if(!name||!pass){document.getElementById('authmsg').textContent='Enter Name + Password';return;}if(mode=='register'&&(!race||!cls)){document.getElementById('authmsg').textContent='Pick Race + Class first!';return;}let r=await fetch('/api/auth',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,pass,race,class:cls,gender,mode})});let j=await r.json();document.getElementById('authmsg').textContent=j.msg;if(j.ok){myName=name;document.getElementById('auth').classList.add('hidden');document.getElementById('dash').classList.remove('hidden');document.getElementById('who').textContent='@'+name;}}async function sendChat(){let t=document.getElementById('cmd').value;if(!t)return;let d=document.createElement('div');d.textContent='You: '+t;document.getElementById('chat').appendChild(d);document.getElementById('cmd').value='';let r=await fetch('/api/command',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:myName,text:t})});let j=await r.json();let d2=document.createElement('div');d2.textContent='Bot: '+j.reply;document.getElementById('chat').appendChild(d2);}</script></body></html>"""
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
    if mode=="register" and (not race or not cls): return jsonify({"ok":False,"msg":"Pick Race + Class first!"})
    if existing and existing.get("registered"): return jsonify({"ok":True,"msg":f"Already registered - Logged in!"})
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
                            if pending: send_whatsapp(sender, f"👤 Player, your registration: /Register {pending['name']} {pending.get('race','')} {pending.get('gender','')} {pending.get('class','')}\n✅ Step 1 Done!\n🔐 Now Create a 4-digit Password (PIN) - Just type 4 numbers")
                        if text.isdigit() and len(text)==4 and "Registration successfully done" in reply:
                            send_whatsapp(sender, f"🎉 Registration Successfully Done @{p_tmp.get('displayName','Player')}\n👋 Welcome to INFINITY HUNTER @{p_tmp.get('displayName','Player')}\n👉 Now do /help to see menu\n📜 Type /menu")
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
def health(): return "OK - Infinity v9 Spirit Stones - No Owner Password Shown"
if __name__=='__main__':
    port=int(os.environ.get('PORT',10000)); print(f"INFINITY v9 LIVE on port {port}"); app.run(host='0.0.0.0', port=port)
