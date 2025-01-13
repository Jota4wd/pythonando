import __init__
from views.view import SubscriptionService
from models.database import engine
from models.model import Subscription
from datetime import datetime
from decimal import Decimal


class UI:
    def __init__(self):
        self.subscription_service = SubscriptionService(engine)

    def start(self):
        while True:
            print(
                """
			[1] -> Adicionar assinatura
			[2] -> Remover assinatura
			[3] -> Valor total
			[4] -> Gastos últimos 12 meses
			[5] -> Pagar
			[6] -> Sair
			"""
            )

            choice = int(input("Escolha uma opção: "))

            if choice == 1:
                self.add_subscription()
            elif choice == 2:
                self.delete_subscription()
            elif choice == 3:
                self.total_value()
            elif choice == 4:
                self.subscription_service.gen_chart()
            elif choice == 5:
                self.pay()
            elif choice == 6:
                break
            else:
                input("Opção não é válida. Pressione Enter para retornar ao menu.")

    def add_subscription(self):
        empresa = input("empresa: ")
        site = input("site: ")
        data_assinatura = datetime.strptime(input("data de assinatura: "), "%d/%m/%Y")
        valor = Decimal(input("valor: "))

        subscription = Subscription(
            empresa=empresa, site=site, data_assinatura=data_assinatura, valor=valor
        )

        self.subscription_service.create(subscription)

        def delete_subscription(self):
            subscriptions = self.subscription_service.list_all()
            print("escolha qual assinatura deseja excluir")

            for i in subscriptions:
                print(f"[{i.id}] -> {i.empresa}")

            choice = int(input("escolha a assinatura: "))

            self.subscription_service.inactivate_payment(choice)
            self.subscription_service.delete(choice)
            print("assinatura excluída com sucesso.")

    def total_value(self):
        print(
            f"seu valor total em assinaturas é: {self.subscription_service.total_value()}"
        )

    def pay(self):
        subscriptions = self.subscription_service.list_all()
        print("escolha qual assinatura deseja pagar: ")

        for i in subscriptions:
            print(f"{i.id} -> {i.empresa} - Valor: R${i.valor:.2f}")

        choice = int(input("escolha a assinatura: "))

        subscription_to_pay = next(
            (sub for sub in subscriptions if sub.id == choice), None
        )

        if subscription_to_pay:
            self.subscription_service.pay(subscription_to_pay)

            print(
                f"pagamento registrado para a assinatura {subscription_to_pay.empresa}."
            )
        else:
            print("escolha inválida. Nenhum pagamento foi registrado.")


if __name__ == "__main__":
    UI().start()
