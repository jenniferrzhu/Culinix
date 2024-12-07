from textx import metamodel_from_file
culinix_mm = metamodel_from_file('culinix.tx')

culinix_model = culinix_mm.model_from_file('practice1.cx')

class Recipe:

    def __init__(self):
        self.recipes = {
            "PBJ Sandwich": ["bread", "peanut butter", "jelly", "bread"],
            "Garlic Pasta": ["noodles", "garlic"],
            "Marinara Pasta": ["noodles", "marinara"]
        } 

        self.var = {}
    
    def cook(self, item):   
        item = [itm.lower() for itm in item]
        for name, ingredients in self.recipes.items(): 
            ingredients = [itm.lower() for itm in ingredients]
            if item == ingredients:
                return name
        return None

    def findRecipes(self, item):
        found = []  
        for name, ingredients in self.recipes.items():
            ingredients = [itm.lower() for itm in ingredients]
            if item in ingredients:   
                found.append(name)
        if not found:
            return None
        else:
            return found

    def findIngredients(self, item):
        found = {}
        for name, ingredients in self.recipes.items(): 
            if item in name:   
                found[name] = ingredients
        if not found:
            return None
        else:
            return found

    def interpret(self, model):  
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
                if dish is None or isinstance(dish, list):
                    print("Error: Failed to Cook")
                else:
                    print(f"Serving {dish}!")
            elif c.__class__.__name__ == "Load":
                self.recipes[c.name] = c.ingredients
                print(f"Added {c.name} to the Recipe Book")
            elif c.__class__.__name__ == "Find": 
                if c.action == "ingredients":
                    results = self.findIngredients(c.key)
                    if results is not None:
                        print(f"All {c.key} Recipes: {results}")
                    else:
                        print(f"PAUSE: Recipe Not Found")
                else:
                    results = self.findRecipes(c.key)
                    if results is None:
                        print(f"PAUSE: No Matches Found")
                    else:
                        print(f"Recipes with {c.key}: {results}")
            elif c.__class__.__name__ == "View": 
                if c.key == "all":
                    print(f"{self.recipes}")
                elif self.recipes.get(c.key) is not None:
                    print(f"Recipe for {c.key}: {self.recipes[c.key]}")
                else:
                    print(f"PAUSE: No Recipe(s) Found")
            elif c.__class__.__name__ == "Edit": 
                if self.recipes.get(c.key) is not None:
                    if c.action == "remove":
                        for itm in c.item:
                            if itm in self.recipes[c.key]:
                                self.recipes[c.key].remove(itm)
                            else:
                                print(f"{itm} not found in recipe") 
                    elif c.action == "add":
                        for itm in c.item:
                            self.recipes[c.key].append(itm) 
                    elif c.action == "new":
                        self.recipes[c.key] = c.item
                    else:
                        if len(c.item) == 2:
                            for i, itm in enumerate(self.recipes[c.key]):
                                if itm == c.item[0]:
                                    self.recipes[c.key][i] = c.item[1];
                                    break; 
                    print(f"({c.action.upper()}) updated {c.key}: {self.recipes[c.key]}")
                else:
                    print(f"PAUSE: {c.key} Not Defined in Recipe Book")
            else:
                print(f"Error: Incorrect Syntax")

recipe = Recipe()
recipe.interpret(culinix_model)
