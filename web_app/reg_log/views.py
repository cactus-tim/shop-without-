from django.shortcuts import render


def reg_log(request):
    return render(request, 'reg_log/reg_log.html')


def reg(request):
    return render(request, 'reg_log/reg.html')


def log(request):
    return render(request, 'reg_log/log.html')

def footer(request):
    return render(request,'reg_log/footer.html')
