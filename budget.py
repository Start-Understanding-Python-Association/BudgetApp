class Category:
    """All of the stuff needed for a budget."""
    def __init__(self, name):
        self.ledger = []
        self.name = name

    def __str__(self):
        self.title_line = list('*' * 30)
        s = ''
        count = 0
        self.body = ''
        for i in self.name:
            self.title_line[15 - int(len(self.name) / 2) + count] = i
            count = count + 1
        for i in self.ledger:
            description = i["description"]
            description = description[:23]
            if len(description) < 23:
                description = description + (23 - len(description)) * ' '
            amount = i["amount"]
            amount = '{:.2f}'.format(amount)[:7]
            if len(amount) < 7:
                amount = (7 - len(amount)) * ' ' + amount
            self.body = self.body + description + amount + '\n'
        self.total = str(round(self.get_balance(), 2))
        return s.join(self.title_line) + '\n' + self.body + 'Total: ' + self.total

    def deposit(self, amount, description=''):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        else:
            return False

    def get_balance(self):
        bal = 0
        for i in self.ledger:
            bal = bal + i["amount"]
        return bal

    def transfer(self, amount, other_category):
        if self.check_funds(amount):
            self.withdraw(amount, 'Transfer to ' + other_category.name)
            other_category.deposit(amount, 'Transfer from ' + self.name)
            return True
        else:
            return False

    def check_funds(self, amount):
        if amount > self.get_balance():
            return False
        else:
            return True


def create_spend_chart(categories):
    withdrawal_total = 0
    withdrawal_itemized = []
    withdrawal_percentages = []
    full_statement = ''
    for i in categories:  # find the total withdrawals within each category and the grand total withdrawals
        cat_withdrawal_total = 0
        for j in i.ledger:
            if j["amount"] < 0:
                cat_withdrawal_total = cat_withdrawal_total - j["amount"]
        withdrawal_itemized.append(cat_withdrawal_total)
        withdrawal_total = withdrawal_total + cat_withdrawal_total

    for i in withdrawal_itemized:  # find the withdrawal percentages
        withdrawal_percentages.append(i / withdrawal_total * 100)

    line_width = 5 + 3 * len(categories)
    count_down = 100
    full_statement = full_statement + 'Percentage spent by category' + '\n'
    while count_down >= 0:
        line = ''
        if len(str(count_down)) == 3:
            line = line + str(count_down)
        if len(str(count_down)) == 2:
            line = line + ' ' + str(count_down)
        if len(str(count_down)) == 1:
            line = line + '  ' + str(count_down)
        line = line + '| '
        for i in withdrawal_percentages:
            if i >= count_down:
                line = line + 'o  '
            else:
                line = line + '   '
        full_statement = full_statement + line + '\n'
        count_down = count_down - 10
    full_statement = full_statement + '    ' + '-' * (line_width - 4) + '\n'

    name_lengths = []
    for i in categories:
        name_lengths.append(len(str(i.name)))
    longest_category_name = max(name_lengths)

    count_up_for_vertical_letters = 0
    while count_up_for_vertical_letters < longest_category_name:
        line = '     '
        for i in categories:
            if count_up_for_vertical_letters < len(i.name):
                line = line + i.name[count_up_for_vertical_letters] + '  '
            else:
                line = line + '   '
        full_statement = full_statement + line + '\n'
        count_up_for_vertical_letters = count_up_for_vertical_letters + 1

    return full_statement[:-1]
