import random
import string
import datetime
from faker import Faker
import names
from fake_useragent import UserAgent
from Assets.emailHosts import weighted_email_domains


class FakeUser_Detailed:
    def __init__(self):
        self.fake = Faker()
        self.first_name = names.get_first_name()
        self.last_name = names.get_last_name()
        self.email = self.generate_random_email()
        self.password = self.generate_random_password()
        self.birthday = self.generate_birthday()
        self.address = self.generate_address()
        self.ssn = self.generate_id_based_on_state("US")
        self.credit_card = self.generate_credit_card()
        self.userAgent = self.generate_userAgent()

    def generate_random_email(self):
        # Generate email with combination of name and domain
        name = f"{self.first_name.lower()}{self.last_name.lower()}"
        use_number = random.choice([True, False])  # Renamed for clarity

        # Calculate cumulative weights
        cumulative_weights = []
        total_weight = 0
        for domain, weight in weighted_email_domains:
            total_weight += weight
            cumulative_weights.append((domain, total_weight))

        # Select domain based on cumulative weights
        random_number = random.randint(1, total_weight)
        for domain, cumulative_weight in cumulative_weights:
            if random_number <= cumulative_weight:
                selected_domain = domain
                break

        # Generate email with or without a number
        if use_number:
            return f"{name}{random.randint(1, 100)}{selected_domain}"
        else:
            return f"{name}{selected_domain}"

    def generate_random_password(self):
        # Generate password using uppercase, lowercase, numbers and special characters
        characters = string.ascii_letters + string.digits
        length = random.randint(12, 20)
        return "".join(random.choice(characters) for _ in range(length))

    def generate_birthday(self):
        start_date = datetime.date(1950, 1, 1)
        end_date = datetime.date(2003, 12, 31)
        random_date = start_date + datetime.timedelta(
            days=random.randint(0, (end_date - start_date).days)
        )
        return random_date.strftime("%Y-%m-%d")

    def generate_address(self):
        street_name = self.fake.street_name()
        city = self.fake.city()
        state = self.fake.state_abbr()
        zip_code = self.fake.zipcode_in_state(state)
        return f"{random.randint(1, 999)} {street_name}, {city}, {state}, {zip_code}"

    def generate_id_based_on_state(self, state_code):
        if state_code == "US":
            area = random.randint(100, 999)
            group = random.randint(10, 99)
            serial = random.randint(1000, 9999)
            return f"{area}-{group}-{serial}"
        else:
            raise ValueError(
                "Invalid state code. Only 'US' is supported for generating SSN."
            )

    def generate_credit_card(self):
        card_type = self.fake.credit_card_provider()
        card_type_map = {
            "Visa": "visa",
            "MasterCard": "mastercard",
            "American Express": "amex",
            "Discover": "discover",
            "Diners Club": "diners",
            "JCB": "jcb",
        }
        if card_type not in card_type_map:
            card_type = "Visa"  # default to Visa if type is unrecognized
        mapped_card_type = card_type_map[card_type]

        phony_cc_number = self.fake.credit_card_number(card_type=mapped_card_type)
        phony_cc_exp = self.fake.credit_card_expire()
        phony_cc_sec = self.fake.credit_card_security_code()
        return f"{card_type} - {phony_cc_number} - exp: {phony_cc_exp} - cvv: {phony_cc_sec}"

    def generate_userAgent(self):
        ua = UserAgent()
        return ua.random

    def get_info(self):
        return {
            "Name": f"{self.first_name} {self.last_name}",
            "Email": self.email,
            "Password": self.password,
            "Birthday": self.birthday,
            "Address": self.address,
            "SSN": self.ssn,
            "Credit Card": self.credit_card,
            "UserAgent": self.userAgent,
        }


def main():
    user = FakeUser_Detailed()
    user_info = user.get_info()

    print("Fake User Information:")
    for key, value in user_info.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
