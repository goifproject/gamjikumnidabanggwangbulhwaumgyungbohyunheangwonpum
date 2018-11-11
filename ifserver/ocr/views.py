from django.http import JsonResponse
import base64
from django.views.decorators.csrf import csrf_exempt
import requests, json, os, base64

from .forms import UploadFileForm
from .models import ImageResult

API_HOST = 'https://vision.googleapis.com/v1/images:annotate?key=AIzaSyA36WzCJokOlopsdqNOiLk-Y-NBuI8fJPc'

categories = [
  {
    "곡/견과류": [
      {
        "peanut": [
          "땅콩"
        ]
      },
      {
        "buckwheat": [
          "메밀"
        ]
      },
      {
        "walnut": [
          "호두"
        ]
      },
      {
        "almond": [
          "아몬드"
        ]
      },
      {
        "wheat": [
          "밀가루"
        ]
      }
    ]
  },
  {
    "과실/채소/버섯류": [
      {
        "cucumber": [
          "오이",
          "피클"
        ]
      },
      {
        "tomato": [
          "토마토"
        ]
      },
      {
        "carrot": [
          "당근"
        ]
      },
      {
        "peach": [
          "복숭아"
        ]
      },
      {
        "mushroom": [
          "버섯"
        ]
      }
    ]
  },
  {
    "육류": [
      {
        "beef": [
          "쇠고기",
          "쇠갈비",
          "등심",
          "송아지고기",
          "목심",
          "사태",
          "설도",
          "안심",
          "양지",
          "우둔",
          "채끝",
          "쇠고기",
          "허파",
          "간혀",
          "사골"
        ]
      },
      {
        "pork": [
          "돼지",
          "순대"
        ]
      },
      {
        "chicken": [
          "닭"
        ]
      },
      {
        "allMeat": [
          "등심",
          "송아지고기",
          "목심",
          "사태",
          "설도",
          "안심",
          "양지",
          "우둔",
          "채끝",
          "허파",
          "간혀",
          "사골",
          "돼지",
          "순대",
          "닭",
          "육류",
          "고기",
          "개구리",
          "다리",
          "거위",
          "살코기",
          "복부정육",
          "비계",
          "염장품",
          "꼬리",
          "가슴",
          "갈비",
          "달팽이",
          "육수"
        ]
      }
    ]
  },
  {
    "해조/어패류": [
      {
        "shrimp": [
          "새우",
          "대하"
        ]
      },
      {
        "clam": [
          "조개",
          "오징어",
          "낙지",
          "꼴뚜기"
        ]
      },
      {
        "mackerel": [
          "고등어"
        ]
      },
      {
        "crab": [
          "게",
          "젓"
        ]
      }
    ]
  },
  {
    "우유/동물성유지류": [
      {
        "milk": [
          "우유"
        ]
      },
      {
        "cheese": [
          "치즈"
        ]
      },
      {
        "cream": [
          "크림"
        ]
      },
      {
        "butter": [
          "버터",
          "우지",
          "쇠기름",
          "돈지"
        ]
      },
      {
        "oil": [
          "버터",
          "우지",
          "쇠기름",
          "돈지",
          "닭기름",
          "돼지기름",
          "생선기름"
        ]
      },
      {
        "allAnimals": [
          "유제품",
          "유지류",
          "우유",
          "치즈",
          "크림",
          "버터",
          "우지",
          "쇠기름",
          "돈지",
          "버터",
          "닭기름",
          "돼지기름",
          "생선기름"
        ]
      }
    ]
  },
  {
    "알": [
      {
        "allEgg":[
          "달걀"
        ]
      }
    ]
  },
  {
    "주류": [
      {
        "allAlcohol":[
          "알콜"
        ]
      }
    ]
  }
]



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
    print(words)
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
                print(image_content)
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
            print(data)

            res = requests.post(API_HOST, data=json.dumps(data))
            print(res.status_code)
            if res.status_code == 200:
                tmp = dict()
                text = res.json()['responses'][0]['textAnnotations'][0]['description']
                # name_index = text.find("제품명")
                #
                # if name_index == -1:
                #     tmp = dict()
                #     tmp['success'] = False
                #     tmp['code'] = 1
                #     return JsonResponse(tmp)
                #
                # try:
                #     tmp['name'] = text[name_index + 3:].split(':')[1].split('·')[0].strip()
                # except:
                #     tmp = dict()
                #     tmp['success'] = False
                #     tmp['code'] = 1
                #     return JsonResponse(tmp)


                info_index = text.find("원재료")

                if info_index == -1:
                    tmp = dict()
                    tmp['success'] = False
                    tmp['code'] = 1
                    return JsonResponse(tmp)
                if ' '.join(text[info_index + 10:].split(':')[1:]).find("·") != -1:
                    tmp2 = ' '.join(text[info_index + 10:].split(':')[1:]).split("·")[0]
                elif ' '.join(text[info_index + 10:].split(':')[1:]).find("●") != -1:
                    tmp2 = ' '.join(text[info_index + 10:].split(':')[1:]).split("●")[0]
                else:
                    tmp2 = ' '.join(text[info_index + 10:].split(':')[1:])

                find, simple = textAnalysis(tmp2)

                tmp['success'] = True
                tmp['simple'] = list(simple)
                tmp['find'] = find
                return JsonResponse(tmp)

    tmp = dict()
    tmp['success'] = False
    return JsonResponse(tmp)


@csrf_exempt
def base64Analysis(req):
    if req.method == "POST":
        req_data = json.loads(req.body.decode("utf-8"))
        image_content = req_data["base64"].split(',')[1]
        data = {
            'requests':
                [
                    {
                        'image':
                            {
                                "content":
                                    image_content
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

        print(data)

        res = requests.post(API_HOST, data=json.dumps(data))
        print(res.status_code)
        if res.status_code == 200:
            tmp = dict()
            print(res.json())
            text = res.json()['responses'][0]['textAnnotations'][0]['description']


            info_index = text.find("원재료")

            if info_index == -1:
                tmp = dict()
                tmp['success'] = False
                tmp['code'] = 1
                return JsonResponse(tmp)
            if ' '.join(text[info_index + 3:].split(':')[1:]).find("·") != -1:
                tmp2 = ' '.join(text[info_index + 3:].split(':')[1:]).split("·")[0]
            elif ' '.join(text[info_index + 3:].split(':')[1:]).find("●") != -1:
                tmp2 = ' '.join(text[info_index + 3:].split(':')[1:]).split("●")[0]
            else:
                tmp2 = ' '.join(text[info_index + 3:].split(':')[1:])

            find, simple = textAnalysis(tmp2)

            tmp['success'] = True
            tmp['simple'] = list(simple)
            tmp['find'] = find
            return JsonResponse(tmp)

    tmp = dict()
    tmp['success'] = False
    return JsonResponse(tmp)