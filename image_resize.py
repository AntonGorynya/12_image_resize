from PIL import Image
import argparse


def create_pic_name(input_image_name, width, hight):
    pic_name = input_image_name[:args.path.rfind('.')] + \
               '__{}x{}'.format(width, hight) + \
               input_image_name[args.path.rfind('.'):]
    return pic_name


def resize_image(path_to_original, out_img,
                 target_width=None, target_hight=None, target_sacle=None):
    img = Image.open(path_to_original)
    if target_hight and target_width:
        if img.size[0]/target_width != img.size[1]/target_hight:
            print('warning! Scale mismatch. x_scale {}, y_scale {}'
                  .format(img.size[0]/target_width, img.size[1]/target_hight))
        width = target_width
        hight = target_width
        target_hight = 0
        target_width = 0
    elif target_sacle and not (target_hight or target_width):
        width = int((float(img.size[0]) * float(target_sacle)))
        hight = int((float(img.size[1]) * float(target_sacle)))
    elif target_hight:
        scale = (target_hight / float(img.size[1]))
        width = int((float(img.size[0]) * float(scale)))
        hight = target_hight
    elif target_width:
        scale = (target_width / float(img.size[0]))
        hight = int((float(img.size[1]) * float(scale)))
        width = target_width
    else:
        print("wrong paramters")
    img = img.resize((width, hight), Image.ANTIALIAS)
    if not out_img:
        out_img = create_pic_name(path_to_original, width, hight)
    img.save(out_img)


def create_parser():
    parser = argparse.ArgumentParser(description='resize image')
    parser.add_argument("path", help="path to image")
    parser.add_argument("-width", type=int, help="input width")
    parser.add_argument("-hight", type=int, help="input hight")
    parser.add_argument("-scale", type=float, help="input hight")
    parser.add_argument("-output",
                        default='',
                        type=str, help="path to output file")
    return parser


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    resize_image(args.path, args.output, args.width, args.hight, args.scale)
