

from contacts.storage import get_storage


def validate_borrower(user_id, contact_id, lending_id, reply_address):
    # Ensure contact exists
