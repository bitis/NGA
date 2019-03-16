import MySQLdb

from nga import NGA

nga = NGA()
db = MySQLdb.connect(host="localhost", user="root", passwd="liuyuan.", db="nga")

subject_sql = "insert into subjects (tid, fid, authorid, subject, postdate, lastpost, replies, forumname) value ('{tid}', '{fid}', '{authorid}', '{subject}', '{postdate}', '{lastpost}', '{replies}', '{forumname}')"

for x in range(1, 101):
    response = nga.t_list('-7', page=str(x))
    c = db.cursor()

    for subject in response['result']['data']:
        try:
            if subject['postdate'] == 0 or subject['is_forum'] != False:
                continue

            sql = subject_sql.format(
                tid=subject['tid'],
                fid=subject['fid'],
                authorid=subject['authorid'],
                subject=subject['subject'],
                postdate=subject['postdate'],
                lastpost=subject['lastpost'],
                replies=subject['replies'],
                forumname=subject['forumname']
            )

            if c.execute('select lastpost from subjects where tid = \'{tid}\''.format(tid=subject['tid'])):
                r = c.fetchone()
                if r[0] < subject['lastpost']:
                    c.execute('update subjects set found_news = true, lastpost = {lastpost} where tid = \'{tid}\''
                              .format(tid=subject['tid'], lastpost=subject['lastpost']))
                    # print('[ * ]', subject['subject'])
                else:
                    pass
                    # print('[ - ]', subject['subject'])
            else:
                c.execute(sql)
                # print('[', c.execute(sql), ']', subject['subject'])
        except KeyError:
            print('[ x ]', subject)

    db.commit()
    c.close()
db.close()
