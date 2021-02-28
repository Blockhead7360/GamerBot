import discord
import os
from message_groups import message_set, profile_set, spd
import utility
from dotenv import load_dotenv
import cexprtk
from bs4 import BeautifulSoup
import urllib
from datetime import datetime
import json

VERSION = "1.4 (extreme gamer epic)"
dev = False

load_dotenv()
client = discord.Client()

key_discordtoken = os.getenv("DISCORD-TOKEN")
key_merriamwebsterdictkey = os.getenv("MW-DICT-KEY")
key_merriamwebstertheskey = os.getenv("MW-THES-KEY")



name = "gamer bot"

sets = []
    
    #add_message_set(basics.init())
#    add_message_set(ignore.init())
class Basics:
    
    def __init__(self):
        
        self.set = [
            message_set(self.empty,
                        ["counter 34 bot"],
                        ["34!gotohell"]),
            message_set(self.tell_other,
                    ["tell "],
                    ["%0, here's a new message from %1: %2"]),
            message_set(self.empty,
                        ["proud of you"],
                        ["aww thank you :blush:",
                         "that means a lot :blush:"]),
            message_set(self.empty,
                        ["how are you made"],
                        ["check it out!\ncode: https://github.com/blockhead7360/gamerbot\nupdate log: http://docs.blockhead7360.com/changelogs/swwa-20010"]),
            message_set(self.empty,
                        ["how are you"],
                        ["i'm doing alright, thanks!",
                         "i'm doing well, thanks!",
                         "i'm good, thanks!",
                         "i'm doing alright.",
                         "i'm doing well.",
                         "i'm good."]),
            
            message_set(self.change_name,
                     ["call you "],
                     ["ok you can call me %0 now",
                      "lmao alright you can call me %0 now"]),
            
            message_set(self.empty,
                        ["pog"],
                        ["PogChamp"])]
        
    def get_msgs(self):
        return self.set

    def change_name(self, message):
        
        new_name = message.content.partition("you ")[2]
        
        global name
        
        name = new_name
        
        return [name]
    
    def tell_other(self, message):
        
        split = message.content.partition(":")
        
        person = split[0].partition("tell ")[2]
        
        return [person, message.author.display_name, split[2]]
    
    def empty(self, message):
        
        return [""]

class Ignore:
    
    def __init__(self):
        
        self.ignore = []
        self._load()
        
        self.set = [
            message_set(self.who_are_you_ignoring,
                    ["who are you ignoring"],
                    ["i'm ignoring these ppl rn: %0",
                     "i don't want to listen to these ppl: %0"]),
    
            message_set(self.ignore_start,
                    ["forever ignore "],
                    ["i'm now ignoring %0"]),
    
            message_set(self.ignore_end,
                    ["stop ignoring "],
                    ["if i was ignoring %0 before, i'm not anymore"])]
        
    def get_msgs(self):
        return self.set
        

    def who_are_you_ignoring(self, message):
        
        if (len(self.ignore) == 0): return [None, "i'm not ignoring anyone atm"]
        
        l = "<@" + self.ignore[0] + ">"
        
        for i in range(1, len(self.ignore)):
            
            l += ", <@" + self.ignore[i] + ">"
        
        return [l]
            
    
        
    def ignore_start(self, message):
        
        person = utility.get_ping_id(message.content)
    
        if person is None:
            return [None, "idk who you want me to ignore :("]
        
        if (person == "203483343281455104"):
            return [None, "no i don't wanna ignore Dilan"]
        
        self.add_ignore(person)
        
        return ["<@" + person + ">"]
    
    def ignore_end(self, message):
            
        person = utility.get_ping_id(message.content)
        
        if person is None:
            return [None, "idk who you want me to stop ignoring :("]
        
        if (person == "203483343281455104"):
            return [None, "i'd never ignore Dilan in the first place"]
        
        self.del_ignore(person)
        
        return ["<@" + person + ">"]
        
        
    
    def is_ignored(self, user):
        return user in self.ignore
    
    def add_ignore(self, user):
        self.ignore.append(user)
        self._save()
        
    def del_ignore(self, user):
        if user in self.ignore:
            self.ignore.remove(user)
            self._save()
            
    def _save(self):
        with open("data/ignore.txt", "w") as writer:
            for l in self.ignore:
                writer.write(l + "\n")
            
    def _load(self):
        with open("data/ignore.txt", "r") as reader:
            self.ignore = reader.readlines()
        
        for i in range(len(self.ignore)):
            
            self.ignore[i] = self.ignore[i].replace("\n", "")
    

