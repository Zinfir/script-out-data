import os, csv


def csv_reader(file_obj):
    """
    Read a csv file
    """
    data = csv.reader(file_obj)

    return data

def csv_writer(data, path):
    """
    Write data to a csv file path
    """
    with open(path, "a", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)


def count_rows(data):
    """
    Return size of data file in number of rows
    """
    count = 0
    for _ in data:
        count += 1
    return count


def render_out_array(data_a_path, data_p_path):
    """
    Return array of out data with unique combinations of columns:
    app, date, campaign, os, installs, spend, cpi
    """

    # out array

    unique_rows_list = []

    # open files to render out data

    with open(data_a_path, 'r') as f_obj_a, open(data_p_path, 'r') as f_obj_p:

        IN_DATA_A = csv_reader(f_obj_a)
        IN_DATA_P = csv_reader(f_obj_p)

        ROWS_IN_DATA_P = count_rows(IN_DATA_P)

        IN_DATA_A_FIELDS = {}
        IN_DATA_P_FIELDS = {}

        u_rows_list_with_ad_ids = []
        unique_row = []
        u_row_with_ad_ids = []
    
        # Creating 2 arrays with unique combinations of columns:
        # Date, Campaign, os, app
        # 2nd array with additional column [] where will be stored  ad ids

        for index, row in enumerate(IN_DATA_A):
            if index == 0:
                for i, column in enumerate(row):
                    IN_DATA_A_FIELDS.update({column: i})
            else:
                for i, column in enumerate(row):
                    if i == IN_DATA_A_FIELDS['Date']:
                        unique_row.append(column)
                        u_row_with_ad_ids.append(column)
                    elif i == IN_DATA_A_FIELDS['Campaign']:
                        unique_row.append(column)
                        u_row_with_ad_ids.append(column)
                    elif i == IN_DATA_A_FIELDS['app']:
                        unique_row.append(column)
                        u_row_with_ad_ids.append(column)
                    elif i == IN_DATA_A_FIELDS['os']:
                        unique_row.append(column)
                        u_row_with_ad_ids.append(column)

                u_row_with_ad_ids.append([])

                if unique_row not in unique_rows_list:
                    unique_rows_list.append(unique_row)
                    u_rows_list_with_ad_ids.append(u_row_with_ad_ids)
                    
                unique_row = []
                u_row_with_ad_ids = []

        spend_list = [[] for i in range(len(unique_rows_list))]
        u_row_index = 0 

        f_obj_a.seek(0)

        tmp_list = []
        
        # Add ad ids array to unique combnation of columns

        for index, row in enumerate(IN_DATA_A):
            if index == 0:
                for i, column in enumerate(row):
                    IN_DATA_A_FIELDS.update({column: i})
            else:
                for i, column in enumerate(row):
                    if i == IN_DATA_A_FIELDS['Date']:
                        unique_row.append(column)
                    elif i == IN_DATA_A_FIELDS['Campaign']:
                        unique_row.append(column)
                    elif i == IN_DATA_A_FIELDS['app']:
                        unique_row.append(column)
                    elif i == IN_DATA_A_FIELDS['os']:
                        unique_row.append(column)
                    elif i == IN_DATA_A_FIELDS['ad_id']:
                        tmp_list.append(column)
                    elif i == IN_DATA_A_FIELDS['Installs']:
                        tmp_list.append(column)

                u_row_index = unique_rows_list.index(unique_row)
                u_rows_list_with_ad_ids[u_row_index][4].append(tmp_list)

                unique_row = []
                tmp_list = []

        tmp_list = []

        print('Start')
        f_obj_p.seek(0)

        # list of integers from 0 to 100 for print progress of calculating

        progress_list = [i for i in range(101)]


        # Creating array of rows with spend and installs items for each unique combination

        for index_p, row_p in enumerate(IN_DATA_P):
            if index_p == 0:
                for i, column in enumerate(row_p):
                    IN_DATA_P_FIELDS.update({column: i})
            else:
                for i in progress_list:
                    if index_p == int(0.01 * i * ROWS_IN_DATA_P):
                        print('{}%'.format(i))
                for index_a, row_a in enumerate(u_rows_list_with_ad_ids):
                    for i, column in enumerate(row_a):
                        if i == 4:
                            for ad_id_installs in column:
                                if ad_id_installs[0] == row_p[IN_DATA_P_FIELDS['ad_id']] and row_p[IN_DATA_P_FIELDS['date']] == row_a[0]:
                                    tmp_list.append(float(row_p[IN_DATA_P_FIELDS['spend']]))
                                    tmp_list.append(float(ad_id_installs[1]))
                                    spend_list[index_a].append(tmp_list)
                    tmp_list = []

        out_spend_list = []
        installs = 0
        spend = 0
        cpi = 0
        tmp_list = []

        # Calculating spend, installs and cpi for each unique combination

        for row in spend_list:
            for item in row:
                spend += item[0]
                installs += item[1]

            if installs == 0:
                cpi = spend
            else:
                cpi = spend / installs
            spend = format(spend, '.3f')
            installs = format(installs, '.3f')
            cpi = format(cpi, '.3f')
            tmp_list.append(spend)
            tmp_list.append(installs)
            tmp_list.append(cpi)
            out_spend_list.append(tmp_list)
            tmp_list = []
            spend = 0
            installs = 0

        # Extend unique_rows_list with out_spend_list items for each unique combination and get columns:
        # Date, Campaign, os, app, spend, installs, cpi

        for index_u, row_u in enumerate(unique_rows_list):
            for index_s, row_s in enumerate(out_spend_list):
                if index_u == index_s:
                    row_u.extend(row_s)

        # recombine columns order as it given in out.csv file:
        # app, date, campaign, os, installs, spend, cpi

        tmp = 0
        tmp_list = []
        for row in unique_rows_list:
            tmp = row.pop(3)
            tmp_list.append(tmp)
            tmp = row.pop(0)
            tmp_list.append(tmp)
            tmp = row.pop(0)
            tmp_list.append(tmp)
            tmp = row.pop(0)
            tmp_list.append(tmp)
            tmp = row.pop(1)
            tmp_list.append(tmp)
            tmp = row.pop(0)
            tmp_list.append(tmp)
            tmp = row.pop(0)
            tmp_list.append(tmp)
            row.extend(tmp_list)
            tmp_list = []

        print('100%\nEnd')

    return unique_rows_list


if __name__ == "__main__":

    DIRNAME = os.path.dirname(__file__)
    IN_DATA_A_PATH = os.path.join(DIRNAME, 'in_data_a.csv')
    IN_DATA_P_PATH = os.path.join(DIRNAME, 'data_p.csv')
    OUT_PATH = os.path.join(DIRNAME, 'out.csv')   

    OUT_DATA = render_out_array(IN_DATA_A_PATH, IN_DATA_P_PATH)

    csv_writer(OUT_DATA, OUT_PATH)
        