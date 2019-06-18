from django.http import JsonResponse
import base64
from django.views.decorators.csrf import csrf_exempt
import requests, json, os

from .forms import UploadFileForm
from .models import ImageResult

API_HOST = 'https://vision.googleapis.com/v1/images:annotate?key=AIzaSyA36WzCJokOlopsdqNOiLk-Y-NBuI8fJPc'

categories = json.loads(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'category.json')).read())


def findOut(word: str):
    for category in categories:
        for inside in list(category.items())[0][1]:
            for in_text in list(inside.items())[0][1]:
                if word == '밀':
                    return 'wheat'
                if word == '알':
                    return 'allEgg'
                if word == '게' or word == '젓':
                    return 'crab'
                if word.find(in_text) != -1:
                    return list(inside.items())[0][0]
    return None


def textAnalysis(p0: str):
    words = p0.split(',')
    result_find = dict()
    result_simple = set()
    for index, word in enumerate(words):
        tmp = findOut(word.strip())
        if tmp:
            if not tmp in result_find:
                result_find[tmp] = list()
            result_find[tmp].append(word.strip())
            result_simple.add(tmp)
    return result_find, result_simple


@csrf_exempt
def imageParse(req):
    if req.method == "POST":
        req_data = req.POST
        print(req_data)
        form = UploadFileForm(req.POST, req.FILES)
        if form.is_valid():
            newImage = ImageResult(Image=req.FILES['image'])
            newImage.save()
            print(newImage.Image.path)
            with open(newImage.Image.path, 'rb') as image:
                image_content = base64.b64encode(image.read())
            data = {
                'requests':
                    [
                        {
                            'image':
                                {
                                    "content":
                                        image_content.decode('UTF-8')
                                },
                            'features':
                                [
                                    {
                                        "type":
                                            "DOCUMENT_TEXT_DETECTION"
                                    }
                                ]
                        }
                    ]
            }

            res = requests.post(API_HOST, data=json.dumps(data))
            print(res.status_code)
            if res.status_code == 200:
                print(categories)
                tmp = dict()
                tmp['success'] = True
                tmp['text'] = res.json()['responses'][0]['textAnnotations'][0]['description']
                return JsonResponse(tmp)

    tmp = dict()
    tmp['success'] = False
    return JsonResponse(tmp)


@csrf_exempt
def imageAnalysis(req):
    if req.method == "POST":
        req_data = req.POST
        print(req_data)
        form = UploadFileForm(req.POST, req.FILES)
        if form.is_valid():
            newImage = ImageResult(Image=req.FILES['image'])
            newImage.save()
            print(newImage.Image.path)
            with open(newImage.Image.path, 'rb') as image:
                image_content = base64.b64encode(image.read())
            data = {
                'requests':
                    [
                        {
                            'image':
                                {
                                    "content":
                                        image_content.decode('UTF-8')
                                },
                            'features':
                                [
                                    {
                                        "type":
                                            "DOCUMENT_TEXT_DETECTION"
                                    }
                                ]
                        }
                    ]
            }

            res = requests.post(API_HOST, data=json.dumps(data))
            print(res.status_code)
            if res.status_code == 200:
                tmp = dict()
                text = res.json()['responses'][0]['textAnnotations'][0]['description']
                name_index = text.find("제품명")

                if name_index == -1:
                    tmp = dict()
                    tmp['success'] = False
                    tmp['code'] = 1
                    return JsonResponse(tmp)

                try:
                    tmp['name'] = text[name_index + 3:].split(':')[1].split('·')[0].strip()
                except:
                    tmp = dict()
                    tmp['success'] = False
                    tmp['code'] = 1
                    return JsonResponse(tmp)


                info_index = text.find("원재료명 및 원산지")

                if info_index == -1:
                    tmp = dict()
                    tmp['success'] = False
                    tmp['code'] = 1
                    return JsonResponse(tmp)

                find, simple = textAnalysis(text[info_index + 10:].split(':')[1])

                tmp['success'] = True
                tmp['simple'] = list(simple)
                tmp['find'] = find
                return JsonResponse(tmp)

    tmp = dict()
    tmp['success'] = False
    return JsonResponse(tmp)
