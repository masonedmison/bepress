import pandas as pd

# master_WP = pd.DataFrame(pd.read_excel('ALL_ZFWP_ID_URL.xls'))
# master_DC = pd.DataFrame(pd.read_excel('missed1_dc_bulk_import.xls'))

# master_WP.set_index('URL', inplace=True)
# master_DC.set_index('source_url', inplace=True)
#
# joined = master_DC.join(master_WP)
#
# joined.to_excel('master_DC_with_ID.xls')

################################################################
# links = pd.DataFrame(pd.read_excel('xls/BePress_fulltext_links.xlsx'))
# master_DC = pd.DataFrame(pd.read_excel('xls/master_DC_with_ID.xls'))
#
# merged = pd.merge(master_DC, links, on='Record ID')
#
# merged.to_excel('xls/DRIVE_master_DC_with_ID.xls')

master = pd.read_excel('xls/05-02_zuck.xlsx')  # master source
dc = pd.read_excel('xls/05-02_dc_vids.xls') # revise videos (books) dc sheet as of 05/02

master_u_id = pd.DataFrame({'Title': master['Title'], 'record_id': master['Record ID'], 'URL': master['URL']})
dc_vid_title_url = pd.DataFrame({'Title': dc['title'], 'dc_url': dc['calc_url'], 'URL': dc['source_url']})


merged = pd.merge(master_u_id, dc_vid_title_url, on='URL', how='right')
print(merged.columns)
#
# merged.drop('URL', axis=1, inplace=True)  # drop redundant URL col
#
merged.to_excel('xls/05-02_dc_vids_to_import_BY_URL.xlsx')  # write to excel



