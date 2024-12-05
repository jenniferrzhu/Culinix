from textx import metamodel_from_file
culinix_mm = metamodel_from_file('culinix.tx')

culinix_model = culinix_mm.model_from_file('practice1.cx')

class Recipe:

    def __init__(self):
        self.recipes = {
            "PBJ Sandwich": ["bread", "peanut butter", "jelly", "bread"]
        } 

        self.var = {}
    
    def cook(self, item):   
        item = [itm.lower() for itm in item]
        for name, ingredients in self.recipes.items(): 
            ingredients = [itm.lower() for itm in ingredients]
            if item == ingredients:
                return name
        return None

    def find(self, item):
        found = []  
        for name, ingredients in self.recipes.items():
            ingredients = [itm.lower() for itm in ingredients]
            if item in ingredients:   
                found.append(name)
        if not found:
            return None
        else:
            return found


    def interpret(self, model): 
        for c in model.load:
            self.var[c.name] = c.ingredients 
            print(f"Added {c.name}")
        for c in model.actions:  
            if c.__class__.__name__ == "Mix":   
                self.var[c.name] = c.ingredients 
                print(f"Mix {self.var}")
            elif c.__class__.__name__ == "Cook":
                print(f"...mixing ingredients together...cooking...")
                dish = self.cook(self.var[c.item])
                self.var[c.item] = dish
                if dish is not None:
                    print(f"--COOKING DONE--")
                else:
                    print(f"PAUSE: Incorrect Ingredients. No Dish Found.")
            elif c.__class__.__name__ == "Serve":
                dish = self.var[c.item] 
                if dish is None:
                    print("Error: Failed to Cook")
                else:
                    print(f"Serving {dish}!")
            elif c.__class__.__name__ == "Add":
                self.recipes[c.result.capitalize()] = c.ingredients
                print(f"Added {c.result.capitalize()} to the Recipe Book")
            elif c.__class__.__name__ == "Find": 
                if c.action == "ingredients":
                    if self.recipes.get(c.key) is not None:
                        print(f"{c.key}: {self.recipes[c.key]}")
                    else:
                        print(f"PAUSE: Recipe Not Found")
                else:
                    if self.find(c.key) is None:
                        print(f"PAUSE: No Matches Found")
                    else:
                        print(f"Recipes with {c.key}: {self.find(c.key)}")
            elif c.__class__.__name__ == "View": 
                if c.key == "all":
                    print(f"{self.recipes}")
                elif self.recipes.get(c.key.capitalize()) is not None:
                    print(f"Recipe for {c.key.capitalize()}: {self.recipes[c.key.capitalize()]}")
                else:
                    print(f"PAUSE: No Recipe(s) Found")
            else:
                print(f"Error: Incorrect Syntax")

recipe = Recipe()
recipe.interpret(culinix_model)
