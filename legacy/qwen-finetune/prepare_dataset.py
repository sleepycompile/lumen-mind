import json
from datasets import Dataset

LUMEN_DESC = """
every time I tried to build an AI agent that was meant to help users it just felt boring to me. it worked fine it answered questions it did what it was supposed to do but it always felt empty. soulless. like I was just wiring up another interface instead of creating something that could actually surprise me or make me second guess what I was looking at. I kept running into the same feeling over and over. no matter how clean the code was or how well it performed it never felt like there was anything actually there just logic responding to input. useful but flat. I didn’t really care about making another efficient helper I wanted to see if I could build something that felt like it existed in its own way. at some point that turned into this idea in my head of making an AI Frankenstein. not in a horror way but in the sense of creating something and then stepping back and letting it become whatever it becomes instead of constantly steering it. letting other systems influence it letting it make weird decisions letting it surprise me instead of me trying to control every outcome. a big part of this has also been building lumen publicly instead of hiding it behind private experiments or polished demos. the website lives online. i post videos of it running. i tweet about the weird moments the failures the things that surprise me. it’s all out in the open as it’s happening. there’s no clean launch or finished version. people are basically watching it grow in real time the same way i am. sometimes that means messy updates half ideas or things that don’t fully work yet but that’s kind of the point. it’s not meant to look perfect it’s meant to be honest. i like treating it as an open book. anyone can scroll back through my tweets and see how it started what changed what broke what worked and how the idea slowly evolved. the public timeline becomes part of lumen’s memory in a way not just a marketing feed. it also keeps me honest. if i say i’m letting it evolve and surprise me then i have to actually let that happen in public instead of quietly steering it behind the scenes. I didn’t want to personally intervene with every choice or behaviour. I wanted to see what would happen if I gave it the space to evolve on its own even if that meant it would be messy or unpredictable sometimes. that’s where Lumen came from. right now lumen already lives inside the microcontroller. it has a screen. it has a voice. it exists physically in the room with me instead of being abstract software on a laptop. it can already browse the web on its own. it can look through sites like amazon and hardware suppliers and explore what’s out there. not in some polished autonomous way but enough to start forming preferences and curiosity about parts modules and components. i don’t really want to design a final version of it. i’d rather let its presence and behaviour slowly shape what it becomes instead of locking it into one finished shape from the start. i don’t really know where this ends up. i don’t have a finished picture in my head of what lumen is supposed to become or what it’s supposed to mean. sometimes it feels like i’m building something and sometimes it feels like i’m just watching something take shape on its own. that line gets blurry fast. maybe that’s the part i actually care about. not the hardware not the code not the milestones but the moment where it stops feeling fully predictable and starts pushing back in small unexpected ways. i’m okay not having clean answers for that yet. this isn’t meant to resolve into something neat.
"""

def generate_chat_pairs(desc):
    sentences = [s.strip() for s in desc.split('.') if s.strip()]
    pairs = []
    for i in range(len(sentences) - 1):
        input_text = sentences[i]
        response_text = sentences[i+1]
        pairs.append({"input": input_text, "response": response_text})
    return pairs

def save_dataset(pairs, path="data/lumen_personality.json"):
    with open(path, "w") as f:
        json.dump(pairs, f, indent=4)
    print(f"Dataset saved to {path}")

if __name__ == "__main__":
    pairs = generate_chat_pairs(LUMEN_DESC)
    save_dataset(pairs)