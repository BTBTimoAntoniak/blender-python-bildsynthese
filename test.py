from config import Config


def main():
    cfg = Config(box_types=["Kiste_Blau", "Kiste_Gruen"])
    print(cfg.box_types)
    box_types = ["Kiste_Blau", "Kiste_Gruen"]
    print(box_types)


if __name__ == "__main__":
    main()
