# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from tinymce.models import HTMLField

class Lesson(models.Model):
    number = models.IntegerField(u'Numero', help_text=u'Tehtävän järjestysnumero')
    name = models.CharField(u'Nimi', max_length=32, help_text=u'Tehtävän nimi')
    description = HTMLField(u'Kuvaus', help_text=u'Tehtävän kuvaus')
    expect = models.TextField(u'Odotettu vastaus', blank=True, help_text=u'Odotettu vastaus')
    LESSON_TYPES = (
        (0, u'Ohjelmointitehtävä'),
        (1, u'Esseetehtävä'),
    )
    type = models.IntegerField(u'Tyyppi', choices=LESSON_TYPES, default=0, help_text=u'Tehtävän tyyppi')
    max_score = models.IntegerField(u'Pistemäärä', help_text=u'Tehtävästä saatava maksimipistemäärä')
    
    def __unicode__(self):
        return "#%d %s" % (self.number, self.name)
    
    def is_answered(self, user):
        try:
            Answer.objects.get(lesson=self, user=user)
        except Answer.DoesNotExist:
            return False
        return True
    
    def format_answer_score(self, user):
        if self.get_status(user) < 4 and self.get_status(user) != 2:
            return "-"
        try:
            answer = Answer.objects.get(lesson=self, user=user)
            return u"%d / %d" % (answer.get_score(), self.max_score)
        except Answer.DoesNotExist:
            return u"%d / %d" % (0, self.max_score)
    
    def get_status(self, user):
        # Get answer object, if it exists
        try:
            answer = Answer.objects.get(lesson=self, user=user)
        except Answer.DoesNotExist:
            answer = None
        
        # Decide on status
        if answer and answer.status == 3:
            return 4
        elif answer and answer.status == 2:
            return 3
        elif answer and answer.status == 1:
            return 2
        elif answer and answer.status == 0:
            return 1
        else:
            return 0
    
    def format_status(self, user):
        status = self.get_status(user)
        # Decide on status
        if status == 4:
            return u"Suoritettu."
        elif status == 3:
            return u"Tehtävässä korjattavaa!"
        elif status == 2:
            return u"Suoritettu, automaattitarkastettu."
        elif status == 1:
            return u"Aloitettu, kesken."
        else:
            return u"Tekemättä."
        
    class Meta:
        verbose_name=u"tehtävä"
        verbose_name_plural=u"tehtävät"

class Answer(models.Model):
    user = models.ForeignKey(User, verbose_name=u'Käyttäjä')
    lesson = models.ForeignKey(Lesson, verbose_name=u'Tehtävä')
    result = models.TextField(u'Vastaus')
    score = models.IntegerField(u'Pistemäärä', blank=True, null=True, 
                                help_text=u'Lopullinen pistemäärä. Aseta tämä vain, jos järjestelmän laskema pistemäärä on väärä.')
    advice = HTMLField(u'Muuta', help_text=u'Opettajan viestikenttä')
    STATUS_TYPES = (
        (0, u'Kesken.'),
        (1, u'Tehty, automaattitarkastettu.'),
        (2, u'Tarkastettu, korjattavaa.'),
        (3, u'Tarkastettu, OK.')
    )
    status = models.IntegerField(u'Tila', choices=STATUS_TYPES, default=0, help_text=u'Vastauksen tila')

    def __unicode__(self):
        return u"%s: %s %s" % (self.lesson.name, self.user.first_name, self.user.last_name)
        
    def get_score(self):
        if self.score:
            return self.score
        elif self.status == 3 or self.status == 1:
            total = self.lesson.max_score
            for u in HintUsage.objects.filter(answer=self):
                total = total - u.hint.value
            return total
        else:
            return 0
        
    class Meta:
        verbose_name=u"vastaus"
        verbose_name_plural=u"vastaukset"

        
class Hint(models.Model):
    name = models.CharField(u'Nimi', max_length=32)
    lesson = models.ForeignKey(Lesson, verbose_name=u'Tehtävä johon neuvo liittyy')
    description = HTMLField(u'Neuvo', help_text=u'Neuvon kuvausteksti')
    value = models.IntegerField(u'Neuvon hinta', help_text=u'Kuinka paljon pisteitä neuvo maksaa')
    level = models.IntegerField(u'Neuvon numero', help_text=u'Monesko neuvo on kyseessä')
    
    def __unicode__(self):
        return "%s: #%d %s" % (self.lesson.name, self.level, self.name)
        
    class Meta:
        verbose_name=u"neuvo"
        verbose_name_plural=u"neuvot"
     
class HintUsage(models.Model):
    hint = models.ForeignKey(Hint)
    answer = models.ForeignKey(Answer)
    
    def __unicode__(self):
        return u"%s %s - %s" % (self.answer.user.first_name, self.answer.user.last_name, self.hint.name)
        
    class Meta:
        verbose_name=u"neuvokäyttö"
        verbose_name_plural=u"neuvokäytöt"
        unique_together = (("hint", "answer"),)

try:
    admin.site.register(Lesson)
    admin.site.register(Answer)
    admin.site.register(Hint)
except:
    pass
