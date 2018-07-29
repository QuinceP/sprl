import random
import textwrap
from enum import Enum, auto

from faker import Faker
import tcod.tcod as libtcod

from game_states import GameStates
from random_utils import diceroll


class Gender(Enum):
    FEMALE = auto()
    MALE = auto()


class SkinColor(Enum):
    PALE = auto()
    FAIR = auto()
    MEDIUM = auto()
    OLIVE = auto()
    BROWN = auto()
    BLACK = auto()


def render_character_creation_screen(con, screen_width, screen_height, game_state):
    if game_state == GameStates.CHARACTER_CREATION:
        character_creation = CharacterCreation()
        character_creation.create_character()

        window = libtcod.console_new(screen_width, screen_height)
        libtcod.console_set_default_foreground(window, libtcod.white)
        libtcod.console_set_default_background(window, libtcod.black)

        x = screen_width // 2
        y = screen_height // 2
        libtcod.console_print_frame(window, 0, 0, screen_width, screen_height, True,
                                    libtcod.BKGND_NONE, 'Character Information')
        libtcod.console_print_ex(window, 1, 2, libtcod.BKGND_SET, libtcod.LEFT,
                                 'Name: {0} {1}'.format(character_creation.first_name, character_creation.last_name))
        libtcod.console_print_ex(window, 1, 3, libtcod.BKGND_SET, libtcod.LEFT,
                                 'Gender: {0}'.format(
                                     ("Female" if character_creation.gender == Gender.FEMALE else "Male")))
        libtcod.console_print_ex(window, 1, 4, libtcod.BKGND_SET, libtcod.LEFT,
                                 'Age: {0}'.format(character_creation.age))
        libtcod.console_print_ex(window, 1, 5, libtcod.BKGND_SET, libtcod.LEFT,
                                 'Species: Human')
        libtcod.console_print_ex(window, 1, 6, libtcod.BKGND_SET, libtcod.LEFT,
                                 'Height: {0}'.format(character_creation.get_height_string()))

        description_lines = textwrap.wrap(character_creation.generate_physical_description(), screen_width - 2)
        index = 0
        for line in description_lines:
            libtcod.console_print_ex(window, 1, 8 + index, libtcod.BKGND_SET, libtcod.LEFT,
                                     line)
            index += 1

        personality_description_lines = textwrap.wrap(character_creation.generate_personality_description(),
                                                      screen_width - 2)
        for line in personality_description_lines:
            libtcod.console_print_ex(window, 1, 9 + index, libtcod.BKGND_SET, libtcod.LEFT,
                                     line)
            index += 1

        libtcod.console_print_ex(window, 1, screen_height - 2, libtcod.BKGND_SET, libtcod.LEFT,
                                 "[esc] Cancel")

        libtcod.console_print_ex(window, (screen_width - 2) // 2, screen_height - 2, libtcod.BKGND_SET, libtcod.CENTER,
                                 "[r] Re-Roll Character")

        libtcod.console_print_ex(window, screen_width - 2, screen_height - 2, libtcod.BKGND_SET, libtcod.RIGHT,
                         "[n] New Game")

        libtcod.console_blit(window, 0, 0, screen_width, screen_height, 0, 0, 0)
        libtcod.console_flush()


