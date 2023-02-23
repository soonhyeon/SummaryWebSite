from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import torch
from transformers import BartForConditionalGeneration,PreTrainedTokenizerFast
from . import models


# Create your views here.
def index(request):
    
    lists = models.database.objects.all()
    data = {"lists":lists}
    
    return render(request, 'tpl.html', data)

def kobart_summary(text):
    tokenizer = PreTrainedTokenizerFast.from_pretrained('digit82/kobart-summarization')
    model = BartForConditionalGeneration.from_pretrained('digit82/kobart-summarization')

    text = text.replace('\n', ' ')
    raw_input_ids = tokenizer.encode(text)
    input_ids = [tokenizer.bos_token_id] + raw_input_ids + [tokenizer.eos_token_id]
    
    summary_ids = model.generate(torch.tensor([input_ids]),  num_beams=4,  max_length=512,  eos_token_id=1)
    summerized_sentence = tokenizer.decode(summary_ids.squeeze().tolist(), skip_special_tokens=True)
    return summerized_sentence

def kobart_summ(request):
    text = request.POST['content']
    summerized_sentence = kobart_summary(text)
    
    article = models.database(before_text = text, after_text = summerized_sentence)
    article.save()
    
    return HttpResponseRedirect(reverse('main'))

def kobart_edit(request, idx):
    lists = models.database.objects.get(id=idx)
    data = {"article":lists}
    return render(request, 'edit.html', data)

def edit(request):
    idx = request.POST['idx']
    text = request.POST['content']
    summerized_sentence = kobart_summary(text)
    
    db_article = models.database.objects.get(id=idx)
    db_article.before_text = text 
    db_article.after_text = summerized_sentence
    db_article.save()
    return HttpResponseRedirect(reverse('main'))

def delete(request, idx):
    article = models.database.objects.get(id=idx)
    article.delete()
    return HttpResponseRedirect(reverse('main'))
    
    
    