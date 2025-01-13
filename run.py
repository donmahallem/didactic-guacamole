from guacamole import BaseApp
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Didactic Guacamole")
    parser.add_argument(
        "--colors", "-c", help="How many colors", type=int, choices=[4, 5, 6], default=4
    )
    parser.add_argument(
        "--seed", "-s", help="What seed to use", type=str, default=None, required=False
    )
    parser.add_argument(
        "--distored", "-d", help="Apply lighthouse output", type=bool, default=False
    )
    args = parser.parse_args()
    app = BaseApp(colors=args.colors, seed=args.seed if args.seed else None)
    app.run()
    app.close()
