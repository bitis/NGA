#!/usr/bin/python
# -*- coding: <utf-8> -*-
import MySQLdb
import html

from nga import NGA

nga = NGA()
db = MySQLdb.connect(host="localhost", user="root", passwd="liuyuan.", db="nga")

comment_sql = "insert into comments (pid, fid, tid, postdate , content, from_client, lou, postdatetimestamp, comment_to_id, vote_good, vote_bad, authorid, reputation, is_user_quote, isTieTiao) value ('{pid}', '{fid}', '{tid}', '{postdate}', '{content}', '{from_client}', '{lou}', '{postdatetimestamp}', '{comment_to_id}', '{vote_good}', '{vote_bad}', '{authorid}', '{reputation}', '{is_user_quote}', '{isTieTiao}')"
c = db.cursor()

if c.execute('select tid, comment_page from subjects where found_news = true') > 1:
    subjects = c.fetchall()
    c.close()

    for subject in subjects:
        data = nga.t_content(subject[0], subject[1])
        c = db.cursor()
        # print("😁", subject[0], subject[1])

        #  结果不存在跳过
        if not data['result']:
            print("xxx")
            c.execute('update subjects set found_news = false where tid = \'{tid}\''.format(tid=subject[0]))
            continue

        try:
            new_comments_count = 0;

            for page in range(subject[1], (data['totalPage'] + 1)):
                if page != subject[1]:
                    data = nga.t_content(subject[0], page)
                comments = data['result']

                if comments is None: break

                for comment in comments:
                    if c.execute(
                            'select id from comments where tid = \'{tid}\' and pid =\'{pid}\''.format(
                                tid=comment['tid'],
                                pid=comment['pid'])):
                        # print('[ - ]', html.escape(comment['content']))
                        pass
                    else:
                        sql = comment_sql.format(
                            pid=comment['pid'],
                            fid=comment['fid'],
                            tid=comment['tid'],
                            postdate=comment['postdate'],
                            content=html.escape(comment['content']),
                            from_client=comment['from_client'],
                            lou=comment['lou'],
                            postdatetimestamp=comment['postdatetimestamp'],
                            comment_to_id=comment['comment_to_id'] if comment['comment_to_id'] else 0,
                            vote_good=comment['vote_good'],
                            vote_bad=comment['vote_bad'],
                            authorid=comment['author']['uid'],
                            reputation= comment['author']['reputation'] if comment['author']['uid'] > 0 else 0,
                            is_user_quote=comment['is_user_quote'],
                            isTieTiao=comment['isTieTiao']
                        )

                        # print('[', c.execute(sql), ']', comment['content'])
                        new_comments_count += c.execute(sql)

                c.execute('update subjects set comment_page = \'{page}\' where tid = \'{tid}\''.format(page=page, tid=comment['tid']))
            print('{tid}:\t{new_comments_count}'.format(
                tid = comment['tid'],
                new_comments_count = new_comments_count
            ))
        except KeyError:
            print(comment)
            print(KeyError.with_traceback())
            exit()
        c.execute('update subjects set found_news = false where tid = \'{tid}\''.format(tid=subject[0]))
        db.commit()
        c.close()
db.close()