class Remember:
    
    def __init__(self):
        
        self._data = {}
        self._load()
        
        self.set2 = [
            message_set(self.hello,
                    ["hello", "hi", "sup", "hey", "say hi to "],
                    ["umm hi %0",
                     "oh hello there %0",
                     "hi %0!!",
                     "hello %0!!",
                     "hey %0! how are you?",
                     "hi %0! how are you doing?",
                     "hello %0. how are you?"])
            
            ]
        
        self.set = [
            message_set(self.all_remember,
                        ["who all do you remember", "who do you remember", "who all do you know"],
                        ["here are the names of everyone i remember: %0 i'd love to meet more people (just tell me to remember your name)!",
                         "i remember these people: %0 i'd love to meet more people though (just tell me to remember your name)!",
                         "here are all the people i know: %0 i'd love to meet more people (just tell me to remember your name)!"]),
            message_set(self.new,
                        ["remember my name is ", "remember that my name is ", "my name is "],
                        ["okay %0! i'll remember you.",
                         "nice to meet you %0! i'll remember you now."]),
            message_set(self.pronouns,
                        ["remember my pronouns are ", "remember that my pronouns are "],
                        ["thanks! i know how to refer to you now.",
                         "okay got it."]),
            message_set(self.talk_about_all,
                        ["tell me about everyone"],
                        ["%0"]),
            message_set(self.talk_about_me,
                        ["tell me about myself"],
                        ["ofc! here's what i know about you, %0: %1"]),
            message_set(self.talk_about_you,
                        ["tell me about yourself"],
                        ["there isn't really to say much about me, %0. i'm a discord bot lmaoo. i do like talking to you though :)",
                         "hmm tbh idrk. i'm a discord bot who likes talking to people, especially you %0 :)",
                         "i like talking to ppl, like you, %0, as well as giving them helpful information. other than that i'm just a little discord bot :)"]),
            message_set(self.talk_about_me,
                        ["do you remember me"],
                        ["ofc i do! here's what i know about you, %0: %1",
                         "how could i forget! here's what i know about you, %0: %1"]),
            message_set(self.forget_about_me,
                        ["forget everything about me"],
                        ["it was nice knowing you, %0! i'll forget everything about you as you requested",
                         "well, ig all friendships come to an end. goodbye %0 :'(",
                         "as you request, %0."]),
            message_set(self.talk_about_other,
                        ["tell me about "],
                        ["ooh okay. here's what i know about %0: %1",
                         "oh I remember %2! here's what i know about %0: %1",
                         "how could i forget about %0! here's what i know about %2: %1"]),
            message_set(self.remember,
                        ["remember ", "remember that "],
                        ["okay %0, i'll remember that now.",
                         "cool! i'll remember that.",
                         "okay. i won't forget"]),
            message_set(self.forget,
                        ["forget ", "forget that "],
                        ["forget what :)",
                         "okay %0, i'll forget about that."]),
            message_set(self.what_is_my,
                        ["what is my ", "what are my "],
                        ["oh i know! %0",
                         "here's what i know: %0"]),
            message_set(self.what_do_i,
                        ["what do i "],
                        ["oh i know! %0",
                         "here's what i know: %0"]),
            message_set(self.what_is_other,
                        ["what is ", "what are "],
                        ["ooh i know this about %0: %1",
                         "%0 told me this earlier: %1",
                         "this is what i know about %0: %1"]),
            message_set(self.what_does_other,
                        ["what does "],
                        ["ooh i know this about %0: %1",
                         "%0 told me this earlier: %1",
                         "this is what i know about %0: %1"]),
            ]
        
    def _load(self):
        
        _, _, files = next(os.walk("data/profiles"))
        
        for f in files:
            
            if not f.endswith(".txt"): continue
            
            number = f[0:len(f) - 4]
            
            with open("data/profiles/" + f, "r") as reader:
                
                lines = reader.readlines()
                
            name = lines[0].replace("\n", "")
            
            pronouns = eval(lines[1].replace("\n", ""))
            
            prof = profile_set(name, number, pronouns)
            
            for i in range(2, len(lines)):
                prof.load_data(lines[i])
                
            self._data[number] = prof
            
    
            
    def get_msgs(self):
        return self.set
    
    def get_msgs2(self):
        return self.set2
    
    def hello(self, message):
        
        global name
        
        if str(message.author.id) not in self._data:
            
            return [None, "oh hello there! i'm " + name + "! i'm not sure who you are but you should tell me your name so i remember."]
        
        your_name = self._data[str(message.author.id)].get_name()
        
        return [your_name]
        
    
    def new(self, message):
        
        if str(message.author.id) in self._data:
            
            name = self._data[str(message.author.id)].get_name()
            
            return [None, "i already remember you as " + name]
        
        name = message.content.partition("my name is ")[2].strip()
        
        if " " in name: name = name.split(" ")[0]
        
        
        ps = profile_set(name, str(message.author.id), ["they", "them", "their", "are"])
        ps.save()
        self._data[str(message.author.id)] = ps 
        
        return [name]
    
    def pronouns(self, message):
        
        if str(message.author.id) not in self._data:
            
            return [None, "oh no i don't know your name. you'll have to let me remember that before i can remember other stuff about you."]
        
        msg = message.content.partition("my pronouns are ")[2].strip()
        
        if " " in msg: msg = msg.split(" ")[0]
        
        ans = self._data[str(message.author.id)].set_pronouns(msg)
        
        if not ans:
            return [None, "sorry, but i don't know what you mean. your pronouns need to be typed like subject/object/possession. for example: they/them/their, she/her/her, he/him/his"]
        
        return [""]
        
    def remember(self, message):
        
        if str(message.author.id) not in self._data:
            
            return [None, "oh no i don't know your name. you'll have to let me remember that before i can remember other stuff about you."]
            
        msg = message.content.partition("remember ")[2]
        
        if msg.startswith("that"): msg = msg.partition("that")[2].strip()
        
        msg = msg.replace(".", "").replace("!", "")
            
        ans = self._data[str(message.author.id)].add_new_data(msg)
        
        if not ans:
            
            return [None, "hmm i already know that."]
        
        return [self._data[str(message.author.id)].get_name()]
    
    def forget(self, message):
        
        if str(message.author.id) not in self._data:
            
            return [None, "oh no i don't know your name. you'll have to let me remember that before i can remember other stuff about you."]
            
        msg = message.content.partition("forget ")[2]
        
        if msg.startswith("that"): msg = msg.partition("that")[2].strip()
        
        msg = msg.replace(".", "").replace("!", "")
            
        ans = self._data[str(message.author.id)].del_data(msg)
        
        if not ans:
            
            return [None, "i can't forget something about you that i didn't know"]
        
        return [self._data[str(message.author.id)].get_name()]
    
    def what_is_my(self, message):
        
        return self._what_i(message, " my ")
    
    def what_do_i(self, message):
        
        return self._what_i(message, " i ")
    
    def _what_i(self, message, split_type):
        
        if str(message.author.id) not in self._data:
            
            return [None, "i'm afraid that i don't know who you are. you'll have to let me remember your name first."]
        
        st = message.content.partition(split_type)[2]
        if (st.strip() in ["name", "name?"]): return ["your name is " + self._data[str(message.author.id)].get_name()]
        else: info = self._data[str(message.author.id)].find(message.content.partition(split_type)[2], True)
        
        if info is None:
            
            return [None, "i don't know :( but you should tell me."]
        
        return [info]
    
    def what_is_other(self, message):
        
        if "what is " in message.content:
            ind = "what is "
        else:
            ind = "what are "
            
        first_part = message.content.split(ind)[1]
        if "'s " not in message.content: return None
        who = first_part.split("'s ")[0]
        msg = first_part.split("'s ")[1].replace("?", "")
        
        return self._what_other(who, msg)

    def what_does_other(self, message):
        
        first_part = message.content.split("what does ")[1]
        if " " not in message.content: return None
        who = first_part.split(" ")[0]
        msg = first_part.split(" ")[1].replace("?", "")
        
        return self._what_other(who, msg)
        
    def _what_other(self, who, msg):
        
        for d in self._data.values():
            
            if d.get_name() == who:
                
                ans = d.find(msg, False)
                if ans is None:
                    return [None, "i know " + d.get_name() + " but i don't know " + d.get_pronouns()[2] + " " + msg + " :("]
                
                return [d.get_name(), ans]
                
        return [None, "i don't know who you're talking about :("]
    
    def talk_about_me(self, message):
        
        if str(message.author.id) not in self._data:
            
            return [None, "aww i don't remember you, sorry! i'd love to hear about you though :)"]
        
        info = self._data[str(message.author.id)]
        lines = info.get_all_format(True)
        
        if lines is None:
            
            return [None, "i remember you but i don't know much about you."]
        
        st = lines[0]
        
        for i in range(1, len(lines)):
            
            if i == len(lines) - 1:
                
                st += ", and " + lines[i] + "."
            
            else:
                
                st += ", " + lines[i]
        
        return [info.get_name(), st]
    
    def talk_about_you(self, message):
        
        
        if str(message.author.id) not in self._data:
            
            return [None, "you first! what's your name?"]
        
        your_name = self._data[str(message.author.id)].get_name()
        
        return [your_name]
    
    def talk_about_other(self, message):
        
        who = message.content.split("tell me about ")[1]
        
        for d in self._data.values():
            
            if d.get_name() == who:
                
                lines = d.get_all_format(False)
                
                if lines is None:
                    
                    return [None, "i know " + d.get_name() + " but i don't know anything about " + d.get_pronouns()[1] + " :("]
                
                st = lines[0]
                
                for i in range(1, len(lines)):
                    
                    if i == len(lines) - 1:
                        
                        st += ", and " + lines[i] + "."
                    
                    else:
                        
                        st += ", " + lines[i]
                
                return [d.get_name(), st, d.get_pronouns()[1]]
                
        return [None, "i don't know who you're talking about :("]
    
    def talk_about_all(self, message):
        
        st = "here's everyone ik:"
        
        nws = []
        
        for d in self._data.values():
            
            lines = d.get_all_format(False)
            
            if lines is None:
                
                nws.append(d.get_name())
                continue
            
            st2 = lines[0]
                
            for i in range(1, len(lines)):
                
                if i == len(lines) - 1:
                    
                    st2 += ", and " + lines[i] + "."
                
                else:
                    
                    st2 += ", " + lines[i]
                    
            pron = d.get_pronouns()
            st += "\n\n**" + d.get_name() + "** *" + "(" + pron[0] + "/" + pron[1] + "/" + pron[2] + ")*\n" + st2
            
        if (len(nws) > 0):
            
            st3 = nws[0]
            
            if len(nws) == 2:
                st3 += " and " + nws[1]
            else:
                for i in range(2, len(nws)):
                    
                    if i == len(nws) - 1:
                        st3 += ", and " + nws[i]
                    else:
                        st3 += ", " + nws[i]
                
        st += "\n\ni also know " + st3 + " but i don't really know anything about them."
        
        return [st]
            
    
    def all_remember(self, message):
        
        if len(self._data.values()) == 0:
            return [None, "i don't know anyone :'("]
        
        val = list(self._data.values())
        
        st = val[0].get_name()
        
        for i in range(1, len(val)):
            
            if i == len(val) - 1:
                
                st += ", and " + val[i].get_name() + "."
                
            else:
                
                st += ", " + val[i].get_name()
                
        return [st]
    
    def forget_about_me(self, message):
        
        if str(message.author.id) not in self._data:
            
            return [None, "i can't forget about someone i don't know xD"]
        
        name = self._data[str(message.author.id)].get_name()

        self._data[str(message.author.id)].forget()
        
        del self._data[str(message.author.id)]
        
        return [name]
    
    
