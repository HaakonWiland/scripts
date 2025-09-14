import pwn 

level_rank = {}
p = pwn.process(["/challenge/run"])

# Rules prompt 
init_prompt = p.recvuntil(b"):").decode()
print(init_prompt)

# Levels 
level_prompt = p.recvuntil(b"5").decode("utf-8")
level_list = level_prompt.split("\n")[1:-1]
print(level_list)

i = 40
for level in level_list:
    level_rank[level] = i
    i -= 1

print(level_rank)

def parse_question(question: str) -> dict:
    subject_part, object_part = question.split(" an Object with")
    # print(f"Subject: {subject_part} \nObject: {object_part}")

    # Parse subject
    s_level = subject_part.split("level")[1].split("and")[0].strip()
    s_categories = subject_part.split("categories")[1].split("}")[0].strip(" {")
    action = subject_part.split("}")[1].strip()

    # print(f"s_categories: {type(s_categories)}")
    # Parse object 
    o_level = object_part.split("level")[1].split("and")[0].strip()
    o_categories = object_part.split("categories")[1].strip("{ }? ")

    summary = {
        "s_level" : s_level,
        "s_categories" : s_categories,
        "action" : action,
        "o_level" : o_level,
        "o_categories": o_categories
    }

    return summary


def answer_questions(summary: dict):
    # print(f"from answer_question: {summary}")

    s_level = summary["s_level"]
    s_categories = set(summary["s_categories"].split(", "))
    action = summary["action"]
    o_level = summary["o_level"]
    o_categories = set(summary["o_categories"].split(", "))

    s_categories.add('')
    o_categories.add('')

    print(f"s_categories: {s_categories} \no_categories: {o_categories}")

    match action:
        case "write":
            if level_rank[s_level] <= level_rank[o_level] and s_categories <= o_categories:
                answer: str = b"yes"
            else:
                answer: str = b"no"
            
            print(answer)

        case "read":
            if level_rank[s_level] >= level_rank[o_level] and o_categories <= s_categories:
                answer: str = b"yes"
            else:
                answer: str = b"no"
            
            print(answer)

    p.sendline(answer)

# Questions 
for i in range(128):
    question = p.recvuntil(b"?").decode().strip()
    print(question)

    parsed_question : dict  = parse_question(question)
    answer_questions(parsed_question)

    feedback = p.recvuntil(b"!")
    print(feedback)

# Read the flag
print(p.recvall().decode())

