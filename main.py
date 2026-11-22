# INFINITY MERGED v8 - FIXED - No markdown fences in file - Web + WhatsApp
# Owners: 0779798568 / Lord Infinity / Immortal Emperor - Pass 2164
import json, random, os, time, datetime
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
        DB["players"][pid]={"id":pid,"name":name,"displayName":name,"registered":False,"password":"","race":"Human","level":1,"exp":0,"zeni":1000000,"bank":0,"bank_open":False,"savings":0,"hp":100,"maxHp":100,"mp":50,"maxMp":50,"atk":15,"def":10,"spd":12,"agi":10,"con":10,"rank":"E - Novice","wins":0,"losses":0,"dungeonClears":0,"dungeon_floor":1,"checkpoint":1,"kills":0,"job":"Unemployed","loan":0,"loanDue":0,"house":"None","houseTier":0,"car":"None","shop":"None","pet":None,"guild":"None","guildRank":"None","lastDaily":0,"lastWork":0,"lastClaim":0,"lastRob":0,"jailed":0,"banned":False,"questsDone":0,"notifications":[],"gender":"Not Set","age":15,"lifespan":80,"birthday":now.strftime("%d %b %Y"),"spouse":None,"title":"Adventurer","titles":["Adventurer"],"cultRealm":0,"cultLayer":1,"cultXp":0,"cultNeed":100,"talentType":"","talentValue":"","talentGrade":"","isInfinity":False,"isChosen":False,"chosenUntil":0,"wood":0,"houseBuilt":False,"sect":"No Sect","sectRank":"-","hunger":100,"family":"No Family","party":"No Party","church":"No Church","inventory":{},"skills":[],"active_skills":[],"awaiting_move_until":0,"gems":5,"str":0,"int":0,"vit":0,"luk":0,"bio":"","emoji":"⚔️","hunger_lvl":100,"cooking":1,"achievements":[],"reg_stage":"none"}
        WORLD["totalPlayers"]+=1
    for k,v in {"password":"","inventory":{},"skills":[],"active_skills":[],"awaiting_move_until":0,"gems":5,"str":0,"int":0,"vit":0,"luk":0,"bio":"","emoji":"⚔️","hunger_lvl":100,"cooking":1,"achievements":[],"reg_stage":"none"}.items():
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
    save(); return box_str(f"🏰 DUNGEON FLOOR {floor}",[f"👹 Enemy: Floor {floor} Boss",f"🎨 Style: {style}",f"❤️ Boss HP: {hp}",f"⚔️ Boss ATK: {atk}",f"💰 Reward: {reward} Zeni",f"📍 Checkpoint: Floor {p.get('checkpoint',1)}","Type /moves to see moves","Then /moves <number> to attack"])
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
        r=gain_zeni(p,d["reward"]); gain_exp(p,d["exp"]); p["dungeonClears"]+=1; cleared=d["floor"]; p["dungeon_floor"]=cleared+1
        if cleared%50==0: p["checkpoint"]=cleared; out.append(f"📍 CHECKPOINT SAVED AT FLOOR {cleared}")
        DB["dungeon"]=None; save(); return box_str("🎉 FLOOR CLEARED",[f"Floor {cleared} cleared",f"💰 +{fmt(r)} Zeni",f"⚡ +{d['exp']} EXP",f"➡️ Next Floor: {cleared+1}",f"📍 Checkpoint: {p['checkpoint']}","Type /dungeon enter"])
    edmg=max(1,d["enemy_atk"]+random.randint(0,10)-p["def"]//2); p["hp"]-=edmg; out.append(f"💥 Boss hit you -{edmg} Your HP: {max(0,p['hp'])}")
    if p["hp"]<=0:
        p["hp"]=1; respawn=p.get("checkpoint",1); p["dungeon_floor"]=respawn; DB["dungeon"]=None; save(); return box_str("💀 YOU DIED",[f"Died on Floor {d['floor']}",f"Respawn at Checkpoint Floor {respawn}","HP set to 1"])
    save(); return "\n".join(out)+"\nYour turn! /moves <number> again"
def apply_owner_perks(p):
    p["isInfinity"]=True; p["isChosen"]=True; p["chosenUntil"]=time.time()+2*24*3600; p["race"]="God"; p["atk"]=100; p["maxHp"]=300; p["hp"]=300; p["mp"]=9999; p["maxMp"]=9999; p["cultRealm"]=1; p["cultLayer"]=9; p["talentType"]="Bloodline"; p["talentValue"]="Primordial Chaos Bloodline"; p["talentGrade"]="Divine Grade"; p["title"]="Immortal Emperor"
    if "Immortal Emperor" not in p.get("titles",[]): p["titles"].append("Immortal Emperor")
def apply_register_details(p, race_raw, gender_raw):
    pretty={"human":"Human","demon":"Demon","fairy":"Fairy","mage":"Mage","elf":"Elf","vampire":"Vampire","dragon":"Dragon","angel":"Angel","god":"God"}
    if race_raw and race_raw.lower() in pretty:
        if race_raw.lower()=="god" and not is_owner(p) and p.get("displayName","").lower() not in OWNER_NAMES: return "God only for Owners"
        p["race"]=pretty[race_raw.lower()]
    if gender_raw and gender_raw.lower() in ["male","female"]: p["gender"]=gender_raw.capitalize()
    if p.get("displayName","").lower() in OWNER_NAMES: apply_owner_perks(p)
    return None

# ===== MENU WITH EMOJIS + PICTURE STYLE - ALL IN LIST FORM =====
def menu_text(p):
    pre=get_prefix(); tag=f"@{p['displayName']}"
    L=[]
    L+=["⚡ INFINITY Hunter",f"👤 {tag} — {p.get('title','Adventurer')} | Lv{p['level']} | {p['race']} {p.get('emoji','⚔️')}",f"🔑 Prefix: {pre}  |  Type {pre}menu to see this again",""]
    L+=["📋 GENERAL",
    f"• 📝 {pre}register <name> — Join the world",
    f"• 📊 {pre}stats — View your stats (picture card)",
    f"• 👤 {pre}profile — View your profile card",
    f"• ✏️ {pre}rename <new name> — Change display name",
    f"• ℹ️ {pre}info — Bot stats, uptime, population",
    f"• 📜 {pre}help — Show this menu",
    f"• 🏓 {pre}ping — Check if bot is alive",""]
    L+=["⚔️ BATTLE",
    f"• ⚔️ {pre}pvp @user — Challenge someone",
    f"• ✨ {pre}skill cast <magic> @user — Cast magic",
    f"• 🔥 {pre}skill activate <name> — Use buff / reactivate passive",
    f"• 🚫 {pre}skill deactivate <name> — Turn off passive (e.g. Gluttony)",
    f"• 🗡️ {pre}move <move> — Use a move in battle",
    f"• 📜 {pre}moves — See options during battle",
    f"• 📚 {pre}mymoves — View full moveset",
    f"• 🎓 {pre}learn — View newly unlocked race moves",
    f"• ✅ {pre}accept — Accept PvP challenge",
    f"• ❌ {pre}decline — Decline challenge",
    f"• 🏳️ {pre}forfeit — Forfeit battle",""]
    L+=["🏰 DUNGEON",
    f"• 🏰 {pre}dungeon enter — Enter dungeon",
    f"• 🎒 {pre}inventory — View items",
    f"• 🧪 {pre}use <item> [qty] — Use item(s)",
    f"• 🧴 Battle potions: Small Heal, Medium Heal, MP Potion, Greater MP Potion, Phoenix Elixir, Stat Boost",
    f"• 💸 {pre}sell <item> [qty] — Sell for Zeni",""]
    L+=["👥 PARTY",
    f"• 👥 {pre}party create <name> — Create party",
    f"• 📩 {pre}party invite @user — Invite",
    f"• ✅ {pre}party accept — Accept invite",
    f"• 🚪 {pre}party leave — Leave party",
    f"• 👢 {pre}party kick @user — Remove member (leader)",""]
    L+=["🌀 LABYRINTH",f"• 🌀 {pre}labyrinth status / enter / attack / move",f"• 👥 {pre}labyrinth team create / invite / accept",""]
    L+=["🏠 FAMILY",f"• 🏠 {pre}family found / add / accept / leave / info",""]
    L+=["🛡️ COUNTRY RAIDS",f"• 🛡️ {pre}raid join / start / attack / move / claim",""]
    L+=["🪞 HALL OF REFLECTIONS",f"• 🪞 {pre}arena enter — 250,000 Zeni",f"• ⚔️ {pre}arena fight — Face reflections",""]
    L+=["🏛️ GUILD",f"• 🏛️ {pre}guild create / join / info / members / quest / fund",""]
    L+=["⛪ CHURCH",f"• ⛪ {pre}church join / leave",f"• 🙏 {pre}pray — Pray (24h)",""]
    L+=["💰 ECONOMY",f"• 🎁 {pre}daily — 1000 Zeni (24h)",f"• 💰 {pre}wallet / {pre}gold — Balance",f"• 🏦 {pre}bank — Bank",f"• 🛒 {pre}shop / {pre}buy — Shop",f"• 💝 {pre}give @user <amount> — Give Zeni",""]
    L+=["💼 JOBS",f"• 💼 {pre}job list / apply / work / info",""]
    L+=["💍 MARRIAGE",f"• 💍 {pre}marry @user — Propose",f"• 💔 {pre}divorce — End marriage",""]
    L+=["🏠 HOUSING & RENTAL",f"• 🏠 {pre}house buy / upgrade / info",f"• 🏘️ {pre}rental list / rent / apply",""]
    L+=["🐉 PETS",f"• 🐉 {pre}pet list / buy / name / train / info",""]
    L+=["🎨 MEDIA & DOWNLOADER",f"• 🎨 {pre}sticker / {pre}unsticker / {pre}play",f"• ⬇️ {pre}tt / {pre}ig / {pre}dl — Download",""]
    L+=["🛒 MARKET",f"• 🛒 {pre}market list / buy / cancel",""]
    L+=["🏆 LEADERBOARDS",f"• 🏆 {pre}leaderboard — Top players (Web + WhatsApp SAME)",f"• 👑 {pre}monarchs — Monarchs",""]
    L+=["👑 OWNER [SHADOW NATION]",f"• 👑 {pre}setprefix <new> — Change prefix (Owners only)",f"• 📢 {pre}broadcast — Announce",f"• 🛡️ {pre}kick / promote / ban / sybau — Group mgmt",""]
    L+=["",f"💡 Tip: {tag} Type {pre}profile to see your card!"]
    return box_str("⚡ INFINITY Hunter", L)

def process_command(sender_id, raw_text, is_group=False, group_id=None):
    # sender_id: WhatsApp JID OR web:<name> OR group:<group_id>:<user_id>
    if sender_id.startswith("web:"):
        name=sender_id[4:]; p=get_player_by_name(name)
        if not p: p=get_player(sender_id, name)
    else: p=get_player(sender_id, sender_id)
    text=(raw_text or "").strip()
    # ===== PIN STEP - DM ONLY: Player sends 4-digit PIN after group register =====
    if text.isdigit() and len(text)==4 and p.get("reg_stage")=="waiting_pin":
        pending=DB.get("pending_reg",{}).get(p["id"])
        if pending:
            p["password"]=text; p["registered"]=True; p["reg_stage"]="done"; p["displayName"]=pending["name"]; p["name"]=pending["name"]
            apply_register_details(p, pending.get("race",""), pending.get("gender",""))
            save()
            # This return is DM message. Group message is sent separately by webhook via pending_reg group_id
            return f"✅ Registration successfully done ✔\n👤 Player: {p['displayName']}\n🔐 PIN saved!\n👉 Please Go back to the group and continue\n🎮 Type /help in group to see menu"
        else:
            p["reg_stage"]="none"; save(); return "No pending registration. Type /register <name> <race> <gender> in group first."
    # Bare number within 5 sec after /moves
    if text.isdigit() and not text.startswith("/"):
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
        if not args: return f"Use: {pre}setprefix <new>  Example: {pre}setprefix .  Current: {pre}"
        DB["config"]["prefix"]=args[0]; save(); return f"✅ Prefix changed to: {args[0]}\nNow use {args[0]}menu, {args[0]}profile"
    if cmd=="prefix": return f"🔑 Current prefix: {pre}\nOwners change with: {pre}setprefix <new>"
    if cmd=="info":
        reg=sum(1 for pl in DB["players"].values() if pl.get("registered"))
        return box_str("ℹ️ BOT INFO",["🤖 Bot: INFINITY AND BEYOND v8","👑 Owners: 0779798568 / Lord Infinity / Immortal Emperor - Pass 2164",f"🔑 Prefix: {pre}",f"👥 Players registered: {reg}",f"👥 Players total: {len(DB['players'])}",f"💰 Economy: {fmt(WORLD['totalZeni'])}","💾 Backups: 3x 1TB - Auto-save"])
    # ===== NEW REGISTER - GROUP -> DM -> PIN -> GROUP DONE =====
    if cmd=="register":
        if not args: return f"Use: {pre}register <name> <race> <gender>\nExample: {pre}register Dominic Mastiria GOD Male"
        # Parse: /register Dominic Mastiria GOD Male  -> name = all except last 2 if last 2 are race/gender
        # Simple: if 3+ args and last is male/female and second-last is race, name = rest
        race_arg=""; gender_arg=""
        name_parts=args[:]
        if len(args)>=3 and args[-1].lower() in ["male","female"]:
            gender_arg=args[-1]; 
            if args[-2].lower() in ["human","demon","fairy","mage","elf","vampire","dragon","angel","god"]:
                race_arg=args[-2]; name_parts=args[:-2]
            else:
                name_parts=args[:-1]
        elif len(args)>=2 and args[-1].lower() in ["human","demon","fairy","mage","elf","vampire","dragon","angel","god"]:
            race_arg=args[-1]; name_parts=args[:-1]
        name=" ".join(name_parts)
        # If already fully registered + not waiting PIN, allow update
        if p.get("registered") and p.get("reg_stage")=="done":
            err=apply_register_details(p, race_arg, gender_arg)
            if err: return err
            save(); return f"✅ Already registered as {p['displayName']}! Type {pre}profile"
        # NEW: If this is in a GROUP (is_group=True) -> Step 1: save pending, tell group to check DM
        # Webhook sets is_group=True when message comes from group. For DM / Web, is_group=False -> direct register + ask PIN
        if is_group:
            # Save pending - do NOT mark registered yet until PIN in DM
            DB.setdefault("pending_reg",{})[p["id"]]={"name":name,"race":race_arg,"gender":gender_arg,"group_id":group_id,"sender":sender_id}
            p["reg_stage"]="waiting_pin"; p["displayName"]=name; p["name"]=name
            # Apply race/gender temp so DM can show it
            apply_register_details(p, race_arg, gender_arg)
            p["registered"]=False  # will become True after PIN
            save()
            # Return value is GROUP message. DM is sent by webhook separately (see webhook code below)
            return f"✅ Registration Done ✔ Player\n👤 {name}\n📩 For the Final step please check your DM with this BOT and finish the final step\n🔐 Bot will ask you for your 4-digit PIN in DM"
        else:
            # DM or Web or Solo chat: direct - save pending and ask for PIN right here
            DB.setdefault("pending_reg",{})[p["id"]]={"name":name,"race":race_arg,"gender":gender_arg,"group_id":group_id,"sender":sender_id}
            p["reg_stage"]="waiting_pin"; p["displayName"]=name; p["name"]=name
            apply_register_details(p, race_arg, gender_arg); p["registered"]=False; save()
            return f"👤 Player, your registration: {pre}Register {name} {race_arg} {gender_arg}\n✅ Step 1 Done!\n🔐 Now Create a 4-digit Password (PIN) - Just type 4 numbers e.g. 1234\n⚠️ Keep it private, don't share it in group!"
    if not p["registered"] and cmd not in ["register","help","menu","ping","info","link","password","prefix"]: return f"❌ Not registered. Type {pre}register <name> <race> <gender>  Example: {pre}register Dominic Mastiria GOD Male"
    if cmd=="profile": return box_str("👤 PROFILE",[f"✨ {p['displayName']} {p['rank']}",f"👑 Title: {p.get('title','Adventurer')}",f"🧬 Race: {p['race']} ⚧ Gender: {p['gender']}",f"❤️ HP {p['hp']}/{p['maxHp']} 🔵 MP {p['mp']}/{p['maxMp']}",f"⚔️ ATK {p['atk']} 🛡️ DEF {p['def']} 💨 SPD {p['spd']}",f"💠 Level {p['level']} ⚡ EXP {p['exp']}/{exp_need(p['level'])}",f"💰 Zeni {fmt(p['zeni'])} 🏦 Bank {fmt(p['bank'])} 💼 Job: {p['job']}",f"🏠 House: {p['house']} 🚗 Car: {p.get('car')}",f"🏰 Dungeon Floor: {p.get('dungeon_floor',1)} 📍 Checkpoint: {p.get('checkpoint',1)}",f"📝 Bio: {p.get('bio','-')} {p.get('emoji','⚔️')}"])
    if cmd=="stats":
        STR=p.get("str",0)+p["atk"]//5; AGI=p.get("agi",10); INT=p.get("int",0)+p["maxMp"]//20; VIT=p.get("vit",0)+p.get("con",10); DEF=p["def"]; LUK=p.get("luk",0)+p["spd"]//3
        # PICTURE SIMULATES - built card like screenshot
        return box_str(f"📊 {p['displayName'].upper()} — ATTRIBUTES",[f"🧩 {p['rank']} | 💠 LV.{p['level']} | 💎 GEMS: {p.get('gems',5)}","━━━━━━━━━━━━━━━━━━━━━━━━━━",f"💪 STR: {STR} (+{STR*2}% DMG)  |  ⚡ AGI: {AGI} (+{AGI}% Crit/Dodge)",f"🧠 INT: {INT} (+{INT}% Skill)  |  ❤️ VIT: {VIT} (+{VIT*10} Max HP)",f"🛡️ DEF: {DEF} (-{DEF} Boss DMG)  |  🍀 LUK: {LUK} (+{LUK}% Luck)","━━━━━━━━━━━━━━━━━━━━━━━━━━",f"❤️ HP {p['hp']} / {p['maxHp']}",bar(p["hp"],p["maxHp"],22),f"⚡ XP {p['exp']} / {exp_need(p['level'])}",bar(p["exp"],exp_need(p['level']),22),"━━━━━━━━━━━━━━━━━━━━━━━━━━",f"💰 Zeni: {fmt(p['zeni'])}  |  🏦 Bank: {fmt(p['bank'])}",f"🏆 Rank: {p['rank']}  |  👑 Title: {p.get('title','Adventurer')}","",f"📊 HUNTER ATTRIBUTES — Upgrade with {pre}addstat [stat] [amt]!"])
    if cmd=="wallet": return box_str("💰 WALLET",[f"💵 Cash: {fmt(p['zeni'])}",f"🏦 Bank: {fmt(p['bank'])}",f"💎 Assets: {fmt(p['zeni']+p['bank']+p.get('savings',0))}"])
    if cmd=="daily":
        now=time.time(); left=86400-(now-p.get("lastDaily",0))
        if left>0: return box_str("⏳ DAILY WAIT",[f"Wait {time_left(left)}"])
        p["lastDaily"]=now; r=gain_zeni(p,10000); gain_exp(p,30); save(); return box_str("🎁 DAILY",[f"💰 +{fmt(r)} Zeni","⚡ +30 EXP"])
    if cmd in ["moves","move"]:
        if args:
            try: num=int(args[0])
            except: return f"Use {pre}moves <number>"
            p["awaiting_move_until"]=0; return use_move_in_dungeon(p,num)
        if not DB.get("dungeon") or not DB["dungeon"].get("in_dungeon"):
            my=get_my_moves(p); lines=[f"{p['displayName']} Lv{p['level']}"]
            for num in my: mv=ALL_MOVES[num]; lines.append(f"{num}. {mv['name']} - {mv['dmg']} dmg - {mv['desc']}")
            return box_str("📚 MY MOVES",lines)
        my=get_my_moves(p); lines=[f"⚔️ BATTLE - Floor {DB['dungeon']['floor']} Boss HP: {DB['dungeon']['enemy_hp']}",f"❤️ Your HP: {p['hp']}/{p['maxHp']} 🔵 MP: {p['mp']}/{p['maxMp']}",""]
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
        if args and args[0]=="floor": return box_str("🏰 DUNGEON FLOOR",[f"Current Floor: {p.get('dungeon_floor',1)}",f"Checkpoint: {p.get('checkpoint',1)}",f"Clears: {p.get('dungeonClears',0)}"])
        if args and args[0]=="leave": DB["dungeon"]=None; save(); return "🚪 Left dungeon"
        return f"Use {pre}dungeon enter | floor | leave"
    if cmd=="leaderboard":
        s=sorted([x for x in DB["players"].values() if x.get("registered")], key=lambda x: x.get("level",1), reverse=True)[:10]
        lines=["🏆 LEADERBOARD - Web + WhatsApp SAME"]
        for i,x in enumerate(s,1): lines.append(f"{i}. 👤 {x['displayName']} Lv{x['level']} 💰 {fmt(x['zeni'])} Zeni")
        return box_str("🏆 LEADERBOARD",lines)
    if cmd=="bank":
        if not args: return box_str("🏦 BANK",[f"💵 Cash {fmt(p['zeni'])}",f"🏦 Bank {fmt(p['bank'])}",f"Open: {'YES ✅' if p.get('bank_open') else 'NO ❌'}"])
        if args[0] in ["register","open"]:
            if p.get("bank_open"): return "✅ Bank already open"
            if p["zeni"]<1000000 and not is_owner(p): return "Need 1,000,000 Zeni"
            p["zeni"]=max(0,p["zeni"]-1000000); p["bank_open"]=True; save(); return box_str("🏦 BANK OPENED",["Paid 1M ✅"])
        if args[0]=="deposit":
            amt=p["zeni"] if len(args)<2 or args[1]=="all" else int(args[1]); p["zeni"]-=amt; p["bank"]+=amt; save(); return f"💰 Deposited {fmt(amt)} Bank {fmt(p['bank'])}"
        if args[0]=="withdraw":
            amt=p["bank"] if len(args)<2 or args[1]=="all" else int(args[1]); p["bank"]-=amt; p["zeni"]+=amt; save(); return f"💵 Withdrew {fmt(amt)}"
        return "Bank done"
    if cmd=="link": return box_str("📱 WHATSAPP LINKED",["Type /password 2164","Bot linked to WhatsApp 0779798568"])
    if cmd=="password":
        if args and args[0]=="2164": return box_str("📱 WHATSAPP LINKED",["✅ Password correct!","Bot linked to WhatsApp 0779798568"])
        return "❌ Wrong password."
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
    return f"❌ No Such Command Player - Type {pre}menu"

app = Flask(__name__)
HTML = """<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>INFINITY HUNTER</title><style>body{background:#050510;color:#fff;font-family:Arial;margin:0}input{width:100%;padding:14px;margin:8px 0;background:#000;color:#fff;border:2px solid #7B2FFF;border-radius:12px;box-sizing:border-box}button{width:100%;padding:14px;background:#FFD700;color:#000;border:none;border-radius:12px;font-weight:900;margin:8px 0}.card{background:#111128;border:1px solid #333;padding:16px;border-radius:16px;margin:12px}pre{white-space:pre-wrap;background:#000;padding:12px;border-radius:10px}.hidden{display:none}</style></head><body><div id='landing' style='text-align:center;padding:60px 16px'><h1 style='color:#FFD700'>⚡ INFINITY HUNTER ⚡</h1><button onclick='showAuth()' style='max-width:300px'>ENTER →</button></div><div id='auth' class='hidden' style='text-align:center;padding:20px'><div class='card' style='max-width:420px;margin:auto;text-align:left'><h2>REGISTER / LOGIN</h2><input id='name' placeholder='Name'><input id='pass' type='password' placeholder='Password - Owners: 2164'><button onclick='doAuth("register")'>⚡ REGISTER</button><button onclick='doAuth("login")' style='background:#7B2FFF;color:#fff'>🔑 LOGIN</button><p id='authmsg'></p></div></div><div id='dash' class='hidden'><div style='background:#111128;padding:12px;display:flex;justify-content:space-between'><b>⚡ INFINITY HUNTER - CHAT</b><span id='who'></span></div><div style='padding:12px'><div class='card'><div id='chat'></div><input id='cmd' placeholder='Type e.g. /menu /profile'><button onclick='sendChat()'>▶ SEND</button></div></div></div><script>let myName='';function showAuth(){document.getElementById('landing').classList.add('hidden');document.getElementById('auth').classList.remove('hidden');}async function doAuth(mode){let name=document.getElementById('name').value.trim();let pass=document.getElementById('pass').value.trim();let r=await fetch('/api/auth',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,pass,mode})});let j=await r.json();document.getElementById('authmsg').textContent=j.msg;if(j.ok){myName=name;document.getElementById('auth').classList.add('hidden');document.getElementById('dash').classList.remove('hidden');document.getElementById('who').textContent='@'+name;}}async function sendChat(){let t=document.getElementById('cmd').value;if(!t)return;let d=document.createElement('div');d.textContent='You: '+t;document.getElementById('chat').appendChild(d);document.getElementById('cmd').value='';let r=await fetch('/api/command',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:myName,text:t})});let j=await r.json();let d2=document.createElement('div');d2.textContent='Bot: '+j.reply;document.getElementById('chat').appendChild(d2);}</script></body></html>"""
@app.route('/')
def home(): return HTML
@app.route('/api/auth', methods=['POST'])
def api_auth():
    data=request.json or {}; name=(data.get('name') or '').strip(); pwd=(data.get('pass') or '').strip(); mode=data.get('mode','register')
    if not name or not pwd: return jsonify({"ok":False,"msg":"Enter Name + Password"})
    if name.lower() in OWNER_NAMES and pwd!=OWNER_PASSWORD: return jsonify({"ok":False,"msg":"Owners must use 2164"})
    existing=get_player_by_name(name)
    if mode=="login":
        if not existing or not existing.get("registered"): return jsonify({"ok":False,"msg":"Not registered. Click REGISTER"})
        if existing.get("password") and existing.get("password")!=pwd: return jsonify({"ok":False,"msg":"Wrong password"})
        return jsonify({"ok":True,"msg":f"Welcome back {name}!"})
    if existing and existing.get("registered"): return jsonify({"ok":True,"msg":f"Already registered - Logged in!"})
    p=get_player(f"web:{name}", name); p["password"]=pwd; p["registered"]=True; p["displayName"]=name; p["name"]=name; p["reg_stage"]="done"
    if name.lower() in OWNER_NAMES: apply_owner_perks(p)
    save(); return jsonify({"ok":True,"msg":f"Registered {name}!"})
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
                # Group detection: WhatsApp Cloud sends group messages with different context - we treat messages with 'context' or group id as group
                # For now: if message has 'context' with group, or metadata, treat as group. Fallback: check if sender is in pending group flow
                for msg in val.get('messages',[]):
                    sender=msg.get('from',''); text=msg.get('text',{}).get('body','')
                    # Detect group: if there is a group id in change value, or message has context
                    is_group=False; group_id=None
                    # WhatsApp Business: group messages come via 'messages' with 'context' - if present, assume group if context has group id
                    # Simpler heuristic used by many bots: if the bot is in a group, the 'from' is still user, but we check if this message was sent to a group by checking 'id' - we store group_id from first register call if user says 'in group'
                    # Here: if user is already waiting PIN, this is DM. If user just sent /register and is NOT waiting PIN, treat as GROUP (most registers happen in group)
                    p_tmp=get_player(sender, sender)
                    if text.lower().startswith(('/register','.register')) and p_tmp.get("reg_stage")!="waiting_pin":
                        is_group=True; group_id="group_"+sender  # placeholder - real group id comes from WhatsApp API when you enable groups
                    if text.startswith('/') or text.startswith('.') or text.isdigit():
                        reply=process_command(sender, text, is_group=is_group, group_id=group_id); save()
                        send_whatsapp(sender, reply)
                        # ===== GROUP -> DM HAND-OFF =====
                        # If this was a group register, also DM the user privately with PIN prompt
                        if is_group and "Registration Done" in reply:
                            pending=DB.get("pending_reg",{}).get(sender)
                            if pending:
                                dm_msg=f"👤 Player, your registration: /Register {pending['name']} {pending.get('race','')} {pending.get('gender','')}\n✅ Step 1 Done in group!\n🔐 Now Create a 4-digit Password (PIN) - Just type 4 numbers e.g. 1234\n⚠️ Do NOT send PIN in group, only here in DM!"
                                send_whatsapp(sender, dm_msg)
                        # If this was PIN completion in DM, also announce in group (if we know group)
                        if text.isdigit() and len(text)==4 and "Registration successfully done" in reply:
                            pending_group=DB.get("pending_reg",{}).get(sender,{}).get("group_id")
                            if pending_group:
                                group_msg=f"🎉 Registration Successfully Done @{p_tmp.get('displayName','Player')}\n👋 Welcome to INFINITY HUNTER @{p_tmp.get('displayName','Player')}\n👉 Now do /help to see menu\n📜 Type /menu to see all commands!"
                                # In real WhatsApp Cloud, you send to group id. Here we send to user as fallback - replace group_id with real group JID when you have it
                                send_whatsapp(sender, group_msg)
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
def health(): return "OK - Infinity v8 Fixed - Owners 0779798568 / Lord Infinity / Immortal Emperor"
if __name__=='__main__':
    port=int(os.environ.get('PORT',10000)); print(f"INFINITY v8 LIVE on port {port}"); app.run(host='0.0.0.0', port=port)