class CharacterCreation:

    def __init__(self):
        self.first_name = None
        self.last_name = None
        self.gender = None
        self.age = None
        self.height = None
        self.weight = None
        self.skin_color = None
        self.eye_color = None
        self.hair_color = None
        self.emotional_disposition = None
        self.moodiness = None
        self.core_traits = None

    def create_character(self):
        fake = Faker()
        # fake.seed(4321)

        self.first_name = ""
        self.last_name = fake.last_name()
        self.gender = random.choice([Gender.FEMALE, Gender.MALE])
        self.age = random.randint(16, 60)
        self.generate_weight(self.generate_height())
        self.generate_skin_color()
        self.generate_eye_color()
        self.generate_hair_color()
        self.generate_emotional_disposition()
        self.generate_moodiness()
        self.generate_core_traits()

        if self.gender == self.gender.FEMALE:
            self.first_name = fake.first_name_female()
        else:  # gender == gender.MALE
            self.first_name = fake.first_name_male()

    def generate_height(self):
        self.height = 56  # inches
        height_modifier = diceroll(2, 10)
        self.height += height_modifier

        return height_modifier

    def get_height_string(self):
        feet = self.height // 12
        inches = self.height % 12
        meters = "{:.2f}".format(((12 * feet + inches) * 0.0254))

        if inches == 0:
            return "{0}m ({1}')".format(meters, feet)

        return "{0}m ({1}'{2}\")".format(meters, feet, inches)

    def generate_weight(self, height_modifier):
        self.weight = 110  # lbs
        self.weight += diceroll(2, 4) * height_modifier

    def get_weight_string(self):
        kilos = "{:.2f}".format(self.weight * 0.45359237)
        return "{0} kg ({1} lbs)".format(kilos, self.weight)

    def generate_skin_color(self):
        colors = ["pale", "fair", "medium", "olive", "brown", "dark brown"]
        self.skin_color = colors[random.choice([e.value for e in SkinColor]) - 1]

    def generate_eye_color(self):
        colors = [
            "blue",
            "light blue",
            "a darkish blue",
            "blue-grey",
            "grey",
            "blue-gray with yellow and brown flecks",
            "gray-green with yellow and brown flecks",
            "green",
            "green with yellow and brown flecks",
            "light brown with hazel",
            "medium brown",
            "dark brown"
        ]

        self.eye_color = random.choice(colors)
        print(self.eye_color)

    def generate_hair_color(self):
        colors = [
            "black", "salt and pepper", "white", "grey"
        ]

        extra_colors = ["blond", "brown", "red"]

        modifiers = ["dark", "medium", "light"]

        for color in extra_colors:
            colors.append(color)
            for modifier in modifiers:
                colors.append("{0} {1}".format(modifier, color))

        self.hair_color = random.choice(colors)
        print(self.hair_color)
        print("\n")

    def generate_physical_description(self):
        return '{0} has {2} skin. {1} eyes are {3}. {0} has {4} hair. '.format(
            ("She" if self.gender == Gender.FEMALE else "He"),
            ("Her" if self.gender == Gender.FEMALE else "His"),
            self.skin_color,
            self.eye_color,
            self.hair_color)

    def generate_personality_description(self):
        traits = []
        for trait in self.core_traits:
            traits.append(("She" if self.gender == Gender.FEMALE else "He") + " " + trait + ".")

        return '{0} often {1}. {2}'.format(
            ("She" if self.gender == Gender.FEMALE else "He"),
            self.emotional_disposition, " ".join(traits))

    def generate_emotional_disposition(self):
        dispositions = ["is joyful", "has an anxious disposition", "is melancholy", "is curious", "is calm", "is angry",
                        "is condescending to others", "is excited about something",
                        "is apathetic about everything", "looks ashamed"]

        self.emotional_disposition = random.choice(dispositions)

    def generate_moodiness(self):
        moods = ["quick-tempered", "even-tempered", "steady-tempered"]
        self.moodiness = random.choice(moods)

    def generate_core_traits(self):
        outlook = random.choice(["has a hopeful outlook on life", "is pessimistic"])
        integrity = random.choice(["is a person of strong integrity", "often does morally questionable things"])
        impulsiveness = random.choice(["thinks about things before acting", "is impulsive"])
        boldness = random.choice(["is bold", "is cautious"])
        agreeableness = random.choice(["is agreeable", "is disagreeable"])
        interactivity = random.choice(["is engaging in conversation", "is shy and reserved"])
        conformity = random.choice(
            ["is conventional and usually sticks to social norms", "is very unorthodox at times"])

        self.core_traits = [outlook, integrity, impulsiveness, boldness, agreeableness, interactivity, conformity]
