TIME_UNIT = 1
COOKS = [{"name": "Bob Monkhouse", 
          "catchphrase": "Bernie, the bolt!", 
          "rank": 1, 
          "proficiency": 1,
          "title": "Line Cook"},
          {"name": "Robby Mouse", 
          "catchphrase": "Bolts and Nuts!", 
          "rank": 1, 
          "proficiency": 1,
          "title": "Line Cook"},
         {"name": "Dick Emery",
          "catchphrase": "Ooh, you are awful ... but I like you!",
          "rank": 2, 
          "proficiency": 2,
          "title": "Saucier"},
         {"name": "Chris Tarrant",
          "catchphrase": "Is that your final answer?",
          "rank": 2,
          "proficiency": 2, 
          "title": "Saucier"},
          {"name": "Christy Wombat",
          "catchphrase": "No catch.",
          "rank": 3,
          "proficiency": 3, 
          "title": "Vice Executive Chef"},
          {"name": "John Torry",
          "catchphrase": "Your answer?",
          "rank": 3,
          "proficiency": 3, 
          "title": "Executive Chef"}]

APPARATUSES = [{"type": "stove", "quantity": 10},
              {"type": "oven", "quantity": 10}]

# docker
DINING_HALL_URL = "http://dining-hall:5000/distribution"

# direct run
#DINING_HALL_URL = "http://localhost:5001/distribution"