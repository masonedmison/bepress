import os
import pandas as pd


def set_working_directory():
    abs_path = os.path.abspath(__file__)
    dir_name = os.path.dirname(abs_path)
    os.chdir(dir_name)


def map_master_to_dc(master, dc, index):
    #grab current length of dc records so new records can be appended to end
    length = len(dc['title']) + 1

    dc['title'][length] = master['Title'][index]
    dc['source_publication'][length] = master['Source'][index]
    dc['document_type'][length] = doc_type_map(master['Type'][index])
    dc['source_url'][length] = master['URL'][index]
    dc['abstract'][length] = '<p>' + master['Description'][index] + '</p>'
    dc['publication_date'][length] = pd.Timestamp(master['Date'][index])
    dc['disciplines'][length] = 'Communication Technology and New Media'

    author_parser(master['Participants'][index], dc, length)


def doc_type_map(master_type):
    """Bepress document types: article; blog; bookreview; conference; dissertation; editorial; financial_comm; gov_doc;
    letter; news; press; pressrelease; response; video_interview

master:
interview
social media post
article
book
correspondence
speech
editorial
corporate communication
promotional
news report
 congressional hearing
    """
    type_mapping = {'article': 'article', 'interview': 'video_interview', 'social media post': 'blog', 'book': 'editorial',
                    'correspondence': 'press', 'speech': 'conference', 'editorial': 'editorial',
                    'corporate communication': 'financial_comm', 'promotional': 'press', 'news': 'news',
                    'congressional hearing': 'gov_doc'}

    if master_type in type_mapping:
        master_type = type_mapping[master_type]
    else:
        master_type = 'blog'

    return master_type


def author_parser(participants, dc, length):
    split_participants = participants.strip().split(';')

    if split_participants[len(split_participants) -1].isspace and isinstance(split_participants, list):
        split_participants.pop(len(split_participants) -1)

    if len(split_participants) > 5 and isinstance(split_participants, list):
        joined = ','.join(split_participants)
        dc['author1_fname'][length] = joined

    elif len(split_participants) == 1:
        name_split = split_participants[0].strip().split(" ")
        if len(name_split) == 1:
            dc['author1_fname'][length] = name_split[0]
        else:
            dc['author1_fname'][length] = name_split[0]
            dc['author1_lname'][length] = name_split[len(name_split) -1]

    elif len(split_participants) > 0 and len(split_participants) < 5:
        for index, name in enumerate(split_participants):
            name_split = name.strip().split(" ")
            if len(name_split) ==1:
                dc['author{}_fname'.format(str(index + 1))][length] = name_split[0]
            else:
                dc['author' + str(index + 1) + "_fname"][length] = name_split[0]
                dc['author' + str(index + 1) + "_lname"][length] = name_split[len(name_split) -1]


def write_to_xls(dc_modified):
    to_xls = pd.DataFrame(dc_modified)
    to_xls.to_excel('missed_dc_bulk_import.xls', sheet_name='Sheet 1')


def write_list_of_pdf_files_needed(pdf_file_list):
    with open('pdf_file_list.txt', 'w', encoding='utf-8') as pdf_list:
        for file in pdf_file_list:
            pdf_list.write('{}, '.format(file))






def main():
    all_master = dict(pd.read_excel('ALL_ZFWP.xls'))
    dc_text_import = dict(pd.read_excel('dc_bulk_import.xls'))

    print(len(dc_text_import['title'].tolist()))

    pdf_file_list = []

    for index, title in enumerate(all_master['Title']):
        if title not in dc_text_import['title'].tolist() and all_master['URL'][index] not in dc_text_import['source_url'].tolist():
            """do something
            send index of zf_master to mapping method (based off title that was not matched"""
            try:
                map_master_to_dc(all_master, dc_text_import, index)
                pdf_file_list.append(all_master['Record ID'][index])

            except Exception as e:
                print(e.args)
                print('Problem with record index: {}, record id: {} '.format(index, all_master['Record ID'][index]))
                pass
    write_to_xls(dc_text_import)
    print(len(dc_text_import['title'].tolist()))
    write_list_of_pdf_files_needed(pdf_file_list)


if __name__ == '__main__':
    main()










