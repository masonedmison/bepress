import pandas as pd
import glob
import re
from drive_api.service import Service


def merge_record_id():
    '''appends record id to digital commons xls sheet'''
    vid_dc = pd.DataFrame(pd.read_excel('xls/VID_DC_REVISE.xls'))
    master = pd.DataFrame(pd.read_excel('xls/ALL_WP_ID_URL.xls'))

    vid_dc.set_index('source_url', inplace=True)
    master.set_index('URL', inplace=True)

    joined = vid_dc.join(master)
    return dict(joined)


def get_thumbnails():
    filenames = []
    for file in glob.glob('thumbnails/*'):
        split_file = file.split('/')
        filenames.append(split_file[1])
    return filenames


def build_drive_link(file_id):
    #drive link format - https://drive.google.com/uc?export=download&id=1U98g_yLel3Aj1IXD6gk2Dg7LxbnJIGeL
    return 'https://drive.google.com/uc?export=download&id={}'.format(file_id)


def write_xls(joined):
    joined.to_excel('xls/revise_dc_with_record_id.xls')


if __name__ == '__main__':
    service = Service()
    folder_id = '9tcjTyAhjJ2G7VrlgLbiiMiac4c6V6XC'
    joined = merge_record_id()
    thumbnails = get_thumbnails()
    records_not_in_wp = []
    for index, title in enumerate(joined['title'].tolist()):
        if isinstance(joined['Record ID'][index], str):
            record_id = joined['Record ID'][index].strip()
            regex = re.compile(record_id)
            thumbnail = list(filter(regex.search, thumbnails))
            for thumb in thumbnail:
                if thumb.endswith('.png'):
                    file_id = service.insert_to_folder(folder_id, record_id, thumb)
                elif thumb.endswith('.jpg'):
                    file_id = service.insert_to_folder(folder_id, record_id, thumb)
                joined['cover_image_url'][index] = build_drive_link(file_id)
        else:
            records_not_in_wp.append(joined['Record ID'][index])









