import random as r
def genvalues():
    foodx,enterx,billx,edux,perx,shopx = 0,0,0,0,0,0
    count = 0
    income = r.randint(2000,3500)
    income_back = income
    food = (r.randint(15,30))/100*income
    income -= food
    entertainment = (r.randint(10,20))/100*income
    income -= entertainment
    bills = (r.randint(20,30))/100*income
    income -= bills
    education = (r.randint(10,20))/100*income
    income -= education
    personal_care = (r.randint(5,40))/100*income
    income -= personal_care
    shopping = (r.randint(15,30))/100*income
    income -= shopping
    savings = round(income)

    things = [food,entertainment,bills,education,personal_care,shopping]
    thing = ['food','entertainment','bills','education','personal_care','shopping']
    c=0
    for a in things:
        cre = round((r.randint(20,70)/100)*a)
        deb = round(a-cre)
        final = {'total_amount': cre+deb, 'debit_amount': deb, 'credit_amount': cre}
        if c==1:
            foodx = final
        if c==2:
            enterx = final
        if c==3:
            billx = final
        if c==4:
            edux = final
        if c==5:
            perx = final
        if c==6:
            shopx = final
        c+=1
        count+=1
    return savings,income_back,foodx,enterx,billx,edux,perx,shopx
    
print(genvalues())
        


    
