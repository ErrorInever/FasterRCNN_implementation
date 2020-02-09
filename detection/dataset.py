import os
import cv2
from torchvision import transforms
from torch.utils.data import Dataset
from PIL import Image
from datetime import datetime
from detection import utils


class Images(Dataset):
    """
    Container for images
    """

    def __init__(self, img_path):
        self.img_path = img_path
        self.img_names = [n for n in os.listdir(img_path) if n.endswith(('jpg', 'jpeg', 'png'))]

    def __getitem__(self, idx):
        img = Image.open(os.path.join(self.img_path, self.img_names[idx])).convert('RGB')
        return self.img_to_tensor(img)

    def __len__(self):
        return len(self.img_names)

    def __str__(self):
        return str(self.img_names[:5])

    @property
    def img_to_tensor(self):
        """Convert an image to a tensor"""
        return transforms.Compose([transforms.ToTensor()])


class Video:
    # TODO: release decorator to track time
    # TODO: release batchs frames
    """ Defines a video"""

    def __init__(self, video_path, save_path):
        """
        :param video_path: path to a video file
        :param save_path: path to output directory
        """
        self.cap = cv2.VideoCapture(video_path)
        self.video_path = video_path
        self.save_path = os.path.join(save_path, 'detection_{}.avi'.format(datetime.today().strftime('%Y-%m-%d')))
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.width, self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), \
                                  int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.duration = self.__len__() / self.fps
        self.out = cv2.VideoWriter(self.save_path, self.fourcc, self.fps, (self.width, self.height))

    def __str__(self):
        info = 'duration: {}\nframes: {}\nresolution: {}x{}\nfps: {}'.format(round(self.duration, 1),
                                                                             self.__len__(),
                                                                             self.width, self.height,
                                                                             round(self.fps, 1))
        return info

    def __len__(self):
        """ total number of frames"""
        return int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def get_frame(self):
        """convert frame to tensor and return object of generator frame by frame"""
        while self.cap.isOpened():
            ret, frame = self.cap.read()

            if ret:
                if cv2.waitKey(1) % 0xFF == ord('q'):
                    break
                frame = utils.frame_to_tensor(frame)
                yield [frame]
            else:
                break
        self.cap.release()
