from trainer.game import ShooterGame


def main():
    game = ShooterGame()

    game.fov.set(1.25)
    
    game.previewmode.set(6)


if __name__ == "__main__":
    main()