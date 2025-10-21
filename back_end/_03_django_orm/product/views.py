from django.shortcuts import render
from django.http import HttpResponse
from product.models import Product, Category, Discount, Review
from django.db.models import Avg, Count
from datetime import datetime, timedelta

# 1:N = Product:Review
def test_n_1(request):

    result = ''

    # 1. 특정 제품의 모든 리뷰 select
    # (1) Review 테이블 1번 + Product 테이블 4번 = 총 5번
    # reviews = Review.objects.filter(product_id=1)

    # (2) Product 테이블 1번 + Review 테이블 1번 + Product 테이블 4번 = 총 6번
    # product = Product.objects.get(id=1)
    # reviews = Review.objects.filter(product=product)

    # ★(3) Product 테이블 1번 + Review 테이블 1번 = 총 2번
    product = Product.objects.get(id=1)
    reviews = product.review.all()

    # (1의 결과를 출력하기 위한 result 생성 구문)
    for review in reviews:
        result += str(review.id) \
                    + '/' + review.product.name \
                    + '/' + str(review.user_id) \
                    + '/' + str(review.rating) \
                    + '/' + review.comment + '<br>'

    # 2. 특정 제품의 평균 평점과 리뷰 개수 select
    product = Product.objects.get(id=1)
    avg_rating = product.review.aggregate(avg_rating=Avg('rating'))['avg_rating']
    review_cnt = product.review.count()

    # (2의 결과를 출력하기 위한 result 생성 구문)
    result = f'{product.name}의 리뷰 평균 평점: {avg_rating}({review_cnt}개 리뷰)<br>'

    # 3. 평점이 높은 리뷰(4점 이상)만 select
    product = Product.objects.get(id=1)
    high_rating_reviews = product.review.filter(rating__gte=4)

    # (3의 결과를 출력하기 위한 result 생성 구문)
    for review in high_rating_reviews:
        result += f'[High Rating] {review.user_id}의 {review.comment}({review.rating}점)<br>'

    # 4. 모든 제품의 평균 평점과 리뷰 개수 select
    products_with_review = Product.objects.annotate(
        avg_rating=Avg('review__rating'),
        review_count=Count('review')
    )

    # (4의 결과를 출력하기 위한 result 생성 구문)
    result = ''
    for product in products_with_review:
        result += f'Product {product.name} | 평균 평점 {product.avg_rating} : 리뷰 개수 {product.review_count}<br>'

    # 5. 특정 기간(한달전~오늘)동안 작성된 리뷰 select
    start_date = datetime.now() - timedelta(weeks=4)
    end_date = datetime.now()
    reviews_by_date = Review.objects.filter(created_at__range=(start_date, end_date))

    # (5의 결과를 출력하기 위한 result 생성 구문)
    for review in reviews_by_date:
        result += str(review.id) \
                    + '/' + review.product.name \
                    + '/' + str(review.user_id) \
                    + '/' + str(review.rating) \
                    + '/' + review.comment + '<br>'

    return HttpResponse(result)


# 1:1 = Product:Discount
def test_1_1(request):

    result = ''

    # ✅ 1. 특정 제품의 할인 정보 select 
    product_id = 1
    # (1) Discount.objects.get()로 조회할 것 (try-except)
    # (2) 출력 예시
    #     - 할인 정보가 있는 제품: Product {제품명} | Discount {할인율}%
    #     - 할인 정보가 없는 제품: {product_id}는 할인 안함!
    try:
        discount = Discount.objects.get(product_id=product_id)
        result = f'Product {discount.product.name} | Discount {discount.discount_percentage}%'
    except Discount.DoesNotExist:
        result = f'{product_id}는 할인 안함!'

    # 2. 할인 중인 모든 제품 select
    # (1) 현재 시점에 할인 중인 제품만 조회할 것
    # (2) 출력 예시: [할인중!!!] {제품명} ({할인율}%)

    # 3. 특정 할인율(20%) 이상인 제품 select
    # (1) 출력 예시: [파격세일!!!] {제품명} ({할인율}%)
    
    # ✅ 4. 할인 정보와 함께 모든 제품 정보 select
    # (1) 출력 예시
    #     - 할인 정보가 있는 제품: {제품명} ({할인율}% 세일)
    #     - 할인 정보가 없는 제품: 할인 안 하는 {제품명}
    products = Product.objects.all()

    result += '<br><br><br>'
    for product in products:
        if hasattr(product, 'discount'):
            result += f'{product.name} ({product.discount.discount_percentage}% 세일)<br>'
        else:
            result += f'할인 안 하는 {product.name}<br>'

    # 5. 할인 기간이 지난 제품 select
    # (1) 출력 예시: [할인 종료!!!] {제품명} ({할인율}%)

    return HttpResponse(result)