class Mathematics:
    
    def __init__(self):
        
        self.set = [
            message_set(self.evaluate_math,
                        [" math: ",
                         "evaluate the following mathematical expression: ",
                         "do my math hw: ",
                         "do my math homework: "],
                        ["good thing i'm a genius. here's what i got: %0",
                         "here's the answer: %0",
                         "i have evaluated a solution: %0",
                         "da math is done: %0"])
            
            ]
        
    def get_msgs(self):
        return self.set
    
    def evaluate_math(self, message):
        
        msg = message.content.partition(": ")[2]
        
        try: ans = cexprtk.evaluate_expression(msg, {})
        except:
            return [None, "sorry i don't understand that math expression :("]
        

        return [str(ans)]

class Northwestern:
    
    def __init__(self):
        
        self.set = [
            message_set(self.get_course_desc,
                        [" course: "],
                        ["ooh okay got it. here's a bit about %0 %1:\n\n**%2**\n%3",
                         "i found the course description for %0 %1:\n\n**%2**\n%3",
                         "here's info on %0 %1:\n\n**%2**\n%3"]),
            message_set(self.get_covid_info,
                        ["covid like",
                         "covid is like",
                         "covid cases",
                         "covid-19 like",
                         "covid-19 is like",
                         "covid-19 cases",
                         "covid positivity rate",
                         "coronavirus like",
                         "coronavirus is like",
                         "coronavirus cases",
                         "coronavirus positivity rate"],
                        ["hmm, it's %0. the positivity rate atm is %1, with %2 positive cases out of %3 in the past 7 days. " + 
                            "since august 20, there have been %5 tests, %6 of which were positive.",
                        "ooh good question. just checked and it's %0 rn. the positivity rate is %1, with %2 positive cases out of %3 in the past week. " +
                            "since august 20, there have been %5 tests, %6 of which were positive.",
                        "well, it's %0. the positivity rate is %1, with %2 positive cases out of %3 in the past 7 days. " +
                            "since august 20, there have been %5 tests, %6 of which were positive."])
            ]
        
        pass
    
    def get_msgs(self):
        return self.set
    
    def get_covid_info(self, message):
        
        try:
            
            page = urllib.request.urlopen("https://www.northwestern.edu/coronavirus-covid-19-updates/university-status/dashboard/index.html")
            soup = BeautifulSoup(page, 'html.parser')
            
            blocks = soup.find_all("div", {"class": "stats-callout"})[0].find_all("div")
            
            info = []
            
            for block in blocks:
                
                data = block.find_all("div", {"class": "big"})
                
                if len(data) == 0: continue
                
                info.append(data[0].text)
            
            pos = float(info[0].replace("%", ""))
            
            if pos <= 1:
                msg = "not too bad"
            elif pos <= 5 and pos > 1:
                msg = "not good"
            else:
                msg = "pretty bad"
                
            info.insert(0, msg)
            
            return info
            
        except:
            return [None, "for some reason i can't get the covid-19 info, sorry :("]
        
    
    def get_course_desc(self, message):
        
        msg = message.content.partition("course: ")[2]
        data = msg.split(" ")
        
        if len(data) < 2:
            return [None, "hmm i don't understand your request. make sure you specify the course subject and number"]
        
        sq = msg.partition(" ")[2]
                
        data = self._convert(data[0], data[1])
        
        found = []
        
        exact = False
        
        try:
            int(data[1].replace("-", ""))
            exact = True
            if "-" not in data[1]: data[1] += "-0"
        except:
            exact = False
        
        try:
            page = urllib.request.urlopen("https://catalogs.northwestern.edu/undergraduate/courses-az/" + data[0] + "/index.html")
            soup = BeautifulSoup(page, 'html.parser')
            
            blocks = soup.find_all("div", {"class": "courseblock"})
            
            for block in blocks:
            
                title = block.find_all("strong")
                if title is None: continue
                
                title = title[0].text.replace("\xa0", " ")
                
                if exact:
                    
                    number = title.split(" ")[1]
                    
                    if number == data[1]:
                    
                        name = title.partition(number + " ")[2].replace("\xa0", "")
                        
                        desc = "*Unable to find the course description*"
                        desc_find = block.find_all("p", {"class": "courseblockdesc"})
                        
                        if len(desc_find) > 0:
                            desc = desc_find[0].text
                        else:
                            desc_find = block.find_all("span", {"class": "courseblockdesc"})
                            if len(desc_find) > 0:
                                desc = desc_find[0].text
                        
                        extra = ""
                        extra_find = block.find_all("p", {"class": "courseblockextra"})
                        
                        if (len(extra_find) > 0):
                            extra = extra_find[0].text
                        else:
                            extra_find = block.find_all("span", {"class": "courseblockextra"})
                            if (len(extra_find) > 0):
                                extra = extra_find[0].text
                            
                        desc = desc.replace("\xa0", " ").replace("\n", "")
                        extra = " \n*" + extra.replace("\xa0", " ").replace("\n", "") + "*"
                            
                        desc += extra
                        
                        return [data[0], number, name, desc]
             
                else:
                    
                    if sq in title.lower():
                        
                        title_split = title.split(" ")
                        subj_number = title_split[0] + " " + title_split[1]
                        name = title.partition(subj_number + " ")[2]
                        
                        found.append("**" + subj_number.lower() + "** " + name)
                        
                    
                            
            if len(found) == 0: return [None, "i couldn't find the class you're looking for :("]
            
            st = "you didn't give me an exact course number to work with, but here's everything i found close to what you asked for:\n"
            
            for l in found:
                st += "\n" + l
                
            st += "\n\nlet me know if you want a description for any of them by providing me with the course number when you search."
            return [None, st]
            
        except:
            return [None, "hmm, i couldn't find what you're looking for."]
        
    def _convert(self, name, number):
        
        if name == "cs":
            return ["comp_sci", number]
        
        if name == "ea":
            return ["gen_eng", "205-" + str(number)]
        
        if name == "dtc":
            return ["dsgn", "106-" + str(number)]
        
        return [name, number]
    
