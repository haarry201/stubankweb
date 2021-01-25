import Transaction, time

start = time.process_time()
new_transaction = Transaction.MLTransaction("Wilko",50.00, 53.374808, -3.023611, 20)
transaction_list = Transaction.gen_values()
new_transaction.analyse_transaction(transaction_list)
print(" --------- time to complete the analysis =", time.process_time()-start, "--------- ")