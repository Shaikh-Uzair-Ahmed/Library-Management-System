from django.db import models,transaction
from django.db.models import Avg
from django.contrib.auth.models import AbstractUser
from datetime import datetime,timedelta
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class LibNumCounter(models.Model):
    current_number = models.PositiveIntegerField(default=0)#Makes database faster in case of many users
    #being created at once hence this table to keep track of count is created

class User(AbstractUser):
    lib_num = models.CharField(max_length=15, unique=True, primary_key=True)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='libraryweb_users',  # Custom related name
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='libraryweb_users',  # Custom related name
        blank=True,
        help_text='Specific permissions for this user.'
    )

    def save(self, *args, **kwargs):
        if not self.lib_num:
            with transaction.atomic():
                current_year = datetime.now().year
                # Find the last user of the current year
                last_user = User.objects.filter(lib_num__startswith=f"{current_year}LIB").order_by('-lib_num').first()
                if last_user:
                    last_number = int(last_user.lib_num[8:]) + 1  # Extract the numeric part
                else:
                    last_number = 1
                self.lib_num = f"{current_year}LIB{last_number:04d}"  # Format: YYYYLIB0001
        super().save(*args, **kwargs)

class BookMain(models.Model):
    id = models.AutoField(primary_key=True)
    isbn = models.CharField(max_length=13, unique=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=50)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)

    @property
    def average_rating(self):
        return self.ratings.aggregate(average=Avg('rating'))['average'] or 0

    def __str__(self):
        return self.title
    
class AvailBooks(models.Model):
    book = models.OneToOneField(BookMain, on_delete=models.CASCADE, related_name="availability")
    total_books = models.PositiveIntegerField(default=0)
    available_books = models.PositiveIntegerField(default=0)

    @property
    def remaining_books(self):
        return self.total_books - self.available_books

    def __str__(self):
        return f"{self.book.title}: {self.available_books}/{self.total_books}"
    
class UserBorrowed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrowed_books")
    book = models.ForeignKey(AvailBooks, on_delete=models.CASCADE, related_name="borrowed_instances")
    borrow_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Check if the user is already borrowing 3 books
        if self.user.borrowed_books.count() >= 3:
            raise ValidationError("A user can only borrow a maximum of 3 books at a time.")
        
        # Check if the book is available
        if self.book.remaining_books == 0:
            raise ValueError("Book is not available for borrowing.")
        
        # Decrease the available books
        self.book.available_books -= 1
        self.book.save()
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.lib_num} borrowed {self.book.book.title}"
    

class LateFees(models.Model):
    user_borrowed = models.OneToOneField(UserBorrowed, on_delete=models.CASCADE, related_name="late_fee")
    days_late = models.PositiveIntegerField(default=0)
    fee = models.PositiveIntegerField(default=0)

    def calculate_fees(self):
        due_date = self.user_borrowed.borrow_date + timedelta(days=7)
        if now() > due_date:
            self.days_late = (now() - due_date).days
            self.fee = self.days_late * 50
        else:
            self.days_late = 0
            self.fee = 0
        self.save()

    def __str__(self):
        return f"Late Fee for {self.user_borrowed.user.lib_num}: ₹{self.fee}"
    

class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="book_requests")
    isbn = models.CharField(max_length=13)
    title = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.lib_num} requested {self.title or 'unknown book'}" #if no title returns unknown book
    

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings") #inside user and bookmain table
    #rating table can be queried using ratings as the table name
    book = models.ForeignKey(BookMain, on_delete=models.CASCADE, related_name="ratings")
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)])  # 0-5 scale
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book') #each user can only review once per book

    def __str__(self):
        return f"{self.user.lib_num} rated {self.book.title} - {self.rating}"