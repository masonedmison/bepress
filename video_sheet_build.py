import pandas as pd
import numpy as np
import glob
import re
from drive_api.service import Service



def merge_record_id():
    '''appends record id to digital commons xls sheet'''
    vid_dc = pd.DataFrame(pd.read_excel('xls/VID_DC_REVISE.xls'))
    master = pd.DataFrame(pd.read_excel('xls/ALL_WP_ID_URL.xls'))

    vid_dc.set_index('source_url', inplace=True)
    master.set_index('URL', inplace=True)

    joined_with_nan = vid_dc.join(master) ##replace nan with a blank character so we can string concatenate
    joined = joined_with_nan.replace(np.nan, '', regex=True)
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
    joined_df = pd.DataFrame(joined)
    joined_df.to_excel('xls/revise_dc_with_thumb.xls')


if __name__ == '__main__':
    service = Service()
    folder_id = '1fqe6pHX_DRB05L_5oMNt9A-MPaJASFYS'
    joined = merge_record_id()
    thumbnails = get_thumbnails()           ##returns dict object
    records_not_in_wp = []
    for index, title in enumerate(joined['title'].tolist()):
        if isinstance(joined['Record ID'][index], str) and joined['Record ID'][index] is not "":
            record_id = joined['Record ID'][index].strip()
            regex = re.compile(record_id)
            thumbnail = list(filter(regex.search, thumbnails))
            if thumbnail:
                for thumb in thumbnail:
                    if thumb.endswith('.png'):
                        file_id = service.insert_to_folder(folder_id, record_id, "thumbnails/{}".format(thumb), 'image/png')
                        break
                    elif thumb.endswith('.jpg'):
                        file_id = service.insert_to_folder(folder_id, record_id, "thumbnails/{}".format(thumb), 'image/jpeg')
                        break

                    joined['cover_image_url'][index] = build_drive_link(file_id)
            else:
                print('No thumbnail image found for {}'.format(record_id))
        else:
            records_not_in_wp.append(joined['Record ID'][index])
    write_xls(joined)









