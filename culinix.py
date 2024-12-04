from textx import metamodel_from_file
culinix_mm = metamodel_from_file('culinix.tx')

culinix_model = culinix_mm.model_from_file('practice1.cx')

class Recipe:

    def __init__(self):
        self.recipes = {

        } 

    def interpret(self, model): 
        for c in model.actions: 
            if c.__class__.__name__ == "Mix":
                print(f"Mix")
            elif c.__class__.__name__ == "Cook":
                print(f"Cook")
            elif c.__class__.__name__ == "Serve":
                print(f"Serve")
            elif c.__class__.__name__ == "Add":
                print(f"Add")
            else:
                print(f"FindIngredients")

recipe = Recipe()
recipe.interpret(culinix_model)
