"""
This middleware checks all auctions: Are they past their end date, do they have a winning bid.
TODO: Test me i veiws test "auction.winner = winning_bid.owner" < -- this happens
"""
from django.utils import timezone

from auctions.models import Auction, Bid


def check_auctions(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Before "response = get_response(request)"
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        auctions = Auction.objects.all()

        for auction in auctions:
            if timezone.now() > auction.end_date and auction.is_active:
                auction.is_active = False

                winning_bid = Bid.objects.all().filter(auction=auction).last()
                if winning_bid:
                    auction.winner = winning_bid.owner

                auction.save()

        response = get_response(request)

        # After "response = get_response(request)"
        # Code to be executed for each request/response after
        # the view is called.
        return response

    return middleware