# prefetch
def test_prefetch(request):
    result = ''

    products = Product.objects.prefetch_related('discount')

    for product in products:
        if hasattr(product, 'discount'):
            result += f'{product.name} ({product.discount.discount_percentage}% 세일)<br>'
        else:
            result += f'할인 안 하는 {product.name}<br>'

    return HttpResponse(result)


# N:M = Product:Category
def test_n_m(request):

    result = ''

    # ✅ 1. 특정 제품이 속한 모든 카테고리 select
    product_id = 9
    # (1) 출력 예시
    #     Product {제품명}의 category
    #     - {카테고리 1} 
    #     - {카테고리 2}
    #     - ... 
    product = Product.objects.get(id=product_id)
    categories = product.categories.all()
    
    result += f'Product {product.name}의 category<br>'
    for category in categories:
        result += f'- {category.name}<br>'

    result += '<br><br><br>'

    # ✅ 2. 특정 카테고리에 속한 모든 제품 정보(이름, 가격, 재고량) select
    category_name = '가전'
    # (1) 출력 예시
    #     Category {카테고리명}의 제품
    #     - {제품명} ({가격}원 / 수량: {재고량}개)
    #     - {제품명} ({가격}원 / 수량: {재고량}개)
    #     - ... 
    category = Category.objects.get(name=category_name)
    products = category.products.all()

    result += f'Category {category.name}의 제품<br>'
    for product in products:
        result += f'- {product.name} ({product.price}원 / 수량: {product.stock}개)<br>'

    result += '<br><br><br>'

    # ✅ 3. 카테고리가 없는 제품 select
    # (1) category가 null인 product 조회
    # (2) 출력 예시
    #     Category 미포함 제품
    #     - {제품명} ({가격}원 / 수량: {재고량}개)
    #     - {제품명} ({가격}원 / 수량: {재고량}개)
    #     - ... 
    products_no_cat = Product.objects.filter(categories__isnull=True)

    result += 'Category 미포함 제품<br>'
    for product in products_no_cat:
        result += f'- {product.name} ({product.price}원 / 수량: {product.stock}개)<br>'
    
    result += '<br><br><br>'

    # ✅ 4. 🔥특정 제품에 새 카테고리 추가
    product_id = 9
    new_category_name = 'Seasonal'
    # (1) 힌트: get_or_create()와 add()
    # (2) 출력 예시: {제품명} ({카테고리명1}, {카테고리명2}, ...)
    product = Product.objects.get(id=product_id)

    new_category, is_created = Category.objects.get_or_create(name=new_category_name) # 새 카테고리 생성
    product.categories.add(new_category)                                              # 새 카테고리-제품 연결

    product_category = product.categories.all()

    result += f'{product.name} ('
    for category in product_category:
        result += f'{category.name}, '
    result += ')<br>'
    
    result += '<br><br><br>'

    # ✅ 5. 모든 카테고리와 각 카테고리의 제품 개수 select
    # (1) 출력 예시
    #     - Category {카테고리명}에는 {제품 개수}개의 제품이!
    #     - Category {카테고리명}에는 {제품 개수}개의 제품이!
    #     - Category {카테고리명}에는 {제품 개수}개의 제품이!
    #     - ...
    categories_with_count = Category.objects.annotate(product_count=Count('products'))

    for category in categories_with_count:
        result += f'- Category {category.name}에는 {category.product_count}개의 제품이!<br>'

    result += '<br><br><br>'

    # ✅ 6. 여러 카테고리에 속한 제품 select
    # (1) 출력 예시
    #     여러 카테고리에 속한 제품 목록
    #     - {제품명} (Category 개수: {카테고리 개수})
    #     - {제품명} (Category 개수: {카테고리 개수})
    #     - {제품명} (Category 개수: {카테고리 개수})
    #     - ...
    multi_cat_products = Product.objects.annotate(cat_count=Count('categories')).filter(cat_count__gt=1)

    result += '여러 카테고리에 속한 제품 목록<br>'
    for product in multi_cat_products:
        result += f'- {product.name} (Category 개수: {product.cat_count})<br>'

    return HttpResponse(result)
