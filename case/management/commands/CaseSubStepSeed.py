from django.core.management.base import BaseCommand
import sys
from sys import stdout
from case.models import CaseSubStep , CaseStep , CaseSubStepStatus
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):

    def handle(self, *args, **options):
        flush_table(CaseSubStep)
        create_sub_step()
def flush_table(model):
    stdout.write('Flushing data from CaseSubStep table...\n')
    table_name = model._meta.db_table
    with connection.cursor() as cursor:
        cursor.execute(f'TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE')
def create_sub_step():
    stdout.write("Creating CaseSubSteps....\n")
    steps = CaseStep.objects.order_by('order').all()
    substeps_data = [
        {
            'step': steps[0],
            'substeps': [
                {
                    'substep_name': 'ساخت پرونده',
                    'description': 'وارد کردن نام و نام خانوادگی',
                    'next': 2,
                    'doer': 'ADMIN',
                    'type': 'TEXT'
                },
                {
                    'substep_name': 'تکمیل پرونده',
                    'description': 'بارگذاری قرارداد، پاسپورت، عکس و تکمیل فرم اپلیکیشن',
                    'next': 3,
                    'doer': 'ADMIN',
                    'type': 'TEXT'
                },
                {
                    'substep_name': 'ارجاع کار به کارشناس',
                    'description': 'پس از واریز قسط اول قرارداد باید انجام گیرد',
                    'next': 4,
                    'doer': 'ADMIN',
                    'type': 'TEXT'
                },
                {
                    'substep_name': 'ساخت ایمیل کاری مشتری و ارسال آن به ادمین',
                    'description': 'ساخت ایمیل کاری مشتری توسط کارشناس و ارسال آن به ادمین به همراه کلمه عبور',
                    'next': 5,
                    'doer': 'EXPERT',
                    'type': 'TEXT'
                },
                {
                    'substep_name': 'ارسال اطلاعات به مشتری',
                    'description': 'اطلاعات عبارتند از:ایمیل ساخته شده به همراه کلمه عبور،لینک ثبت نام جهت احراز هویت، آموزش و راهنمایی جهت تکمیل فرم احراز هویت',
                    'next': 6,
                    'doer': 'ADMIN',
                    'type': 'TEXT'
                },
                {
                    'substep_name': 'دریافت ایمیل تاییدیه ثبت درخواست احراز هویت از مشتری',
                    'description': 'تکمیل و انجام مراحل احراز هویت توسط مشتری و ارسال ایمیل تاییدیه ثبت درخواست احراز هویت از مشتری به ادمین با ایمیل شخصی مشتری )حدود 2ساعت بعد از تکمیل فرم(',
                    'next': 7,
                    'doer': 'ADMIN',
                    'type': 'TEXT'
                }
            ]
        },
        {
            'step': steps[1],
            'substeps': [
                {
                    'substep_name': 'شروع مراحل اداری ثبت شرکت',
                    'description': 'ارسال و ارجاع کار از ادمین به کارشناس جهت شروع مراحل اداری ثبت شرکت',
                    'next': 8,
                    'doer': 'ADMIN',
                    'type': 'TEXT'
                }
            ]
        },
        {
            'step': steps[2],
            'substeps': [
                {
                    'substep_name': 'ثبت CR',
                    'description': 'ثبت CR و تحویل مدارک به مکتب سند توسط کارشناس',
                    'next': 9,
                    'doer': 'EXPERT',
                    'type': 'TEXT'
                },
                {
                    'substep_name': 'ارسال ایمیل ثبت  CR به ادمین ',
                    'description': 'ارسال ایمیل ثبت CR توسط کارشناس به ادمین',
                    'next': 10,
                    'doer': 'EXPERT',
                    'type': 'TEXT'
                },
                {
                    'substep_name': 'تایید حصول نتیجه CR',
                    'description': 'نوتیفیکیشن و اعلان به کارشناس جهت پیگیری CR یا اسم شرکت 2روز بعد از ثبت CR تا زمان حصول نتیجه و تایید توسط کارشناس (حداکثر 3روز)',
                    'next': 11,
                    'doer': 'EXPERT',
                    'type': 'TEXT'
                },
                {
                    'substep_name': 'ارسال CR نهایی به ادمین',
                    'description': 'ارسال CR نهایی توسط کارشناس به ادمین',
                    'next': 12,
                    'doer': 'EXPERT',
                    'type': 'FILE'
                },
                {
                    'substep_name': 'ارسال CR نهایی به مشتری',
                    'description': 'ارسال CR نهایی توسط ادمین به مشتری توسط ایمیل شخصی',
                    'next': 13,
                    'doer': 'ADMIN',
                    'type': 'TEXT'
                }
            ]
        },
        {
        'step': steps[3],
        'substeps': [
            {
                'substep_name': 'شروع فرآیند دریافت لایسنس',
                'description': 'ارائه شماره کارت بانکی مشتری به مکتب سند جهت شروع فرآیند دریافت لایسنس توسط کارشناس',
                'next': 14,
                'doer': 'EXPERT',
                'type': 'TEXT'
            },
            {
                'substep_name': 'تایید حصول نتیجه ثبت لایسنس',
                'description': 'نوتیفیکیشن و اعلان به کارشناس جهت پیگیری لایسنس 2روز بعد از ثبت لایسنس تا زمان حصول نتیجه و تایید توسط کارشناس (حداکثر10روز)',
                'next': 15,
                'doer': 'EXPERT',
                'type': 'TEXT'
            },
            {
                'substep_name': 'ارسال لایسنس به ادمین',
                'description': 'ارسال لایسنس توسط کارشناس به ادمین',
                'next': 16,
                'doer': 'EXPERT',
                'type': 'FILE'
            },
            {
                'substep_name': 'ارسال لایسنس به مشتری با ایمیل شرکت',
                'description': 'ارسال لایسنس توسط ادمین به مشتری با ایمیل شرکت',
                'next': 17,
                'doer': 'ADMIN',
                'type': 'TEXT'
            },
        ]
        },
        {
            'step': steps[4],
            'substeps': [
                {
                    'substep_name': 'ثبت درخواست ماذونیه',
                    'description': 'ثبت درخواست ماذونیه در مکتب سند توسط کارشناس',
                    'next': 18,
                    'doer': 'EXPERT',
                    'type': 'TEXT'
                },
                {
                    'substep_name': 'ارسال ایمیل تاییدیه ثبت درخواست ماذونیه به ادمین',
                    'description': 'ارسال ایمیل تاییدیه ثبت درخواست ماذونیه توسط کارشناس به ادمین',
                    'next': 19,
                    'doer': 'EXPERT',
                    'type': 'TEXT'
                },
                {
                    'substep_name': 'تایید حصول نتیجه ماذونیه',
                    'description': 'نوتیفیکیشن و اعلان به کارشناس جهت پیگیری فاکتور ماذونیه 2روز بعد از ثبت ماذونیه تا زمان حصول نتیجه و تایید توسط کارشناس(حداکثر15روز)',
                    'next': 20,
                    'doer': 'EXPERT',
                    'type': 'TEXT'
                },
                {
                    'substep_name': 'ارسال فاکتور ماذونیه به ادمین',
                    'description': 'ارسال فاکتور ماذونیه توسط کارشناس به ادمین',
                    'next': 21,
                    'doer': 'EXPERT',
                    'type': 'FILE'
                },
                {
                    'substep_name': 'ارسال فاکتور ماذونیه به مشتری',
                    'description': 'ارسال فاکتور ماذونیه توسط ادمین به مشتری',
                    'next': 22,
                    'doer': 'ADMIN',
                    'type': 'TEXT'
                },
                {
                    'substep_name': 'تایید پرداخت قسط دوم',
                    'description': 'اعلان به ادمین جهت پیگیری پرداخت قسط دوم 1روز بعد از ارسال ایمیل فاکتور ماذونیه تا زمان حصول نتیجه و تایید توسط ادمین (حداکثر15روز)',
                    'next': 23,
                    'doer': 'ADMIN',
                    'type': 'TEXT'
                },
                {
                    'substep_name': 'دریافت فیش واریزی ماذونیه از مشتری',
                    'description': 'ارسال فیش واریزی ماذونیه توسط مشتری به ادمین با ایمیل شخصی به ایمیل شرکت',
                    'next': 24,
                    'doer': 'ADMIN',
                    'type': 'TEXT'
                },
                {
                    'substep_name': 'ارسال فیش واریزی مشتری به مدیر حسابداری یا مدیر',
                    'description': 'ارسال فیش واریزی مشتری توسط ادمین به مدیر حسابداری یا مدیر جهت واریز مبلغ به حساب کارشناس',
                    'next': 25,
                    'doer': 'ADMIN',
                    'type': 'FILE'
                },
                {
                    'substep_name': 'دریافت تایید پرداخت از مدیر یا مدیر حسابداری',
                    'description': 'تایید پرداخت مدیر حسابداری یا مدیر به ادمین درخصوص واریز وجه به حساب کارشناس',
                    'next': 26,
                    'doer':'ADMIN',
                    'type': 'TEXT'
                },
                {
                    'substep_name': 'دستور ادامه کار به کارشناس جهت پرداخت فیش ماذونیه',
                    'description': 'دستور ادامه کار توسط ادمین به کارشناس جهت پرداخت فیش ماذونیه',
                    'next': 27,
                    'doer': 'ADMIN',
                    'type': 'TEXT'
                },
                {
                    'substep_name': 'ارسال ماذونیه مشتری به ادمین',
                    'description': 'ارسال ماذونیه مشتری از کارشناس به ادمین',
                    'next': 28,
                    'doer': 'EXPERT',
                    'type': 'FILE'
                },
                {
                    'substep_name': 'ارسال ماذونیه به مشتری با ایمیل شرکت',
                    'description': 'ارسال ماذونیه توسط ادمین به مشتری با ایمیل شرکت',
                    'next': 29,
                    'doer': 'ADMIN',
                    'type': 'TEXT'
                }
            ]
        },
        {
            'step': steps[5],
            'substeps': [
                {
                    'substep_name': 'شروع مراحل اخذ ویزا در مکتب سند',
                    'description': 'شروع مراحل اخذ ویزا توسط کارشناس در مکتب سند',
                    'next': 30,
                    'doer': 'EXPERT',
                    'type': 'TEXT'
                },
                {
                    'substep_name': 'تایید حصول نتیجه ثبت ویزا',
                    'description': 'نوتیفیکیشن و اعلان به کارشناس جهت پیگیری ویزا 2روز بعد از ثبت ویزا تا زمان حصول نتیجه و تایید توسط کارشناس (حداکثر10روز)',
                    'next': 31,
                    'doer': 'EXPERT',
                    'type': 'TEXT'
                },
                {
                    'substep_name': 'دریافت و ارسال ویزا به ادمین',
                    'description': 'دریافت و ارسال ویزا توسط کارشناس به ادمین',
                    'next': 32,
                    'doer': 'EXPERT',
                    'type': 'FILE'
                },
                {
                    'substep_name': 'ارسال ویزا به مشتری',
                    'description': 'ارسال ویزا توسط ادمین به مشتری با ایمیل شرکت و همچنین هماهنگی جهت تهیه و خرید بلیط براساس تقویم کشور عمان (یک هفته قبل از خرید بلیط با کارشناس هماهنگی صورت گیرد.)',
                    'next': 33,
                    'doer': 'ADMIN',
                    'type': 'TEXT'
                }
            ]
        },
        {
          'step': steps[6],
          'substeps': [
              {
                  'substep_name': 'هماهنگی خرید بلیط با کارشناس',
                  'description': 'تاریخ بلیت بر اساس تقویم کشور عمان هماهنگ شود و در ایمیل گفته شود سیمکارت در فرودگاه عمان خریداری شود',
                  'next': 34,
                  'doer': 'ADMIN',
                  'type': 'TEXT'
              },
              {
                  'substep_name': 'دریافت بلیط از مشتری',
                  'description': 'ارسال بلیط توسط مشتری به ادمین با ایمیل شخصی به ایمیل شرکت',
                  'next': 35,
                  'doer': 'ADMIN',
                  'type': 'TEXT'
              },
              {
                  'substep_name': 'ارسال بلیط به کارشناس',
                  'description': 'ارسال بلیط توسط ادمین به کارشناس',
                  'next': 36,
                  'doer': 'ADMIN',
                  'type': 'FILE'
              },
              {
                  'substep_name': 'دریافت مدارک مشتری',
                  'description': 'بعد از ورود مشتری به فرودگاه عمان ارسال عکس مهر ورود پاسپورت به همراه شماره موبایل خریداری شده با ایمیل شخصی به ایمیل شرکت',
                  'next': 37,
                  'doer': 'ADMIN',
                  'type': 'TEXT'
              },
              {
                  'substep_name': 'ارسال اطلاعات ورود به کارشناس',
                  'description': 'ارسال عکس مهر ورود پاسپورت به همراه شماره موبایل خریداری شده توسط ادمین به کارشناس',
                  'next': 38,
                  'doer': 'ADMIN',
                  'type': 'FILE'
              }
          ]
        },
        {
          'step': steps[7],
          'substeps':[
              {
                'substep_name': 'مراجعه به مکتب سند و دریافت نامه پزشکی',
                'description': 'مراجعه به مکتب سند و دریافت نامه پزشکی توسط کارشناس',
                'next': 39,
                'doer': 'EXPERT',
                'type': 'TEXT'
              },
              {
                'substep_name': 'ارسال نامه پزشکی به ادمین',
                'description': 'ارسال نامه پزشکی و گزارش مشکل احتمالی توسط کارشناس به ادمین',
                'next': 40,
                'doer': 'EXPERT',
                'type': 'FILE'
              },
              {
                'substep_name': 'هماهنگی با مشتری جهت حضور در مراکز درمانی جهت انجام آزمایشات',
                'description': 'هماهنگی با مشتری جهت حضور در مراکز درمانی جهت انجام آزمایشات',
                'next': 41,
                'doer': 'EXPERT',
                'type': 'TEXT'
              },
              {
                'substep_name': 'اعلام هماهنگی جهت انجام آزمایشات به ادمین',
                'description': 'اعلام هماهنگی جهت انجام آزمایشات توسط کارشناس به ادمین',
                'next': 42,
                'doer': 'EXPERT',
                'type': 'TEXT'
              },
              {
                'substep_name': 'اعلام حضور مشتری در مرکز درمانی جهت انجام آزمایشات به ادمین',
                'description': 'اعلام حضور مشتری در مرکز درمانی جهت انجام آزمایشات توسط کارشناس به ادمین',
                'next': 43,
                'doer': 'EXPERT',
                'type': 'TEXT'
              },
              {
                'substep_name': 'اعلام انجام آزمایشات در مرکز درمانی به ادمین',
                'description': 'اعلام انجام آزمایشات در مرکز درمانی توسط کارشناس به ادمین',
                'next': 44,
                'doer': 'EXPERT',
                'type': 'TEXT'
              },
              {
                'substep_name': 'دریافت و ارسال جواب آزمایشات مشتری به ادمین',
                'description': 'دریافت و ارسال جواب آزمایشات مشتری توسط کارشناس به ادمین',
                'next': 45,
                'doer': 'EXPERT',
                'type': 'FILE'
              },
          ]
        },
        {
        'step': steps[8],
        'substeps': [
            {
                'substep_name': 'تهیه و دریافت مدارک از مکتب سند جهت صدور CARD ID',
                'description': 'تهیه و دریافت مدارک )CR، ماذونیه به زبان عربی و جواب آزمایش( از مکتب سند جهت صدور CARD ID',
                'next': 46,
                'doer': 'EXPERT',
                'type': 'TEXT'
            },
            {
                'substep_name': 'اعلام دریافت مدارک از مکتب سند جهت صدور CARD ID به ادمین',
                'description': 'اعلام دریافت مدارک از مکتب سند جهت صدور CARD ID توسط کارشناس',
                'next': 47,
                'doer': 'EXPERT',
                'type': 'TEXT'
            },
            {
                'substep_name': 'هماهنگی با مشتری درخصوص مراجعه به پلیس مهاجرت ',
                'description': 'هماهنگی با مشتری درخصوص مراجعه به پلیس مهاجرت جهت انجام مراحل صدور CARD ID',
                'next': 48,
                'doer': 'EXPERT',
                'type': 'TEXT'
            },
            {
                'substep_name': 'اعلام هماهنگی با مشتری جهت مراجعه به پلیس مهاجرت به ادمین',
                'description': 'اعلام هماهنگی با مشتری جهت مراجعه به پلیس مهاجرت توسط کارشناس به ادمین',
                'next': 49,
                'doer': 'EXPERT',
                'type': 'TEXT'
            },
            {
                'substep_name': ' مراجعه به پلیس مهاجرت جهت انجام مراحل صدور CARD ID',
                'description': ' مراجعه به پلیس مهاجرت جهت انجام مراحل صدور CARD ID',
                'next': 50,
                'doer': 'EXPERT',
                'type': 'TEXT'
            },
            {
                'substep_name': 'اعلام مراجعه به پلیس مهاجرت جهت انجام مراحل صدور CARD ID به ادمین',
                'description': 'اعلام مراجعه به پلیس مهاجرت جهت انجام مراحل صدور CARD ID توسط کارشناس به ادمین',
                'next': 51,
                'doer': 'EXPERT',
                'type': 'TEXT'
            },
            {
                'substep_name': 'دریافت ID CARD مشتری',
                'description': 'دریافت ID CARD مشتری',
                'next': 52,
                'doer': 'EXPERT',
                'type': 'TEXT'
            },
            {
                'substep_name': 'ارسال عکس ID CARD مشتری به ادمین',
                'description': 'ارسال عکس ID CARD مشتری توسط کارشناس به ادمین',
                'next': 53,
                'doer': 'EXPERT',
                'type': 'FILE'
            },
        ]
        },
        {
        'step':steps[9],
        'substeps':[
            {
                'substep_name': ' هماهنگی با مشتری جهت افتتاح حساب بانکی',
                'description': ' هماهنگی با مشتری جهت افتتاح حساب بانکی',
                'next': 54,
                'doer': 'EXPERT',
                'type': 'TEXT'
            },
            {
                'substep_name': 'اعلام هماهنگی با مشتری جهت افتتاح حساب بانکی',
                'description': 'اعلام هماهنگی با مشتری جهت افتتاح حساب بانکی',
                'next': 55,
                'doer': 'EXPERT',
                'type': 'TEXT'
            },
            {
                'substep_name': 'اعلام حضور مشتری در بانک جهت افتتاح حساب بانکی به ادمین',
                'description': 'اعلام حضور مشتری در بانک جهت افتتاح حساب بانکی توسط کارشناس به ادمین',
                'next': 56,
                'doer': 'EXPERT',
                'type': 'TEXT'
            },
            {
                'substep_name': 'افتتاح حساب بانکی مشتری',
                'description': 'افتتاح حساب بانکی مشتری',
                'next': 57,
                'doer': 'EXPERT',
                'type': 'TEXT'
            },
            {
                'substep_name': 'اعلام به مشتری جهت مراجعه مجدد به بانک',
                'description': 'اعلام به مشتری جهت مراجعه مجدد به بانک سه روز کاری پس از افتتاح حساب جهت دریافت کارت بانکی',
                'next': 58,
                'doer': 'EXPERT',
                'type': 'TEXT'
            },
            {
                'substep_name': 'اعلام نهایی شدن و افتتاح حساب بانکی مشتری به ادمین',
                'description': 'اعلام نهایی شدن و افتتاح حساب بانکی مشتری توسط کارشناس به ادمین',
                'next': None,
                'doer': 'EXPERT',
                'type': 'TEXT'
            },
        ]
        }
    ]

    for data in substeps_data:
        step = data['step']
        for substep in data['substeps']:
            CaseSubStep.objects.create(
                substep_name=substep['substep_name'],
                step=step,
                type=substep['type'],
                description=substep['description'],
                doer=substep['doer'],
            )

    # Set previous and next fields for CaseSubStep instances
    substeps = list(CaseSubStep.objects.all())
    for i, substep in enumerate(substeps):
        substep.next_id = substeps[i + 1].id if i < len(substeps) - 1 else None
        substep.save()
    first = CaseSubStep.objects.first()
    first.is_start = True
    first.save()

