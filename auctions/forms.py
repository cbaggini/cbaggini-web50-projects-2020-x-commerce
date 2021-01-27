from django.forms import ModelForm, Textarea, HiddenInput
from .models import Listing, User, Bid, Comment

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['creator', 'title', 'description', 'starting_bid', 
            'imageURL', 'category']
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 20}),
            'creator': HiddenInput(),
        }

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['listing', 'amount', 'bid_user']
        widgets = {'listing': HiddenInput(),
                'bid_user': HiddenInput(),
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['listing', 'text', 'author']
        widgets = {
            'text': Textarea(attrs={'cols': 20, 'rows': 10}),
            'listing': HiddenInput(),
            'author': HiddenInput(),
        }

