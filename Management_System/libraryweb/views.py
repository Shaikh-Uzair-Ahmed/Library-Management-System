from django.shortcuts import render,redirect,get_object_or_404
import json
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic import ListView,DetailView,FormView,TemplateView,View
from django.urls import reverse
from .forms import BookRequestForm,SignUpForm,ResetPasswordForm,SignInForm,ProfileEditForm
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.forms import SetPasswordForm
from .models import LibraryUser,BookMain,Request
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.views.generic.list import ListView
from django.contrib.auth.hashers import check_password


class ProfileView(TemplateView):
    template_name = 'libraryweb/main/profile.html'

    def get_context_data(self, **kwargs):
        # Get the context from the parent class
        context = super().get_context_data(**kwargs)
        
        # Get lib_num from the URL
        lib_num = self.kwargs.get('lib_num', None)
        
        # Add lib_num to the context
        context['lib_num'] = lib_num

        try:
            # Get the LibraryUser associated with the lib_num
            library_user = get_object_or_404(LibraryUser, lib_num=lib_num)
            user = library_user.user

            # Check if the user is active
            if not user.is_active or not library_user.is_active:
                print("User is not active, redirecting to signin")
                messages.error(self.request, "Your account is inactive. Please sign in again.")
                return redirect('libraryweb:signout')

            # Add user and library_profile to the context
            context['user'] = user
            context['library_profile'] = library_user

        except Exception as e:
            # Log and handle unexpected errors
            print(f"Unexpected error: {e}")
            messages.error(self.request, "An error occurred while loading your profile.")
            return redirect('libraryweb:signout')

        return context

class UpdateProfileView(View):
    def post(self, request, *args, **kwargs):
        lib_num = kwargs.get('lib_num')
        try:
            library_user = LibraryUser.objects.get(lib_num=lib_num)
            # Parse JSON data from the request body
            data = json.loads(request.body)
            fav_genre = data.get('fav_genre')

            if fav_genre:
                library_user.fav_genre = fav_genre
                library_user.save()
                # Send success response with profile URL
                profile_url = reverse('libraryweb:profile', kwargs={'lib_num': lib_num})
                return JsonResponse({'success': True, 'redirect_url': profile_url})
            
            profile_url = reverse('libraryweb:profile', kwargs={'lib_num': lib_num})
            return JsonResponse({'success': False , 'redirect_url': profile_url})
        except LibraryUser.DoesNotExist:
            return JsonResponse({'success': False})

def check_user_status(request):
    """
    Helper function to check if the user associated with lib_num is active.
    If not, it redirects to the signout page.
    """
    lib_num = request.session.get('lib_num', None)

    if lib_num:
        try:
            # Check if the LibraryUser exists and if the associated user is active
            library_user = LibraryUser.objects.get(lib_num=lib_num)
            user = library_user.user

            if not user.is_active:
                # If the user is inactive, redirect to signout or sign-in page
                return redirect('libraryweb:signout')

        except LibraryUser.DoesNotExist:
            # Redirect if no LibraryUser is found
            return redirect('libraryweb:signout')

        except Exception as e:
            # Handle other unexpected errors
            print(f"Unexpected error: {e}")
            return redirect('libraryweb:signout')

    return None
    

def custom_authenticate(username, password):
    """
    Custom authentication function to authenticate a user by username and password.

    Args:
        username (str): The username of the user.
        password (str): The plaintext password of the user.

    Returns:
        User: The authenticated user object if credentials are valid.
        None: If authentication fails.
    """
    try:
        # Find the user by username
        user = User.objects.get(username=username)
        
        # Check if the password is correct
        if check_password(password, user.password):
            # Return the user if credentials are valid
            return user
        else:
            return None
    except User.DoesNotExist:
        # Return None if the user does not exist
        return None


def error_404(request, exception=None):
    lib_num = request.session.get('lib_num', None)
    return render(request,'error404.html',{'lib_num': lib_num}, status=404)

def error_500(request):
    lib_num = request.session.get('lib_num', None)
    return render(request,'error500.html',{'lib_num': lib_num}, status=500)


#from django.utils.decorators import method_decorator
#from django.views.decorators.csrf import csrf_exempt
#from django.http import JsonResponse
#from django.views.decorators.http import require_POST
#from django.shortcuts import get_object_or_404

