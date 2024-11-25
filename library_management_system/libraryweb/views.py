from django.shortcuts import render,redirect
from django.http import Http404
from django.views.generic import ListView,DetailView,FormView,TemplateView
from django.urls import reverse
from .forms import BookRequestForm,SignUpForm,ResetPasswordForm,SignInForm
from django.http import HttpResponseServerError
from django.urls import reverse_lazy
from django.contrib.auth.forms import SetPasswordForm
from .models import User
from django.contrib import messages
from django.contrib.auth import login,logout


def error_404(request, exception=None):
    return render(request,'error404.html', status=404)

def error_500(request):
    return render(request,'error500.html', status=500)


def authenticate_by_username(username, password):
    if not username or not password:
        return None  # Early return if username or password is empty
    
    try:
        # Find user by username
        user = User.objects.get(username=username)
        
        # Check if the password matches
        if user.check_password(password):
            return user
        else:
            return None  # Return None if password does not match
    except User.DoesNotExist:
        return None  # Return None if no user is found with the given username

#from django.utils.decorators import method_decorator
#from django.views.decorators.csrf import csrf_exempt
#from django.http import JsonResponse
#from django.views.decorators.http import require_POST
#from django.shortcuts import get_object_or_404

# Create your views here.

#in home page we will use for loop to take out data, later this will be done by real database
def Home_Page(request,lib_num):
    try:
        lib_num = request.session.get('lib_num')

        if lib_num:
        # Optionally, fetch user details using lib_num if needed
            user = User.objects.get(lib_num=lib_num)
            if not user.is_active:
                return redirect('libraryweb:signin') 
        
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
    ]
        return render(request,'libraryweb/main/home.html',{'popular_books':popular_books,'lib_num': lib_num})
    except User.DoesNotExist:
        # Handle case where the user does not exist in the database
        return redirect('libraryweb:signin')
    except Exception as e:
        # Log the unexpected error for debugging
        print(f"Unexpected error: {e}")
        return redirect('libraryweb:signin')

    

def Notification(request,lib_num):#will turn this also into listview later 
    try:
        lib_num = request.session.get('lib_num')

        if lib_num:
        # Optionally, fetch user details using lib_num if needed
            user = User.objects.get(lib_num=lib_num)
            if not user.is_active:
                return redirect('libraryweb:signin') 
    
    except Exception:
        return redirect('libraryweb:signin')
    return render(request,'libraryweb/main/notifications.html')

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
    try:
        BOOKS_DATA = [
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
        {"title": "The Divine Comedy", "author": "Dante Alighieri", "genre": "Epic Poetry", "isbn": "9780142437223", "cover_url": "https://example.com/divine-comedy.jpg"},
        {"title": "The Brothers Karamazov", "author": "Fyodor Dostoevsky", "genre": "Philosophical", "isbn": "9780374528379", "cover_url": "https://example.com/brothers-karamazov.jpg"},
        {"title": "Les Misérables", "author": "Victor Hugo", "genre": "Historical Fiction", "isbn": "9780451419439", "cover_url": "https://example.com/les-miserables.jpg"},
        {"title": "Anna Karenina", "author": "Leo Tolstoy", "genre": "Romantic Fiction", "isbn": "9780143035008", "cover_url": "https://example.com/anna-karenina.jpg"},
        {"title": "Wuthering Heights", "author": "Emily Brontë", "genre": "Gothic", "isbn": "9780486292563", "cover_url": "https://example.com/wuthering-heights.jpg"},
        {"title": "The Iliad", "author": "Homer", "genre": "Epic", "isbn": "9780140275360", "cover_url": "https://example.com/iliad.jpg"},
        {"title": "Dracula", "author": "Bram Stoker", "genre": "Horror", "isbn": "9780486411094", "cover_url": "https://example.com/dracula.jpg"},
        ]
        context_object_name = "books"
        paginate_by = 10
        template_name = 'libraryweb/main/search.html'


        def get_queryset(self):
            # Get the search query from the request
            query = self.request.GET.get("query", "")
            
            # Filter the temporary data
            filtered_books = [
                book for book in self.BOOKS_DATA
                if query.lower() in book["title"].lower()
                or query.lower() in book["author"].lower()
                or query.lower() in book["genre"].lower()
                or query in book["isbn"]
            ]
            
            # Return the filtered data
            return filtered_books
        # Will be removed when database added later
    except Exception:
        pass

    
