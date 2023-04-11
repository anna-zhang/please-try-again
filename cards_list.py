all_card_indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32] # all possible card indices
remaining_card_indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32] # keep track of which cards have already been seen

class Card:
  def __init__(self, id, prompt, rule, input_types, options = None):
    self.id = id # Int: unique identifier for each card
    self.prompt = prompt # String: prompt for content provider
    self.rule = rule # String: rule for moderator
    self.input_types = input_types # list of input types ["text", "image", "date", "color", "password", "email", "radio", "checkbox", "telephone", "time", "textarea", "url", "number"]
    self.options = options # hold checkbox, radio options, if those input types apply for this prompt/rule pair

cards = [
  Card(1, "Describe a dream you had recently.", "It must be at least five sentences long.", ["textarea"]), 
  Card(2, "Describe a childhood memory that makes you smile.", "There can only be a maximum of one sentence that starts with “I…”", ["textarea"]), 
  Card(3, "How are you feeling? Describe with a list of five emotions.", "The following are not allowed: happy, sad, angry, tired, stressed", ["text"]), 
  Card(4, "Write a fictional story about a person who defeats monsters.", "It must begin with “Once upon a time…”", ["textarea"]), 
  Card(5, "Share a country that you want to visit.", "The country must start with the letter C.", ["text"]), 
  Card(6, "Share a photo that makes you happy.", "There must be a person in the photo.", ["image"]), 
  Card(7, "Share a photo of a place you've been to. ", "The photo must be in black and white.", ["image"]), 
  Card(8, "Share a photo from a day with nice weather.", "It must be a photo of a sunset or sunrise.", ["image"]), 
  Card(9, "Share a photo of an activity that you did this weekend.", "It must be a nighttime photo.", ["image"]), 
  Card(10, "Describe a dream you had.", "One word must be mispelled.", ["textarea"]), 
  Card(11, "Give a recipe with ingredients and steps.", "It must not have eggs or flour on the list of ingredients.", ["textarea"]), 
  Card(12, "Describe a recent trip you had. Where did you go? How did you get there?", "It must include a mode of transportation. It cannot include plane or car (flying, driving). Acceptable answers include walking/by foot, train, and bike.", ["textarea"]), 
  Card(13, "Where do you see yourself in the future?", "It must be an interior space.", ["image"]), 
  Card(14, "Share a website that you love.", "It must be a URL that does not end with “.com”", ["url"]), 
  Card(15, "What is an event that you're looking forward to?", "The date must be six months from now.", ["text", "date"]), 
  Card(16, "What do you want to try?", "Can only select one of the options.", ["checkbox"], ["sky diving", "eating 100 hot dogs", "giving my loved one flowers", "backflipping on cross campus"]), 
  Card(17, "What would you name your next car?", "The name must be 3-4 letters long.", ["text"]),
  Card(18, "Describe something you don't know that you're interested in learning more about.", "Must include the “?” character.", ["textarea"]),
  Card(19, "Come up with a strong password.", "The number of letter characters and numbers have to equal each other.", ["password"]),
  Card(20, "What is your lucky color?", "The color must be black or white.", ["color"]),
  Card(21, "Describe a memorable moment in your life.", "The associated date input has to be from at least five years ago.", ["date", "textarea"]),
  Card(22, "Write a letter to your oldest friend.", "The letter must start with “Dear”", ["textarea"]),
  Card(23, "What's your workout routine?", "It must include numerical values.", ["textarea"]),
  Card(24, "You're registering for a dating website. What's your email?", "The email must not have a generic domain (e.g., @gmail.com, @yahoo.com, @outlook.com, @icloud.com, @hotmail.com).", ["email"]),
  Card(25, "What's your pro wrestling name?", "The name must be in ALL CAPS.", ["text"]),
  Card(26, "Rank these fruits: apple, orange, mango, watermelon, banana", "The order has to be alphabetical by the first letter of the fruit.", ["text"]),
  Card(27, "What types of weather do you enjoy?", "Half of the options must be checked. The other half of the options must remain unchecked.", ["checkbox"], ["rainy", "sunny", "humid", "dry", "misty", "hurricane", "snowy", "cold", "warm", "hot"]),
  Card(28, "Describe silence.", "The input must be empty (left blank).", ["textarea"]),
  Card(29, "What's your favorite animal?", "The animal must live underwater.", ["image"]),
  Card(30, "What's the magic number?", "The answer must be 7.", ["number"]),
  Card(31, "How much wood could a woodchuck chuck if a woodchuck could chuck wood?", "The answer must be a prime number.", ["number"]),
  Card(32, "Come up with a phone number for your pet.", "The digits must all be the same (e.g., 888-888-8888).", ["telephone"]),
  Card(33, "What's your favorite time of the day?", "The time must be in the A.M.", ["time"])
]