# Create your views here.
def Home_Page(request, lib_num):
    try:

        library_user = LibraryUser.objects.get(lib_num=lib_num)
        

        user = library_user.user
        

        if not user.is_active:
            return redirect('libraryweb:signout')

        # Example popular books data
        popular_books = [
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Fiction", "isbn": "9780743273565", "cover_url": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1677887611i/71102288.jpg"},
    {"title": "1984", "author": "George Orwell", "genre": "Dystopian", "isbn": "9780451524935", "cover_url": "https://example.com/path-to-1984-cover.jpg"},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Fiction", "isbn": "9780061120084", "cover_url": "https://example.com/path-to-mockingbird-cover.jpg"},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "genre": "Romance", "isbn": "9780141439518", "cover_url": "https://example.com/path-to-pride-prejudice-cover.jpg"},
    {"title": "Moby-Dick", "author": "Herman Melville", "genre": "Adventure", "isbn": "9781503280786", "cover_url": "https://example.com/path-to-moby-dick-cover.jpg"},
    {"title": "War and Peace", "author": "Leo Tolstoy", "genre": "Historical Fiction", "isbn": "9781853260629", "cover_url": "https://example.com/path-to-war-peace-cover.jpg"},
    {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "genre": "Fiction", "isbn": "9780316769488", "cover_url": "https://example.com/path-to-catcher-rye-cover.jpg"},
    {"title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "genre": "Fantasy", "isbn": "9780544003415", "cover_url": "https://d28hgpri8am2if.cloudfront.net/book_images/onix/cvr9781608873821/the-lord-of-the-rings-9781608873821_hr.jpg"},
    {"title": "Crime and Punishment", "author": "Fyodor Dostoevsky", "genre": "Psychological Fiction", "isbn": "9780140449136", "cover_url": "https://example.com/path-to-crime-punishment-cover.jpg"},
    {"title": "Brave New World", "author": "Aldous Huxley", "genre": "Dystopian", "isbn": "9780060850524", "cover_url": "https://example.com/path-to-brave-new-world-cover.jpg"},
    ]  # Your books data here

        return render(request, 'libraryweb/main/home.html', {'popular_books': popular_books, 'lib_num': lib_num})
    
    except LibraryUser.DoesNotExist:
        return redirect('libraryweb:signout')
    
    except Exception as e:
        return redirect('libraryweb:signout')

#in home page we will use for loop to take out data, later this will be done by real database

    

def Notification(request,lib_num):#will turn this also into listview later 
    try:
        library_user = LibraryUser.objects.get(lib_num=lib_num)
        user = library_user.user

        if not user.is_active:
            print("User is not active, redirecting to signin")
            return redirect('libraryweb:signout')
    
    except LibraryUser.DoesNotExist:
        print(f"No LibraryUser found with lib_num: {lib_num}")
        return redirect('libraryweb:signout')
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return redirect('libraryweb:signout')
    return render(request,'libraryweb/main/notifications.html',{'lib_num': lib_num})


#Future reference
"""def notification_count(request):
    # Placeholder for logic to get the actual count of unchecked notifications
    # Replace with your own logic, e.g., querying from the database
    unchecked_count = 3  # Example count
    return JsonResponse({'count': unchecked_count})


@require_POST
def update_notification_status(request):
    notification_id = request.POST.get('notification_id')
    notification = get_object_or_404(Notification, id=notification_id)
    notification.is_checked = True
    notification.save()
    unchecked_count = Notification.objects.filter(is_checked=False).count()
    return JsonResponse({'count': unchecked_count})"""

class SearchPageView(ListView):
    model = BookMain
    context_object_name = "books"
    paginate_by = 10
    template_name = 'libraryweb/main/search.html'

    def get_queryset(self):
    # Get the search query from the request
        query = self.request.GET.get("query", "")

        # Query the database
        if query:
            return BookMain.objects.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query) |
                Q(genre__icontains=query) |
                Q(isbn__icontains=query)
            ).order_by("title")  # Add ordering by title (or any other field)
    
        return BookMain.objects.all().order_by("title") 

    def get_context_data(self, **kwargs):
        # Get the context from the parent class
        context = super().get_context_data(**kwargs)
        
        # Get lib_num from the URL
        lib_num = self.kwargs.get('lib_num', None)
        
        # Add lib_num to the context
        context['lib_num'] = lib_num

        # Check if the user exists and is active
        try:
            library_user = LibraryUser.objects.get(lib_num=lib_num)
            user = library_user.user
            
            if not user.is_active:
                print("User is not active, redirecting to signin")
                return redirect('libraryweb:signout')
                
        except LibraryUser.DoesNotExist:
            print(f"No LibraryUser found with lib_num: {lib_num}")
            return redirect('libraryweb:signout')
        
        except Exception as e:
            print(f"Unexpected error: {e}")
            return redirect('libraryweb:signout')

        return context

    

    
class DetailPage(DetailView):
    model = BookMain
    context_object_name = "bookdetail"
    template_name = "libraryweb/main/detail.html"

    def get_object(self):
        # Retrieve the ISBN from the URL
        isbn = self.kwargs.get("isbn")
        
        # Fetch the book from the database
        try:
            book = BookMain.objects.get(isbn=isbn)
        except BookMain.DoesNotExist:
            raise Http404("Book Not Found")

        # Check if availability data exists for the book
        availability = getattr(book, 'availability', None)

        # Add availability information to the book object
        if availability:
            book.total_books = availability.total_books
            book.available_books = availability.available_books
            book.remaining_books = availability.remaining_books  # Access the remaining_books property
            book.earliest_return = availability.earliest_return()  # Access the earliest_return method
        else:
            # Default values if no availability data is present
            book.total_books = 0
            book.available_books = 0
            book.remaining_books = 0
            book.earliest_return = None

        return book

    def get_context_data(self, **kwargs):
        # Get the context from the parent class
        context = super().get_context_data(**kwargs)
        
        # Get lib_num from the URL
        lib_num = self.kwargs.get('lib_num', None)
        
        # Add lib_num to the context
        context['lib_num'] = lib_num

        # Check if the user exists and is active
        try:
            library_user = LibraryUser.objects.get(lib_num=lib_num)
            user = library_user.user
            
            if not user.is_active:
                print("User is not active, redirecting to signin")
                return redirect('libraryweb:signout')
                
        except LibraryUser.DoesNotExist:
            print(f"No LibraryUser found with lib_num: {lib_num}")
            return redirect('libraryweb:signout')
        
        except Exception as e:
            print(f"Unexpected error: {e}")
            return redirect('libraryweb:signout')

        return context
     

