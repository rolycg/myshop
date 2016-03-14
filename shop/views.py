from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.utils.translation import gettext_lazy as _
from .models import Category, Product, MyUser
from cart.forms import CartAddProductForm
from django.core.urlresolvers import reverse
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
    return render(request, 'shop/base_new.html', {'category': category,
                                                  'categories': categories,
                                                  'products': products})


@require_POST
def set_language(request):
    _next = request.POST['next']
    if not _next:
        _next = get_refer(request)
    translation.activate(request.POST['language'])
    request.session[translation.LANGUAGE_SESSION_KEY] = request.POST['language']
    return HttpResponseRedirect(_next)


def get_refer(request):
    return request.environ['HTTP_REFERER'].split('?')[0]


def update_context(context):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    return context.update({
        'categories': categories,
        'products': products,
    })


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


def login(request):
    if request.method == 'GET':
        context = update_context({})
        return render(request, 'login.html', context)
    elif request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            try:
                user = MyUser.objects.get(user__username=username)
                if user.check_password(password):
                    request.session['username'] = user.username
                    request.session['password'] = user.password
                    return HttpResponseRedirect(reverse('shop:product_list'))
                else:
                    context = {'error': _('Wrong username or password')}
                    context = update_context(context)
                    return render(request, 'login.html', context)
            except MyUser.DoesNotExist:
                context = {'error': _('Wrong username or password')}
                context = update_context(context)
                return render(request, 'login.html', context)
        except KeyError:
            context = {'error': _('No username or password')}
            context = update_context(context)
            return render(request, 'login.html', context)
    else:
        raise Http404()


def signup(request):
    if request.method == 'GET':
        context = update_context({})
        return render(request, 'register.html', context)
    elif request.method == 'POST':
        try:
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            password2 = request.POST['confirm_password']
            password = request.POST['password']
            if password == password2:
                user = MyUser.objects.create(first_name=first_name, username=email, email=email,
                                             password=password, last_name=last_name)
                request.session['username'] = user.username
                request.session['password'] = user.password
                user.save()
                return HttpResponseRedirect(reverse('shop:product_list'))
            else:
                context = {'error': _('Passwords aren\'t the same!!!')}
                context = update_context(context)
                return render(request, 'register.html', context)
        except KeyError:
            context = {'error': _('No username or password')}
            context = update_context(context)
            return render(request, 'register.html', context)

    else:
        raise Http404()


def all_products(request):
    language = request.LANGUAGE_CODE
    raise NotImplemented()
