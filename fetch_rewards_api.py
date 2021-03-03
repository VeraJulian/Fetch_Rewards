import collections
import json
import tornado.httpserver
import tornado.web
import tornado.httpserver

from tornado.ioloop import IOLoop




# hold transactions
transactions = []

# track payers total points spent
points_spent = collections.defaultdict(int)

# hold payers point balance
balance = collections.defaultdict(int)


"""
This class handles adding transactions
"""
class AddTransactionsHandler(tornado.web.RequestHandler):

    def post(self):
        transaction = json.loads(self.request.body)
        transactions.append(transaction)
        self.write('Transaction posted')


        
"""
This class handles spending points
"""
class SpendPointsHandler(tornado.web.RequestHandler):

    """
    We try to spend all points requested
    Return how many points each payer spent
    """
    def spend_points(self, amount):
        for transaction in transactions:
            points_to_spend = transaction.get('points')
            payer = transaction.get('payer')

            if amount == 0:
                break
            
            if points_to_spend > amount:
                points_spent[payer] -= amount
                amount = 0
            else:
                amount -= points_to_spend
                points_spent[payer] -= points_to_spend
                
        return [{"payer": payer, "points": points} for payer, points in points_spent.items()]
       
    """
    write the result from spend_points
    """
    def post(self):
        transactions.sort(key=lambda item: item.get("timestamp"))
        request_body = json.loads(self.request.body)
        amount = int(request_body.get("points"))
        res = self.spend_points(amount)
        self.write(json.dumps(res))
            

        
"""
This class handles calculating payer's balances
"""
class PointsBalanceHandler(tornado.web.RequestHandler):
    
    """
    calculate balances
    """
    def points_balance(self):
        for transaction in transactions:
            payer = transaction.get('payer')
            points = transaction.get('points')
            balance[payer] += points

        for payer in balance:
            balance[payer] += points_spent[payer]
            
        return dict(balance)
    
    def get(self):
        self.write(json.dumps(self.points_balance()))

        
        
class Application(tornado.web.Application):
    def get_handlers(self):
        return [
            (r"/api/add_transactions", AddTransactionsHandler),
            (r"/api/spend_points", SpendPointsHandler),
            (r"/api/get_balances", PointsBalanceHandler)
        ]

    def __init__(self):
        tornado.web.Application.__init__(self, self.get_handlers())


def main():
    http_server = tornado.httpserver.HTTPServer(Application(), xheaders=True)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.current().start()


    
if __name__ == '__main__':
    main()

