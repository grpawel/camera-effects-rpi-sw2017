import time
from image_processors import ImagePipeline, ImageProcessor
from finger.fingers.finger_processor import finger_processor

def main():
    pipeline = ImagePipeline()
    pipeline.run()
    time.sleep(3)
    pipeline.replace_processor(ImageProcessor(finger_processor))
    pipeline.run()
    time.sleep(3)
    pipeline.stop_all()


if __name__ == '__main__':
    main()
