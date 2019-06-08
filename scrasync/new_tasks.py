#
# from .app import celery
#
#
# @celery.task(bind=True)
# @save_task_id
# def parse_and_save(self, path: str = None, endpoint: str = None,
#                    corpusid: str = None, corpus_file_path: str = None):
#     """ Calling the html parser and saving the data to file. """
#
#     if not os.path.isfile(path):
#         return []
#
#     with open(path, 'r') as html_txt:
#         _dt = DataToTxt(url=endpoint, http_resp=html_txt.read())
#         _dt()
#
#     if not _dt:
#         raise RuntimeError(_dt)
#
#     links = _dt.links
#     uid = uuid.uuid4().hex
#
#     celery.send_task(EXTRACTXT_TASKS['extract_from_txt'], kwargs={
#         'file_path': path,
#         'unique_id': uid,
#         'corpus_files_path': corpus_file_path,
#         'corpusid': corpusid,
#     }, link=parse_callback.signature(path, **{
#         'corpusid': corpusid,
#         'fileid': uid,
#         'corpus_file_path': corpus_file_path,
#         'endpoint': endpoint,
#         'title': _dt.title,
#         'links': links,
#     }))
#
#     # hasher = hashlib.md5()
#     # with open(os.path.join(corpus_file_path, uid), 'a+') as _file:
#     #     hasher.update(bytes(_dt.title, 'utf-8'))
#     #     _file.write(_dt.title)
#     #     for txt in _dt.out_data:
#     #         hasher.update(bytes(txt, 'utf-8'))
#     #         _file.write(txt)
#     # texthash = hasher.hexdigest()
#
#
#
#
# @celery.task
# def parse_callback(success, path, **kwds):
#
#     if success:
#         celery.send_task(RMXBOT_TASKS.get('create_data'), kwargs=kwds)
#
#     os.remove(path)


