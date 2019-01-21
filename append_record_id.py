import pandas as pd

# master_WP = pd.DataFrame(pd.read_excel('ALL_ZFWP_ID_URL.xls'))
# master_DC = pd.DataFrame(pd.read_excel('missed1_dc_bulk_import.xls'))

# master_WP.set_index('URL', inplace=True)
# master_DC.set_index('source_url', inplace=True)
#
# joined = master_DC.join(master_WP)
#
# joined.to_excel('master_DC_with_ID.xls')

links = pd.DataFrame(pd.read_excel('xls/BePress_fulltext_links.xlsx'))
master_DC = pd.DataFrame(pd.read_excel('xls/master_DC_with_ID.xls'))

merged = pd.merge(master_DC, links, on='Record ID')

merged.to_excel('xls/DRIVE_master_DC_with_ID.xls')

