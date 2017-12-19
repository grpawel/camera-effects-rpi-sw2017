import time
from image_processors import ImagePipeline


def main():
    pipeline = ImagePipeline()
    pipeline.run()
    time.sleep(3)
    pipeline.stop_all()


if __name__ == '__main__':
    main()
