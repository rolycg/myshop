from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Category, Product
from cart.forms import CartAddProductForm
from .recommender import Recommender
from django.utils import translation


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category,
                                     translations__language_code=request.LANGUAGE_CODE,
                                     translations__slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'base_new.html', {'category': category,
                                             'categories': categories,
                                             'products': products})


@require_POST
def set_language(request):
    _next = request.POST['next']
    if not _next:
        _next = request.environ['HTTP_REFERER'].split('?')[0]
    translation.activate(request.POST['language'])
    request.session[translation.LANGUAGE_SESSION_KEY] = request.POST['language']
    return HttpResponseRedirect(_next)


def product_detail(request, id, slug):
    language = request.LANGUAGE_CODE
    product = get_object_or_404(Product,
                                id=id,
                                translations__language_code=language,
                                translations__slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    # r = Recommender()
    # recommended_products = r.suggest_products_for([product], 4)
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,
                   'recommended_products': []})


def search(request):
    language = request.LANGUAGE_CODE
    raise NotImplemented()


def login(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category,
                                     translations__language_code=request.LANGUAGE_CODE,
                                     translations__slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'login.html', {'category': category,
                                          'categories': categories,
                                          'products': products})


def signup(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category,
                                     translations__language_code=request.LANGUAGE_CODE,
                                     translations__slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'register.html', {'category': category,
                                             'categories': categories,
                                             'products': products})


def all_products(request):
    language = request.LANGUAGE_CODE
    raise NotImplemented()
