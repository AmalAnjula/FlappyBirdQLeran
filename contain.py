
from bot import FlappyBirdQLearningBot
 
# Initialize the bot
myBot = FlappyBirdQLearningBot()

screenWidth = 288
screenHeight = 512
# amount by which base can maximum shift to left
pipGapz = 100  # gap between upper and lower part of pipe
baseY = screenHeight * 0.79
# image, sound and hitmask  dicts
IMAGES, SOUNDS, HITMASKS = {}, {}, {}


newTime=0


start_time=0
# list of all possible players (tuple of 3 positions of flap)
birdModels = (
    # red bird
    (
        "data/assets/sprites/redbird-upflap.png",
        "data/assets/sprites/redbird-midflap.png",
        "data/assets/sprites/redbird-downflap.png",
    ),
    # blue bird
    (
        # amount by which base can maximum shift to left
        "data/assets/sprites/bluebird-upflap.png",
        "data/assets/sprites/bluebird-midflap.png",
        "data/assets/sprites/bluebird-downflap.png",
    ),
    # yellow bird
    (
        "data/assets/sprites/yellowbird-upflap.png",
        "data/assets/sprites/yellowbird-midflap.png",
        "data/assets/sprites/yellowbird-downflap.png",
    ),
)

# list of backgrounds
backGroundList = (
    "data/assets/sprites/background-day.png",
    "data/assets/sprites/background-night.png",
)

# list of pipes
pipeList = ("data/assets/sprites/pipe-green.png", "data/assets/sprites/pipe-red.png")

