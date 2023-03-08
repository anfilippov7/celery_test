import uuid
import os
from tasks import cpu_bound
from flask import Flask
from flask import request
from flask.views import MethodView
from flask import jsonify
from celery import Celery
from celery.result import AsyncResult

from upscale import example, upscale

# from face_checker import FaceChecker


app_name = 'app'
app = Flask(app_name)
app.config['UPLOAD_FOLDER'] = 'files'

celery = Celery(
    app_name,
    backend='redis://localhost:6379/3',
    broker='redis://localhost:6379/4'
)

celery.conf.update(app.config)


class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)


celery.Task = ContextTask


@celery.task()
def match_photos(path_1):
    # result = cpu_bound.delay(1)
    # result2 = cpu_bound.delay(2)
    result = upscale(path_1, 'lama.png')
    print(result, 'this')
    # result = example()

    # return 'dfsdgfg'

    return result


class Upscale(MethodView):

    def get(self, task_id):
        task = AsyncResult(task_id, app=celery)
        return jsonify({
            'status': task.status,
            'result:': task.result,
            # 'link': self.save_image('image_1')
        })

    def post(self):
        # image = request.files.get(field)
        # extension = image.filename.split('.')[-1]
        # path_result = os.path.join('files', f'{uuid.uuid4()}.{extension}')


        image_pathes = self.save_image('image_1')
        print(image_pathes)

        task = match_photos.delay(image_pathes)
        # print(task)
        # print(jsonify({
        #     'task_id': task.id
        # }))
        return jsonify({
            'task_id': task.id
        })

        # return 'fsdfsdgf'


    def save_image(self, field):
        image = request.files.get(field)
        print(image.filename)
        extension = image.filename.split('.')[-1]
        path = os.path.join('files', f'{uuid.uuid4()}.{extension}')
        print(path)
        image.save(path)
        return path


upscale_view = Upscale.as_view('upscale')
app.add_url_rule('/upscale/<string:task_id>', view_func=upscale_view, methods=['GET'])
app.add_url_rule('/upscale/', view_func=upscale_view, methods=['POST'])
app.add_url_rule('/processed/{file}', view_func=upscale_view, methods=['GET'])

if __name__ == '__main__':
    app.run()





























# from face_checker import FaceChecker
#
#
# app_name = 'app'
# app = Flask(app_name)
# app.config['UPLOAD_FOLDER'] = 'files'
# celery = Celery(
#     app_name,
#     backend='redis://localhost:6379/3',
#     broker='redis://localhost:6379/4'
# )
# celery.conf.update(app.config)
#
#
# class ContextTask(celery.Task):
#     def __call__(self, *args, **kwargs):
#         with app.app_context():
#             return self.run(*args, **kwargs)
#
#
# celery.Task = ContextTask
#
#
# @celery.task()
# def match_photos(path_1, path_2):
#
#     result = FaceChecker.with_files().match(path_1, path_2)
#     # result = example()
#     return result
#
#
# class Comparsion(MethodView):
#
#     def get(self, task_id):
#         task = AsyncResult(task_id, app=celery)
#         return jsonify({
#             'status': task.status,
#             'result:': task.result
#         })
#
#     def post(self):
#         image_pathes = [self.save_image(field) for field in ('image_1', 'image_2')]
#         task = match_photos.delay(*image_pathes)
#         return jsonify({
#             'task_id': task.id
#         })
#
#     def save_image(self, field):
#         image = request.files.get(field)
#         extension = image.filename.split('.')[-1]
#         path = os.path.join('files', f'{uuid.uuid4()}.{extension}')
#         image.save(path)
#         return path
#
#
# comparison_view = Comparsion.as_view('comparison')
# app.add_url_rule('/comparison/<string:task_id>', view_func=comparison_view, methods=['GET'])
# app.add_url_rule('/comparison/', view_func=comparison_view, methods=['POST'])
#
# if __name__ == '__main__':
#     app.run()