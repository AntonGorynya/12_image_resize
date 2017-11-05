from PIL import Image
import argparse


def create_pic_name(input_image_name, width, hight):
    pic_name = input_image_name[:args.path.rfind('.')] + \
               '__{}x{}'.format(width, hight) + \
               input_image_name[args.path.rfind('.'):]
    return pic_name


def set_size(original_width, original_hight,
             target_width=None, target_hight=None, target_sacle=None):
    if target_hight and target_width:
        if original_width/target_width != original_hight/target_hight:
            print('warning! Scale mismatch. x_scale {}, y_scale {}'
                  .format(original_width/target_width,
                          original_hight/target_hight))
        width = target_width
        hight = target_width
        return width, hight
    elif target_sacle and not (target_hight or target_width):
        width = int((float(original_width) * float(target_sacle)))
        hight = int((float(original_hight) * float(target_sacle)))
        return width, hight
    elif target_hight:
        scale = (target_hight / float(original_hight))
        width = int((float(original_width) * float(scale)))
        hight = target_hight
        return width, hight
    elif target_width:
        scale = (target_width / float(original_width))
        hight = int((float(original_hight) * float(scale)))
        width = target_width
        return width, hight
    else:
        print("wrong paramters")


def resize_image(path_to_original, out_img,
                 target_width=None, target_hight=None, target_sacle=None):
    img = Image.open(path_to_original)
    original_width = img.size[0]
    original_hight = img.size[1]
    width, hight = set_size(original_width, original_hight,
                            target_width, target_hight, target_sacle)
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
