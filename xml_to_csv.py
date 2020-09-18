import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
from absl import app
from absl import flags

flags.DEFINE_string('annotations_dir', '', 'Path to annotatiosn')
flags.DEFINE_string('output_path', '', 'Path to output csv file')
FLAGS = flags.FLAGS

def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size').find('width').text),
                     int(root.find('size').find('height').text),
                     member.find('name').text,
                     int(member.find('bndbox').find('xmin').text),
                     int(member.find('bndbox').find('ymin').text),
                     int(member.find('bndbox').find('xmax').text),
                     int(member.find('bndbox').find('ymax').text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def main(_):
    annotations_path = os.path.join(FLAGS.annotations_dir)
    output_csv_path = os.path.join(FLAGS.output_path)
    xml_df = xml_to_csv(annotations_path)
    xml_df.to_csv(output_csv_path, index=None)
    print('Successfully converted xml to csv.')


if __name__ == '__main__':
    app.run(main)
