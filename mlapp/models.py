from django.db import models

# Create your models here.
from datetime import date


# こちらでテーブルの中身を定義します
class Customer(models.Model):
  # 選択式のものはここで定義します（左：実際にDBに格納される値、右：UIに表示される値）
  education_options = (
  (1, 'graduate_school'),
  (2, 'university'),
  (3, 'high school'),
  (4, 'other'),
  )

  marriage_options = (
  (1, 'married'),
  (2, 'single'),
  (3, 'others')
  )

  # DBのカラムに相当する部分の定義
  id = models.AutoField(primary_key=True)
  last_name = models.CharField('名字', max_length=30)
  first_name = models.CharField('名前', max_length=30)
  limit_balance = models.IntegerField('残高', default=100000) # default : デフォルト値の設定
  education = models.IntegerField('学歴', choices=education_options, default=0)
  marriage = models.IntegerField('結婚歴', choices=marriage_options, default=0)
  age = models.IntegerField('年齢')
  result = models.IntegerField(blank=True, null=True) #null(空白）を許可する設定、この場合 blank=True にしないとエラーになる
  proba = models.FloatField(default=0.0)
  comment = models.CharField(max_length=200, blank=True, null=True)
  registered_date = models.DateField(default=date.today()) #default=date.today() : 本日の日付をデフォルトに設定

  # 管理画面に表示方法を定義：必須項目が入っているかどうかで表示内容を分ける
  # %s:文字列,%d:数値
  def __str__(self):
    if self.proba == 0.0:
      return '%s,%s' % (self.registered_date.strftime('%Y-%m-%d'), self.last_name+self.first_name)
    else:
      return '%s, %s, %d, %s' % (self.registered_date.strftime('%Y-%m-%d'), self.last_name+self.first_name, self.result, self.comment)