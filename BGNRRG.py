import pyscreenshot
from pymouse import PyMouse
import pytesseract
import os
import argparse as arg
import time
import sys


class Buttons(object):
    def __init__(self, setting_dict):
        try:
            self.reroll = setting_dict["reroll"]
            if len(self.reroll) != 2:
                raise SettingError
            self.store = setting_dict["store"]
            if len(self.store) != 2:
                raise SettingError
            self.recall = setting_dict["recall"]
            if len(self.recall) !=2:
                raise SettingError
            self.total_roll = setting_dict["total_roll"]
            if len(self.total_roll) != 4:
                raise SettingError
        except (KeyError, SettingError):
            print("Setting incomplete or badly formatted.")
            sys.exit()


class SettingError(Exception):
    pass


def read_setting():
    setting_dict = {}
    with open("config.txt", "rU") as setting_file:
        for line in setting_file:
            line = line.rstrip("\n").split(" ")
            setting_dict[line[0]] = tuple(map(int, line[1:]))
    return(setting_dict)


def create_setting():
    """
    Create setting dict by prompting user to hover mouse over
    required positions and pressing enter.
    """
    mouse = PyMouse()
    setting_dict = {}
    print(("Initializing buttons:\n"
           "Hover mouse over required button and press enter."))
    raw_input("Hover over reroll button:")
    setting_dict["reroll"] = mouse.position()
    print "reroll initialized at: ", setting_dict["reroll"]
    raw_input("Hover over recall button:")
    setting_dict["recall"] = mouse.position()
    print "recall initialized at: ", setting_dict["recall"]
    raw_input("Hover over store button:")
    setting_dict["store"] = mouse.position()
    print "store initialized at: ", setting_dict["store"]
    raw_input("Hover over top left corner of total roll number:")
    top_left = mouse.position()
    raw_input("Hover over bottom right corner of total roll number:")
    bottom_right = mouse.position()
    setting_dict["total_roll"] = top_left + bottom_right
    print "total roll coordinates initialized at: ", setting_dict["total_roll"]
    print("done!")
    return(setting_dict)


def write_setting(setting_dict):
    """
    Write button setting to config.txt
    """
    setting_list = setting_dict.items()
    setting_text = []
    for item in setting_list:
        item_text = item[0] + " " + " ".join(str(x) for x in item[1])
        setting_text.append(item_text)
    with open("config.txt", "w") as config_file:
        config_file.write("\n".join(setting_text))


def initialize():
    setting_dict = create_setting()
    write_setting(setting_dict)


def config_exists():
    if not os.path.isfile("config.txt"):
        sys.exit("config.txt not found. You must first initialize BGNRRG")


def printv(text, verbose):
    if verbose:
        print(text)


def check_image(im, lang):
    """
    Process image with tesseract
    """
    value = pytesseract.image_to_string(im, config="-psm 6 -l " + lang)
    return(value)


def screen_grab(box):
    """
    Make screenshot of area specified by box and returns image.
    """
    im = pyscreenshot.grab(box)
    return(im)


def click(button, mouse, delay=0.1):
    """
    Perform click on coordinates specific by button and sleeps.
    """
    mouse.click(button[0], button[1], 1)
    time.sleep(delay)


def make_directory(path):
    """Safe way of creating directory."""
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise


def repeats(buttons, number=100, delay=0.1, lang="bgee2", verbose=False):
    mouse = PyMouse()
    im = screen_grab(buttons.total_roll)
    value = int(check_image(im, lang))
    click(buttons.store, mouse, delay)
    maximum = value
    printv("starting value: {0}".format(value), verbose)
    for i in range(number):
        click(buttons.reroll, mouse, delay)
        im = screen_grab(buttons.total_roll)
        value = int(check_image(im, lang))
        printv("step: {0}, roll: {1}".format(i, value), verbose)
        if value > maximum:
            click(buttons.store, mouse, delay)
            printv("old max: {0} new max: {1}".format(maximum, value), verbose)
            maximum = value
            #file_name = "maximums/" + str(i) + "_" + str(maximum) + ".png"
            #im.save(file_name, "PNG")
    click(buttons.recall, mouse, delay)
    printv("FINISHED\nHighest roll: {0}".format(maximum), verbose)


def training_images(buttons, number=100, delay=0.1, lang="bgee2"):
    mouse = PyMouse()
    make_directory("training_examples")
    for i in range(number):
        click(buttons.reroll, mouse, delay)
        im = screen_grab(buttons.total_roll)
        value = check_image(im, lang)
        file_name = os.path.join("training_examples",
                                 str(i) + "_" + value + ".png")
        im.save(file_name, "PNG")


def parse_args():
    parser = arg.ArgumentParser(
        prog="BGNRRG",
        description=(
            "Baldur's Gate NonRandom Roll Generator is usefull tool that "
            "helps find highest possible character roll for OP characters"
            " in Baldur's Gate: Enhanced Edition. Saves time and makes "
            "characters stronger."
            )
        )
    parser.add_argument(
        "-d", "--delay", required=False, default=0.1, type=int,
        help=("Delay after each click. This is required as if no or too"
              " short delay is employed, behaviour starts to be"
              " non-deterministics. Probably some clicks are ignored or done"
              " in wrong order, so value that is returned is not maximal"
              " value found. From testing, 0.05 works as well, but 0.01"
              " does not work. Test it on your machine and set delay"
              " that works for you."
              )
        )
    parser.add_argument(
        "-v", "--verbose", required=False, default=False, action="store_true",
        help=("Verbose output with some information about rolled (and"
              " recognized) values, as well as information when new"
              " maximum was rolled. Helps with debuging or when"
              " you want to see all these rolls."
              )
        )
    parser.add_argument(
        "-i", "--initialize", required=False, default=False,
        action="store_true",
        help=("Before usage, you need to initialize config.txt with positions"
              " of each button and area with total rolled value. This"
              " setting will guide you trough initialization, save these values"
              " and exit."
              )
        )
    parser.add_argument(
        "-t", "--training", required=False, default=False, action="store_true",
        help=("If you want to check how tesseract recognize images, use this"
              " switch. Instead of normal run, scanned area are saved as"
              " PNG images into newly created folder \"training_examples\"."
              " These examples can be checked for corretness or used for"
              " further training."
              )
        )
    parser.add_argument(
        "-l", "--language", required=False, default="bgee2", type=str,
        help=("Language setting for tesseract, basically \"library\" of shapes"
              " that are recognized. By default, bgee2 is used, which is"
              " made by training tesseract on BG:EE sherwood font and then"
              " additional level of training was performed to further refine"
              " learning process. See training files of BGNRRG."
              )
        )
    parser.add_argument(
        "-n", "--number", required=False, default=100, type=int,
        help=("Number of rerolls that are done. Program cannot be stopped, so"
              " it is safer to go for lower number and run program several"
              " times. It remember the last maximum (it starts from current"
              " value)."
              )
        )
    args = parser.parse_args()
    return(args)

def main():
    args = parse_args()
    if args.initialize:
        initialize()
    else:
        config_exists()
        setting_dict = read_setting()
        buttons = Buttons(setting_dict)
        if args.training:
            training_images(buttons, number=args.number,
            delay=args.delay, lang=args.language)
        else:
            repeats(buttons, number=args.number, delay=args.delay,
                    lang=args.language, verbose=args.verbose)


if __name__ == "__main__":
    main()
