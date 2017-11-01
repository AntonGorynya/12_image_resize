from PIL import Image
import argparse


def resize_image(path_to_original, path_to_result,
                 target_width=None, target_hight=None, target_sacle=None):
    img = Image.open(path_to_original)
    if target_hight and target_width:
        if img.size[0]/target_width != img.size[1]/target_hight:
            print('warning! Scale mismatch. x_scale {}, y_scale {}'
                  .format(img.size[0]/target_width, img.size[1]/target_hight))
        img = img.resize((target_width, target_hight), Image.ANTIALIAS)
        target_hight = 0
        target_width = 0
    elif target_sacle and not (target_hight or target_width):
        width = int((float(img.size[0]) * float(target_sacle)))
        hight = int((float(img.size[1]) * float(target_sacle)))
        img = img.resize((width, hight), Image.ANTIALIAS)
    elif target_hight:
        scale = (target_hight / float(img.size[1]))
        width = int((float(img.size[0]) * float(scale)))
        img = img.resize((width, target_hight), Image.ANTIALIAS)
    elif target_width:
        scale = (target_width / float(img.size[0]))
        hight = int((float(img.size[1]) * float(scale)))
        img = img.resize((target_width, hight), Image.ANTIALIAS)
    else:
        print("wrong paramters")
    img.save(path_to_result)


def create_parser():
    parser = argparse.ArgumentParser(description='resize image')
    parser.add_argument("path", help="path to checking folder")
    parser.add_argument("-width", type=int, help="input width")
    parser.add_argument("-hight", type=int, help="input hight")
    parser.add_argument("-scale", type=float, help="input hight")
    parser.add_argument("-output",
                        default='sompic.jpg',
                        type=str, help="path to output file")
    return parser


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    resize_image(args.path, args.output, args.width, args.hight, args.scale)