class Definitions:
    
    def __init__(self):
        
        self.set = [
            message_set(self.get_definition,
                        ["what does & mean"],
                        ["here's what i found for %0 (%1):\n%2"]),
            message_set(self.get_synonyms,
                        ["a synonym for ",
                         "another word for "],
                        ["ooh here are some synonyms for %0:\n%1",
                         "i found some other words for %0:\n%1"]),
            message_set(self.get_antonyms,
                        ["the opposite of "],
                        ["here are some antonyms for %0:\n%1",
                         "i found these antonyms for %0:\n%1"])
            ]
        
    def get_msgs(self):
        return self.set
    
    def get_synonyms(self, message):
        
        text = message.content.partition(" for ")[2].replace("?", "")
        word = text.replace(" ", "%20")
        
        with urllib.request.urlopen("https://www.dictionaryapi.com/api/v3/references/thesaurus/json/" + word + "?key=" + key_merriamwebstertheskey) as url:
            data = json.loads(url.read().decode())
        
        if len(data) == 0:
            return [None, "i'm sorry, i couldn't find any synonyms for that word."]
        
        if type(data[0]) == dict:
            syns = data[0]["meta"]["syns"]
            
            if len(syns) == 0:
                return [None, "i couldn't find any synonyms for that word."]
            
            syn = ""
            
            if len(syns) == 1:
                
                syns = syns[0]
                
                syn = "\n" + syns[0]
                
                for i in range(len(syns)):
                
                    syn += ", " + syns[i]
                
            else:
                
                for x in range(len(syns)):
                    
                    syn += "\n" + str(x + 1) + ". " + syns[x][0]
                    
                    
                    for i in range(len(syns[x])):
                
                        syn += ", " + syns[x][i]
            
            return [text, syn]
        
        st = data[0]
        
        for i in range(1, len(data)):
            st += ", " + data[i]
        
        return [None, "i couldn't find that word specifically, but here are some words that are close: " + st]
        
    def get_antonyms(self, message):
        
        text = message.content.partition(" of ")[2].replace("?", "")
        word = text.replace(" ", "%20")
        
        with urllib.request.urlopen("https://www.dictionaryapi.com/api/v3/references/thesaurus/json/" + word + "?key=" + key_merriamwebstertheskey) as url:
            data = json.loads(url.read().decode())
        
        if len(data) == 0:
            return [None, "i'm sorry, i couldn't find any antonyms for that word."]
        
        if type(data[0]) == dict:
            ants = data[0]["meta"]["ants"]
            
            ant = ""
            
            if len(ants) == 1:
                
                ants = ants[0]
                
                ant = "\n" + ants[0]
                
                for i in range(len(ants)):
                
                    ant += ", " + ants[i]
                
            else:
                
                for x in range(len(ants)):
                    
                    ant += "\n" + str(x + 1) + ". " + ants[x][0]
                    
                    
                    for i in range(len(ants[x])):
                
                        ant += ", " + ants[x][i]
            
            return [text, ant]
        
        st = data[0]
        
        for i in range(1, len(data)):
            st += ", " + data[i]
        
        return [None, "i couldn't find that word specifically, but here are some words that are close: " + st]
        
    def get_definition(self, message):
        
        text = message.content.partition("does ")[2].partition(" mean")[0]
        word = text.replace(" ", "%20")
        
        with urllib.request.urlopen("https://www.dictionaryapi.com/api/v3/references/collegiate/json/" + word + "?key=" + key_merriamwebsterdictkey) as url:
            data = json.loads(url.read().decode())
        
        
        if len(data) == 0:
            return [None, "i'm sorry, i couldn't find what that word means!"]
        
        if type(data[0]) == dict:
            word_type = data[0]["fl"]
            word_defs = data[0]["shortdef"]
            
            if len(word_defs) == 0:
                return [None, "i couldn't find a good definition for that word."]
            
            word_def = ""
            
            if len(word_defs) == 1:
                word_def = "\n" + word_defs[0]
            else:
                
                for i in range(len(word_defs)):
                    
                    word_def += "\n" + str(i + 1) + ". " + word_defs[i]
            
            
            return [text, word_type, word_def]
        
        st = data[0]
        
        for i in range(1, len(data)):
            st += ", " + data[i]
        
        return [None, "i couldn't find that word specifically, but here are some words that are close: " + st]
            
            
        
    

