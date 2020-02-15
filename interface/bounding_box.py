import cv2
import numpy as np


def draw_bbox(img, prediction, cls_names, colors):
    """ draws bounding boxes, scores and classes on image
    :param img: tensor
    :param prediction: dictionary
    {boxes: [[x1, y1, x2, y2], ...],
     scores: [float],
     labels: [int]}
    :param cls_names: dictionary class names
    :param colors: numpy array of colors
    """
    img = img.permute(1, 2, 0).cpu().numpy().copy()
    img = img * 255
    boxes = prediction['boxes'].cpu()
    scores = prediction['scores'].cpu().detach().numpy()
    labels = prediction['labels'].cpu().detach().numpy()

    for i, bbox in enumerate(boxes):
        score = round(scores[i]*100, 1)
        label = labels[i]
        p1, p2 = tuple(bbox[:2]), tuple(bbox[2:])
        cv2.rectangle(img, p1, p2, color=colors[label], thickness=3)
        text = '{cls} {prob}%'.format(cls=cls_names[label], prob=score)
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_PLAIN, 1, 1)[0]

        p3 = (p1[0] - 2, p1[1] - text_size[1] - 6)
        p4 = (p1[0] + text_size[0] + 4, p1[1])

        cv2.rectangle(img, p3, p4, color=colors[label], thickness=-1)
        cv2.putText(img, text, (p1[0], p1[1] - text_size[1] + 6), fontFace=cv2.FONT_HERSHEY_PLAIN,
                    fontScale=1, color=(0, 0, 0), thickness=1)
    return img


def color_bounding_box(classes):
    """
    Each execution makes different colors
    :return numpy array"""
    return np.random.uniform(0, 255, size=(len(classes), 3))