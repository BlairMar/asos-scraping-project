import argparse 
parser = argparse.ArgumentParser(description='Scraper Config')
parser.add_argument('--M',action='store_false', default=False)
# parser.add_argument('--M', action=argparse.BooleanOptionalAction) #men
# parser.add_argument('--W', action=argparse.BooleanOptionalAction) #women
# parser.add_argument('--L', action=argparse.BooleanOptionalAction) #save locally
# parser.add_argument('--S3', action=argparse.BooleanOptionalAction) #saves to s3 bucket
# parser.add_argument('--SJ', action=argparse.BooleanOptionalAction) #savejson
# parser.add_argument('--SI', action=argparse.BooleanOptionalAction) #saveimage
parser.add_argument("-BN", "--BUCKET_NAME", help="Name of your S3 Bucket") #bucketname
parser.add_argument("-NUM", "--PRODUCTS_PER_CATEGORY", help="Number of products per category", default='all')
parser.add_argument("-OM", "--OPTIONS_MEN", help="(1)New in, (2)Clothing, (3)Shoes, (4)Accessories, (5)Topman, (6)Sportswear, (7)Face + Body", default=[0])
parser.add_argument("-OW", "--OPTIONS_WOMEN", help="(1)New in, (2)Clothing, (3)Shoes, (4)Accessories, (5)Topshop, (6)Sportswear, (7)Face + Body", default=[0])

args = parser.parse_args()
# print(args)

x = 'yay!'
options_men = list(str(args.OPTIONS_MEN))
for _ in range(len(options_men)):
    if options_men[_] == '1':
        options_men[_] = 'New in'
    elif options_men[_] == '2':
        options_men[_] = 'Clothing'
    elif options_men[_] == '3':
        options_men[_] = 'Shoes'
    elif options_men[_] == '4':
        options_men[_] = 'Accessories'
    elif options_men[_] == '5':
        options_men[_] = 'Topman'
    elif options_men[_] == '6':
        options_men[_] = 'Sportswear'
    elif options_men[_] == '7':
        options_men[_] = 'Face + Body'
    else:
        pass
options_women = list(args.OPTIONS_WOMEN)
for _ in range(len(options_women)):
    if options_women[_] == '1':
        options_women[_] = 'New in'
    elif options_women[_] == '2':
        options_women[_] = 'Clothing'
    elif options_women[_] == '3':
        options_women[_] = 'Shoes'
    elif options_women[_] == '4':
        options_women[_] = 'Accessories'
    elif options_women[_] == '5':
        options_women[_] = 'Topshop'
    elif options_women[_] == '6':
        options_women[_] = 'Sportswear'
    elif options_women[_] == '7':
        options_women[_] = 'Face + Body'
    else:
        pass
print(options_women)
print(args)
print(args.M)
print(args.W)
print(args.L)
print(args.S3)
print(args.SJ)
print(args.SI)
print(args.SI)
print(args.PRODUCTS_PER_CATEGORY)
print(args.OPTIONS_MEN)
print(args.OPTIONS_WOMEN)
print(options_men)
