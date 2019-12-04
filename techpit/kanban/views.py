from django.shortcuts import render
from django.contrib.auth import login # 追加
from django.contrib.auth.forms import UserCreationForm # 追加
from django.shortcuts import render, redirect # redirectをインポート
from django.contrib.auth.decorators import login_required # 追加
from django.contrib.auth.models import User # 追加
from django.views.generic import DetailView # 追加
from django.shortcuts import render, redirect, resolve_url # resolve_urlを追加
from django.views.generic import DetailView, UpdateView # 追加
from .forms import UserForm, ListForm, CardForm # 追記
from .mixins import OnlyYouMixin # 忘れずにインポートする
from django.contrib.auth.mixins import LoginRequiredMixin # 追加
from django.urls import reverse_lazy # 追加
from django.views.generic import DetailView, UpdateView, CreateView # 追加
from .forms import UserForm, ListForm # 追加
from .models import List, Card # 追記
from django.views.generic import DetailView, UpdateView, CreateView, ListView # 追加
from django.views.generic import DetailView, UpdateView, CreateView, ListView, DeleteView # 追加
from django.shortcuts import render, redirect, resolve_url, get_object_or_404 # get_object_or_404を追加
from .forms import UserForm, ListForm, CardForm, CardCreateFromHomeForm # CardCreateFromHomeFormを追加

# Create your views here.

# 以下を追記
from django.http import HttpResponse


def index(request):
    return render(request, "kanban/index.html")

def home(request):
    return render(request, "kanban/home.html")

# ここから追加
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user_instance = form.save()
            login(request, user_instance)
            return redirect("kanban:home")
    else:
        form = UserCreationForm()

    context = {
        "form": form
    }
    return render(request, 'kanban/signup.html', context)
# ここまで追加

class HomeView(LoginRequiredMixin, ListView):
    model = List
    template_name = "kanban/home.html"

class UserDetailView(LoginRequiredMixin, DetailView): # 編集
    model = User
    template_name = "kanban/users/detail.html"

class UserUpdateView(OnlyYouMixin, UpdateView): # この行のみ編集
    model = User
    template_name = "kanban/users/update.html"
    form_class = UserForm

    def get_success_url(self):
        return resolve_url('kanban:users_detail', pk=self.kwargs['pk'])

class ListCreateView(LoginRequiredMixin, CreateView):
    model = List
    template_name = "kanban/lists/create.html"
    form_class = ListForm
    success_url = reverse_lazy("kanban:lists_list") # 変更

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ListListView(LoginRequiredMixin, ListView):
    model = List
    template_name = "kanban/lists/list.html"

class ListDetailView(LoginRequiredMixin, DetailView):
    model = List
    template_name = "kanban/lists/detail.html"

class ListUpdateView(LoginRequiredMixin, UpdateView):
    model = List
    template_name = "kanban/lists/update.html"
    form_class = ListForm

class ListDeleteView(LoginRequiredMixin, DeleteView):
    model = List
    template_name = "kanban/lists/delete.html"
    form_class = ListForm
    success_url = reverse_lazy("kanban:lists_list")

class CardCreateView(LoginRequiredMixin, CreateView):
    model = Card
    template_name = "kanban/cards/create.html"
    form_class = CardForm
    success_url = reverse_lazy("kanban:cards_list") # 変更

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CardListView(LoginRequiredMixin, ListView):
    model = Card
    template_name = "kanban/cards/list.html"

class CardDetailView(LoginRequiredMixin, DetailView):
    model = Card
    template_name = "kanban/cards/detail.html"

class CardUpdateView(LoginRequiredMixin, UpdateView):
    model = Card
    template_name = "kanban/cards/update.html"
    form_class = CardForm

class CardDeleteView(LoginRequiredMixin, DeleteView):
    model = Card
    template_name = "kanban/cards/delete.html"
    form_class = CardForm
    success_url = reverse_lazy("kanban:cards_list")

class CardCreateFromHomeView(LoginRequiredMixin, CreateView):
    model = Card
    template_name = "kanban/cards/create.html"
    form_class = CardCreateFromHomeForm
    success_url = reverse_lazy("kanban:home")

    def form_valid(self, form):
        list_pk = self.kwargs['list_pk']
        list_instance = get_object_or_404(List, pk=list_pk)
        form.instance.list = list_instance
        form.instance.user = self.request.user
        return super().form_valid(form)