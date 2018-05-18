from PIL import Image, ImageDraw
import argparse
import logging
import os


VERBOSITY_TO_LOGGING_LEVELS = {
    0: logging.WARNING,
    1: logging.INFO,
    2: logging.DEBUG,
}


def create_pic_name(input_image_name, width, hight):
    pic_name = input_image_name[:args.path.rfind('.')] + \
               '__{}x{}'.format(width, hight) + \
               input_image_name[args.path.rfind('.'):]
    return pic_name


def set_size(original_width, original_hight,
             target_width=None, target_hight=None, target_scale=None):
    logging.debug('\noriginal_width={}\n'
                  'original_hight={}\n'
                  'target_width={}\n'
                  'target_hight={}\n'
                  'target_scale={}'
                  .format(original_width, original_hight,
                          target_width, target_hight, target_scale))
    if target_hight and target_width and not target_scale:
        x_scale = original_width/target_width
        y_scale = original_hight/target_hight
        rel_tol = 1e-09
        abs_tol = 0.0
        if abs(x_scale-y_scale) > max(rel_tol*max(x_scale, y_scale), abs_tol):
            logging.info('\nwarning! Scale mismatch. x_scale {}, y_scale {}'
                         .format(x_scale, y_scale))
        width = target_width
        hight = target_hight
        return width, hight
    elif target_scale and not (target_hight or target_width):
        width = int((float(original_width) * float(target_scale)))
        hight = int((float(original_hight) * float(target_scale)))
        return width, hight
    elif target_hight and not target_width:
        scale = (target_hight / float(original_hight))
        width = int((float(original_width) * float(scale)))
        hight = target_hight
        return width, hight
    elif target_width and not target_hight:
        scale = (target_width / float(original_width))
        hight = int((float(original_hight) * float(scale)))
        width = target_width
        return width, hight
    else:
        logging.info('wrong paramters')


def resize_image(path_to_original, out_dir=None,
                 target_width=None, target_hight=None, target_scale=None):
    img = Image.open(path_to_original)
    original_width, original_hight = img.size
    try:
        width, hight = set_size(original_width, original_hight,
                                target_width, target_hight, target_scale)
        img = img.resize((width, hight), Image.ANTIALIAS)
        out_img_name = create_pic_name(path_to_original, width, hight)
        if not out_dir:
            out_img = out_img_name
        else:
            out_img = os.path.join(out_dir, out_img_name)        
        img.save(out_img)
    except TypeError:
        logging.info('image don\'t created')


def add_border(path_to_original, border_width, out_dir=None):
    logging.info('processing {}'.format(path_to_original))
    original_img = Image.open(path_to_original)
    original_width, original_hight = original_img.size
    out_width = original_width + border_width*2
    out_hight = original_hight + border_width*2
    out_img = Image.new('RGBA', [out_width, out_hight], (255, 255, 255, 0))
    out_img.paste(original_img, (border_width, border_width))
    # write to stdout
    out_img_name = path_to_original
    if out_dir:
        out_img_name = os.path.join(out_dir, out_img_name)
    out_img.save(out_img_name)


def create_parser():
    parser = argparse.ArgumentParser(description='resize image')
    parser.add_argument('path', help='path to image')
    parser.add_argument('-width', type=int, help='input width')
    parser.add_argument('-hight', type=int, help='input hight')
    parser.add_argument('-scale', type=float, help='input hight')
    parser.add_argument('--verbose', '-v', type=int, default=0)
    parser.add_argument('-board', '-b', type=int, default=0)
    parser.add_argument('-output',
                        default='',
                        type=str, help='path to output dir')
    return parser


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    logging_level = VERBOSITY_TO_LOGGING_LEVELS[args.verbose]
    logging.basicConfig(level=logging_level)
    resize_image(args.path, args.output, args.width, args.hight, args.scale)
    if args.board:
        add_border(args.path, args.board)
