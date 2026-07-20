from decimal import Decimal


async def calculate_cash_paid(denomination: dict[str, int]) -> Decimal:
        total = Decimal("0")
        for note, count in denomination.items():
            total += Decimal(str(note)) * Decimal(str(count))
        return total

async def calculate_change(amount: Decimal) -> dict[str, int]:

        amount = int(amount)
        notes = [500, 200, 100, 50, 20, 10, 5, 2, 1]
        change = {}
        for note in notes:
            qty = amount // note
            if qty:
                change[str(note)] = qty
                amount %= note
        return change