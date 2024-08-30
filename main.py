
import os
import json
import base64

class Vault:

    def __init__(self, key):
        os.system("cls")
        self.hash = [int(str(ord(character))[-1]) for character in base64.b64encode(key.encode()).decode()]
        if not os.path.isfile("config.json"):
            with open("config.json", "w") as file:
                file.write(json.dumps({ "id": "".join([str(character) for character in self.hash]), "strength": 20, "names": [] }))
                file.close()
        self.config = json.loads(open("config.json", "r").read())
        if self.config["id"] != "".join([str(character) for character in self.hash]): quit()
        self.start()

    def start(self):
        os.system("cls")
        print("\n  the vault")
        option = input("  select option (create, passwords, quit): ").lower()
        if option == "create":
            key = self.create(input("  account: "))
            if key is None:
                print("\n  account already exists.")
            else:
                print("\n  {}\n  {}".format(key[1], key[0], key[2]))
        elif option == "passwords":
            print("")
            if len(self.config["names"]) > 0:
                for index, name in enumerate(self.config["names"]):
                    print("  [{}] {} (strength: {})".format(index, name[0], name[1]))
                selected = self.config["names"][int(input("\n  >  "))]
                option = input("\n  select option (show, delete): ").lower()
                if option == "show":
                    key = self.generate(selected[0], selected[1])
                    print("\n  {}\n  {}".format(key[1], key[0]))
                elif option == "delete":
                    self.config["names"].remove(selected)
                    open("config.json", "w").write(json.dumps(self.config))
                    print("  {} deleted.".format(selected[0]))
            else: print("  no passwords available.")
        elif option == "quit":
            os.system("cls")
            quit()
        input("\n  press ENTER to continue. ")
        self.start()

    def create(self, name):
        name = "-".join(name.lower().split(" "))
        if name not in [item[0] for item in self.config["names"]]:
            key = self.generate(name, self.config["strength"])
            self.config["names"].append([key[1], key[2]])
            open("config.json", "w").write(json.dumps(self.config))
            return key
        else:
            return None

    def generate(self, name, size):
        result = []
        name = "-".join(name.lower().split(" "))
        characters = "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ1!2@3#4$5%6^7&8*9(0)`~-_=+[{]};:',<.>/?"
        _hash = [[int(str(ord(character))[-2:]) for character in base64.b64encode(name.encode()).decode()], self.hash]
        while len(_hash[0]) < size:
            _hash[0].extend(_hash[0])
        _hash[0][0:size] = _hash[0][0:size]
        while len(_hash[1]) < len(_hash[0]):
            _hash[1].extend(_hash[1])
        result = [character ^ _hash[1][index] for index, character in enumerate(_hash[0])]
        threshold = [max(result, key=lambda value: int(value)), min(result, key=lambda value: int(value))]
        result = [characters[round(((character-threshold[1])/(threshold[0]-threshold[1])) * len(characters))-1] for character in result]
        return ("".join(result), name, size)

if __name__ in "__main__":
    Vault(input("login (password): "))
