import csv

numberList = []
questionList = []
alphaList = []
betaList = []
gammaList = []
deltaList = []
question_answers = []


class Admin:
    all = []
    admins = {}
    methods = ['make questions', 'delete all questions', 'make new questions file', 'create new admin', 'log out']
    fileList = ['testQuestions.csv']
    n = 0
    i = 0

    def __init__(self, username, password):
        self.username = username
        self.password = password

        Admin.all.append(self)
        Admin.admins[self.username] = password


# class to assign questions to answers
class Question:
    def __init__(self, num, prompt, alpha1, beta1, gamma1, delta1, ans):
        self.num = num
        self.prompt = prompt
        self.alpha = alpha1
        self.beta = beta1
        self.gamma = gamma1
        self.delta = delta1
        self.ans = ans


# convert questions in csv file to array
with open(f'{Admin.fileList[Admin.n]}', 'r') as f:
    reader = csv.DictReader(f)
    items = list(reader)

for item in items:
    n = item.get('number')
    q = item.get('questions')
    al = item.get('alpha')
    be = item.get('beta')
    ga = item.get('gamma')
    de = item.get('delta')
    ar = item.get('answer')

    numberList.append(n)
    questionList.append(q)
    alphaList.append(al)
    betaList.append(be)
    gammaList.append(ga)
    deltaList.append(de)
    question_answers.append(ar)

testQuestions = [
    Question(numberList[n], questionList[n], alphaList[n], betaList[n], gammaList[n], deltaList[n], question_answers[n])
    for n in range(0, len(questionList))
]
currentTest = testQuestions