class RequestSuccessView(TemplateView):
    template_name = 'libraryweb/main/success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the 'isbn' from the query parameters
        
        # Get the 'lib_num' from the session or query parameters
        lib_num = self.request.session.get('lib_num', self.request.GET.get('lib_num'))
        
        # Add 'isbn' and 'lib_num' to the context
        context['lib_num'] = lib_num
        
        return context

def book_request_view(request, lib_num):
    # Create the form instance
    if request.method == 'POST':
        form = BookRequestForm(request.POST)
        
        if form.is_valid():
            # Extract cleaned data from the form
            title = form.cleaned_data['title']
            isbn = form.cleaned_data.get('isbn')

            # Query the database for a book matching the title or ISBN
            try:
                # Try to get the book from the BookMain model by title or ISBN
                book = BookMain.objects.get(isbn=isbn)
                
                # Redirect to the detail page if the book is found
                return redirect(reverse('libraryweb:detail', args=[lib_num,book.isbn]))
            
            except BookMain.DoesNotExist:
                # If the book is not found, create a Request instance and save it
                library_user = LibraryUser.objects.get(lib_num=lib_num)
                
                # Create a new Request record
                new_request = Request(
                    user=library_user,
                    isbn=isbn,
                    title=title,
                    author=form.cleaned_data.get('author'),
                )
                new_request.save()  # Save the request to the database

                # Redirect to the success page with the ISBN
                return redirect(reverse('libraryweb:success', args=[lib_num,isbn]))
        
        else:
            # If the form is invalid, re-render the form with error messages
            return render(request, 'libraryweb/main/request.html', {'form': form})

    else:
        form = BookRequestForm()  # Empty form for GET request

    # Check user status before rendering
    redirect_response = check_user_status(request)
    if redirect_response:
        return redirect_response

    # Get lib_num from the session or URL
    lib_num = request.session.get('lib_num', None)

    # Render the request page with the form and context
    return render(request, 'libraryweb/main/request.html', {
        'form': form,
        'lib_num': lib_num
    })






class CreditsView(TemplateView):
    template_name="libraryweb/main/credits.html"   

class SignInView(FormView):
    template_name = 'libraryweb/auth/signin.html'
    form_class = SignInForm

    def form_valid(self, form):
        # Extract username and password from the form
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        # Authenticate the user
        user = custom_authenticate(username=username, password=password)


        if user and hasattr(user, 'library_profile'):
            # If the user is authenticated, log them in
            if not user.is_active or not user.library_profile.is_active:
                user.is_active = True
                user.library_profile.is_active = True
                user.save()
                user.library_profile.save()
                self.request.session['lib_num'] = user.library_profile.lib_num

            login(self.request, user)
            return redirect('libraryweb:home', lib_num=user.library_profile.lib_num)
        else:
            # Invalid credentials
            messages.error(self.request, "Invalid username or password.")
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)
    

class SignUpView(FormView):
    template_name = 'libraryweb/auth/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('libraryweb:signin')

    def form_valid(self, form):
        user = form.save()  # Save the user instance
        LibraryUser.objects.create(user=user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


def reset_password(request):
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            lib_num = form.cleaned_data['lib_num']
            new_password = form.cleaned_data['new_password1']

            try:
                # Check if the user exists with the provided username and lib_num
                user = User.objects.get(username=username)
                userlib = LibraryUser.objects.get(lib_num=lib_num)

                if userlib:
                
                # Update the user's password
                    user.set_password(new_password)
                    user.save()

                    messages.success(request, "Your password has been successfully updated.")
                    return redirect('libraryweb:signin')  # Redirect to login page after success
            except User.DoesNotExist and LibraryUser.DoesNotExist:
                messages.error(request, "No matching user found with the provided Username and LIB Number.")
    else:
        form = ResetPasswordForm()

    return render(request, 'libraryweb/auth/forgot_password.html', {'form': form})



def sign_out(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Set the user's 'is_active' status to False
        user = request.user
        user.is_active = False
        if hasattr(user, 'library_profile'):
            user.library_profile.is_active = False
            user.library_profile.save()
        user.save()
        # Clear the user's session data
        request.session.flush()
        # Log the user out
        logout(request)

    # Redirect to the sign-in page after logging out
    return redirect('libraryweb:signin')