class DetailPage(DetailView):
    context_object_name="bookdetail"
    template_name='libraryweb/main/detail.html'
    BOOKS_DATA = [
        {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Fiction", "isbn": "9780743273565", "cover_url": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1677887611i/71102288.jpg", "total_books": 5, "borrowed_books": 2},
        {"title": "1984", "author": "George Orwell", "genre": "Dystopian", "isbn": "9780451524935", "cover_url": "https://example.com/path-to-1984-cover.jpg", "total_books": 8, "borrowed_books": 3},
        {"title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Fiction", "isbn": "9780061120084", "cover_url": "https://example.com/path-to-mockingbird-cover.jpg", "total_books": 6, "borrowed_books": 1},
        {"title": "Pride and Prejudice", "author": "Jane Austen", "genre": "Romance", "isbn": "9780141439518", "cover_url": "https://example.com/path-to-pride-prejudice-cover.jpg", "total_books": 7, "borrowed_books": 4},
        {"title": "Moby-Dick", "author": "Herman Melville", "genre": "Adventure", "isbn": "9781503280786", "cover_url": "https://example.com/path-to-moby-dick-cover.jpg", "total_books": 3, "borrowed_books": 1},
        {"title": "War and Peace", "author": "Leo Tolstoy", "genre": "Historical Fiction", "isbn": "9781853260629", "cover_url": "https://example.com/path-to-war-peace-cover.jpg", "total_books": 5, "borrowed_books": 2},
        {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "genre": "Fiction", "isbn": "9780316769488", "cover_url": "https://example.com/path-to-catcher-rye-cover.jpg", "total_books": 4, "borrowed_books": 3},
        {"title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "genre": "Fantasy", "isbn": "9780544003415", "cover_url": "https://d28hgpri8am2if.cloudfront.net/book_images/onix/cvr9781608873821/the-lord-of-the-rings-9781608873821_hr.jpg", "total_books": 10, "borrowed_books": 5},
        {"title": "Crime and Punishment", "author": "Fyodor Dostoevsky", "genre": "Psychological Fiction", "isbn": "9780140449136", "cover_url": "https://example.com/path-to-crime-punishment-cover.jpg", "total_books": 6, "borrowed_books": 2},
        {"title": "Brave New World", "author": "Aldous Huxley", "genre": "Dystopian", "isbn": "9780060850524", "cover_url": "https://example.com/path-to-brave-new-world-cover.jpg", "total_books": 4, "borrowed_books": 1},
        {"title": "The Divine Comedy", "author": "Dante Alighieri", "genre": "Epic Poetry", "isbn": "9780142437223", "cover_url": "https://example.com/divine-comedy.jpg", "total_books": 3, "borrowed_books": 1},
        {"title": "The Brothers Karamazov", "author": "Fyodor Dostoevsky", "genre": "Philosophical", "isbn": "9780374528379", "cover_url": "https://example.com/brothers-karamazov.jpg", "total_books": 7, "borrowed_books": 3},
        {"title": "Les Misérables", "author": "Victor Hugo", "genre": "Historical Fiction", "isbn": "9780451419439", "cover_url": "https://example.com/les-miserables.jpg", "total_books": 6, "borrowed_books": 2},
        {"title": "Anna Karenina", "author": "Leo Tolstoy", "genre": "Romantic Fiction", "isbn": "9780143035008", "cover_url": "https://example.com/anna-karenina.jpg", "total_books": 4, "borrowed_books": 2},
        {"title": "Wuthering Heights", "author": "Emily Brontë", "genre": "Gothic", "isbn": "9780486292563", "cover_url": "https://example.com/wuthering-heights.jpg", "total_books": 3, "borrowed_books": 1},
        {"title": "The Iliad", "author": "Homer", "genre": "Epic", "isbn": "9780140275360", "cover_url": "https://example.com/iliad.jpg", "total_books": 5, "borrowed_books": 2},
        {"title": "Dracula", "author": "Bram Stoker", "genre": "Horror", "isbn": "9780486411094", "cover_url": "https://example.com/dracula.jpg", "total_books": 4, "borrowed_books": 1}
    ]

    def get_object(self):
        # Retrieve the ISBN from the URL
        isbn = self.kwargs.get("isbn")
        
        # Search for the book in the hardcoded list
        book = next((book for book in self.BOOKS_DATA if book['isbn'] == isbn), None)

        if not book:
            raise Http404("Book Not Found")

        # Calculate available books
        book["available_books"] = book["total_books"] - book["borrowed_books"]
        
        return book
     

class RequestSuccessView(TemplateView):
    template_name = 'libraryweb/main/success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['isbn'] = self.request.GET.get('isbn') 
        return context
    
class BookRequestView(FormView):
    BOOKS_DATA = [
        {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Fiction", "isbn": "9780743273565", "cover_url": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1677887611i/71102288.jpg", "total_books": 5, "borrowed_books": 2},
        {"title": "1984", "author": "George Orwell", "genre": "Dystopian", "isbn": "9780451524935", "cover_url": "https://example.com/path-to-1984-cover.jpg", "total_books": 8, "borrowed_books": 3},
        {"title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Fiction", "isbn": "9780061120084", "cover_url": "https://example.com/path-to-mockingbird-cover.jpg", "total_books": 6, "borrowed_books": 1},
        {"title": "Pride and Prejudice", "author": "Jane Austen", "genre": "Romance", "isbn": "9780141439518", "cover_url": "https://example.com/path-to-pride-prejudice-cover.jpg", "total_books": 7, "borrowed_books": 4},
        {"title": "Moby-Dick", "author": "Herman Melville", "genre": "Adventure", "isbn": "9781503280786", "cover_url": "https://example.com/path-to-moby-dick-cover.jpg", "total_books": 3, "borrowed_books": 1},
        {"title": "War and Peace", "author": "Leo Tolstoy", "genre": "Historical Fiction", "isbn": "9781853260629", "cover_url": "https://example.com/path-to-war-peace-cover.jpg", "total_books": 5, "borrowed_books": 2},
        {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "genre": "Fiction", "isbn": "9780316769488", "cover_url": "https://example.com/path-to-catcher-rye-cover.jpg", "total_books": 4, "borrowed_books": 3},
        {"title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "genre": "Fantasy", "isbn": "9780544003415", "cover_url": "https://d28hgpri8am2if.cloudfront.net/book_images/onix/cvr9781608873821/the-lord-of-the-rings-9781608873821_hr.jpg", "total_books": 10, "borrowed_books": 5},
        {"title": "Crime and Punishment", "author": "Fyodor Dostoevsky", "genre": "Psychological Fiction", "isbn": "9780140449136", "cover_url": "https://example.com/path-to-crime-punishment-cover.jpg", "total_books": 6, "borrowed_books": 2},
        {"title": "Brave New World", "author": "Aldous Huxley", "genre": "Dystopian", "isbn": "9780060850524", "cover_url": "https://example.com/path-to-brave-new-world-cover.jpg", "total_books": 4, "borrowed_books": 1},
        {"title": "The Divine Comedy", "author": "Dante Alighieri", "genre": "Epic Poetry", "isbn": "9780142437223", "cover_url": "https://example.com/divine-comedy.jpg", "total_books": 3, "borrowed_books": 1},
        {"title": "The Brothers Karamazov", "author": "Fyodor Dostoevsky", "genre": "Philosophical", "isbn": "9780374528379", "cover_url": "https://example.com/brothers-karamazov.jpg", "total_books": 7, "borrowed_books": 3},
        {"title": "Les Misérables", "author": "Victor Hugo", "genre": "Historical Fiction", "isbn": "9780451419439", "cover_url": "https://example.com/les-miserables.jpg", "total_books": 6, "borrowed_books": 2},
        {"title": "Anna Karenina", "author": "Leo Tolstoy", "genre": "Romantic Fiction", "isbn": "9780143035008", "cover_url": "https://example.com/anna-karenina.jpg", "total_books": 4, "borrowed_books": 2},
        {"title": "Wuthering Heights", "author": "Emily Brontë", "genre": "Gothic", "isbn": "9780486292563", "cover_url": "https://example.com/wuthering-heights.jpg", "total_books": 3, "borrowed_books": 1},
        {"title": "The Iliad", "author": "Homer", "genre": "Epic", "isbn": "9780140275360", "cover_url": "https://example.com/iliad.jpg", "total_books": 5, "borrowed_books": 2},
        {"title": "Dracula", "author": "Bram Stoker", "genre": "Horror", "isbn": "9780486411094", "cover_url": "https://example.com/dracula.jpg", "total_books": 4, "borrowed_books": 1}
    ]
    template_name = 'libraryweb/main/request.html'
    form_class = BookRequestForm

    def form_valid(self, form):
        # Extract cleaned data from the form
        title = form.cleaned_data['title']
        isbn = form.cleaned_data.get('isbn')

        # Check if the book is available in the library
        for book in self.BOOKS_DATA:
            if book['title'] == title or (isbn and book['isbn'] == isbn):
                # If the book is found, redirect to the detail page
                return redirect(reverse('libraryweb:detail', args=[book['isbn']]))

        # If the book is not available, return a success page
        return redirect(f"{reverse('libraryweb:success')}?isbn={isbn}")

    def form_invalid(self, form):
        # If the form is invalid, re-render the form with error messages
        return super().form_invalid(form)

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
        user = authenticate_by_username(username=username, password=password)

        if user is not None:
            # If the user is successfully authenticated, set their account as active
            if not user.is_active:
                user.is_active = True
                user.save()

            # Log in the user after marking them as active
            login(self.request, user)
            self.request.session['lib_num'] = user.lib_num
            # Redirect to user's personalized homepage based on lib_num
            return redirect('libraryweb:home', lib_num=user.lib_num)

        else:
            # Invalid credentials
            messages.error(self.request, "Invalid username or password.")
            return self.form_invalid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

class SignUpView(FormView):
    template_name = 'libraryweb/auth/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('libraryweb:signin')

    def form_valid(self, form):
        form.save()  # Save the user instance
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
                user = User.objects.get(username=username, lib_num=lib_num)
                
                # Update the user's password
                user.set_password(new_password)
                user.save()

                messages.success(request, "Your password has been successfully updated.")
                return redirect('libraryweb:signin')  # Redirect to login page after success
            except User.DoesNotExist:
                messages.error(request, "No matching user found with the provided Username and LIB Number.")
    else:
        form = ResetPasswordForm()

    return render(request, 'libraryweb/auth/forgot_password.html', {'form': form})


def sign_out(request):
    # Set the user's 'is_active' status to False
    if request.user.is_authenticated:
        user = request.user
        user.is_active = False
        user.save()

    # Clear the user's session data (flush all session data)
    request.session.flush()

    # Log the user out (if using Django's built-in auth system)
    logout(request)

    # Redirect to the sign-in page after logging out
    return redirect('libraryweb:signin')

    