def add_message_set(init):
    
    for i in init:
        sets.append(i)

basics = Basics()
ignore = Ignore()
remember = Remember()
mathematics = Mathematics()
northwestern = Northwestern()
definitions = Definitions()

whitelist = ["Blockhead7360#5000"]

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if ignore.is_ignored(str(message.author.id)): return
    
    message.content = message.content.lower()
    
    if name in message.content:
        
        if dev:
            
            if str(message.author) not in whitelist:
                await message.channel.send("aww sorry i can't respond rn. i'm in developer mode.")
                return
            
        history(message)
            
        if message.content.startswith(name + " /"):
            
            cmd = message.content.partition(name + " /")[2]
            
            if cmd == "version":
                await message.channel.send(VERSION)
                return
            
            if cmd.startswith("forcesend "):
                
                if str(message.author) in whitelist:

                    await message.channel.send(cmd.partition("forcesend ")[2])
                    return
                
                else:
                    await message.channel.send("you aren't whitelisted to use /forcesend.")
                    return
                
            if cmd.startswith("spd "):
                
                if str(message.author) in whitelist:
                    
                    split = cmd.partition("spd ")[2].split(" ")
                    
                    if len(split) != 2:
                        await message.channel.send("fail.")
                        return
                    
                    spd.add_to_map(split[0], split[1])
                    
                    await message.channel.send("updated subject pronoun dictionary: " + split[0] + " -> " + split[1])
                    return
                
                else:
                    await message.channel.send("you aren't whitelisted to use /spd.")
                    return
        
        for s in sets:
            
            if s.should_activate(message.content):
                val = s.call_function(message)
                if val is not None:
                    
                    if val[0] is None:
                        
                        msg = val[1]
                    
                    else:
                        
                        msg = s.random_message()
                    
                    if "@everyone" in msg or "@here" in msg:
                        await message.channel.send("Don't force gamer bot to ping everyone :(")
                    else:
                        await message.channel.send(msg)

                return
                
@client.event
async def on_ready():
    listening = discord.Activity(type=discord.ActivityType.listening, name="gamer music")
    await client.change_presence(activity=listening)
    
def history(message):
    
    
    
    with open("data/history/" + str(message.author.id) + ".txt", "a") as writer:
            writer.write("[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") \
                         + "] [" + str(message.channel.id) + "] " + message.content + "\n")

add_message_set(ignore.get_msgs())
add_message_set(definitions.get_msgs())
add_message_set(northwestern.get_msgs())
add_message_set(remember.get_msgs())
add_message_set(mathematics.get_msgs())
add_message_set(basics.get_msgs())
add_message_set(remember.get_msgs2())
       

# lmao no i'm not letting the bot token appear on github
client.run(key_discordtoken)


